#!/usr/bin/env python3
"""
LLM 토론 기반 파인튜닝 데이터 생성 스케줄러
- 월~금 02:00에 최대 2시간 배치 실행 (run_scheduler.py와 동일 요일)
- Qwen(초안) → Gemini(비평) → Qwen(최종) 파이프라인
"""

import os

os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

import argparse
import ast
import concurrent.futures
import hashlib
import json
import re
import shutil
import sys
import time
import threading
from datetime import datetime
from pathlib import Path

import schedule
import telebot
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

from core.config.agent_config import GEMINI_MODEL, get_gemini_api_keys
from core.llm.agent_gemini import gemini_sdk_generate_json
from core.llm.agent_llm import get_llm_debate_scheduler_llm
from core.execution.retry_utils import retry_on_network_error
from pipelines.debate.llm_debate_spawn_guard import update_debate_heartbeat

# ============ 설정 ============
RAW_DATA_QUEUE = Path("./raw_data_queue")
PROCESSED_DATA_DIR = Path("./raw_data_queue/processed")
FINETUNE_OUTPUT = Path("./finetune_datasets/train_data.jsonl")
FINETUNE_OUTPUT_V2 = Path("./finetune_datasets/train_data_v2.jsonl")
DEBATE_INDEX_PATH = Path("./finetune_datasets/debated_paper_ids.jsonl")
# Phase 2: 시즌2 토론 주제(순회). 세부 논제는 Gemini가 JSON으로 생성.
DEBATE_SEASON2_THEMES: tuple[str, ...] = (
    "Agentic RAG",
    "Graph RAG",
    "Long Context",
    "Hallucination",
    "Multimodal",
    "Retrieval Optimization",
)
SEASON2_THEME_CURSOR_PATH = Path("./finetune_datasets/.season2_theme_cursor.json")
# 시즌2 중복 방지: 동일 주제·질문 지문 또는 동일 근거 논문 집합
SEASON2_DEDUPE_INDEX_PATH = Path("./finetune_datasets/train_data_v2_season2_dedupe.jsonl")
_season2_seen_triple_fp: set[str] = set()
_season2_seen_evidence_fp: set[str] = set()
_season2_dedupe_loaded: bool = False
_season2_dedupe_lock = threading.RLock()
SEASON2_CURSOR_LOCK = threading.Lock()
# 시즌2: 하이브리드로 가져온 컨텍스트 상한(프롬프트·RAM)
DEBATE_SEASON2_RAG_CONTEXT_MAX_CHARS = 45000
# 스케줄/수동 실행 기본 시간 상한(초). 0 이하 = 무제한. (run_scheduler는 .env LLM_DEBATE_BATCH_DURATION_SEC로 덮어씀)
EVENT_DURATION_SEC = 0
LLM_DELAY_SEC = 10
# Qwen/Gemini에 넣는 논문 본문 상한(문자 수). 초과 시 앞부분만 사용 → 컨텍스트·RAM 부담 감소
DEBATE_PAPER_BODY_MAX_CHARS = 15000
DEBATE_BODY_TRUNCATION_NOTICE = (
    "\n\n(논문이 길어 중략되었습니다. 위 내용을 바탕으로 핵심을 도출하세요.)"
)
# 시즌2·최종 답변: 마크다운 구조 강제 (프롬프트·system 공통)
DEBATE_MARKDOWN_OUTPUT_RULE_KO = (
    "답변을 작성할 때는 반드시 마크다운(Markdown) 포맷을 사용하여 가독성을 극대화할 것. "
    "서론, 본론(1., 2., 3. 등 글머리 기호 및 핵심 키워드 볼드체 사용), 결론의 구조를 명확히 나누어 작성하라."
)
# 생각 유출(CoT) 블록 제거
_REDACTED_THINKING_BLOCK_RE = re.compile(
    r"<redacted_thinking\b[^>]*>.*?</redacted_thinking\s*>",
    re.DOTALL | re.IGNORECASE,
)
_REDACTED_THINKING_OPEN_ONLY_RE = re.compile(
    r"<redacted_thinking\b[^>]*>.*",
    re.DOTALL | re.IGNORECASE,
)
# 영어 혼잣말 한 줄(근거 본문과 혼동되지 않게 한글 없는 짧은 메타 라인만)
_ENGLISH_META_ASIDE_LINE_RE = re.compile(
    r"(?im)^\s*(?:wait|let me|i need to|i should|hmm|okay|oh)\b[,.\s!].{0,800}\s*$"
)
# run_scheduler.py 의 LLM 토론 트리거 요일과 맞출 것
DEBATE_SCHEDULE_WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday")


