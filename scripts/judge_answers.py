#!/usr/bin/env python3
"""RAG 답변이 정답 논문을 정확히 설명하는지 더 강한 모델(Groq gpt-oss-120b)로 판정한다.

설계: docs/experiments/answer_quality_1010/README.md

  .venv/bin/python scripts/judge_answers.py --label ans_full
  .venv/bin/python scripts/judge_answers.py --label ans_v13 --base-url <vLLM /v1>   # RunPod H100 gpt-oss-120b, 병렬

입력: docs/experiments/e2e_ko_1008/results/<label>.jsonl (eval_e2e_ko.py --answer 출력)
출력: docs/experiments/answer_quality_1010/judged_<label>.jsonl
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "docs" / "experiments" / "answer_quality_1010"

PROMPT = """You are grading a research assistant's answer.

The user asked (in Korean):
{question}

The paper the user was looking for (the correct answer):
- arXiv ID: {pid}
- Title: {title}
- Abstract: {abstract}

The assistant's answer:
<<<
{answer}
>>>

Judge ONLY against the paper above. Return a single JSON object, no other text:
{{"identifies_paper": true|false,       // does the answer present this paper (by ID or unmistakable title/description) as a result?
  "description": "correct"|"partial"|"wrong"|"absent",
      // correct = the main contribution is described accurately; partial = right paper but key point missing or vague;
      // wrong = attributes claims to this paper that contradict the abstract; absent = the paper is not described
  "fabrication": true|false,            // does the answer state specific facts about this paper (numbers, methods, results) not supported by the abstract?
  "note": "<one short sentence>"}}"""


def load_corpus() -> dict[str, dict]:
    out: dict[str, dict] = {}
    files = sorted(glob.glob(str(ROOT / "raw_data_queue/processed/crawled_papers*.jsonl")))
    files.append(str(ROOT / "raw_data_queue/crawled_papers.jsonl"))
    for f in files:
        for line in open(f, encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("paper_id"):
                out[re.sub(r"v\d+$", "", d["paper_id"])] = d
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--resume", action="store_true", help="기존 출력에서 판정되지 않은 문항만 다시")
    ap.add_argument("--pace", type=float, default=3.0, help="호출 사이 대기(초) — Groq 분당 한도")
    ap.add_argument("--base-url", default="", help="OpenAI 호환 서버(vLLM). 주면 Groq 대신 병렬로 쓴다")
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args()
    if args.base_url:
        return run_openai(args)

    from core.llm.agent_llm import GROQ_CODING_MODEL, get_coding_groq_llm, normalize_ai_message_content

    rows = [json.loads(l) for l in (ROOT / f"docs/experiments/e2e_ko_1008/results/{args.label}.jsonl").read_text().splitlines()]
    questions = dict(l.split("\t", 1) for l in (ROOT / "docs/experiments/e2e_ko_1008/ko_questions.tsv").read_text().splitlines())
    gold = {json.loads(l)["id"]: json.loads(l)["relevant_papers"] for l in (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines()}
    corpus = load_corpus()
    llm = get_coding_groq_llm()
    print(f"judge={GROQ_CODING_MODEL} 문항={len(rows)}", flush=True)

    EXP.mkdir(parents=True, exist_ok=True)
    out_path = EXP / f"judged_{args.label}.jsonl"
    prev: dict[str, dict] = {}
    if args.resume and out_path.exists():
        prev = {x["id"]: x for x in map(json.loads, out_path.read_text(encoding="utf-8").splitlines())}
    # 임시 파일에 쓰고 끝에서 교체한다 — 중간에 멈추면 이미 판정한 행을 잃던 문제(2026-10-10).
    tmp_path = out_path.with_suffix(".jsonl.tmp")
    with tmp_path.open("w", encoding="utf-8") as w:
        for k, r in enumerate(rows, 1):
            old = prev.get(r["id"])
            if old and (old.get("judged") or old.get("reason")):
                w.write(json.dumps(old, ensure_ascii=False) + "\n")
                continue
            res: dict = {"id": r["id"], "slot": r["slot"], "route": r["route"], "ctx_ok": r["ok"]}
            answer = (r.get("answer") or "").strip()
            if r["route"] != "direct_answer/B" or not answer:
                res.update({"judged": False, "reason": "not_rag_or_empty"})
            else:
                # 정답이 여럿(C1 survey)이면 답변이 인용한 정답 중 첫 번째, 없으면 목록의 첫 번째로 판정
                cited = [g for g in gold[r["id"]] if g in (r.get("answer_papers") or [])]
                pid = (cited or gold[r["id"]])[0]
                p = corpus.get(pid, {})
                prompt = PROMPT.format(question=questions[r["id"]], pid=pid, title=p.get("title", ""),
                                       abstract=(p.get("abstract") or "")[:2000], answer=answer[:4000])
                verdict = None
                time.sleep(args.pace)
                for attempt in range(5):
                    try:
                        raw = normalize_ai_message_content(llm.invoke(prompt))
                        m = re.search(r"\{.*\}", raw, re.S)
                        verdict = json.loads(m.group(0)) if m else None
                        if verdict:
                            break
                    except Exception as exc:  # 재시도
                        print(f"  재시도 {r['id']}: {type(exc).__name__}: {str(exc)[:160]}", flush=True)
                        time.sleep(30 * (attempt + 1))
                res.update({"judged": verdict is not None, "gold_judged": pid, **(verdict or {})})
                if verdict is None:
                    res["reason"] = "judge_error"  # --resume 이 다시 붙잡지 않게 남긴다
            w.write(json.dumps(res, ensure_ascii=False) + "\n")
            w.flush()
            print(f"[{k}/{len(rows)}] {r['id']} {res.get('description', res.get('reason', '?'))}", flush=True)
    tmp_path.replace(out_path)
    print(f"저장: {out_path}")
    return 0


def build_prompt(r: dict, questions: dict, gold: dict, corpus: dict) -> tuple[str, str]:
    cited = [g for g in gold[r["id"]] if g in (r.get("answer_papers") or [])]
    pid = (cited or gold[r["id"]])[0]
    p = corpus.get(pid, {})
    return pid, PROMPT.format(question=questions[r["id"]], pid=pid, title=p.get("title", ""),
                              abstract=(p.get("abstract") or "")[:2000], answer=(r.get("answer") or "").strip()[:4000])


def run_openai(args) -> int:
    """vLLM(gpt-oss-120b) 병렬 판정 — 프롬프트·출력 형식은 Groq 경로와 같다."""
    from concurrent.futures import ThreadPoolExecutor

    import requests

    rows = [json.loads(l) for l in (ROOT / f"docs/experiments/e2e_ko_1008/results/{args.label}.jsonl").read_text().splitlines()]
    questions = dict(l.split("\t", 1) for l in (ROOT / "docs/experiments/e2e_ko_1008/ko_questions.tsv").read_text().splitlines())
    gold = {json.loads(l)["id"]: json.loads(l)["relevant_papers"] for l in (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines()}
    corpus = load_corpus()
    url = args.base_url.rstrip("/") + "/chat/completions"

    def one(r: dict) -> dict:
        res: dict = {"id": r["id"], "slot": r["slot"], "route": r["route"], "ctx_ok": r["ok"]}
        if r["route"] != "direct_answer/B" or not (r.get("answer") or "").strip():
            return {**res, "judged": False, "reason": "not_rag_or_empty"}
        pid, prompt = build_prompt(r, questions, gold, corpus)
        verdict = None
        for attempt in range(4):
            try:
                body = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0, "max_tokens": 4000, "reasoning_effort": "medium"}
                raw = requests.post(url, json=body, timeout=600).json()["choices"][0]["message"]["content"] or ""
                m = re.search(r"\{.*\}", raw, re.S)
                verdict = json.loads(m.group(0)) if m else None
                if verdict:
                    break
            except Exception as exc:
                print(f"  재시도 {r['id']}: {type(exc).__name__}: {str(exc)[:120]}", flush=True)
                time.sleep(10 * (attempt + 1))
        res.update({"judged": verdict is not None, "gold_judged": pid, **(verdict or {})})
        if verdict is None:
            res["reason"] = "judge_error"
        return res

    with ThreadPoolExecutor(args.workers) as ex:
        out = list(ex.map(one, rows))
    out_path = EXP / f"judged_gptoss_{args.label}.jsonl"
    out_path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out), encoding="utf-8")
    print(f"저장: {out_path} · 판정 {sum(x.get('judged', False) for x in out)}/{len(out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
