#!/usr/bin/env python3
"""검색 평가셋 v2 (189문항) — 논문 단위 Recall@5 를 세 갈래로 잰다.

설계·판정은 docs/experiments/retrieval_eval_1007/README.md (측정 전에 고정).

  .venv/bin/python scripts/eval_retrieval.py --label minilm

갈래:
  vector     : Chroma 벡터만. fetch_n 청크를 가져와 논문 단위로 중복 제거한 상위 k
  bm25       : BM25 만 (논문 단위)
  production : 운영 랭킹과 같은 경로 (hybrid_retrieve_paper_ids_for_eval)

출력: results/<label>/<갈래>.jsonl — 문항당 한 줄, scripts/eval_pairwise.py 형식
(id·slot·model·ok). ok = 정답 논문이 상위 5편 안에 있음. 다른 임베더와의 짝지은
비교는 `python scripts/eval_pairwise.py results/A/vector.jsonl results/B/vector.jsonl --rule any`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ROOT = Path(__file__).resolve().parent.parent
EXP_DIR = ROOT / "docs" / "experiments" / "retrieval_eval_1007"
EVAL_SET = EXP_DIR / "eval_set.jsonl"
# 문항을 의도적으로 바꿨다면 README §2 와 이 값을 같이 갱신할 것
EXPECT_SHA = "8567e909dc1e"
K_PRIMARY = 5
K_MAX = 10


def normalize_pid(pid: str) -> str:
    return re.sub(r"v\d+$", "", (pid or "").strip())


def load_eval_set() -> list[dict]:
    raw = EVAL_SET.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()[:12]
    rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
    print(f"문항 집합: {len(rows)}문항 sha256={digest}")
    if digest != EXPECT_SHA:
        print(f"❌ sha256 불일치 (기대 {EXPECT_SHA}) — 측정 중단")
        print("   문항을 의도적으로 바꿨다면 README §2 와 EXPECT_SHA 를 같이 갱신할 것")
        sys.exit(1)
    return rows


def corpus_raw_ids() -> dict[str, set[str]]:
    """정규화 ID → JSONL 에 있던 원래 ID 들 (버전 접미사 포함). Chroma 존재 확인용."""
    out: dict[str, set[str]] = {}
    files = sorted((ROOT / "raw_data_queue" / "processed").glob("crawled_papers*.jsonl"))
    files.append(ROOT / "raw_data_queue" / "crawled_papers.jsonl")
    for f in files:
        if not f.exists():
            continue
        for line in f.open(encoding="utf-8", errors="replace"):
            m = re.search(r'"paper_id"\s*:\s*"([^"]+)"', line)
            if m:
                out.setdefault(normalize_pid(m.group(1)), set()).add(m.group(1))
    return out


def gold_presence(collection, rows: list[dict]) -> dict[str, bool]:
    raw = corpus_raw_ids()
    present: dict[str, bool] = {}
    for pid in sorted({p for r in rows for p in r["relevant_papers"]}):
        cands = sorted(raw.get(pid, set()) | {pid})
        hit = collection.get(where={"paper_id": {"$in": cands}}, limit=1, include=[])
        present[pid] = bool(hit.get("ids"))
    return present


def dedupe_papers(metas: list[dict], k: int) -> list[str]:
    out: list[str] = []
    for m in metas:
        pid = normalize_pid(m.get("paper_id") or "")
        if pid and pid not in out:
            out.append(pid)
            if len(out) >= k:
                break
    return out


def score(rows: list[dict], retrieved: dict[str, list[str]], arm: str, label: str) -> list[dict]:
    out = []
    for r in rows:
        gold = {normalize_pid(p) for p in r["relevant_papers"]}
        got = retrieved[r["id"]]
        rank = next((i + 1 for i, p in enumerate(got) if p in gold), None)
        out.append({
            "id": r["id"],
            "slot": r["stratum"],
            "model": f"{label}:{arm}",
            "ok": rank is not None and rank <= K_PRIMARY,
            "rank": rank,
            "retrieved": got,
        })
    return out


def summarize(scored: list[dict]) -> dict:
    def agg(xs: list[dict]) -> dict:
        n = len(xs)
        return {
            "n": n,
            f"recall@{K_PRIMARY}": round(sum(x["ok"] for x in xs) / n, 4),
            f"recall@{K_MAX}": round(sum(x["rank"] is not None for x in xs) / n, 4),
            f"mrr@{K_MAX}": round(sum(1 / x["rank"] for x in xs if x["rank"]) / n, 4),
        }

    res = {"all": agg(scored)}
    for s in sorted({x["slot"] for x in scored}):
        res[s] = agg([x for x in scored if x["slot"] == s])
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--label", required=True, help="결과 폴더 이름 (예: minilm)")
    ap.add_argument("--collection", default="arxiv_papers")
    ap.add_argument("--embedding-model", default=None, help="기본: EMBEDDING_MODEL")
    args = ap.parse_args()

    rows = load_eval_set()

    import chromadb
    from chromadb.config import Settings
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

    from core.config.agent_config import CHROMA_DB_DIR, CHROMA_FETCH_MIN, CHROMA_FETCH_MULTIPLIER, EMBEDDING_MODEL
    from core.rag.agent_chroma_rag import hybrid_retrieve_paper_ids_for_eval
    from core.rag.bm25_index import get_bm25_searcher

    model = args.embedding_model or EMBEDDING_MODEL
    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR), settings=Settings(anonymized_telemetry=False))
    ef = SentenceTransformerEmbeddingFunction(model_name=model, device="cpu", normalize_embeddings=True)
    collection = client.get_collection(args.collection, embedding_function=ef)
    print(f"임베딩: {model} · 컬렉션: {args.collection} · 청크 {collection.count():,}")

    # README §3.1: 정답이 Chroma 에 없는 문항은 결과를 보기 전에 제외한다
    present = gold_presence(collection, rows)
    dropped = []
    kept = []
    for r in rows:
        alive = [p for p in r["relevant_papers"] if present[normalize_pid(p)]]
        if alive:
            kept.append({**r, "relevant_papers": alive})
        else:
            dropped.append(r["id"])
    absent = sorted(p for p, ok in present.items() if not ok)
    print(f"정답 논문 {len(present)}편 중 Chroma 에 없음 {len(absent)}편 {absent}")
    print(f"제외 문항 {len(dropped)}개 {dropped} → 측정 {len(kept)}문항")

    bm25 = get_bm25_searcher()
    fetch_n = int(max(K_MAX * CHROMA_FETCH_MULTIPLIER, CHROMA_FETCH_MIN))
    print(f"fetch_n={fetch_n} · BM25 논문 {bm25.paper_count:,}")

    arms = {}
    t0 = time.time()
    vec = {}
    for r in kept:
        res = collection.query(query_texts=[r["query"]], n_results=fetch_n, include=["metadatas"])
        vec[r["id"]] = dedupe_papers((res.get("metadatas") or [[]])[0], K_MAX)
    arms["vector"] = vec
    print(f"  vector {time.time() - t0:.0f}s")

    t0 = time.time()
    arms["bm25"] = {
        r["id"]: dedupe_papers(bm25.search(r["query"], top_k=K_MAX * 3), K_MAX) for r in kept
    }
    print(f"  bm25 {time.time() - t0:.0f}s")

    t0 = time.time()
    arms["production"] = {
        r["id"]: [normalize_pid(p) for p in hybrid_retrieve_paper_ids_for_eval(
            collection, r["query"], fetch_n=fetch_n, top_k=K_MAX)]
        for r in kept
    }
    print(f"  production {time.time() - t0:.0f}s")

    out_dir = EXP_DIR / "results" / args.label
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "label": args.label,
        "embedding_model": model,
        "eval_sha": EXPECT_SHA,
        "n_measured": len(kept),
        "dropped": dropped,
        "absent_gold": absent,
        "arms": {},
    }
    for arm, retrieved in arms.items():
        scored = score(kept, retrieved, arm, args.label)
        with (out_dir / f"{arm}.jsonl").open("w", encoding="utf-8") as w:
            for x in scored:
                w.write(json.dumps(x, ensure_ascii=False) + "\n")
        summary["arms"][arm] = summarize(scored)

    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{'갈래':<11} {'층':<4} {'n':>4} {'R@5':>7} {'R@10':>7} {'MRR@10':>7}")
    for arm, res in summary["arms"].items():
        for s, m in res.items():
            print(f"{arm:<11} {s:<4} {m['n']:>4} {m['recall@5']:>7.3f} {m['recall@10']:>7.3f} {m['mrr@10']:>7.3f}")
    print(f"\n저장: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