def _configure_utf8_stdio() -> None:
    """cron/launch 환경에서도 한글 로그가 깨지지 않도록 UTF-8 고정.
    nohup >> log 시 블록 버퍼로 tail -f 가 멈춘 것처럼 보이지 않게 줄 단위 플러시."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(
                    encoding="utf-8",
                    errors="replace",
                    line_buffering=True,
                )
            except Exception:
                try:
                    stream.reconfigure(encoding="utf-8", errors="replace")
                except Exception:
                    pass


def _get_telegram_targets() -> tuple[str, list[str]]:
    token = os.getenv("TELEGRAM_TOKEN") or ""
    chat_ids = [cid.strip() for cid in (os.getenv("ALLOWED_CHAT_ID") or "").split(",") if cid.strip()]
    return token, chat_ids


@retry_on_network_error
def _do_send_telegram(token: str, chat_ids: list[str], message: str) -> None:
    """네트워크 재시도 적용 텔레그램 전송"""
    bot = telebot.TeleBot(token)
    for cid in chat_ids:
        bot.send_message(cid, message)
    print(f"✅ 텔레그램 알림 전송 성공: {len(chat_ids)}명")


def _send_telegram_notification(message: str) -> bool:
    token, chat_ids = _get_telegram_targets()
    if not token or not chat_ids:
        print(
            "ℹ️ 텔레그램 알림 스킵: "
            f"token={'Y' if bool(token) else 'N'}, "
            f"chat_ids={len(chat_ids)}"
        )
        return False

    try:
        _do_send_telegram(token, chat_ids, message)
        return True
    except Exception as e:
        print(f"⚠️ 텔레그램 알림 전송 실패: {e}")
        return False


def get_unprocessed_raw_data(target_file: str | None = None) -> tuple[Path, list[dict]] | None:
    """
    raw_data_queue/에서 미처리 JSONL 파일 하나를 읽어 반환.
    반환: (파일경로, [레코드 리스트]) 또는 None
    """
    RAW_DATA_QUEUE.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if target_file:
        target = Path(target_file)
        if not target.is_absolute():
            target = RAW_DATA_QUEUE / target
        if not target.exists():
            print(f"  ❌ 지정한 파일이 없습니다: {target}")
            return None
        jsonl_files = [target]
    else:
        jsonl_files = list(RAW_DATA_QUEUE.glob("*.jsonl"))
        jsonl_files = [f for f in jsonl_files if not f.name.startswith(".")]

    if not jsonl_files:
        return None

    target = jsonl_files[0]
    records = []
    try:
        with open(target, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
    except Exception as e:
        print(f"  ❌ 파일 읽기 오류 ({target}): {e}")
        return None

    if not records:
        target.rename(PROCESSED_DATA_DIR / f"{target.stem}_empty{target.suffix}")
        return None

    return (target, records)


def mark_file_processed(file_path: Path) -> None:
    """처리 완료된 파일을 processed/로 이동"""
    try:
        dest = PROCESSED_DATA_DIR / file_path.name
        if dest.exists():
            dest = PROCESSED_DATA_DIR / f"{file_path.stem}_{int(time.time())}{file_path.suffix}"
        shutil.move(str(file_path), str(dest))
        print(f"  📁 처리 완료: {file_path.name} → processed/")
    except Exception as e:
        print(f"  ⚠️ 파일 이동 실패: {e}")
        file_path.rename(file_path.with_suffix(".processed.jsonl"))


def _load_debated_paper_ids() -> set[str]:
    """이미 토론 완료된 paper_id 집합을 로드. 인덱스가 없으면 processed 폴더 기준으로 1회 부트스트랩."""
    ids: set[str] = set()

    if DEBATE_INDEX_PATH.exists():
        try:
            with open(DEBATE_INDEX_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        item = json.loads(line)
                        paper_id = str(item.get("paper_id", "")).strip()
                        if paper_id:
                            ids.add(paper_id)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"  ⚠️ 토론 인덱스 로드 실패: {e}")
        return ids

    # 인덱스가 아직 없으면 과거 processed JSONL에서 1회 수집해 중복 토론을 최대한 방지
    try:
        PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        for path in PROCESSED_DATA_DIR.glob("*.jsonl"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            item = json.loads(line)
                            raw_id = str(item.get("paper_id", "")).strip()
                            paper_id = raw_id.split("v", 1)[0] if raw_id else raw_id
                            if paper_id:
                                ids.add(paper_id)
                        except json.JSONDecodeError:
                            continue
            except Exception:
                continue
        if ids:
            DEBATE_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(DEBATE_INDEX_PATH, "a", encoding="utf-8") as f:
                for paper_id in sorted(ids):
                    f.write(json.dumps({"paper_id": paper_id, "source": "bootstrap"}, ensure_ascii=False) + "\n")
            print(f"  ♻️ 과거 토론 이력 부트스트랩 완료: {len(ids)}건")
    except Exception as e:
        print(f"  ⚠️ 토론 인덱스 부트스트랩 실패: {e}")

    return ids


def _mark_paper_debated(paper_id: str, title: str = "") -> None:
    """토론 완료된 paper_id를 인덱스에 append 저장."""
    if not paper_id:
        return
    # 버전 접미사 제거: 2401.12345v2 -> 2401.12345 기준으로 dedupe
    base_id = paper_id.split("v", 1)[0].strip()
    if not base_id:
        base_id = paper_id
    try:
        DEBATE_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DEBATE_INDEX_PATH, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "paper_id": base_id,
                        "title": title,
                        "debated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    },
                    ensure_ascii=False,
                ) + "\n"
            )
    except Exception as e:
        print(f"  ⚠️ 토론 인덱스 저장 실패: {e}")


def save_to_finetune_jsonl(record: dict) -> bool:
    """고품질 Q&A를 train_data.jsonl에 append 저장"""
    try:
        rec = dict(record)
        for k in ("instruction", "output"):
            if k in rec and isinstance(rec[k], str):
                rec[k] = _sanitize_qa_field_for_storage(rec[k])
        FINETUNE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(rec, ensure_ascii=False) + "\n"
        with open(FINETUNE_OUTPUT, "a", encoding="utf-8") as f:
            f.write(line)
        return True
    except Exception as e:
        print(f"  ❌ 저장 실패: {e}")
        return False


def save_to_finetune_v2_jsonl(record: dict) -> bool:
    """시즌2 Q&A를 train_data_v2.jsonl에 append (기존 파일 유지)."""
    try:
        rec = dict(record)
        for k in ("instruction", "output"):
            if k in rec and isinstance(rec[k], str):
                rec[k] = _sanitize_qa_field_for_storage(rec[k])
        FINETUNE_OUTPUT_V2.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(rec, ensure_ascii=False) + "\n"
        with open(FINETUNE_OUTPUT_V2, "a", encoding="utf-8") as f:
            f.write(line)
        return True
    except Exception as e:
        print(f"  ❌ train_data_v2 저장 실패: {e}")
        return False


def _season2_next_theme_index() -> tuple[int, str]:
    """다음 순회 인덱스와 주제 라벨. 커서 파일로 순환. 병렬 시 한 번에 한 스레드만 갱신."""
    n = len(DEBATE_SEASON2_THEMES)
    with SEASON2_CURSOR_LOCK:
        idx = 0
        if SEASON2_THEME_CURSOR_PATH.exists():
            try:
                raw = json.loads(SEASON2_THEME_CURSOR_PATH.read_text(encoding="utf-8"))
                idx = int(raw.get("next", 0)) % n
            except Exception:
                idx = 0
        theme = DEBATE_SEASON2_THEMES[idx]
        next_idx = (idx + 1) % n
        try:
            SEASON2_THEME_CURSOR_PATH.parent.mkdir(parents=True, exist_ok=True)
            SEASON2_THEME_CURSOR_PATH.write_text(
                json.dumps({"next": next_idx}, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as e:
            print(f"  ⚠️ 시즌2 커서 저장 실패(무시): {e}")
        return idx, theme


def _season2_norm_fp(s: str) -> str:
    return " ".join((s or "").split())


def _season2_triple_fingerprint(theme: str, sub: str, debate_question: str) -> str:
    raw = (
        f"{_season2_norm_fp(theme)}\x1f{_season2_norm_fp(sub)}\x1f{_season2_norm_fp(debate_question)}"
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _extract_paper_ids_from_debate_context(ctx: str) -> list[str]:
    """하이브리드 블록의 paper_id=… 및 JSONL 폴백의 [NNNN.NNNNN] 패턴에서 ID 수집."""
    text = ctx or ""
    from_pid = re.findall(r"paper_id=([^\s\n]+)", text)
    arxiv_bracket = re.findall(r"\[(\d{4}\.\d{5}(?:v\d+)?)\]", text)
    seen: set[str] = set()
    out: list[str] = []
    for p in from_pid + arxiv_bracket:
        p = (p or "").strip()
        if not p or p == "__anon__":
            continue
        base = p.split("v", 1)[0] if re.match(r"^\d{4}\.\d{5}", p) else p
        if base not in seen:
            seen.add(base)
            out.append(base)
    return sorted(out)


def _season2_evidence_fingerprint(theme: str, sub: str, debate_question: str, paper_ids: list[str]) -> str:
    triple = _season2_triple_fingerprint(theme, sub, debate_question)
    tail = ",".join(paper_ids)
    raw = f"{triple}\x1f{tail}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _season2_load_dedupe_sets_once() -> None:
    """train_data_v2.jsonl + dedupe 인덱스에서 중복 키를 메모리에 적재(최초 1회)."""
    global _season2_seen_triple_fp, _season2_seen_evidence_fp, _season2_dedupe_loaded
    with _season2_dedupe_lock:
        if _season2_dedupe_loaded:
            return
        triples: set[str] = set()
        evidence: set[str] = set()
        if FINETUNE_OUTPUT_V2.exists():
            try:
                with open(FINETUNE_OUTPUT_V2, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if rec.get("source") != "season2_hybrid_rag":
                            continue
                        t = str(rec.get("debate_theme", "") or "")
                        st = str(rec.get("debate_sub_theme", "") or "")
                        dq = str(rec.get("debate_question", "") or "")
                        if not dq:
                            continue
                        triples.add(_season2_triple_fingerprint(t, st, dq))
                        ep = rec.get("evidence_paper_ids")
                        if isinstance(ep, list) and ep:
                            pids = sorted(
                                str(x).split("v", 1)[0]
                                for x in ep
                                if x is not None and str(x).strip()
                            )
                            evidence.add(
                                _season2_evidence_fingerprint(t, st, dq, pids)
                            )
            except OSError as e:
                print(f"  ⚠️ 시즌2 중복 부트스트랩(train_data_v2 읽기) 실패: {e}")
        if SEASON2_DEDUPE_INDEX_PATH.exists():
            try:
                with open(SEASON2_DEDUPE_INDEX_PATH, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            row = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        tfp = row.get("triple_sha256")
                        efp = row.get("evidence_sha256")
                        if isinstance(tfp, str) and tfp:
                            triples.add(tfp)
                        if isinstance(efp, str) and efp:
                            evidence.add(efp)
            except OSError as e:
                print(f"  ⚠️ 시즌2 dedupe 인덱스 읽기 실패: {e}")
        _season2_seen_triple_fp = triples
        _season2_seen_evidence_fp = evidence
        _season2_dedupe_loaded = True


def _append_season2_dedupe_index(
    triple_fp: str,
    evidence_fp: str,
    paper_ids: list[str],
    *,
    update_memory_sets: bool = True,
) -> None:
    """dedupe 인덱스 파일 append. ``update_memory_sets=False``는 집합에 이미 반영된 경우(병렬 예약 후)."""
    global _season2_seen_triple_fp, _season2_seen_evidence_fp
    with _season2_dedupe_lock:
        SEASON2_DEDUPE_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        line = (
            json.dumps(
                {
                    "triple_sha256": triple_fp,
                    "evidence_sha256": evidence_fp,
                    "paper_ids": paper_ids,
                    "saved_at": datetime.now().isoformat(),
                },
                ensure_ascii=False,
            )
            + "\n"
        )
        with open(SEASON2_DEDUPE_INDEX_PATH, "a", encoding="utf-8") as f:
            f.write(line)
        if update_memory_sets:
            _season2_seen_triple_fp.add(triple_fp)
            _season2_seen_evidence_fp.add(evidence_fp)


def generate_season2_debate_plan(theme_label: str) -> dict | None:
    """Gemini JSON: 세부 논제·토론 질문·검색 쿼리."""
    prompt = f"""당신은 연구 토론 디렉터다. 아래 **대주제**에 대해, 최신 논문 검색에 쓸 키워드와
