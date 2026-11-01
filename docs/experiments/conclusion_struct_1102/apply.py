"""conclusion_struct_1102 §2 — 저장된 답에 swap_conclusion(D)을 오프라인으로 적용한다(운영 코드 그대로 · 플래그는 안 켬).

    .venv/bin/python docs/experiments/conclusion_struct_1102/apply.py OUT IN [IN ...]
    예) apply.py cs1_dev recheck_1031 weekly_20261101   ·   apply.py cs1_heldout cs0_heldout

e2e_ko_1008/results/{IN}.jsonl 을 읽어 {OUT}.jsonl 에 행마다 상태 · 전/후 답 · 바꾼 문장 쌍 · 영어로 둔 사유 · 번역 초를 쓴다.
화면에는 수만 찍는다(held-out 답 내용은 판정 묶음을 만들기 전에 안 본다). OUT 이 있으면 덮어쓰지 않고 멈춘다.
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from core.config.agent_config import RAG_ANSWER_MODEL  # noqa: E402
from core.llm.answer_fix import _CITED  # noqa: E402
from core.llm.conclusion_swap import _translator, swap_conclusion  # noqa: E402

RES = ROOT / "docs" / "experiments" / "e2e_ko_1008" / "results"


def main() -> int:
    out_label, *ins = sys.argv[1:]
    out = RES / f"{out_label}.jsonl"
    if out.exists():
        print(f"{out.name} 이 이미 있다 — 덮어쓰지 않는다")
        return 2
    tr = _translator(RAG_ANSWER_MODEL)
    rows = []
    for lab in ins:
        for line in (RES / f"{lab}.jsonl").open(encoding="utf-8"):
            r = json.loads(line)
            if not (r.get("answer") and r.get("numbered_context")):
                rows.append({"id": r["id"], "slot": r.get("slot"), "src": lab, "status": "답 없음", "changed": False})
                continue
            ids = {i + 1: p for i, p in enumerate(r["doc_ids"])}
            after, status, info = swap_conclusion(r["answer"], r["numbered_context"], ids, RAG_ANSWER_MODEL, translate=tr)
            cb, ca = sorted(set(_CITED.findall(r["answer"]))), sorted(set(_CITED.findall(after)))
            rows.append({"id": r["id"], "slot": r.get("slot"), "src": lab, "status": status, "changed": after != r["answer"],
                         "before": r["answer"], "after": after, **info, "cited_same": cb == ca,
                         "cited_before": cb, "cited_after": ca})
    with out.open("w", encoding="utf-8") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    ch = [x for x in rows if x["changed"]]
    print(f"답 {len(rows)} · 바뀐 답 {len(ch)} · 상태 {dict(Counter(x['status'].split()[0] for x in rows))}")
    print(f"바꾼 인용 문장 {sum(len(x['pairs']) for x in ch)} · 넣은 문장 {sum(len(p['after']) for x in ch for p in x['pairs'])}"
          f" · 영어로 둠 {dict(Counter(w.split()[0] for x in ch for w in x['fallback']))} · 본론 밖 뺌 {sum(x['dropped'] for x in ch)}")
    if ch:
        print(f"번역 초 중앙 {statistics.median(x['tsec'] for x in ch):.1f} · 최대 {max(x['tsec'] for x in ch):.1f}"
              f" · 인용 집합 다른 답 {sum(not x['cited_same'] for x in ch)}")
    print("갈래별 바뀐 답", dict(sorted(Counter(x["slot"] for x in ch).items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
