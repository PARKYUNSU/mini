"""cite_graph_1102 §1 후보: DB 논문 본문에 적힌 arXiv 인용 → DB 에 없는 논문을 DB 안 인용 수 순으로 N편.

손으로 고르지 않는다. 외부 호출은 arXiv API 메타데이터(100편씩, 호출 사이 3초)뿐이다.

    .venv/bin/python docs/experiments/cite_graph_1102/candidates.py
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
import time
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from core.config.agent_config import CHROMA_DB_DIR, COLLECTION_NAME  # noqa: E402
from core.rag.bm25_index import _normalize_pid  # noqa: E402

D = Path(__file__).resolve().parent
N = 200
# "arXiv preprint arXiv:2005.11401" · "ArXiv abs/2310.06116" · "CoRR, abs/1810.04805" · "arxiv.org/pdf/2005.11401v2"
# · "10.48550/arXiv.2310.06116" — 'arxiv' · 'abs/' · 'corr' 뒤 숫자 없이 25자 안에 오는 새 꼴 ID 만 센다.
CITE = re.compile(r"(?:arxiv|abs/|corr)[^\d\n]{0,25}?(\d{4}\.\d{4,5})(?!\d)", re.I)
ATOM = "{http://www.w3.org/2005/Atom}"


def valid(aid: str) -> bool:
    """새 꼴 arXiv ID 인가 — 0704 ~ 2611, 1412 까지 뒤 4자리 · 1501 부터 5자리."""
    yymm = int(aid[:4])
    return 704 <= yymm <= 2611 and 1 <= yymm % 100 <= 12 and len(aid) == (9 if yymm <= 1412 else 10)


def db_ids() -> set[str]:
    """운영 Chroma 의 paper_id — SQLite 읽기 전용(chroma_gap_1101/find_gap.py 와 같은 방식)."""
    con = sqlite3.connect(f"file:{Path(CHROMA_DB_DIR) / 'chroma.sqlite3'}?immutable=1", uri=True)
    seg, = con.execute(
        "SELECT s.id FROM segments s JOIN collections c ON s.collection = c.id WHERE c.name = ? AND s.scope = 'METADATA'",
        (COLLECTION_NAME,),
    ).fetchone()
    rows = con.execute(
        "SELECT DISTINCT m.string_value FROM embedding_metadata m JOIN embeddings e ON e.id = m.id "
        "WHERE m.key = 'paper_id' AND m.string_value IS NOT NULL AND e.segment_id = ?",
        (seg,),
    )
    ids = {_normalize_pid(v.strip()) for v, in rows if v and v.strip()}
    con.close()
    return ids


def jsonl_files() -> list[Path]:
    """bm25_index._load 와 같은 순서."""
    files = sorted((ROOT / "raw_data_queue" / "processed").glob("crawled_papers*.jsonl"))
    main = ROOT / "raw_data_queue" / "crawled_papers.jsonl"
    return files + ([main] if main.exists() else [])


def citations(db: set[str]) -> dict[str, set[str]]:
    """DB 논문마다 본문(content)에 적힌 arXiv ID 집합. 자기 자신은 뺀다. 같은 논문이 여러 줄이면 합친다."""
    cited: dict[str, set[str]] = {}
    for f in jsonl_files():
        with f.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                pid = _normalize_pid(str(d.get("paper_id") or "").strip())
                if pid not in db:
                    continue
                found = {_normalize_pid(m) for m in CITE.findall(d.get("content") or "")}
                cited.setdefault(pid, set()).update(i for i in found if valid(i) and i != pid)
    return cited


def arxiv_meta(ids: list[str]) -> dict[str, dict]:
    """arXiv API 로 제목 · 초록 · 날짜 · 주 분류. 없는 ID 는 결과에 없다."""
    out: dict[str, dict] = {}
    for k in range(0, len(ids), 100):
        chunk = ids[k : k + 100]
        for attempt in range(3):
            try:
                r = requests.get("http://export.arxiv.org/api/query",
                                 params={"id_list": ",".join(chunk), "max_results": len(chunk)}, timeout=120)
                r.raise_for_status()
                break
            except requests.RequestException as exc:
                print(f"arXiv API 다시 {attempt + 1}: {type(exc).__name__}", flush=True)
                time.sleep(10)
        else:
            sys.exit("arXiv API 실패 — 목록을 쓰지 않는다")
        for e in ET.fromstring(r.content).findall(f"{ATOM}entry"):
            aid = _normalize_pid((e.findtext(f"{ATOM}id") or "").rsplit("/abs/", 1)[-1])
            title = " ".join((e.findtext(f"{ATOM}title") or "").split())
            if aid in chunk and title:
                cat = e.find("{http://arxiv.org/schemas/atom}primary_category")
                out[aid] = {"title": title, "published": (e.findtext(f"{ATOM}published") or "")[:10],
                            "category": cat.get("term", "") if cat is not None else "",
                            "abstract": " ".join((e.findtext(f"{ATOM}summary") or "").split())[:1200]}
        time.sleep(3)
    return out


def main() -> None:
    assert CITE.findall("arXiv preprint arXiv:2005.11401. ArXiv abs/2310.06116 CoRR, abs/1810.04805 "
                        "arxiv.org/pdf/2005.11401v2 10.48550/arXiv.2310.06116 arXiv:2005.114011") == \
        ["2005.11401", "2310.06116", "1810.04805", "2005.11401", "2310.06116"]
    assert valid("1412.6980") and valid("2005.11401") and not valid("2023.12345") and not valid("2005.1140")
    db = db_ids()
    cited = citations(db)
    cnt = Counter(i for s in cited.values() for i in s if i not in db)
    ranked = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
    # 순위대로 arXiv 에 있는 것만 N편 — 없는 ID(오탈자 · 철회)는 건너뛰고 다음 순위로 채운다
    picked: list[str] = []
    meta: dict[str, dict] = {}
    k = 0
    while len(picked) < N and k < len(ranked):
        batch = [i for i, _ in ranked[k : k + N - len(picked) + 20]]
        k += len(batch)
        meta.update(arxiv_meta(batch))
        picked += [i for i in batch if i in meta][: N - len(picked)]
    skipped = [i for i, _ in ranked[: ranked.index((picked[-1], cnt[picked[-1]])) + 1] if i not in meta]
    ext = Path(ROOT / ".bridge" / "external_candidates.jsonl")
    ext_ids = {_normalize_pid(a) for l in ext.open(encoding="utf-8") for a in json.loads(l).get("arxiv", [])} if ext.exists() else set()
    stats = {
        "db_papers": len(db), "db_papers_read": len(cited), "db_papers_citing": sum(1 for s in cited.values() if s),
        "edges_to_outside": sum(cnt.values()), "edges_to_db": sum(len(s & db) for s in cited.values()),
        "outside_ids": len(cnt), "cites_at_rank_1": cnt[picked[0]], f"cites_at_rank_{N}": cnt[picked[-1]],
        "skipped_no_arxiv": skipped, "in_external_candidates": sum(1 for i in picked if i in ext_ids),
    }
    papers = [{"rank": r + 1, "id": i, "cites": cnt[i], **meta[i]} for r, i in enumerate(picked)]
    (D / "candidates.json").write_text(json.dumps({"N": N, "stats": stats, "papers": papers}, ensure_ascii=False, indent=1),
                                       encoding="utf-8")
    (D / "candidates.yaml").write_text("classics:\n" + "".join(
        f'  - id: "{p["id"]}"\n    note: "cite_graph_1102 #{p["rank"]} cites={p["cites"]}"\n' for p in papers), encoding="utf-8")
    (D / "ranked_top1000.tsv").write_text("".join(f"{i}\t{c}\n" for i, c in ranked[:1000]), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False))
    print("주 분류", Counter(p["category"] for p in papers).most_common(12))


if __name__ == "__main__":
    main()