깊이 있는 토론(한계점 비판·실무적 완화책)을 유도하는 **단일 질문**을 설계하라.

대주제: "{theme_label}"

출력은 JSON 한 객체만 (설명·마크다운 금지):
{{
  "sub_theme": "한국어로 세부 주제 한 줄",
  "debate_question": "한국어 한 문장. 한계·실패 사례·완화 전략을 묻는 질문",
  "retrieval_query": "영어 키워드 위주 1~2문장. arXiv/학술 검색에 적합하게"
}}
"""
    try:
        text = gemini_sdk_generate_json(get_gemini_api_keys(), GEMINI_MODEL, prompt)
        data = json.loads(text)
        if not isinstance(data, dict):
            return None
        rq = (data.get("retrieval_query") or theme_label).strip()
        dq = (data.get("debate_question") or "").strip()
        st = (data.get("sub_theme") or "").strip()
        if not dq or not rq:
            return None
        return {"sub_theme": st, "debate_question": dq, "retrieval_query": rq}
    except Exception as e:
        print(f"    ❌ 시즌2 주제 계획 생성 실패: {e}")
        return None


def run_season2_debate_pipeline(
    theme_label: str,
    plan: dict,
    rag_context: str,
    *,
    rag_paper_ids: list[str] | None = None,
) -> dict | None:
    """Qwen → Gemini → Qwen. 근거는 하이브리드 RAG Top-5 컨텍스트."""
    sub = plan.get("sub_theme", "")
    dq = plan.get("debate_question", "")
    ctx = (rag_context or "").strip()
    if len(ctx) > DEBATE_SEASON2_RAG_CONTEXT_MAX_CHARS:
        ctx = ctx[:DEBATE_SEASON2_RAG_CONTEXT_MAX_CHARS] + "\n\n(컨텍스트 상한으로 중략)"
    if not ctx.strip():
        print("  ⚠️ RAG 컨텍스트 비어 있음")
        return None

    source_excerpt = ctx[:20000]
    meta_header = f"[대주제] {theme_label}\n[세부] {sub}\n[토론 질문] {dq}\n\n"

    llm_qwen = get_llm_debate_scheduler_llm()
    print("    [S2 1/3] Qwen 초안…")
    try:
        draft_prompt = f"""다음은 하이브리드 검색으로 모은 상위 논문 발췌다. 이 근거만 사용해
한계점·실패 모드·완화 전략을 묻고 답하는 Q&A 1세트를 JSON으로 작성해.

{meta_header}

[근거 논문 발췌]
{ctx}

규칙:
- instruction: 한국어 질문 1문장. 반드시 비판·한계·대안을 유도할 것. 전문 용어(예: Agentic RAG)는 논문·근거와 동일한 철자로 끝까지 쓸 것.
- output: 한국어 답변. {DEBATE_MARKDOWN_OUTPUT_RULE_KO} 근거에 없는 숫자·수치는 쓰지 말 것.
- <redacted_thinking> 등 사고 과정 태그·영어 혼잣말 금지. 오직 JSON 객체만 출력.
- JSON만: {{"instruction":"...","output":"..."}}"""
        draft_resp = llm_qwen.invoke([HumanMessage(content=draft_prompt)])
        draft_qa = draft_resp.content.strip() if draft_resp.content else ""
        time.sleep(LLM_DELAY_SEC)
    except Exception as e:
        print(f"    ❌ Qwen 초안 실패: {e}")
        return None

    print("    [S2 2/3] Gemini 비평…")
    try:
        critique_prompt = f"""Qwen 초안 Q&A와 근거 텍스트를 비교한다.

