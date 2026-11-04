"""image_1104: 20편 고르기 · 그림 추출 · 9B 비전 설명. 운영 Chroma · .env 는 쓰지 않는다.

    .venv/bin/python docs/experiments/image_1104/run.py select
    .venv/bin/python docs/experiments/image_1104/run.py extract
    .venv/bin/python docs/experiments/image_1104/run.py describe
    .venv/bin/python docs/experiments/image_1104/run.py sample
"""

import base64
import glob
import json
import random
import re
import statistics
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path("docs/experiments/image_1104")
WORK = Path("tmp/image_1104")
IMG = WORK / "img"
SEED = 1104
MIN_SIDE = 100  # pt. 이보다 작으면 수식 · 줄 조각이 대부분이다(README §1).
CTX_CHARS = 500
MODEL = "qwen3.5:9b"
PLACEHOLDER = re.compile(r"picture \[(\d+) x (\d+)\] intentionally omitted")
CAPTION = re.compile(r"^\W*(?:figure|fig\.?)\s*\d+", re.I)
TEXT_CLASSES = {"text", "list-item", "caption", "footnote", "section-header", "title"}

PROMPT = """You are writing a search-index note about one figure from a research paper.
Paper title: {title}
Figure caption: {caption}
Text before the figure: {before}
Text after the figure: {after}

Look at the image and write 3 to 5 plain English sentences:
- what kind of figure it is (architecture diagram, line chart, bar chart, table image, screenshot, example)
- the components, axis labels, legends or method names you can read in the image
- the main trend or structure it shows
Only state what you can see in the image. Copy a number only if you can read it clearly. Do not guess.
If the image is unreadable or decorative, say so in one sentence."""


def bare(pid: str) -> str:
    return re.sub(r"v\d+$", "", pid.strip())


