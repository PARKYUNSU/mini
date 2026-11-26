"""주간 신규 논문 다이제스트 (6차 피드백 작업 4 · 7차 승인, 설계 .cron/work_1126/design_feedback_digest.md).

주제마다: 지난 7일 OpenAlex 신규 논문 + 매일 수집분(published 7일 이내) → 27B 문서 판정(운영 judge_docs)에서
직접만 요약 · 부분은 제목 2편 → 주제당 최대 5편 → 초록 기반 1~2문장 요약(숫자는 초록에 있는 것만) → 텔레그램 DM.

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
from itertools import zip_longest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv  # noqa: E402

load_dotenv()

# (이름, OpenAlex 검색어들, 27B 판정 질문, 매일 수집분 거르기 정규식)
# 11-26 첫 발송 피드백: ESG 0편(저널 논문 제외 탓) → 검색어 넓힘 · 기업 공시 분석 포함, RAG 평가는 응용 시스템이 D 로 올라와 평가 연구로 좁힘
TOPICS = [
    # 7차 회신: 주제를 기업 공시 전반으로 넓힘 — AI · 사이버 위험 공시도 포함(2611.25841)
    ("기업 공시 NLP (ESG · 지속가능성 중심)",
     # 맨 단어 검색어("greenwashing" 등)는 NLP 아닌 재무 논문으로 상한을 채워 텍스트 분석 검색어를 붙인다
     ["ESG sustainability disclosure natural language processing", "corporate risk disclosure text analysis",
      "climate disclosure text analysis", "sustainability report language model", "greenwashing detection NLP",
      "ESG rating carbon accounting language model", "AI risk cybersecurity disclosure 10-K text analysis"],
     "기업 공시 문서(ESG · 지속가능성 · 기후 공시, 기업 위험 공시 — AI · 사이버 위험 공시 포함 — , ESG 평가 · 그린워싱 · 탄소 회계)를"
     " 텍스트 분석 · NLP · LLM 으로 분석 · 추출 · 분류 · 평가하는 연구",
     r"\b(?:ESG|sustainab\w*|climate|TCFD|GRI|ISSB|disclosure|10-K|greenwash\w*|carbon accounting)"),
    ("RAG 평가 · 근거 충실도", ["retrieval-augmented generation evaluation faithfulness", "RAG evaluation benchmark metric"],
     "RAG 시스템이나 LLM 답변의 근거 충실도 · 인용 정확도 · 검색 품질을 평가하는 방법 · 지표 · 벤치마크를 제안하거나 비교하는 연구"
     " (근거 기반 응용 시스템을 만들고 자기 성능만 보고한 논문은 해당하지 않는다)",
     r"\b(?:RAG|retrieval-augmented|faithful\w*|grounded\w*|citation)"),
    ("문서 · 표 추출", ["document parsing table extraction PDF"],
     "PDF 등 문서에서 표 · 구조 · 숫자를 추출하거나 파싱하는 방법이나 그 평가를 다루는 연구"
     " (추출 · 파싱을 한 단계로 쓰기만 하는 응용 시스템은 해당하지 않는다)", r"\b(?:table|tabular|document parsing|PDF|layout)"),
    ("LLM 판정자 · 평가", ["LLM as a judge evaluation agreement"],
     "LLM 을 판정자로 쓸 때 사람 판단과의 일치 · 신뢰성을 다루는 연구", r"\b(?:LLM-as-a-judge|LLM judge|judges?|evaluator)"),
]
MAX_PER_TOPIC = 4  # 7차 회신: 섹션당 최대 4편
MAX_CANDS = 36  # 27B 에 12편씩 3번까지
OUT_DIR = Path(".cron/digest")
# 7차 회신: 저품질 출처 — IGI 책 챕터 · IRJMETS · IJARSCT (DOI 접두어)
EXCLUDE_DOI = ("10.4018/", "10.56726/", "10.48175/")


def openalex_new(query: str, since: date, today: date) -> list[dict]:
    """지난 7일 공개된 OpenAlex 논문 (초록 있는 것). arXiv 는 번호 연월로, 저널 논문은 publication_date 로 기간을 본다."""
    import requests

    from core.rag.external_search import OPENALEX_URL, _abstract, _arxiv_id

    key = os.getenv("OPENALEX_API_KEY", "").strip()
    try:
        r = requests.get(OPENALEX_URL, params={
            "search": query, "per-page": 25,
            "filter": f"from_publication_date:{since.isoformat()},to_publication_date:{today.isoformat()}",
            "select": "id,title,ids,doi,publication_date,locations,abstract_inverted_index"},
            headers={"Authorization": f"Bearer {key}"} if key else None, timeout=30)
        r.raise_for_status()
        works = r.json().get("results") or []
    except Exception as exc:  # 외부 장애면 그 검색어는 건너뜀
        print(f"[digest] OpenAlex 실패: {type(exc).__name__}: {str(exc)[:120]}")
        return []
    out = []
    for w in works:
        ax, ab = _arxiv_id(w), _abstract(w)
        if len(ab) < 200:
            continue
        if ax:
            # OpenAlex 공개일은 옛 arXiv 논문도 새로 잡는다(2506.10016) — arXiv 번호의 연월이 한 달 안인 것만
            if ax[:4] < (since - timedelta(days=31)).strftime("%y%m"):
                continue
            pid, url = ax, ""
        else:
            # arXiv 가 아닌 저널 논문(ESG 는 재무 · 회계 저널이 많다) — publication_date 로 기간 확인
            if not (since.isoformat() <= (w.get("publication_date") or "") <= today.isoformat()):
                continue
            doi = re.sub(r"^https?://doi\.org/", "", str(w.get("doi") or ""))
            if doi.lower().startswith(EXCLUDE_DOI):
                continue
            pid = doi or str(w.get("id") or "").rsplit("/", 1)[-1]
            url = f"https://doi.org/{doi}" if doi else str(w.get("id") or "")
        out.append({"arxiv": pid, "url": url, "title": re.sub(r"\s+", " ", w.get("title") or "").strip(), "abstract": ab[:1500]})
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
            out.append({"arxiv": re.sub(r"v\d+$", "", r.get("paper_id", "")), "url": "", "title": r.get("title", ""),
                        "abstract": (r.get("abstract") or "")[:1500]})
    return out


# 미리 보기 1126c: 프롬프트의 "논문 이름 … 없이" 때문에 결과 문장 주어("ESGPT가")가 빠져 뜻이 반대로 읽혔다
SUBJECT_RULE = ("- 단, 결과를 말하는 문장 · 절마다 주어(제안한 모델 · 방법 이름)를 쓴다. 특히 '…지만' 으로 다른 대상과 대조한 뒤에는"
                " 뒤 절의 주어를 반드시 다시 쓴다(예: '일반 모델은 A 지만, 제안 모델 X 는 B'). 이름을 빼라는 말은 맨 앞 머리말에만 해당한다.\n")


def summarize(question: str, c: dict, llm) -> tuple[str | None, str]:
    """항목 다시 쓰기와 같은 프롬프트 · 검사(초록 밖 숫자 · 길이 · 한자) → (요약 1~2문장, 실패 사유). 통과 못 하면 None."""
    from langchain_core.messages import HumanMessage, SystemMessage

    from core.llm.format_fix import fix_terms, term_rule
    from core.llm.item_rewrite import PROMPT, SYSTEM, check_item

    src = f"[{c['arxiv']}] {c['title']}\n[초록] {c['abstract']}"
    try:
        text = str(llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=PROMPT.format(
            question=question, block=src, item="(아직 없음)", term_rule=term_rule() + SUBJECT_RULE))]).content or "").strip()
    except Exception as exc:
        return None, f"호출 실패 {type(exc).__name__}"
    text = fix_terms(re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", text)).strip())[0]
    why = check_item(text, "", src)
    if why == "문서 밖 숫자":
        # '8-billion' → '80억' 처럼 바르게 옮긴 숫자도 걸린다(10.68212/2958-6631.1078) — 걸린 문장만 빼고 남은 게 충분하면 쓴다
        from core.llm.item_rewrite import _bad

        rest = " ".join(x for x in re.split(r"(?<=[.!?])\s+", text) if not _bad(x, src))
        if len(rest) >= 80:
            text, why = rest, ""
        else:
            why = "문서 밖 숫자(남은 문장 짧음)"
    if why:
        return None, why
    return " ".join(re.split(r"(?<=[.!?])\s+", text)[:2]), ""  # 7차 회신: 1~2문장


def _judge(question: str, cands: list[dict]) -> dict[int, str]:
    """12편씩 27B 판정 → 전체 번호(1부터) 기준 D/P/N."""
    from core.llm.doc_judge import judge_docs

    out = {}
    for s in range(0, len(cands), 12):
        part = cands[s:s + 12]
        ctx = "\n\n".join(f"[문서 {i}]\n[{c['arxiv']}] {c['title']}\n[초록] {c['abstract']}" for i, c in enumerate(part, 1))
        for n, lab in (judge_docs(question, ctx) or {}).items():
            out[s + n] = lab
    return out


def _ref(c: dict) -> str:
    return f"[{c['arxiv']}]" + (f" {c['url']}" if c.get("url") else "")


def build(today: date) -> tuple[list[str], list[dict]]:
    """섹션별 텍스트(처음 것에 머리말) · 기록. 섹션 i 의 항목 버튼은 log[i]['kept'] 순서."""
    from langchain_ollama import ChatOllama

    from core.config.agent_config import ollama_kwargs

    since = today - timedelta(days=7)
    # 미리 보기 1126c: 9B(v13)는 주어 규칙을 넣어도 대조 절 주어를 뺐다 → 판정과 같은 27B 로 요약(모델 교체도 없음, 요약당 ~10s)
    model = os.getenv("RAG_DOC_JUDGE_MODEL", "qwen3.6:27b-q4_K_M")
    llm = ChatOllama(**ollama_kwargs(model=model, temperature=0.0, seed=0, reasoning=False, num_predict=400))
    sections, log = [], []
    for name, queries, question, pattern in TOPICS:
        seen, cands = set(), []
        # 11-26 미리 보기: OpenAlex 가 상한을 먼저 채워 매일 수집분(arXiv)이 잘렸다 → 수집분 먼저, 검색어는 번갈아
        oa = zip_longest(*[openalex_new(q, since, today) for q in queries])
        for c in collected_new(pattern, since) + [x for row in oa for x in row if x]:
            if c["arxiv"] and c["arxiv"] not in seen:
                seen.add(c["arxiv"])
                cands.append(c)
        cands = cands[:MAX_CANDS]
        labels = _judge(question, cands) if cands else {}
        # 첫 미리 보기(11-26): 부분(P) 5편 중 4편이 주제 밖이었다 → 요약은 직접(D)만
        keep = [cands[n - 1] for n in sorted(labels) if labels[n] == "D"][:MAX_PER_TOPIC]
        # 7차 회신: '가까운 것'은 정밀도가 낮아(P 판정도 주제 밖 다수) 싣지 않고 기록에만 남긴다
        near = [cands[n - 1] for n in sorted(labels) if labels[n] == "P"][:2]
        fails = {}
        if not keep:
            lines = [f"■ {name} — 이번 주 없음"]
        else:
            lines = [f"■ {name}"]
            for i, c in enumerate(keep, 1):
                s, why = summarize(question, c, llm)
                lines.append(f"{i}. {c['title']} {_ref(c)}")
                if s:  # 요약 검사를 통과 못 하면 제목만 (사유는 기록에만)
                    lines.append(f"  {s}")
                else:
                    fails[c["arxiv"]] = why
        sections.append("\n".join(lines))
        log.append({"topic": name, "candidates": len(cands), "labels": {str(k): v for k, v in labels.items()},
                    "cand_ids": [c["arxiv"] for c in cands],
                    "kept": [{"id": c["arxiv"], "title": c["title"]} for c in keep], "near": [c["arxiv"] for c in near],
                    "summary_fail": fails})
        time.sleep(1)
    sections[0] = f"📬 주간 논문 다이제스트 ({since.isoformat()} ~ {today.isoformat()})\n\n" + sections[0]
    sections[-1] += "\n\n항목마다 👍/👎 를 눌러 주세요. 빠진 논문은 답장으로 알려 주세요."
    return sections, log


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="사용자 DM 으로 보낸다 (ALLOWED_CHAT_ID 첫 번째)")
    args = ap.parse_args()
    today = date.today()
    sections, log = build(today)
    text = "\n\n".join(sections)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{today.isoformat()}.md").write_text(text, encoding="utf-8")
    (OUT_DIR / f"{today.isoformat()}.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    print(text)
    if args.send:
        import html as _h

        import telebot

        from apps.telegram_bot.agent_telegram import linkify_arxiv_html, no_link_preview
        from apps.telegram_bot.answer_feedback import digest_markup
        from core.config.agent_config import ALLOWED_CHAT_ID, TELEGRAM_TOKEN

        chat = ALLOWED_CHAT_ID.split(",")[0].strip()  # 처음 4주는 사용자 DM 만 (팀 채널 게시는 별도 승인)
        bot = telebot.TeleBot(TELEGRAM_TOKEN)
        day = today.strftime("%Y%m%d")
        # 섹션마다 한 메시지 — 항목별 👍/👎 버튼을 그 섹션 메시지에 단다 (4주 뒤 주제별 정밀도)
        for t, sec in enumerate(sections):
            body = linkify_arxiv_html(_h.escape(sec))[:4000]
            n = len(log[t]["kept"])
            bot.send_message(chat, body, parse_mode="HTML", reply_markup=digest_markup(day, t, n) if n else None,
                             **no_link_preview())
        print(f"[digest] DM 보냄 (섹션 {len(sections)}개)")


if __name__ == "__main__":
    main()