[초안]
{draft_qa[:8000]}

[근거 일부]
{ctx[:12000]}

초안이 근거를 벗어나거나 피상적이면 지적하고, 한계 분석·해결책이 드러나도록 수정안을 JSON 한 개로만 출력.
답변(output)은 {DEBATE_MARKDOWN_OUTPUT_RULE_KO}
전문 용어 철자는 근거와 일치시킬 것. 사고 태그·영어 메타 코멘트 금지.
{{"instruction":"...","output":"..."}}"""
        critique_text = gemini_sdk_generate_json(
            get_gemini_api_keys(),
            GEMINI_MODEL,
            critique_prompt,
        )
        time.sleep(LLM_DELAY_SEC)
    except Exception as e:
        print(f"    ❌ Gemini 비평 실패: {e}")
        return None

    print("    [S2 3/3] Qwen 최종…")
    try:
        final_prompt = f"""비평 반영해 최종 Q&A JSON만 출력. 머리말·코드블록·<redacted_thinking> 금지.
{{"instruction":"...","output":"..."}}
output은 반드시 마크다운 구조로: {DEBATE_MARKDOWN_OUTPUT_RULE_KO}
instruction·output 문자열은 JSON 이스케이프 규칙을 지키고, 용어 철자를 잘리지 않게 완전한 단어로 쓸 것.

