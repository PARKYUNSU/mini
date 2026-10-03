#!/usr/bin/env python3
"""Production Hybrid에서 Recall@K 미스인 쿼리만 상세 점수 분석 + 자동 원인 분류.

🥇 태그 분포 먼저 (가장 중요):
    .venv/bin/python3 scripts/debug_production_miss.py --top-k 5 --no-detail

태그: retrieval_missing | ranking_drop | weak_multi_evidence | weak_title_signal
상세 청크/상위5논문: --no-detail 없이 실행.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import statistics
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)

RETRIEVAL_MISSING = "retrieval_missing"
RANKING_DROP = "ranking_drop"
WEAK_MULTI_EVIDENCE = "weak_multi_evidence"
WEAK_TITLE_SIGNAL = "weak_title_signal"

# Δ = top1.paper_score_final - 정답.paper_score_final (풀에 있을 때만)
_DELTA_SMALL_HI = 0.05
_DELTA_LARGE_LO = 0.2


def _pad5(xs: list[float]) -> list[float]:
    out = list(xs)[:5]
    while len(out) < 5:
        out.append(0.0)
    return out


def _classify_gt(
    hit: dict | None,
    *,
    top_k: int,
    weak_title_thr: float,
) -> tuple[list[str], str]:
    """(태그 목록, 한 줄 힌트)."""
    if hit is None:
        return [RETRIEVAL_MISSING], "후보 풀에 정답 논문 없음 → fetch/retrieval 쪽 점검"

    rank = int(hit.get("rank") or 1_000_000)
    tags: list[str] = []
    n_strong = int(hit.get("n_strong_chunks") or 0)
    n_chunks = int(hit.get("n_chunks_in_paper") or 0)
    ts = float(hit.get("title_sim") or 0.0)

    if rank > top_k:
        tags.append(RANKING_DROP)
    if n_chunks < 2 or n_strong < 2:
        tags.append(WEAK_MULTI_EVIDENCE)
    if ts < weak_title_thr:
        tags.append(WEAK_TITLE_SIGNAL)

    if RETRIEVAL_MISSING in tags:
        hint = "retrieval"
    elif RANKING_DROP in tags:
        parts = ["순위 밀림: paper_score_final / top1 격차·제목·멀티청크 확인"]
        if WEAK_TITLE_SIGNAL in tags:
            parts.append("title 가중↑ 실험")
        if WEAK_MULTI_EVIDENCE in tags:
            parts.append("멀티 에비던스 약함 → s2~s5·β 튜닝")
        hint = " | ".join(parts)
    else:
        hint = "기타 (태그 확인)"

    return tags, hint


def _fmt_row(r: dict) -> str:
    pid = r.get("paper_id") or "(no id)"
    top5 = _pad5(list(r.get("chunk_scores_top5") or []))
    s_labels = "  ".join(f"s{i+1}={top5[i]:.4f}" for i in range(5))
    top5_s = ", ".join(f"{x:.4f}" for x in top5)
    ts = float(r.get("title_sim") or 0.0)
    pb = float(r.get("paper_score_before_title") or 0.0)
    pchunk = float(r.get("paper_score_chunk_only") or pb)
    meb = float(r.get("multievidence_bonus") or 0.0)
    pf = float(r.get("paper_score_final") or 0.0)
    rk = r.get("rank")
    title = (r.get("title") or "")[:80]
    return (
        f"    paper_id={pid}  rank={rk}\n"
        f"    title: {title!r}\n"
        f"    chunk s1~s5: {s_labels}\n"
        f"    chunk_scores_top5: [{top5_s}]\n"
        f"    paper_score_chunk_only={pchunk:.6f}  multievidence_bonus={meb:.6f}  "
        f"n_chunks={r.get('n_chunks_in_paper')}  n_strong={r.get('n_strong_chunks')}\n"
        f"    paper_score_before_title={pb:.6f}  title_sim={ts:.4f}  paper_score_final={pf:.6f}"
    )


def _print_case_blocks(summary: dict[str, int]) -> None:
    """태그 최빈값에 ★ 표시 + 케이스 1~4 고정 해석 출력."""
    rm = summary[RETRIEVAL_MISSING]
    rd = summary[RANKING_DROP]
    wme = summary[WEAK_MULTI_EVIDENCE]
    wts = summary[WEAK_TITLE_SIGNAL]
    tot = rm + rd + wme + wts
    mx = max(rm, rd, wme, wts) if tot else 0

    def star(n: int) -> str:
        return "  ★ (현재 태그 최다)" if tot and n == mx and n > 0 else ""

    print("  ┌─ 해석 기준 (그대로 사용) ─────────────────────────────────────────")
    print("  │ 🔥 한 줄: retrieval_missing ↑ → 검색 문제 | ranking_drop ↑ → 점수(랭킹) 문제")
    print("  │")
    print(f"  │ 케이스 1️⃣  ranking_drop가 대부분{star(rd)}")
    print("  │   의미: 후보는 이미 충분 → 순위 문제 (랭킹 튜닝 단계)")
    print("  │   다음: title weight ↑, multi-evidence(α·γ·δ·ε·β) ↑")
    print("  │")
    print(f"  │ 케이스 2️⃣  retrieval_missing 많음{star(rm)}")
    print("  │   의미: 후보 풀 자체 부족")
    print("  │   다음: BM25_UNION_TOP_M ↑ (예: 50→80), CHROMA_FETCH_MULTIPLIER ↑")
    print("  │")
    print(f"  │ 케이스 3️⃣  weak_multi_evidence 많음{star(wme)}")
    print("  │   의미: 정답 논문이 여러 청크로 강하지 않음")
    print("  │   다음: α↑ (0.12→0.15), γ↑ (0.1→0.15), δ↑, ε↑")
    print("  │")
    print(f"  │ 케이스 4️⃣  weak_title_signal 많음{star(wts)}")
    print("  │   의미: 제목 매칭이 핵심인데 영향 약함")
    print("  │   다음: --title-add-weight 0.15 / 0.2")
    print("  └──────────────────────────────────────────────────────────────────")


def _print_delta_block(gaps: list[float]) -> None:
    """Δ = top1_final - 정답_final. 풀에 정답이 있을 때만 집계."""
    print("=== Δ (top1 대비 차이) 요약 — 반드시 볼 것 ===")
    if not gaps:
        print("  집계할 Δ 없음 (정답이 전부 풀 밖이거나 데이터 없음).")
        print("  → K 스윕·retrieval_missing 비중으로 retrieval 여부 판단.")
        return

    mean = statistics.mean(gaps)
    med = statistics.median(gaps)
    n = len(gaps)
    tiny = sum(1 for g in gaps if g < 0.02)
    small = sum(1 for g in gaps if 0.02 <= g <= _DELTA_SMALL_HI)
    mid = sum(1 for g in gaps if _DELTA_SMALL_HI < g < _DELTA_LARGE_LO)
    large = sum(1 for g in gaps if g >= _DELTA_LARGE_LO)

    print(f"  n={n}  mean={mean:.4f}  median={med:.4f}  min={min(gaps):.4f}  max={max(gaps):.4f}")
    print()
    print("  패턴 해석:")
    print(f"    🟢 Δ 작음 (0.02~{_DELTA_SMALL_HI}): {small}건 — 거의 맞았는데 밀림 → 미세 튜닝(title·α·γ)으로 해결 가능성")
    print(f"    ··· Δ 아주 작음 (<0.02): {tiny}건 — 더 미세")
    print(f"    ··· 중간 ({_DELTA_SMALL_HI}~{_DELTA_LARGE_LO}): {mid}건")
    print(f"    🔴 Δ 큼 (≥{_DELTA_LARGE_LO}): {large}건 — top1과 정답이 점수 구조상 멀다 (스코어링·노이즈·후보 혼입)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Production miss 쿼리 점수·원인 분석")
    parser.add_argument("--top-k", type=int, default=5, help="Recall@K (미스 판정)")
    parser.add_argument(
        "--title-add-weight",
        type=float,
        default=None,
        metavar="W",
        help="HYBRID_PAPER_TITLE_SIM_ADD_WEIGHT 오버라이드 (예: 0.15, 0.2). import 전에 env 설정.",
    )
    parser.add_argument(
        "--weak-title-threshold",
        type=float,
        default=0.5,
        help="이 값 미만 title_sim이면 weak_title_signal (기본 0.5)",
    )
    parser.add_argument(
        "--no-detail",
        action="store_true",
        help="태그·Δ 요약 중심 (쿼리당 한 줄). 태그 분포 먼저 볼 때 권장.",
    )
    args = parser.parse_args()
    top_k = max(1, int(args.top_k))
    weak_title_thr = float(args.weak_title_threshold)

    if args.title_add_weight is not None:
        os.environ["HYBRID_PAPER_TITLE_SIM_ADD_WEIGHT"] = str(args.title_add_weight)
        print(f"[env] HYBRID_PAPER_TITLE_SIM_ADD_WEIGHT={args.title_add_weight}\n")

    import chromadb
    from chromadb.config import Settings
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

    from core.config.agent_config import CHROMA_FETCH_MIN, CHROMA_FETCH_MULTIPLIER, EMBEDDING_MODEL
    from core.rag.agent_chroma_rag import hybrid_retrieve_paper_ids_for_eval, production_retrieval_debug_for_eval

    _eval_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval_rag_hybrid.py")
    _spec = importlib.util.spec_from_file_location("eval_rag_hybrid_standalone", _eval_path)
    assert _spec and _spec.loader
    _eval_mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_eval_mod)
    EVAL_DATA = _eval_mod.EVAL_DATA
    normalize_pid = _eval_mod.normalize_pid

    fetch_n = int(max(float(top_k) * CHROMA_FETCH_MULTIPLIER, float(CHROMA_FETCH_MIN)))

    print("ChromaDB 연결 중...")
    client = chromadb.PersistentClient(path="./chroma_db", settings=Settings(anonymized_telemetry=False))
    ef = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL, device="cpu", normalize_embeddings=True)
    collection = client.get_collection("arxiv_papers", embedding_function=ef)
    print(f"  fetch_n={fetch_n} (K={top_k}, mult={CHROMA_FETCH_MULTIPLIER}, min={CHROMA_FETCH_MIN})\n")
    if args.no_detail:
        print(
            "[모드] --no-detail: 태그 분포·Δ 요약 위주 (상세 청크/상위5논문 생략).\n"
            "       K 스윕은: .venv/bin/python3 scripts/eval_rag_hybrid.py (기본 top_k 5,8,10,15)\n"
        )

    misses: list[tuple[dict, list[str]]] = []
    for item in EVAL_DATA:
        q = item["query"]
        relevant = {normalize_pid(p) for p in item["relevant_papers"]}
        pids = [
            normalize_pid(p)
            for p in hybrid_retrieve_paper_ids_for_eval(
                collection,
                q,
                fetch_n=fetch_n,
                top_k=top_k,
            )
        ]
        topk_set = set(pids)
        if relevant & topk_set:
            continue
        misses.append((item, pids))

    print(f"=== Production Recall@{top_k} 미스: {len(misses)}건 / 전체 {len(EVAL_DATA)}건 ===\n")

    summary: dict[str, int] = {
        RETRIEVAL_MISSING: 0,
        RANKING_DROP: 0,
        WEAK_MULTI_EVIDENCE: 0,
        WEAK_TITLE_SIGNAL: 0,
    }
    gaps_for_delta: list[float] = []

    for item, prod_topk_pids in misses:
        q = item["query"]
        rel = [normalize_pid(p) for p in item["relevant_papers"]]
        dbg = production_retrieval_debug_for_eval(collection, q, fetch_n=fetch_n)
        if dbg.get("error"):
            print(f"QUERY: {q!r}\n  ERROR: {dbg}\n")
            continue

        rows = dbg.get("ranked_papers") or []
        by_pid = {r["paper_id"]: r for r in rows if r.get("paper_id")}
        top1 = rows[0] if rows else None
        top1_final = float(top1.get("paper_score_final") or 0.0) if top1 else 0.0

        if args.no_detail:
            q_short = (q[:68] + "…") if len(q) > 70 else q
            print("-" * 72)
            print(f"QUERY: {q_short!r}")
        else:
            print("-" * 72)
            print(f"QUERY: {q!r}")
            print(f"  search_query: {dbg.get('search_query')!r}")
            print(f"  n_chunks_in_pool={dbg.get('n_chunks_in_pool')}  papers_in_pool={len(rows)}")
            print(f"  정답 paper_id(들): {rel}")
            print(f"  Production top-{top_k} (paper_id 순서): {prod_topk_pids}")
            if top1:
                print(
                    f"  [top1] paper_id={top1.get('paper_id')}  "
                    f"paper_score_final={top1_final:.6f}  title_sim={float(top1.get('title_sim') or 0):.4f}"
                )
            print("\n  === 자동 분석 (정답별) ===")

        line_parts: list[str] = []
        for tgt in rel:
            hit = by_pid.get(tgt)
            tags, hint = _classify_gt(hit, top_k=top_k, weak_title_thr=weak_title_thr)
            for t in tags:
                if t in summary:
                    summary[t] += 1

            if hit is None:
                if args.no_detail:
                    line_parts.append(f"{tgt}:pool✗ tags={tags}")
                else:
                    print(f"\n  --- paper_id={tgt} ---")
                    print(f"    rank: (없음)  |  top1 대비 Δ: n/a  |  title_sim: n/a")
                    print(f"    s1~s5: (풀에 없음)")
                    print(f"    tags: {tags}")
                    print(f"    hint: {hint}")
            else:
                gt_final = float(hit.get("paper_score_final") or 0.0)
                gap = top1_final - gt_final
                gaps_for_delta.append(gap)
                ts = float(hit.get("title_sim") or 0.0)
                rk = int(hit.get("rank") or 0)
                t5 = _pad5(list(hit.get("chunk_scores_top5") or []))
                sline = "  ".join(f"s{i+1}={t5[i]:.4f}" for i in range(5))
                if args.no_detail:
                    line_parts.append(
                        f"{tgt}:r{rk} Δ={gap:.4f} ts={ts:.2f} tags={','.join(tags)}"
                    )
                else:
                    print(f"\n  --- paper_id={tgt} ---")
                    print(f"    rank: {rk}  |  top1 대비 Δ(final): {gap:+.6f}  |  title_sim: {ts:.4f}")
                    print(f"    s1~s5: {sline}")
                    print(f"    tags: {tags}")
                    print(f"    hint: {hint}")
                    print(_fmt_row(hit))

        if args.no_detail and line_parts:
            print("  " + " | ".join(line_parts))

        if not args.no_detail:
            print("\n  [Production 상위 5논문 — 동일 지표]")
            for r in dbg.get("production_top5") or []:
                print(_fmt_row(r))
                print()

    print("\n" + "=" * 72)
    print("=== 🥇 태그 분포 (정답 논문 단위, 복수 태그 가능) ===")
    print(f"  {RETRIEVAL_MISSING}:        {summary[RETRIEVAL_MISSING]}")
    print(f"  {RANKING_DROP}:             {summary[RANKING_DROP]}")
    print(f"  {WEAK_MULTI_EVIDENCE}:      {summary[WEAK_MULTI_EVIDENCE]}")
    print(f"  {WEAK_TITLE_SIGNAL}:        {summary[WEAK_TITLE_SIGNAL]}")
    print()
    _print_case_blocks(summary)
    print()
    _print_delta_block(gaps_for_delta)
    print()
    print("=== 🥉 K 스윕 결과 해석 (eval_rag_hybrid) ===")
    print("  패턴 A: K↑ 할수록 Recall 계속 ↑ → 정답은 풀에 많음 → 순위(ranking) 문제")
    print("  패턴 B: K를 올려도 Recall이 거의 안 오름 → 후보 부족 → retrieval 문제")
    print()
    print("=== 다음 튜닝 (핵심 2개) ===")
    print("  1) title weight:  .venv/bin/python3 scripts/debug_production_miss.py --title-add-weight 0.15")
    print("                     동일하게 0.2 — P@1·MRR에 유효할 수 있음")
    print("  2) multi-evidence: agent_config에서 α·γ·δ·ε (예: 0.15 / 0.12 / 0.1 / 0.08) 실험")
    print()
    print("상태: 데이터·임베딩·Hybrid·BM25·Dedup 이후 → 남은 것은 랭킹 튜닝(마지막 10~20%).")
    print("\n끝.")


if __name__ == "__main__":
    main()