def records():
    for path in ["raw_data_queue/crawled_papers.jsonl", *sorted(glob.glob("raw_data_queue/processed/*.jsonl"))]:
        for line in open(path, encoding="utf-8", errors="replace"):
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def select() -> None:
    wanted: dict[str, list[str]] = {}
    for line in open("docs/experiments/topic_split2_1104/labels_hu.tsv", encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        q, pid, topics = line.rstrip("\n").split("\t")[:3]
        if topics.strip() != "-":
            wanted.setdefault(bare(pid), []).append(q)
    found = {}
    for r in records():
        pid = bare(str(r.get("paper_id") or ""))
        if pid not in wanted or pid in found:
            continue
        figs = sum(1 for w, h in PLACEHOLDER.findall(r.get("content") or "") if min(int(w), int(h)) >= MIN_SIDE)
        found[pid] = {"paper_id": pid, "title": r.get("title"), "pdf_url": r.get("pdf_url"), "figs_in_text": figs, "questions": sorted(set(wanted[pid]))}
    usable = sorted(p for p, v in found.items() if v["figs_in_text"] >= 1 and v["pdf_url"])
    random.Random(SEED).shuffle(usable)
    picked = usable[:20]
    with open(ROOT / "papers.jsonl", "w", encoding="utf-8") as f:
        for p in picked:
            f.write(json.dumps(found[p], ensure_ascii=False) + "\n")
    print(f"라벨 논문 {len(wanted)} · 수집 기록에 있음 {len(found)} · 그림 있음 {len(usable)} · 고름 {len(picked)}")


def box_text(box) -> str:
    return " ".join(s.get("text", "") for line in (box.textlines or []) for s in line.get("spans", [])).strip()


def parse_one(pid: str, title: str) -> None:
    """자식 프로세스 전용. 일부 PDF 는 파서가 멈추므로 부모가 시간 제한을 건다."""
    from collections import Counter

    from pymupdf4llm.helpers.document_layout import parse_document

    IMG.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    doc = parse_document(str(WORK / f"{pid}.pdf"), filename=pid, image_path=str(IMG), write_images=True, image_dpi=150)
    parse_s = time.time() - t0
    classes = Counter()
    figs = []
    for page in doc.pages:
        boxes = page.boxes
        classes.update(b.boxclass for b in boxes)
        for i, b in enumerate(boxes):
            if b.boxclass != "picture" or min(b.x1 - b.x0, b.y1 - b.y0) < MIN_SIDE or not isinstance(b.image, str):
                continue
            texts = [(j, box_text(x)) for j, x in enumerate(boxes) if x.boxclass in TEXT_CLASSES]
            caps = [(abs(j - i), j, t) for j, t in texts if CAPTION.match(t) or (boxes[j].boxclass == "caption" and t)]
            cap_j, caption = (min(caps)[1], min(caps)[2]) if caps else (None, "")
            before = " ".join(t for j, t in texts if j < i and j != cap_j)[-CTX_CHARS:]
            after = " ".join(t for j, t in texts if j > i and j != cap_j)[:CTX_CHARS]
            path = Path(b.image)
            assert path.exists(), b.image
            figs.append(
                {
                    "id": path.stem,
                    "paper_id": pid,
                    "title": title,
                    "page": page.page_number,
                    "w": round(b.x1 - b.x0),
                    "h": round(b.y1 - b.y0),
                    "path": str(path),
                    "caption": caption,
                    "before": before,
                    "after": after,
                }
            )
    out = {"paper_id": pid, "pages": doc.page_count, "parse_s": round(parse_s, 1), "classes": dict(classes), "figures": figs}
    (WORK / f"{pid}.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")


def extract() -> None:
    from pipelines.ingest.arxiv_fetcher import ArxivFetcher

    WORK.mkdir(parents=True, exist_ok=True)
    fetcher = ArxivFetcher()
    with open(ROOT / "extract.jsonl", "w", encoding="utf-8") as out, open(ROOT / "figures.jsonl", "w", encoding="utf-8") as figs:
        for line in open(ROOT / "papers.jsonl", encoding="utf-8"):
            p = json.loads(line)
            pid, pdf = p["paper_id"], WORK / f"{p['paper_id']}.pdf"
            if not pdf.exists() and not fetcher.download_pdf(p["pdf_url"], str(pdf)):
                out.write(json.dumps({"paper_id": pid, "error": "download"}) + "\n")
                continue
            size = pdf.stat().st_size
            try:
                subprocess.run([sys.executable, str(ROOT / "run.py"), "parse_one", pid, p["title"] or ""], check=True, timeout=600)
            except (subprocess.SubprocessError, OSError) as e:
                out.write(json.dumps({"paper_id": pid, "bytes": size, "error": repr(e)[:200]}) + "\n")
                continue
            r = json.loads((WORK / f"{pid}.json").read_text(encoding="utf-8"))
            for fig in r.pop("figures"):
                figs.write(json.dumps(fig, ensure_ascii=False) + "\n")
                r["n_figures"] = r.get("n_figures", 0) + 1
            r["bytes"] = size
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
            out.flush()
            figs.flush()
            print(pid, r.get("pages"), "쪽", r.get("n_figures", 0), "장", round(size / 1e6, 1), "MB", r["parse_s"], "s", flush=True)


def call_vision(fig: dict) -> dict:
    prompt = PROMPT.format(title=fig["title"], caption=fig["caption"] or "(none found)", before=fig["before"] or "(none)", after=fig["after"] or "(none)")
    body = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "keep_alive": "5m",
        "messages": [{"role": "user", "content": prompt, "images": [base64.b64encode(Path(fig["path"]).read_bytes()).decode()]}],
        "options": {"temperature": 0.2, "top_p": 0.8, "repeat_penalty": 1.18, "num_predict": 400},
    }
    req = urllib.request.Request("http://localhost:11434/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as res:
        d = json.load(res)
    ns = 1e9
    return {
        "desc": d["message"]["content"].strip(),
        "total_s": round(d.get("total_duration", 0) / ns, 1),
        "load_s": round(d.get("load_duration", 0) / ns, 1),
        "prompt_s": round(d.get("prompt_eval_duration", 0) / ns, 1),
        "eval_s": round(d.get("eval_duration", 0) / ns, 1),
        "prompt_tokens": d.get("prompt_eval_count"),
        "eval_tokens": d.get("eval_count"),
        "done_reason": d.get("done_reason"),
    }


def describe() -> None:
    path = ROOT / "desc.jsonl"
    done = {json.loads(x)["id"] for x in open(path, encoding="utf-8")} if path.exists() else set()
    figs = [json.loads(x) for x in open(ROOT / "figures.jsonl", encoding="utf-8")]
    with open(path, "a", encoding="utf-8") as out:
        for k, fig in enumerate(figs, 1):
            if fig["id"] in done:
                continue
            try:
                row = {"id": fig["id"], "paper_id": fig["paper_id"], **call_vision(fig)}
            except Exception as e:  # 한 장 실패로 전체를 멈추지 않는다.
                row = {"id": fig["id"], "paper_id": fig["paper_id"], "error": repr(e)[:200]}
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            print(k, "/", len(figs), fig["id"], row.get("total_s"), row.get("prompt_tokens"), row.get("eval_tokens"), row.get("error", ""), flush=True)
    rows = [json.loads(x) for x in open(path, encoding="utf-8")]
    ok = [r for r in rows if "desc" in r]
    print("완료", len(ok), "오류", len(rows) - len(ok))
    if ok:
        print("제외 중앙", statistics.median(r["total_s"] - r["load_s"] for r in ok), "포함 중앙", statistics.median(r["total_s"] for r in ok))


def sample() -> None:
    figs = {json.loads(x)["id"]: json.loads(x) for x in open(ROOT / "figures.jsonl", encoding="utf-8")}
    rows = [json.loads(x) for x in open(ROOT / "desc.jsonl", encoding="utf-8")]
    ok = sorted((r for r in rows if "desc" in r), key=lambda r: r["id"])
    picked = random.Random(SEED).sample(ok, min(30, len(ok)))
    texts = {}
    want = {r["paper_id"] for r in picked}
    for r in records():
        pid = bare(str(r.get("paper_id") or ""))
        if pid in want and pid not in texts:
            texts[pid] = (r.get("content") or "").lower()
    with open(ROOT / "sample.jsonl", "w", encoding="utf-8") as out:
        for r in picked:
            f = figs[r["id"]]
            words = set(re.findall(r"[A-Za-z][A-Za-z\-]{3,}|\d+(?:\.\d+)?", r["desc"]))
            novel = sorted(w for w in words if w.lower() not in texts.get(r["paper_id"], ""))
            out.write(json.dumps({"id": r["id"], "path": f["path"], "title": f["title"], "caption": f["caption"], "desc": r["desc"], "novel": novel}, ensure_ascii=False) + "\n")
    print("표본", len(picked))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "parse_one":
        parse_one(sys.argv[2], sys.argv[3])
    else:
        {"select": select, "extract": extract, "describe": describe, "sample": sample}[cmd]()