비평:
{critique_text[:4000]}"""
        final_resp = llm_qwen.invoke([HumanMessage(content=final_prompt)])
        final_text = final_resp.content.strip() if final_resp.content else critique_text
        time.sleep(LLM_DELAY_SEC)
    except Exception as e:
        print(f"    ❌ Qwen 최종 실패: {e}")
        final_text = critique_text

    try:
        for block in (final_text, critique_text, draft_qa):
            qa = _extract_qa_from_text(block)
            if qa:
                qa = _normalize_qa_fields(qa)
                if _needs_qa_repair(qa, source_excerpt):
                    print("    [S2 보정] QA 재정리…")
                    repaired = _repair_qa_candidate(
                        llm_qwen, qa, source_excerpt, f"{theme_label} — {sub}"
                    )
                    if repaired and not _needs_qa_repair(repaired, source_excerpt):
                        return _merge_season2_meta(
                            repaired, theme_label, plan, paper_ids=rag_paper_ids
                        )
                    if repaired:
                        qa = repaired
                if not _needs_qa_repair(qa, source_excerpt):
                    return _merge_season2_meta(qa, theme_label, plan, paper_ids=rag_paper_ids)
        print("    ⚠️ 시즌2 Q&A 추출 실패")
        return None
    except Exception as e:
        print(f"    ❌ 시즌2 파싱 오류: {e}")
        return None


def _merge_season2_meta(
    qa: dict,
    theme_label: str,
    plan: dict,
    *,
    paper_ids: list[str] | None = None,
) -> dict:
    out = dict(qa)
    out["system"] = (
        "당신은 최신 AI 논문을 비판적으로 분석하고, 한계와 대안을 제시하는 수석 연구원입니다. "
        + DEBATE_MARKDOWN_OUTPUT_RULE_KO
    )
    for k in ("instruction", "output"):
        if k in out and isinstance(out[k], str):
            out[k] = _sanitize_qa_field_for_storage(out[k])
    out["debate_theme"] = theme_label
    out["debate_sub_theme"] = plan.get("sub_theme", "")
    out["debate_question"] = plan.get("debate_question", "")
    out["source"] = "season2_hybrid_rag"
    if paper_ids is not None:
        out["evidence_paper_ids"] = list(paper_ids)
    return out


def season2_single_round(*, theme_override: str | None = None) -> bool:
    """한 주제 1회: 계획 → 하이브리드 RAG → 토론 → train_data_v2 append."""
    from core.rag.agent_chroma_rag import hybrid_retrieve_context_for_debate

    if theme_override and theme_override.strip():
        theme_label = theme_override.strip()
        print(f"  🎭 시즌2 (주제 고정): {theme_label}")
    else:
        _idx, theme_label = _season2_next_theme_index()
        print(f"  🎭 시즌2 주제 [{_idx+1}/{len(DEBATE_SEASON2_THEMES)}]: {theme_label}")

    plan = generate_season2_debate_plan(theme_label)
    if not plan:
        return False
    print(f"    세부: {plan.get('sub_theme', '')}")
    sub = plan.get("sub_theme", "") or ""
    dq = plan.get("debate_question", "") or ""
    _season2_load_dedupe_sets_once()
    triple_fp = _season2_triple_fingerprint(theme_label, sub, dq)
    with _season2_dedupe_lock:
        if triple_fp in _season2_seen_triple_fp:
            print("    ⏭️ 시즌2 스킵: 동일 대주제·세부·토론 질문으로 이미 저장된 레코드가 있음")
            return False

    rq = plan["retrieval_query"]
    rag = hybrid_retrieve_context_for_debate(
        rq,
        top_k_papers=5,
        light_rerank_input_max_chars=2000,
    )
    paper_ids = _extract_paper_ids_from_debate_context(rag)
    ev_fp = _season2_evidence_fingerprint(theme_label, sub, dq, paper_ids)
    with _season2_dedupe_lock:
        if (
            triple_fp in _season2_seen_triple_fp
            or ev_fp in _season2_seen_evidence_fp
        ):
            print(
                "    ⏭️ 시즌2 스킵: 동일 근거 논문 집합·질문 조합으로 이미 토론 데이터가 있음 "
                f"(paper_ids={paper_ids})"
            )
            return False

    qa = run_season2_debate_pipeline(
        theme_label, plan, rag, rag_paper_ids=paper_ids
    )
    if not qa:
        return False

    with _season2_dedupe_lock:
        if triple_fp in _season2_seen_triple_fp or ev_fp in _season2_seen_evidence_fp:
            print("    ⏭️ 시즌2 스킵: 다른 워커가 동일 지문/근거로 먼저 반영함")
            return False
        _season2_seen_triple_fp.add(triple_fp)
        _season2_seen_evidence_fp.add(ev_fp)
    try:
        if not save_to_finetune_v2_jsonl(qa):
            with _season2_dedupe_lock:
                _season2_seen_triple_fp.discard(triple_fp)
                _season2_seen_evidence_fp.discard(ev_fp)
            return False
        _append_season2_dedupe_index(
            triple_fp, ev_fp, paper_ids, update_memory_sets=False
        )
        print("    ✅ train_data_v2.jsonl 저장")
        return True
    except Exception:
        with _season2_dedupe_lock:
            _season2_seen_triple_fp.discard(triple_fp)
            _season2_seen_evidence_fp.discard(ev_fp)
        raise


def weekly_llm_debate_season2_event(
    *,
    rounds: int = 1,
    theme_override: str | None = None,
    workers: int = 1,
) -> dict:
    """시즌2: 주제 순회·하이브리드 RAG 기반 토론 데이터 생성.

    ``workers``>1 이면 서로 다른 라운드를 스레드 풀로 병렬 실행(주제 고정 시에는 1로 강제).
    """
    _configure_utf8_stdio()
    start = time.time()
    rounds_n = max(1, int(rounds))
    w = max(1, min(int(workers), rounds_n, 8))
    if (theme_override or "").strip():
        if w > 1:
            print("ℹ️ 시즌2: --season2-theme 지정 시에는 병렬 비활성 (워커 1).")
        w = 1
    print("\n" + "=" * 60)
    print(
        f"🎭 시즌2 논문 토론 공장 시작: {datetime.now().isoformat()}  "
        f"(라운드: {rounds_n}, 워커: {w})"
    )
    print("=" * 60)
    ok = 0
    if w <= 1:
        for r in range(rounds_n):
            print(f"\n--- 라운드 {r+1}/{rounds_n} ---")
            if season2_single_round(theme_override=theme_override):
                ok += 1
            time.sleep(LLM_DELAY_SEC)
    else:
        print(f"\n⚡ 병렬 실행: 동시에 최대 {w}개 라운드 (Gemini·Ollama 부하 주의)\n", flush=True)

        def _one_round(batch_idx: int, slot: int) -> bool:
            print(f"  [배치 #{batch_idx} 슬롯 {slot}] 라운드 시작…", flush=True)
            return bool(season2_single_round(theme_override=theme_override))

        batch = 0
        remaining = rounds_n
        while remaining > 0:
            batch += 1
            this_chunk = min(w, remaining)
            with concurrent.futures.ThreadPoolExecutor(max_workers=this_chunk) as pool:
                fts = [
                    pool.submit(_one_round, batch, slot + 1)
                    for slot in range(this_chunk)
                ]
                for fut in concurrent.futures.as_completed(fts):
                    try:
                        if fut.result():
                            ok += 1
                    except Exception as e:
                        print(f"  ❌ 시즌2 워커 예외: {e}", flush=True)
            remaining -= this_chunk
            if remaining > 0:
                time.sleep(LLM_DELAY_SEC)
    elapsed = time.time() - start
    print(f"\n🏁 시즌2 종료 | 성공 {ok}/{rounds_n} | 소요 {elapsed:.1f}s")
    return {"success": ok, "rounds": rounds_n, "workers": w}


def _truncate_paper_body_for_debate(text: str, max_chars: int = DEBATE_PAPER_BODY_MAX_CHARS) -> str:
    """논문 본문을 앞에서부터 max_chars자까지만 사용. 초과 시 안내 문구 부착."""
    s = (text or "").strip()
    if not s:
        return s
    if len(s) <= max_chars:
        return s
    return s[:max_chars] + DEBATE_BODY_TRUNCATION_NOTICE


def _normalize_text(text: str) -> str:
    return (
        (text or "")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("？", "?")
        .replace("؟", "?")
        .strip()
    )


def _strip_redacted_thinking(text: str) -> str:
    """<redacted_thinking>...</redacted_thinking> 및 닫히지 않은 동일 태그 제거."""
    if not text:
        return text
    s = _REDACTED_THINKING_BLOCK_RE.sub("", text)
    s = _REDACTED_THINKING_OPEN_ONLY_RE.sub("", s)
    return s


def _strip_english_meta_aside_lines(text: str) -> str:
    """JSON에 섞인 짧은 영어 메타 혼잣말 라인만 제거(한글이 있는 줄은 유지)."""
    if not text:
        return text
    out: list[str] = []
    for line in text.splitlines():
        raw = line
        ln = line.strip()
        if not ln:
            out.append(raw)
            continue
        if re.search(r"[가-힣]", ln):
            out.append(raw)
            continue
        if len(ln) > 900:
            out.append(raw)
            continue
        if _ENGLISH_META_ASIDE_LINE_RE.match(ln):
            continue
        out.append(raw)
    return "\n".join(out)


def _sanitize_llm_output_before_qa_parse(text: str) -> str:
    """파싱·저장 전: CoT 블록·메타 라인 제거 후 유니코드 정규화."""
    s = _strip_redacted_thinking(text or "")
    s = _strip_english_meta_aside_lines(s)
    return _normalize_text(s)


def _sanitize_qa_field_for_storage(text: str) -> str:
    """레코드 필드 최종 저장 직전 한 번 더 정리."""
    if not isinstance(text, str):
        return text
    return _sanitize_llm_output_before_qa_parse(text).strip()


def _coerce_qa_dict(parsed: dict) -> dict | None:
    if not isinstance(parsed, dict):
        return None

    instruction = ""
    output = ""

    for key in ("instruction", "question", "prompt", "질문"):
        value = parsed.get(key)
        if isinstance(value, str) and value.strip():
            instruction = value.strip()
            break

    for key in ("output", "answer", "response", "답변"):
        value = parsed.get(key)
        if isinstance(value, str) and value.strip():
            output = value.strip()
            break

    if instruction and output:
        instruction = _sanitize_qa_field_for_storage(instruction)
        output = _sanitize_qa_field_for_storage(output)
        if not instruction or not output:
            return None
        return {
            "system": "당신은 최신 AI 논문을 분석하는 수석 연구원입니다.",
            "instruction": instruction,
            "output": output,
        }
    return None


def _strip_leading_label(text: str, labels: tuple[str, ...]) -> str:
    """Q:/A: 형태만 벗긴다. 한 글자 라벨(A, Q)은 콜론이 있어야 하며,
    그렇지 않으면 'Agentic'의 선행 A처럼 본문이 잘리는 오류가 난다."""
    text = (text or "").strip()
    for label in labels:
        if len(label) == 1:
            pattern = rf"^\s*{re.escape(label)}\s*[:：]\s*"
        else:
            pattern = rf"^\s*{re.escape(label)}\s*[:：]?\s*"
        text = re.sub(pattern, "", text, flags=re.IGNORECASE).strip()
    return text


def _normalize_qa_fields(qa: dict) -> dict:
    instruction = _strip_leading_label(qa.get("instruction", ""), ("Q", "Question", "질문"))
    output = _strip_leading_label(qa.get("output", ""), ("A", "Answer", "답변"))
    return {
        "system": "당신은 최신 AI 논문을 분석하는 수석 연구원입니다.",
        "instruction": instruction.strip(),
        "output": output.strip(),
    }


def _looks_like_generic_instruction(text: str) -> bool:
    text = (text or "").strip()
    if not text:
        return True
    generic_markers = ("Q&A를 작성", "Q&A 작성", "요약한 Q&A", "작성해주세요", "작성해 주세요")
    return any(marker in text for marker in generic_markers)


def _has_multi_qa_markers(text: str) -> bool:
    text = (text or "").strip()
    if not text:
        return False
    markers = re.findall(r"(?i)(?:^|[\n\r\s])(?:Q\s*:|A\s*:|Question\s*:|Answer\s*:|질문\s*[:：]|답변\s*[:：])", text)
    return len(markers) >= 2


def _extract_number_tokens(text: str) -> list[str]:
    return re.findall(r"\d+(?:\.\d+)?", text or "")


def _has_unsupported_numbers(text: str, source_text: str) -> bool:
    source_text = source_text or ""
    if not source_text.strip():
        return False
    for token in _extract_number_tokens(text):
        if not re.search(rf"(?<!\d){re.escape(token)}(?!\d)", source_text):
            return True
    return False


def _needs_qa_repair(qa: dict, source_text: str) -> bool:
    instruction = qa.get("instruction", "")
    output = qa.get("output", "")
    if _looks_like_generic_instruction(instruction):
        return True
    if _has_multi_qa_markers(output):
        return True
    if _has_unsupported_numbers(f"{instruction}\n{output}", source_text):
        return True
    return False


def _extract_qa_from_text(text: str) -> dict | None:
    text = _sanitize_llm_output_before_qa_parse(text)
    if not text:
        return None

    candidates: list[str] = [text]

    fenced_blocks = re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    candidates.extend(block.strip() for block in fenced_blocks if block.strip())

    if "{" in text and "}" in text:
        start = text.find("{")
        end = text.rfind("}") + 1
        if end > start:
            candidates.append(text[start:end].strip())

    for candidate in candidates:
        if not candidate:
            continue

        for loader in (json.loads, ast.literal_eval):
            try:
                parsed = loader(candidate)
                qa = _coerce_qa_dict(parsed)
                if qa:
                    return qa
            except Exception:
                pass

        key_patterns = [
            r'"instruction"\s*:\s*"(?P<instruction>.*?)"\s*,\s*"output"\s*:\s*"(?P<output>.*?)"',
            r'"question"\s*:\s*"(?P<instruction>.*?)"\s*,\s*"answer"\s*:\s*"(?P<output>.*?)"',
            r"(?:instruction|question|질문)\s*[:：]\s*(?P<instruction>.+?)(?:\n|\r\n)+(?:output|answer|답변)\s*[:：]\s*(?P<output>.+)",
        ]
        for pattern in key_patterns:
            match = re.search(pattern, candidate, flags=re.DOTALL | re.IGNORECASE)
            if match:
                instruction = match.group("instruction").strip().strip('"').strip()
                output = match.group("output").strip().strip('"').strip()
                instruction = _sanitize_qa_field_for_storage(instruction)
                output = _sanitize_qa_field_for_storage(output)
                if instruction and output:
                    return {
                        "system": "당신은 최신 AI 논문을 분석하는 수석 연구원입니다.",
                        "instruction": instruction,
                        "output": output,
                    }

    return None


def _repair_qa_candidate(llm_qwen: ChatOllama, qa: dict, source_text: str, paper_title: str) -> dict | None:
    """부정확하거나 형식이 흔들린 QA를 단일 질문/답변으로 보수적으로 재정리."""
    prompt = f"""다음은 논문 기반 학습 데이터 초안이다. 아래 규칙에 맞게 단 하나의 질문과 단 하나의 답변으로 다시 정리하라.

