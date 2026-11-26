"""image_1104 §7: 같은 30장을 큰 비전 모델로 설명 · 가림 묶음 · 채점.

    .venv/bin/python docs/experiments/image_1104/run2.py describe qwen3.6:27b-q4_K_M
    .venv/bin/python docs/experiments/image_1104/run2.py packet
    .venv/bin/python docs/experiments/image_1104/run2.py score
"""
import json
import random
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import run  # noqa: E402

ROOT = run.ROOT
MODELS = ["qwen3.5:9b", "qwen3.6:27b-q4_K_M", "qwen3.6:35b-a3b-q4_K_M"]
SEED = 1126


def out_path(model: str) -> Path:
    return ROOT / f"desc_{model.replace(':', '_')}.jsonl"


def sample():
    return [json.loads(x) for x in open(ROOT / "sample.jsonl", encoding="utf-8")]


def describe(model: str) -> None:
    run.MODEL = model
    figs = {json.loads(x)["id"]: json.loads(x) for x in open(ROOT / "figures.jsonl", encoding="utf-8")}
    path = out_path(model)
    done = {json.loads(x)["id"] for x in open(path, encoding="utf-8")} if path.exists() else set()
    with open(path, "a", encoding="utf-8") as out:
        for k, s in enumerate(sample(), 1):
            if s["id"] in done:
                continue
            try:
                row = {"id": s["id"], **run.call_vision(figs[s["id"]])}
            except Exception as e:  # 한 장 실패로 멈추지 않는다
                row = {"id": s["id"], "error": repr(e)[:200]}
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            print(k, s["id"], row.get("total_s"), row.get("eval_tokens"), row.get("error", ""), flush=True)
    rows = [json.loads(x) for x in open(path, encoding="utf-8")]
    ok = [r for r in rows if "desc" in r]
    print(model, "완료", len(ok), "오류", len(rows) - len(ok),
          "제외 중앙", statistics.median(r["total_s"] - r["load_s"] for r in ok) if ok else "-")


def descs():
    d = {MODELS[0]: {s["id"]: s["desc"] for s in sample()}}
    for m in MODELS[1:]:
        d[m] = {r["id"]: r.get("desc", "(오류)") for r in map(json.loads, open(out_path(m), encoding="utf-8"))}
    return d


def packet() -> None:
    d, rng, key = descs(), random.Random(SEED), {}
    lines = ["# image_1104 §7 가림 묶음 — 그림 경로를 열어 보고 x · y · z 를 따로 분류한다.\n"]
    for n, s in enumerate(sample(), 1):
        order = MODELS[:]
        rng.shuffle(order)
        key[s["id"]] = order
        lines.append(f"## {n}. {s['id']}\n그림: {s['path']}\n제목: {s['title']}\n캡션: {s['caption']}\n")
        for tag, m in zip("xyz", order):
            lines.append(f"**{tag}:** {d[m][s['id']]}\n")
    (ROOT / "packet2.md").write_text("\n".join(lines), encoding="utf-8")
    (ROOT / "packet2_key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    print("묶음", len(key))


def score() -> None:
    """classes2.tsv: 번호 id 종류 태그(x|y|z) 정확 숫자오독 새정보 메모."""
    key = json.loads((ROOT / "packet2_key.json").read_text(encoding="utf-8"))
    rows = [x.rstrip("\n").split("\t") for x in open(ROOT / "classes2.tsv", encoding="utf-8") if x.strip() and not x.startswith("#")]
    assert all(r[4] in ("O", "△", "X") and r[5] in ("Y", "N") and r[6] in ("Y", "N") for r in rows)
    assert len(rows) == 90 and {r[1] for r in rows} == set(key)
    by = {m: [] for m in MODELS}
    for r in rows:
        by[key[r[1]]["xyz".index(r[3])]].append(r)
    old = {r[1]: r for r in (x.rstrip("\n").split("\t") for x in open(ROOT / "classes.tsv", encoding="utf-8") if x.strip() and not x.startswith("#"))}
    for m, rs in by.items():
        acc, new = Counter(r[4] for r in rs), sum(r[6] == "Y" for r in rs)
        print(f"{m}: 정확 {dict(acc)} · 숫자 오독 {sum(r[5] == 'Y' for r in rs)} · 새 정보 {new} · 맞으면서 새 정보 {sum(r[6] == 'Y' and r[4] != 'X' for r in rs)}"
              f" | G1 {'통과' if acc['X'] <= 6 else '미달'} · G2 {'통과' if new >= 9 else '미달'}")
        for kind in sorted({r[2] for r in rs}):
            part = [r for r in rs if r[2] == kind]
            print(f"    {kind} {len(part)}: {dict(Counter(r[4] for r in part))} · 새 정보 {sum(r[6] == 'Y' for r in part)}")
    nine = by[MODELS[0]]
    print("9B 재분류 vs §6: 정확 일치", sum(old[r[1]][3] == r[4] for r in nine), "/30 · 새 정보 일치", sum(old[r[1]][5] == r[6] for r in nine), "/30")


if __name__ == "__main__":
    {"describe": lambda: describe(sys.argv[2]), "packet": packet, "score": score}[sys.argv[1]]()
