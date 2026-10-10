#!/usr/bin/env python3
"""v12 RAG 학습용 한국어 질문을 코퍼스 논문에서 만든다 — docs/experiments/yunsur_v12/README.md §2.

  .venv/bin/python scripts/gen_v12_questions.py --n 700

- 로컬 base(qwen3.5:9b)로 생성한다 (무료). 평가 세트 정답 논문은 뽑지 않는다.
- 평가 162문항과 임베딩 유사도(다국어 MiniLM) ≥ 0.85 인 질문은 버린다(§2.1).
- 이어서 하기: 출력에 이미 있는 src_pid 는 건너뛴다.
출력: finetune_datasets/v12/questions.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "finetune_datasets" / "v12" / "questions.jsonl"
SIM_MAX = 0.85  # 다국어 임베더 기준 — README §2.1

PAPER_PROMPT = """아래 논문을 찾고 싶은 사용자가 챗봇에게 할 법한 한국어 질문을 **한 문장** 만들어라.

규칙:
- 논문 제목·arXiv ID·저자는 쓰지 않는다. 방법 이름(약어)도 되도록 쓰지 않고 **무엇을 어떻게 했는지**로 묘사한다.
- 초록의 핵심 기여 한두 가지를 구체적으로 짚는다 (너무 일반적이면 안 된다).
- 끝맺음은 "~연구 있어?", "~방법 알려줘", "~논문 설명해줘", "~연구 요약해줘" 중 하나처럼 자연스럽게.
- 질문 한 문장만 출력한다. 따옴표·설명·번호 금지.

예시 (다른 논문들):
대규모 언어모델이 표 데이터를 이해하도록 행과 열 구조를 프롬프트에 넣는 방법 알려줘
의료 영상에서 라벨 없이 병변을 분할하는 자기지도 학습 연구 있어?
강화학습 에이전트가 보상 함수의 허점을 파고들지 못하게 막는 방법을 다룬 논문 설명해줘

논문 제목: {title}
초록: {abstract}

질문:"""

SURVEY_PROMPT = """아래 서베이(리뷰) 논문을 찾는 사용자가 챗봇에게 할 법한 짧은 한국어 질문을 **한 문장** 만들어라.

규칙:
- 제목을 그대로 옮기지 말고 주제를 한국어로 짧게 말한다. "서베이", "리뷰", "정리한 글" 중 하나를 넣는다.
- 끝맺음은 "~서베이 알려줘", "~정리한 리뷰 있어?", "~서베이 요약해줘" 처럼.
- 질문 한 문장만 출력한다.

예시: 그래프 신경망을 추천 시스템에 쓰는 연구를 정리한 서베이 알려줘

논문 제목: {title}
초록: {abstract}

질문:"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=700)
    ap.add_argument("--survey-frac", type=float, default=0.15)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    from langchain_core.messages import HumanMessage
    from langchain_ollama import ChatOllama
    from sentence_transformers import SentenceTransformer

    from core.config.agent_config import ollama_kwargs
    from scripts.judge_answers import load_corpus

    corpus = load_corpus()
    evalset = [json.loads(l) for l in (ROOT / "docs/experiments/retrieval_eval_1007/eval_set.jsonl").read_text().splitlines() if l.strip()]
    eval_gold = {re.sub(r"v\d+$", "", g) for e in evalset for g in e["relevant_papers"]}
    eval_q = [l.split("\t", 1)[1] for l in (ROOT / "docs/experiments/e2e_ko_1008/ko_questions.tsv").read_text().splitlines() if "\t" in l]

    pool = sorted(p for p, d in corpus.items() if p not in eval_gold and d.get("abstract") and d.get("title"))
    rng = random.Random(args.seed)
    surveys = [p for p in pool if re.search(r"survey|review", corpus[p]["title"], re.I)]
    others = [p for p in pool if p not in set(surveys)]
    rng.shuffle(surveys)
    rng.shuffle(others)
    n_s = int(args.n * args.survey_frac)
    picks = [(p, "survey") for p in surveys[:n_s]] + [(p, "paper") for p in others[: args.n - min(n_s, len(surveys))]]
    rng.shuffle(picks)

    done = set()
    if OUT.exists():
        done = {json.loads(l)["src_pid"] for l in OUT.read_text().splitlines() if l.strip()}
    emb = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", device="cpu")
    eval_v = emb.encode(eval_q, normalize_embeddings=True)
    llm = ChatOllama(**ollama_kwargs(temperature=0.7, top_p=0.9, reasoning=False, num_predict=160, model="qwen3.5:9b"))

    kept = dropped = 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("a", encoding="utf-8") as w:
        for k, (pid, kind) in enumerate(picks, 1):
            if pid in done:
                continue
            d = corpus[pid]
            tmpl = SURVEY_PROMPT if kind == "survey" else PAPER_PROMPT
            raw = str(llm.invoke([HumanMessage(content=tmpl.format(title=d["title"], abstract=d["abstract"][:1500]))]).content)
            q = raw.strip().splitlines()[-1].strip().strip('"“”\'') if raw.strip() else ""
            if not q or len(q) < 10 or not re.search(r"[가-힣]", q) or re.search(r"\d{4}\.\d{4,5}", q):
                dropped += 1
                continue
            sim = float((emb.encode([q], normalize_embeddings=True) @ eval_v.T).max())
            row = {"src_pid": pid, "kind": kind, "question": q, "max_eval_sim": round(sim, 3), "keep": sim < SIM_MAX}
            w.write(json.dumps(row, ensure_ascii=False) + "\n")
            w.flush()
            kept += row["keep"]
            print(f"[{k}/{len(picks)}] {kind} sim={sim:.2f} {q[:70]}", flush=True)
    print(f"완료: 유지 {kept} · 생성 실패 {dropped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