[논문 제목]
{paper_title}

[근거 텍스트]
{source_text[:12000]}

[초안 instruction]
{qa.get("instruction", "")}

[초안 output]
{qa.get("output", "")}

[규칙]
1. instruction은 자연스러운 질문 1문장만 작성한다. 전문 용어는 잘리지 않게 완전한 철자로 쓴다.
2. output은 그 질문에 대한 답변 하나만. {DEBATE_MARKDOWN_OUTPUT_RULE_KO}
3. Q:, A:, 질문:, 답변: 형태의 접두만 허용(단, 답변 본문이 A로 시작하는 영어 단어인 경우 임의로 앞글자를 제거하지 말 것).
4. 근거 텍스트에 명시적으로 없는 숫자, 비용, 성능 수치, 무게, 개수, 자유도, 비율은 절대 추가하지 말고 삭제한다.
5. 확실하지 않은 세부 정보는 보수적으로 생략한다.
6. <redacted_thinking>, 영어 혼잣말, 설명 머리말, 코드블록 없이 JSON 객체 1개만 출력한다.

반드시 아래 형식만 출력:
{{"instruction": "질문", "output": "답변"}}"""
    try:
        resp = llm_qwen.invoke([HumanMessage(content=prompt)])
        repaired_text = resp.content.strip() if resp.content else ""
        repaired = _extract_qa_from_text(repaired_text)
        if repaired:
            return _normalize_qa_fields(repaired)
    except Exception as e:
        print(f"    ⚠️ QA 재정리 실패: {e}")
    return None


def run_debate_pipeline(raw_record: dict) -> dict | None:
    """
    Qwen(초안) → Gemini(비평) → Qwen(최종) 토론 파이프라인
    반환: {"system", "instruction", "output"} 또는 None
    """
    content_raw = raw_record.get("content", raw_record.get("body", ""))
    if not (content_raw or "").strip():
        print("  ⚠️ content/body 필드 없음, 건너뜀")
        return None

    paper_content = _truncate_paper_body_for_debate(content_raw)
    raw_pid = str(raw_record.get("paper_id", "unknown")).strip()
    paper_id = raw_pid.split("v", 1)[0] if raw_pid else raw_pid
    paper_title = raw_record.get("title", paper_id or raw_pid or "unknown")
    abstract = raw_record.get("abstract", "")
    source_excerpt = f"[title]\n{paper_title}\n\n[abstract]\n{abstract}\n\n[content]\n{paper_content}"

    # 1. Qwen 초안
    print("    [1/3] Qwen 초안 생성 중...")
    try:
        llm_qwen = get_llm_debate_scheduler_llm()
        draft_prompt = f"""다음 학술 논문 본문을 읽고, 핵심 내용을 묻고 답하는 Q&A 1세트를 작성해.
형식: 질문 1개 + 답변 1개. JSON 형태로 instruction과 output만 출력해.
설명 문장, 머리말, <redacted_thinking>, 코드블록 없이 아래 JSON 객체 1개만 출력:
{{"instruction": "질문", "output": "답변"}}
- 질문은 실제 논문 내용을 묻는 구체적인 질문 1개여야 한다. 전문 용어는 논문과 동일한 철자로 끝까지 쓸 것.
- 답변: {DEBATE_MARKDOWN_OUTPUT_RULE_KO}
- 논문 본문에 명시적으로 없는 숫자, 비용, 성능 수치, 무게, 개수는 절대 추측하지 말고 쓰지 마라.

논문 본문:
{paper_content}
"""
        draft_resp = llm_qwen.invoke([HumanMessage(content=draft_prompt)])
        draft_qa = draft_resp.content.strip() if draft_resp.content else ""
        time.sleep(LLM_DELAY_SEC)
    except Exception as e:
        print(f"    ❌ Qwen 초안 실패: {e}")
        return None

    # 2. Gemini 비평 및 수정 (429 시 다음 키로 폴백 — get_gemini_api_keys 순서)
    print("    [2/3] Gemini 비평/수정 중...")
    try:
        critique_prompt = f"""다음은 Qwen이 만든 Q&A 초안입니다.

