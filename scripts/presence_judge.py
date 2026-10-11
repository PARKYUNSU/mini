#!/usr/bin/env python3
"""정답 유무 판정 호출을 오프라인으로 잰다 — docs/experiments/presence_judge_1011/README.md.

  .venv/bin/python scripts/presence_judge.py --model qwen3.5:9b
  .venv/bin/python scripts/presence_judge.py --model yunsur_v13

입력: e2e_ko_1008/results/ctx_1011.jsonl (eval_e2e_ko.py --save-context), 비교 기준 ans_v13.jsonl
출력: docs/experiments/presence_judge_1011/judge_<model>.jsonl + 요약 출력
판정 설정은 운영 로컬 호출과 같다: Ollama, reasoning=False, temperature 0, seed 0.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "docs" / "experiments" / "e2e_ko_1008" / "results"
EXP = ROOT / "docs" / "experiments" / "presence_judge_1011"

# 측정 전에 고정 (README §2). 바꾸면 새 측정으로 기록한다.
PROMPT = """아래 [참고 문서]는 사용자의 질문으로 검색한 논문 발췌다. 사용자는 **특정한 연구 하나**를 찾고 있다.

질문이 묘사하는 바로 그 연구가 참고 문서 중에 있으면 그 문서 번호를, 없으면 `없음`을 답하라.
- 주제만 비슷하고 질문이 묘사하는 방법·대상·결과와 맞지 않으면 `없음`이다.
- 같은 논문이 여러 번호에 나뉘어 있으면 가장 앞 번호 하나만 적는다.

출력은 정확히 한 줄: `답: 문서 N` 또는 `답: 없음`

[질문]
{question}

[참고 문서]
{context}"""

ANS = re.compile(r"답\s*[:：]\s*(?:\[?\s*문서\s*(\d{1,2})\s*\]?|(없음))")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--ctx", default="ctx_1011")
    ap.add_argument("--ref", default="ans_v13", help="context_papers 가 같은 문항만 쓴다")
    args = ap.parse_args()

    from langchain_ollama import ChatOllama

    llm = ChatOllama(model=args.model, temperature=0.0, seed=0, reasoning=False, num_predict=64)
    C = {json.loads(l)["id"]: json.loads(l) for l in (RES / f"{args.ctx}.jsonl").read_text().splitlines()}
    R = {json.loads(l)["id"]: json.loads(l) for l in (RES / f"{args.ref}.jsonl").read_text().splitlines()}
    questions = dict(l.split("\t", 1) for l in (ROOT / "docs/experiments/e2e_ko_1008/ko_questions.tsv").read_text().splitlines())
    gold = {json.loads(l)["id"]: {re.sub(r"v\d+$", "", g) for g in json.loads(l)["relevant_papers"]}
            for l in (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines()}
    ids = [i for i in C if C[i]["route"] == "direct_answer/B" and C[i].get("numbered_context")
           and i in R and R[i]["route"] == "direct_answer/B" and R[i]["context_papers"] == C[i]["context_papers"]]
    print(f"model={args.model} 문항={len(ids)} (ctx 와 {args.ref} 컨텍스트 동일)", flush=True)

    EXP.mkdir(parents=True, exist_ok=True)
    out = []
    for k, i in enumerate(ids, 1):
        c = C[i]
        t0 = time.time()
        raw = str(llm.invoke(PROMPT.format(question=questions[i], context=c["numbered_context"])).content or "")
        dt = time.time() - t0
        m = ANS.search(raw)
        pick = None if not m else ("없음" if m.group(2) else int(m.group(1)))
        gold_nums = [n + 1 for n, p in enumerate(c["doc_ids"]) if p in gold[i]]
        row = {"id": i, "gold_in_context": bool(gold_nums), "gold_nums": gold_nums, "pick": pick,
               "format_ok": m is not None, "raw": raw[:200], "sec": round(dt, 2)}
        out.append(row)
        print(f"[{k}/{len(ids)}] {i} gold={gold_nums} pick={pick} {dt:.1f}s", flush=True)
    suffix = "" if args.ctx == "ctx_1011" else f"_{args.ctx}"  # 기본 컨텍스트 외에는 이름을 달리해 덮어쓰지 않는다
    path = EXP / f"judge_{args.model.replace(':', '_')}{suffix}.jsonl"
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out), encoding="utf-8")

    g = [r for r in out if r["gold_in_context"]]
    ng = [r for r in out if not r["gold_in_context"]]
    false_none = sum(r["pick"] == "없음" for r in g)
    none_recall = sum(r["pick"] == "없음" for r in ng)
    right_num = sum(isinstance(r["pick"], int) and r["pick"] in r["gold_nums"] for r in g)
    print(f"\n=== {args.model} ===")
    print(f"정답 있음 {len(g)}: 거짓 '없음' {false_none} ({false_none / max(len(g), 1):.1%}) · 정답 번호 {right_num} ({right_num / max(len(g), 1):.1%})")
    print(f"정답 없음 {len(ng)}: '없음' 재현 {none_recall}/{len(ng)}")
    print(f"형식 오류 {sum(not r['format_ok'] for r in out)} · 평균 {sum(r['sec'] for r in out) / max(len(out), 1):.1f}s")
    ok = false_none <= 0.05 * len(g) and none_recall >= 7
    print(f"기준(거짓 '없음' ≤ 5% 그리고 재현 ≥ 7/21): {'통과' if ok else '미달'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
