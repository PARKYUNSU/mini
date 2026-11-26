"""주간 신규 논문 다이제스트 (6차 피드백 작업 4 · 7차 승인, 설계 .cron/work_1126/design_feedback_digest.md).

주제마다: 지난 7일 OpenAlex 신규 논문 + 매일 수집분(published 7일 이내) → 27B 문서 판정(운영 judge_docs)에서
직접 · 부분만 → 주제당 최대 5편 → 초록 기반 1~2문장 요약(숫자는 초록에 있는 것만) → 텔레그램 DM.

    .venv/bin/python scripts/weekly_digest.py            # 미리 보기 파일만 (.cron/digest/YYYY-MM-DD.md)
    .venv/bin/python scripts/weekly_digest.py --send     # 사용자 DM 으로 (처음 4주는 DM 만 — 팀 채널은 별도 승인)

비용 0원(로컬 모델 + OpenAlex 무료 키). 주제 이름 · 검색어에 회사 · 고객 이름을 넣지 않는다.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv  # noqa: E402

load_dotenv()

TOPICS = [
    ("ESG · 지속가능성 공시 NLP", "ESG sustainability disclosure report natural language processing",
     "ESG · 지속가능성 공시 문서를 NLP 나 LLM 으로 분석 · 추출 · 분류하는 연구", r"\b(?:ESG|sustainab\w*|climate|TCFD|GRI|ISSB|disclosure)"),
    ("RAG 평가 · 근거 충실도", "retrieval-augmented generation evaluation faithfulness",
     "RAG 시스템이나 LLM 답변의 근거 충실도 · 인용 · 검색 품질을 평가하는 연구", r"\b(?:RAG|retrieval-augmented|faithful\w*|grounded\w*|citation)"),
    ("문서 · 표 추출", "document parsing table extraction PDF",
     "PDF 등 문서에서 표 · 구조 · 숫자를 추출하거나 파싱하는 연구", r"\b(?:table|tabular|document parsing|PDF|layout)"),
    ("LLM 판정자 · 평가", "LLM as a judge evaluation agreement",
     "LLM 을 판정자로 쓸 때 사람 판단과의 일치 · 신뢰성을 다루는 연구", r"\b(?:LLM-as-a-judge|LLM judge|judges?|evaluator)"),
]
MAX_PER_TOPIC = 5
OUT_DIR = Path(".cron/digest")


def openalex_new(query: str, since: date) -> list[dict]:
    """지난 7일 공개된 OpenAlex 논문 (arXiv ID · 초록 있는 것만)."""
    import requests

    from core.rag.external_search import OPENALEX_URL, _abstract, _arxiv_id

    key = os.getenv("OPENALEX_API_KEY", "").strip()
    try:
        r = requests.get(OPENALEX_URL, params={
            "search": query, "per-page": 25, "filter": f"from_publication_date:{since.isoformat()}",
            "select": "id,title,ids,doi,publication_year,locations,abstract_inverted_index"},
            headers={"Authorization": f"Bearer {key}"} if key else None, timeout=30)
        r.raise_for_status()
        works = r.json().get("results") or []
    except Exception as exc:  # 외부 장애면 그 주제는 수집분만
        print(f"[digest] OpenAlex 실패: {type(exc).__name__}: {str(exc)[:120]}")
        return []
    out = []
    for w in works:
        ax, ab = _arxiv_id(w), _abstract(w)
        # OpenAlex 공개일은 옛 arXiv 논문도 새로 잡는다(2506.10016) — arXiv 번호의 연월이 한 달 안인 것만
        if ax and ax[:4] < (since - timedelta(days=31)).strftime("%y%m"):
            continue
        if ax and len(ab) >= 200:
            out.append({"arxiv": ax, "title": re.sub(r"\s+", " ", w.get("title") or "").strip(), "abstract": ab[:1500]})
    return out


def collected_new(pattern: str, since: date) -> list[dict]:
    """매일 수집분 중 published 가 since 이후이고 제목 · 초록이 주제 패턴에 맞는 것."""
    out, rx = [], re.compile(pattern, re.I)
    p = Path("raw_data_queue/crawled_papers.jsonl")
    if not p.exists():
        return out
    for line in p.open(encoding="utf-8", errors="replace"):
        try:
            r = json.loads(line)
        except Exception:
            continue
        if (r.get("published") or "")[:10] < since.isoformat():
            continue
        text = f"{r.get('title', '')} {r.get('abstract', '')}"
        if rx.search(text):
            out.append({"arxiv": re.sub(r"v\d+$", "", r.get("paper_id", "")), "title": r.get("title", ""),
                        "abstract": (r.get("abstract") or "")[:1500]})
    return out


def summarize(question: str, c: dict, llm) -> str | None:
    """항목 다시 쓰기와 같은 프롬프트 · 검사(초록 밖 숫자 · 길이 · 한자) — 통과 못 하면 None."""
    from langchain_core.messages import HumanMessage, SystemMessage

    from core.llm.format_fix import term_rule
    from core.llm.item_rewrite import PROMPT, SYSTEM, check_item

    src = f"[{c['arxiv']}] {c['title']}\n[초록] {c['abstract']}"
    try:
        text = str(llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=PROMPT.format(
            question=question, block=src, item="(아직 없음)", term_rule=term_rule()))]).content or "").strip()
    except Exception as exc:
        print(f"[digest] 요약 실패: {type(exc).__name__}")
        return None
    text = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", text)).strip()
    return None if check_item(text, "", src) else text


def build(today: date) -> tuple[str, list[dict]]:
    from langchain_ollama import ChatOllama

    from core.config.agent_config import RAG_ANSWER_MODEL, ollama_kwargs
    from core.llm.doc_judge import judge_docs

    since = today - timedelta(days=7)
    llm = ChatOllama(**ollama_kwargs(model=RAG_ANSWER_MODEL, temperature=0.0, seed=0, reasoning=False, num_predict=400))
    lines = [f"📬 주간 논문 다이제스트 ({since.isoformat()} ~ {today.isoformat()})", ""]
    log = []
    for name, query, question, pattern in TOPICS:
        seen, cands = set(), []
        for c in openalex_new(query, since) + collected_new(pattern, since):
            if c["arxiv"] and c["arxiv"] not in seen:
                seen.add(c["arxiv"])
                cands.append(c)
        cands = cands[:12]  # 27B 한 번에 판정할 만큼
        ctx = "\n\n".join(f"[문서 {i}]\n[{c['arxiv']}] {c['title']}\n[초록] {c['abstract']}" for i, c in enumerate(cands, 1))
        labels = judge_docs(question, ctx) if cands else {}
        # 첫 미리 보기(11-26): 부분(P) 5편 중 4편이 주제 밖이었다 → 요약은 직접(D)만, 부분은 제목만 2편까지
        keep = [cands[n - 1] for n in sorted(labels or {}) if labels[n] == "D"][:MAX_PER_TOPIC]
        near = [cands[n - 1] for n in sorted(labels or {}) if labels[n] == "P"][:2]
        lines.append(f"■ {name}")
        if not keep:
            lines.append("  이번 주 직접 해당 없음")
        for c in keep:
            s = summarize(question, c, llm)
            lines.append(f"• {c['title']} [{c['arxiv']}]")
            lines.append(f"  {s}" if s else "  (요약 검사 통과 못 함 — 제목만)")
        if near:
            lines.append("  가까운 것(요약 없음): " + " · ".join(f"{c['title']} [{c['arxiv']}]" for c in near))
        lines.append("")
        log.append({"topic": name, "candidates": len(cands), "labels": {str(k): v for k, v in (labels or {}).items()},
                    "kept": [c["arxiv"] for c in keep], "near": [c["arxiv"] for c in near]})
        time.sleep(1)
    lines.append("주제가 맞지 않거나 빠진 논문이 있으면 답장으로 알려 주세요.")
    return "\n".join(lines), log


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="사용자 DM 으로 보낸다 (ALLOWED_CHAT_ID 첫 번째)")
    args = ap.parse_args()
    today = date.today()
    text, log = build(today)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{today.isoformat()}.md").write_text(text, encoding="utf-8")
    (OUT_DIR / f"{today.isoformat()}.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    print(text)
    if args.send:
        import telebot

        from apps.telegram_bot.agent_telegram import linkify_arxiv_html, no_link_preview
        from core.config.agent_config import ALLOWED_CHAT_ID, TELEGRAM_TOKEN

        chat = ALLOWED_CHAT_ID.split(",")[0].strip()  # 처음 4주는 사용자 DM 만 (팀 채널 게시는 별도 승인)
        import html as _h

        body = linkify_arxiv_html(_h.escape(text))
        bot = telebot.TeleBot(TELEGRAM_TOKEN)
        for i in range(0, len(body), 3800):
            bot.send_message(chat, body[i:i + 3800], parse_mode="HTML", **no_link_preview())
        print(f"[digest] DM 보냄 ({len(body)}자)")


if __name__ == "__main__":
    main()