[초안 Q&A]
{draft_qa[:6000]}

[원시 논문 일부]
{paper_content}

초안 Q&A의 논리적 오류나 개선점을 비판하고, 더 정확하고 심층적인 Q&A로 수정해 줘.
오직 완성된 JSON 형태만 출력: {{"instruction": "질문", "output": "답변"}}
- 숫자, 비용, 성능 수치, 무게, 개수는 원문에 명시된 경우에만 유지하고, 불명확하면 삭제해.
- output: {DEBATE_MARKDOWN_OUTPUT_RULE_KO}
- 사고 태그·영어 메타 코멘트 금지. output에는 여러 개의 Q&A를 넣지 말고 단일 답변만 남겨.
"""
        critique_text = gemini_sdk_generate_json(
            get_gemini_api_keys(),
            GEMINI_MODEL,
            critique_prompt,
        )
        time.sleep(LLM_DELAY_SEC)
    except Exception as e:
        print(f"    ❌ Gemini 비평 실패: {e}")
        return None

    # 3. Qwen 최종 수정
    print("    [3/3] Qwen 최종 생성 중...")
    try:
        final_prompt = f"""다음 비평을 반영해 최종 Q&A를 완성해.
비평/수정안: {critique_text[:3000]}

반드시 JSON만 출력: {{"instruction": "질문", "output": "답변"}}
추가 설명, 머리말, <redacted_thinking>, 코드블록 금지.
- instruction은 질문 1문장만. 용어 철자 완전성 유지.
- output: {DEBATE_MARKDOWN_OUTPUT_RULE_KO}
- 원문에 없는 숫자/비용/정량 정보는 삭제.
"""
        final_resp = llm_qwen.invoke([HumanMessage(content=final_prompt)])
        final_text = final_resp.content.strip() if final_resp.content else critique_text
        time.sleep(LLM_DELAY_SEC)
    except Exception as e:
        print(f"    ❌ Qwen 최종 실패: {e}")
        final_text = critique_text

    # JSON/평문 파싱
    try:
        for block in (final_text, critique_text, draft_qa):
            qa = _extract_qa_from_text(block)
            if qa:
                qa = _normalize_qa_fields(qa)
                if _needs_qa_repair(qa, source_excerpt):
                    print("    [보정] 형식/근거 검수 후 QA 재정리 중...")
                    repaired = _repair_qa_candidate(llm_qwen, qa, source_excerpt, paper_title)
                    if repaired and not _needs_qa_repair(repaired, source_excerpt):
                        return repaired
                    if repaired:
                        qa = repaired
                if not _needs_qa_repair(qa, source_excerpt):
                    return qa
        print("    ⚠️ 유효한 Q&A(JSON/평문) 추출 실패")
        print(f"    [디버그] final_text 미리보기: {_normalize_text(final_text)[:300]}")
        print(f"    [디버그] critique_text 미리보기: {_normalize_text(critique_text)[:300]}")
        return None
    except Exception as e:
        print(f"    ❌ 파싱 오류: {e}")
        return None


def _debate_time_limit_reached(start: float, duration_sec: int) -> bool:
    """duration_sec <= 0 이면 시간 제한 없음 (큐 소진·데이터 없음·target_file 완료까지)."""
    if duration_sec <= 0:
        return False
    return (time.time() - start) >= duration_sec


def weekly_llm_debate_event(
    *,
    target_file: str | None = None,
    max_records: int | None = None,
    duration_sec: int = EVENT_DURATION_SEC,
    stop_on_empty: bool = False,
) -> dict:
    """스케줄러가 월~금 02:00에 호출. ``duration_sec`` 초 동안 처리; 0 이하이면 시간 제한 없음."""
    _configure_utf8_stdio()
    start = time.time()
    print("\n" + "=" * 60)
    print(f"🚀 LLM 토론 배치 시작: {datetime.now().isoformat()}")
    if duration_sec <= 0:
        print("⏱️ 이번 실행 시간 한도: 없음 (큐가 비거나 Ctrl+C까지, Gemini는 요청마다 키 순환)")
    else:
        print(f"⏱️ 이번 실행 시간 한도: {duration_sec}초 ({duration_sec / 3600:.2f}시간)")
    print("=" * 60)
    sys.stdout.flush()
    sys.stderr.flush()

    # 관측용 heartbeat: 장시간(특히 duration<=0) 실행 중 "최근 업데이트 시각"을 기록한다.
    # heartbeat가 오래 갱신되지 않으면(기본 15분 초과) spawn 가드가 "정상 대기"가 아닌 장애로 판단할 수 있다.
    hb_interval_sec = int(os.getenv("LLM_DEBATE_HEARTBEAT_INTERVAL_SEC", "60"))
    hb_stop = threading.Event()
    hb_thread: threading.Thread | None = None

    if hb_interval_sec > 0:
        pid = os.getpid()

        def _heartbeat_loop() -> None:
            while not hb_stop.wait(hb_interval_sec):
                update_debate_heartbeat(pid=pid, status="running")

        hb_thread = threading.Thread(target=_heartbeat_loop, daemon=True)
        hb_thread.start()
        # 시작 직후 1회 즉시 기록 (파일 생성 지연 방지)
        update_debate_heartbeat(pid=pid, status="running")

    processed_count = 0
    error_count = 0
    skipped_count = 0
    duplicate_skipped_count = 0
    processed_files: list[str] = []
    found_any_data = False
    stop_reason = ""
    print("  📇 이미 토론한 논문 ID 인덱스 로드 중...", flush=True)
    debated_paper_ids = _load_debated_paper_ids()
    print(f"  📇 인덱스 로드 완료 ({len(debated_paper_ids)}건)", flush=True)
    seen_in_this_run: set[str] = set()

    while not _debate_time_limit_reached(start, duration_sec):
        if duration_sec > 0:
            remaining = int(duration_sec - (time.time() - start))
            print(f"\n⏱️ 남은 시간: {remaining}초")
        else:
            elapsed = int(time.time() - start)
            print(f"\n⏱️ 경과: {elapsed}초 (시간 제한 없음)")

        result = get_unprocessed_raw_data(target_file=target_file)
        if result is None:
            if stop_on_empty and found_any_data:
                print("  📭 처리할 원시 데이터 없음. 큐 소진으로 배치를 종료합니다.")
                stop_reason = "queue_depleted"
                break
            print("  📭 처리할 원시 데이터 없음. 대기 중...")
            if target_file:
                break
            time.sleep(60)
            continue

        found_any_data = True
        file_path, records = result
        if max_records is not None:
            records = records[:max_records]
        print(f"  📄 처리 중: {file_path.name} ({len(records)}건)")

        success_in_file = 0
        exited_by_timeout = False
        resume_from_index = 0
        for i, rec in enumerate(records):
            if duration_sec > 0 and (time.time() - start) >= duration_sec:
                print(f"  ⏰ 시간 한도({duration_sec}s) 도달, 배치 종료")
                exited_by_timeout = True
                resume_from_index = i
                break

            paper_id = str(rec.get("paper_id", "")).strip()
            paper_title = str(rec.get("title", "")).strip()
            if paper_id and (paper_id in debated_paper_ids or paper_id in seen_in_this_run):
                skipped_count += 1
                duplicate_skipped_count += 1
                print(f"    ⏭️ [{i+1}/{len(records)}] 이미 토론한 논문이라 건너뜀: {paper_id}")
                continue

            try:
                qa = run_debate_pipeline(rec)
                if qa and save_to_finetune_jsonl(qa):
                    success_in_file += 1
                    processed_count += 1
                    if paper_id:
                        debated_paper_ids.add(paper_id)
                        seen_in_this_run.add(paper_id)
                        _mark_paper_debated(paper_id, paper_title)
                    print(f"    ✅ [{i+1}/{len(records)}] 저장 완료")
                else:
                    skipped_count += 1
                    print(f"    ⏭️ [{i+1}/{len(records)}] 건너뜀")
            except Exception as e:
                error_count += 1
                print(f"    ❌ [{i+1}/{len(records)}] 오류: {e}")
                time.sleep(5)

        # 시간 부족으로 중간에 끊기면, 아직 안 본 레코드는 같은 JSONL에 남겨 다음 배치가 이어서 처리하게 함.
        # (예전에는 통째로 processed/로 옮겨 나머지 ~900편이 큐에서 사라짐)
        if exited_by_timeout and resume_from_index < len(records):
            remaining = records[resume_from_index:]
            try:
                with open(file_path, "w", encoding="utf-8") as out:
                    for r in remaining:
                        out.write(json.dumps(r, ensure_ascii=False) + "\n")
                print(
                    f"  📌 미처리 {len(remaining)}건을 `{file_path.name}`에 유지했습니다. "
                    "다음 배치에서 이어서 처리됩니다.",
                    flush=True,
                )
            except Exception as e:
                print(f"  ⚠️ 미처리 큐 재기록 실패 ({file_path}): {e}", flush=True)
        else:
            mark_file_processed(file_path)
            processed_files.append(file_path.name)
        print(f"  📊 파일 처리 완료: {success_in_file}/{len(records)}건 저장")
        if target_file:
            break

    print("\n" + "=" * 60)
    print(
        f"🏁 배치 종료 | 성공: {processed_count}건 | 건너뜀: {skipped_count}건 "
        f"(중복 논문 {duplicate_skipped_count}건 포함) | 오류: {error_count}건"
    )
    print("=" * 60 + "\n")

    if not found_any_data:
        _send_telegram_notification(
            "ℹ️ LLM 토론 배치 스킵\n"
            f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "사유: 처리할 원시 데이터가 없습니다."
        )
    else:
        mode = "테스트" if target_file or max_records is not None or duration_sec != EVENT_DURATION_SEC else "정규"
        lines = [
            "🔔 LLM 토론 배치 완료",
            f"실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"실행 모드: {mode}",
            f"성공 저장: {processed_count}건",
            f"건너뜀: {skipped_count}건",
            f"중복 논문 스킵: {duplicate_skipped_count}건",
            f"오류: {error_count}건",
        ]
        if stop_reason == "queue_depleted":
            lines.append("종료 사유: 큐 소진(자동 종료)")
        if processed_files:
            lines.append(f"처리 파일: {', '.join(processed_files[:5])}")
            if len(processed_files) > 5:
                lines.append(f"... 외 {len(processed_files) - 5}개 파일")
        _send_telegram_notification("\n".join(lines))

    result = {
        "processed_count": processed_count,
        "skipped_count": skipped_count,
        "duplicate_skipped_count": duplicate_skipped_count,
        "error_count": error_count,
        "processed_files": processed_files,
        "found_any_data": found_any_data,
        "stop_reason": stop_reason,
    }

    hb_stop.set()
    if hb_thread is not None:
        hb_thread.join(timeout=2)

    return result


def main() -> None:
    _configure_utf8_stdio()
    if not get_gemini_api_keys():
        print("❌ .env에 GEMINI_API_KEY(또는 GEMINI_API_KEYS / GEMINI_API_KEY_2…_20)를 설정하세요.")
        return

    parser = argparse.ArgumentParser(description="LLM 토론 기반 파인튜닝 데이터 생성 배치")
    parser.add_argument("--test", action="store_true", help="배치를 즉시 1회 실행")
    parser.add_argument("--file", type=str, default=None, help="처리할 특정 JSONL 파일명 또는 경로")
    parser.add_argument("--max-records", type=int, default=None, help="테스트 시 최대 처리 레코드 수")
    parser.add_argument(
        "--duration-sec",
        type=int,
        default=EVENT_DURATION_SEC,
        help=f"최대 실행 시간(초). 0 이하면 시간 제한 없음 (기본 {EVENT_DURATION_SEC})",
    )
    parser.add_argument(
        "--stop-on-empty",
        action="store_true",
        help="처리 도중 큐가 소진되면 자동 종료(주로 텔레그램 /debate_start 무제한 모드용)",
    )
    parser.add_argument(
        "--season2",
        action="store_true",
        help="Phase2: 6대 주제 순회·하이브리드 RAG Top-5 기반 시즌2 토론 → train_data_v2.jsonl append",
    )
    parser.add_argument(
        "--season2-rounds",
        type=int,
        default=1,
        help="시즌2 라운드 수(주제 커서는 라운드당 1칸 전진). 기본 1",
    )
    parser.add_argument(
        "--season2-theme",
        type=str,
        default=None,
        help="시즌2 대주제를 고정(영문). 예: 'Graph RAG'. 미지정 시 커서로 순회",
    )
    parser.add_argument(
        "--season2-workers",
        type=int,
        default=1,
        help="시즌2 동시 라운드 수(1~8). 2면 서로 다른 주제 2개를 병렬 처리. --season2-theme 시 1로 강제",
    )
    args = parser.parse_args()

    if args.season2:
        to = (args.season2_theme or "").strip() or None
        weekly_llm_debate_season2_event(
            rounds=max(1, int(args.season2_rounds)),
            theme_override=to,
            workers=max(1, int(args.season2_workers)),
        )
        return

    if args.test:
        print("🧪 테스트 모드: 배치 1회 즉시 실행")
        weekly_llm_debate_event(
            target_file=args.file,
            max_records=args.max_records,
            duration_sec=args.duration_sec,
            stop_on_empty=args.stop_on_empty,
        )
        return

    for _day in DEBATE_SCHEDULE_WEEKDAYS:
        getattr(schedule.every(), _day).at("02:00").do(weekly_llm_debate_event)

    print(f"📅 LLM 토론 스케줄러 시작 (월~금 02:00, {len(DEBATE_SCHEDULE_WEEKDAYS)}회/주)")
    print("   테스트: python llm_debate_scheduler.py --test --file sample.jsonl --max-records 3")
    print("   Ctrl+C로 종료\n")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
