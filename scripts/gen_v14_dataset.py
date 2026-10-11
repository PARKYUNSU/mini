#!/usr/bin/env python3
"""yunsur_v14 학습 데이터 — v13 에서 정답 있는 RAG 30행을 정답 없는 새 30행으로 바꾼다 (yunsur_v14 README §2).

  python3 scripts/gen_v14_dataset.py

- 정답 없음 30 → 60 (7.5% → 15%), 정답 있음 370 → 340. 총 1,100 유지.
- 빠지는 정답 있음 30행: v13 정답 있음 행 중 시드 0. 그 자리에 새 정답 없음 행을 넣는다(순서 유지).
- 나머지 1,070행은 v13 과 바이트 동일 (검증한다).
출력: finetune_datasets/v14/train_data_v14.jsonl, stats.json
"""
import collections
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V12 = ROOT / "finetune_datasets" / "v12"
V13 = ROOT / "finetune_datasets" / "v13"
D = ROOT / "finetune_datasets" / "v14"


def main() -> int:
    P = {json.loads(l)["src_pid"]: json.loads(l) for l in (V12 / "prompts.jsonl").read_text().splitlines() if l.strip()}
    by_user = {p["user"]: p for p in P.values() if p.get("user")}
    new = [json.loads(l) for l in (D / "nogold.jsonl").read_text().splitlines() if l.strip()]
    assert len(new) == 30, len(new)
    lines = [l for l in (V13 / "train_data_v13.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = [json.loads(l) for l in lines]
    gold_idx = [k for k, r in enumerate(rows) if r["slot"] == "rag" and by_user[r["instruction"]]["gold_in_context"]]
    nogold_idx = [k for k, r in enumerate(rows) if r["slot"] == "rag" and not by_user[r["instruction"]]["gold_in_context"]]
    assert len(gold_idx) == 370 and len(nogold_idx) == 30, (len(gold_idx), len(nogold_idx))
    drop = sorted(random.Random(0).sample(gold_idx, 30))
    it = iter(new)
    out = list(lines)
    for k in drop:
        n = next(it)
        p = P[n["src_pid"]]
        out[k] = json.dumps({"slot": "rag", "system": p["system"], "instruction": p["user"], "output": n["answer"],
                             "source": "v14_teacher_gptoss120b (nogold_format)"}, ensure_ascii=False)
    kept = [l for k, l in enumerate(lines) if k not in set(drop)]
    assert collections.Counter(kept) == collections.Counter(l for k, l in enumerate(out) if k not in set(drop))
    (D / "train_data_v14.jsonl").write_text("\n".join(out) + "\n", encoding="utf-8")
    final = [json.loads(l) for l in out]
    ng = sum(1 for r in final if r["slot"] == "rag" and not by_user[r["instruction"]]["gold_in_context"])
    stats = {
        "version": "v14", "samples": len(out),
        "slot_dist": dict(collections.Counter(r["slot"] for r in final)),
        "rag_nogold": ng, "rag_gold": 400 - ng,
        "change": {"kind": "ratio", "from": "v13 정답 없음 30/400 (7.5%)", "to": f"정답 없음 {ng}/400",
                   "replaced_gold_rows": len(drop), "new_prompts_replaced": sum(n["replaced"] for n in new)},
        "unchanged_rows": len(kept),
        "note": "MAX_SEQ_LENGTH=3072, 하이퍼파라미터 v13 과 동일",
    }
    (D / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
