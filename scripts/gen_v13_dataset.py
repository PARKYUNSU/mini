#!/usr/bin/env python3
"""yunsur_v13 학습 데이터 — v12 에서 정답 없는 RAG 30건의 답만 새 형식으로 바꾼다 (yunsur_v13 README §2).

  python3 scripts/gen_v13_dataset.py

- v12 의 나머지 1,070행(RAG 정답 있음 370 · 잡담 300 · 계획 400)은 바이트 동일 (검증한다).
- 정답 없는 30행: finetune_datasets/v13/nogold.jsonl 의 답으로 교체. 대체된 프롬프트(replaced)는
  instruction/system 도 그 프롬프트 것으로 바꾼다. 행 순서는 v12 와 같다.
출력: finetune_datasets/v13/train_data_v13.jsonl, stats.json
"""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V12 = ROOT / "finetune_datasets" / "v12"
D = ROOT / "finetune_datasets" / "v13"


def main() -> int:
    P = {json.loads(l)["src_pid"]: json.loads(l) for l in (V12 / "prompts.jsonl").read_text().splitlines() if l.strip()}
    F = {json.loads(l)["answer"]: json.loads(l)["src_pid"] for l in (V12 / "final_pass.jsonl").read_text().splitlines() if l.strip()}
    targets = json.loads((D / "v12_nogold_pids.json").read_text())
    new = [json.loads(l) for l in (D / "nogold.jsonl").read_text().splitlines() if l.strip()]
    assert len(new) == len(targets), f"새 답 {len(new)} != 대상 {len(targets)}"
    by_pid = {n["src_pid"]: n for n in new}
    replacements = [n for n in new if n["replaced"]]
    spare_iter = iter(replacements)

    lines = [l for l in (V12 / "train_data_v12.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    out, swapped, kept = [], 0, []
    for l in lines:
        r = json.loads(l)
        pid = F.get(r["output"]) if r["slot"] == "rag" else None
        if pid in targets:
            n = by_pid.get(pid) or next(spare_iter)
            p = P[n["src_pid"]]
            out.append(json.dumps({"slot": "rag", "system": p["system"], "instruction": p["user"], "output": n["answer"],
                                   "source": "v13_teacher_gptoss120b (nogold_format)"}, ensure_ascii=False))
            swapped += 1
        else:
            out.append(l)
            kept.append(l)
    assert swapped == len(targets)
    assert len(kept) == len(lines) - len(targets)
    (D / "train_data_v13.jsonl").write_text("\n".join(out) + "\n", encoding="utf-8")
    stats = {
        "version": "v13", "samples": len(out),
        "slot_dist": dict(collections.Counter(json.loads(l)["slot"] for l in out)),
        "change": {"kind": "replace_rows", "rows": swapped, "replaced_prompts": len(replacements),
                   "from": "v12 정답 없는 RAG 30 (서론만 '없다', 결론 9/30 만 '없다')",
                   "to": "서론·본론(관련 연구)·결론 모두 '없다' 형식, 근거 검증 통과"},
        "unchanged_rows": len(kept),
        "note": "MAX_SEQ_LENGTH=3072, 하이퍼파라미터 v12 와 동일",
    }
    (D / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
