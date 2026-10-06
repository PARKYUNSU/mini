"""심층 모드(`wants_depth`)가 실제로 효과를 내는지 **짝지어** 재다.

앞선 측정(07_single_path)은 wants_depth 시행이 4개뿐이고 문서 수가 섞여 있어
판정하지 못했다. 게다가 rag_context **길이를 기록하지 않아** 심층 경로의
same-paper merge(상한 8000자)가 더 많은 텍스트를 줬는지 확인할 수 없었다.

설계: 같은 질문의 `자세히` 유무 쌍 6개 × 3회 = 36시행. 사전 검증으로 쌍의 두
변형이 **모두 단일 경로**이고 **심층 플래그만 다르다**(len<=44 유지).
컨텍스트 길이를 트레이스에서 뽑아 기록한다 — 지시 효과와 컨텍스트 양을 분리해야 한다.
"""
import io, json, re, sys, contextlib

sys.path.insert(0, "/Volumes/T7 Shield/mini")
from core.graph.agent_nodes import direct_answer_node

PAIRS = [
    ("RAG 환각 원인 설명해줘.", "RAG 환각 원인 자세히 설명해줘."),
    ("리랭커 개선 방법 알려줘.", "리랭커 개선 방법 자세히 알려줘."),
    ("KV 캐시 압축 기법 설명해줘.", "KV 캐시 압축 기법 자세히 설명해줘."),
    ("청킹 전략 설명해줘.", "청킹 전략 자세히 설명해줘."),
    ("지식 그래프 RAG 요약해줘.", "지식 그래프 RAG 자세히 요약해줘."),
    ("멀티홉 질의응답 접근 알려줘.", "멀티홉 질의응답 접근 자세히 알려줘."),
]
REPEATS = 3

out = []
n = 0
total = len(PAIRS) * 2 * REPEATS
for pi, pair in enumerate(PAIRS, 1):
    for kind, q in zip(("normal", "depth"), pair):
        for t in range(1, REPEATS + 1):
            n += 1
            state = {"user_request": q, "router_choice": "B"}
            config = {"configurable": {"chat_id": f"depth_{pi}_{kind}_{t}", "bot": None}}
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    res = direct_answer_node(state, config=config)
                err = ""
            except Exception as e:  # noqa: BLE001
                res, err = {}, f"{type(e).__name__}: {e}"
            log = buf.getvalue()
            g = lambda rx: (re.search(rx, log).group(1) if re.search(rx, log) else None)
            # 컨텍스트 길이: 필터 단계의 len= (심층은 same-paper merged, 일반은 top-1 only)
            ctx_len = g(r"rag_context (?:same-paper merged \(depth\)|top-1 only|top-5 only) \| len=(\d+)")
            out.append({
                "pair": pi, "kind": kind, "q": q, "trial": t, "error": err,
                "wants_depth": g(r"wants_depth=(\w+)"),
                "prefer_single_hit": g(r"prefer_single_hit=(\w+)"),
                "ctx_len": int(ctx_len) if ctx_len else None,
                "docs": int(g(r"numbered \| docs=(\d+)") or 0) or None,
                "answer": res.get("direct_response") or "",
            })
            print(f"[{n}/{total}] {kind:6} {q}", file=sys.stderr, flush=True)

with open(".cron/depth_paired.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done", file=sys.stderr)
