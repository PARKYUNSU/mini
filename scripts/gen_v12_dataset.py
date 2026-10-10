#!/usr/bin/env python3
"""yunsur_v12 학습 데이터 — v9 의 RAG 400건만 '문서에 근거한 교사 답' 400건으로 바꾼다 (README §1~2).

  python3 scripts/gen_v12_dataset.py

- 잡담 300·계획 400 은 v9 와 바이트 동일(검증한다).
- RAG 400: 검증 통과분(final_pass.jsonl) 중 영어 답(본론 한글 비율 < 0.5) 제외 후 시드 0 으로 400건.
  instruction = 운영 사용자 메시지(문서 5편 + 템플릿) 그대로, system = 운영 시스템 프롬프트 그대로.
출력: finetune_datasets/v12/train_data_v12.jsonl, stats.json
"""
import collections
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V9 = ROOT / "finetune_datasets" / "v9" / "train_data_v9.jsonl"
D = ROOT / "finetune_datasets" / "v12"


def main() -> int:
    v9_lines = [l for l in V9.read_text(encoding="utf-8").splitlines() if l.strip()]
    keep = [l for l in v9_lines if json.loads(l)["slot"] != "rag"]
    P = {json.loads(l)["src_pid"]: json.loads(l) for l in (D / "prompts.jsonl").read_text().splitlines() if l.strip()}
    F = [json.loads(l) for l in (D / "final_pass.jsonl").read_text().splitlines() if l.strip()]
    pool = sorted((f for f in F if f["ko"] >= 0.5), key=lambda f: f["src_pid"])
    pick = random.Random(0).sample(pool, 400)
    rag = [json.dumps({"slot": "rag", "system": P[f["src_pid"]]["system"], "instruction": P[f["src_pid"]]["user"],
                       "output": f["answer"], "source": f"v12_teacher_gptoss120b ({f['stage']})"}, ensure_ascii=False)
           for f in pick]
    out = keep + rag
    random.Random(1).shuffle(out)
    (D / "train_data_v12.jsonl").write_text("\n".join(out) + "\n", encoding="utf-8")
    # 잡담·계획이 v9 와 바이트 동일한지
    assert collections.Counter(keep) == collections.Counter(l for l in out if json.loads(l)["slot"] != "rag")
    stats = {
        "version": "v12", "samples": len(out),
        "slot_dist": dict(collections.Counter(json.loads(l)["slot"] for l in out)),
        "rag_pool": len(pool), "rag_gold_in_context": sum(f["gold"] for f in pick),
        "rag_stage": dict(collections.Counter(f["stage"] for f in pick)),
        "change": {"kind": "replace_slot", "slot": "rag", "rows": 400,
                   "from": "v9 RAG 400 (문서 없음, 기억 에세이)", "to": "운영 프롬프트(문서 5편) + gpt-oss-120b 교사 + 근거 검증"},
        "note": "max_seq_length 3072 로 학습 (MAX_SEQ_LENGTH) — RAG 입력+답이 2048 을 넘는다 (표본 25건 중 16건, 최대 2372).",
    }
    (D / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
