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
import json
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import google.generativeai as genai
import schedule
import telebot
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

load_dotenv()

from agent_llm import get_llm_debate_scheduler_llm
from retry_utils import retry_on_network_error

# ============ 설정 ============
RAW_DATA_QUEUE = Path("./raw_data_queue")
PROCESSED_DATA_DIR = Path("./raw_data_queue/processed")
FINETUNE_OUTPUT = Path("./finetune_datasets/train_data.jsonl")
DEBATE_INDEX_PATH = Path("./finetune_datasets/debated_paper_ids.jsonl")
GEMINI_MODEL = "gemini-2.5-flash"
EVENT_DURATION_SEC = 7200  # 2시간
LLM_DELAY_SEC = 10
CONTENT_MAX_CHARS = 80000  # 논문 본문 최대 길이
# run_scheduler.py 의 LLM 토론 트리거 요일과 맞출 것
DEBATE_SCHEDULE_WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday")


def _configure_utf8_stdio() -> None:
    """cron/launch 환경에서도 한글 로그가 깨지지 않도록 UTF-8 고정."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream and hasattr(stream, "reconfigure"):
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
                            paper_id = str(item.get("paper_id", "")).strip()
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
    try:
        DEBATE_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DEBATE_INDEX_PATH, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "paper_id": paper_id,
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
        FINETUNE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record, ensure_ascii=False) + "\n"
        with open(FINETUNE_OUTPUT, "a", encoding="utf-8") as f:
            f.write(line)
        return True
    except Exception as e:
        print(f"  ❌ 저장 실패: {e}")
        return False


def _truncate(content: str, max_len: int = CONTENT_MAX_CHARS) -> str:
    if len(content) <= max_len:
        return content
    return content[:max_len] + "\n\n[... 생략 ...]"


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
        return {
            "system": "당신은 최신 AI 논문을 분석하는 수석 연구원입니다.",
            "instruction": instruction,
            "output": output,
        }
    return None


def _strip_leading_label(text: str, labels: tuple[str, ...]) -> str:
    text = (text or "").strip()
    for label in labels:
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
    text = _normalize_text(text)
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
1. instruction은 자연스러운 질문 1문장만 작성한다.
2. output은 그 질문에 대한 답변 1문단만 작성한다.
3. Q:, A:, 질문:, 답변:, bullet, 여러 개의 Q&A 금지.
4. 근거 텍스트에 명시적으로 없는 숫자, 비용, 성능 수치, 무게, 개수, 자유도, 비율은 절대 추가하지 말고 삭제한다.
5. 확실하지 않은 세부 정보는 보수적으로 생략한다.
6. 설명 문장, 머리말, 코드블록 없이 JSON 객체 1개만 출력한다.

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
    content = raw_record.get("content", raw_record.get("body", ""))
    if not content:
        print("  ⚠️ content/body 필드 없음, 건너뜀")
        return None

    content = _truncate(content)
    paper_id = raw_record.get("paper_id", "unknown")
    paper_title = raw_record.get("title", paper_id)
    abstract = raw_record.get("abstract", "")
    source_excerpt = f"[title]\n{paper_title}\n\n[abstract]\n{abstract}\n\n[content]\n{content[:15000]}"

    # 1. Qwen 초안
    print(f"    [1/3] Qwen 초안 생성 중...")
    try:
        llm_qwen = get_llm_debate_scheduler_llm()
        draft_prompt = f"""다음 학술 논문 본문을 읽고, 핵심 내용을 묻고 답하는 Q&A 1세트를 작성해.
형식: 질문 1개 + 답변 1개. JSON 형태로 instruction과 output만 출력해.
설명 문장, 머리말, 코드블록 마크다운 없이 아래 JSON 객체 1개만 출력:
{{"instruction": "질문", "output": "답변"}}
- 질문은 실제 논문 내용을 묻는 구체적인 질문 1개여야 한다.
- 답변은 단일 문단 1개만 작성한다.
- 논문 본문에 명시적으로 없는 숫자, 비용, 성능 수치, 무게, 개수는 절대 추측하지 말고 쓰지 마라.

논문 본문:
{content[:40000]}
"""
        draft_resp = llm_qwen.invoke([HumanMessage(content=draft_prompt)])
        draft_qa = draft_resp.content.strip() if draft_resp.content else ""
        time.sleep(LLM_DELAY_SEC)
    except Exception as e:
        print(f"    ❌ Qwen 초안 실패: {e}")
        return None

    # 2. Gemini 비평 및 수정
    print(f"    [2/3] Gemini 비평/수정 중...")
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel(
            GEMINI_MODEL,
            generation_config=genai.types.GenerationConfig(response_mime_type="application/json"),
        )
        critique_prompt = f"""다음은 Qwen이 만든 Q&A 초안입니다.

[초안 Q&A]
{draft_qa[:6000]}

[원시 논문 일부]
{content[:15000]}

초안 Q&A의 논리적 오류나 개선점을 비판하고, 더 정확하고 심층적인 Q&A로 수정해 줘.
오직 완성된 JSON 형태만 출력: {{"instruction": "질문", "output": "답변"}}
- 숫자, 비용, 성능 수치, 무게, 개수는 원문에 명시된 경우에만 유지하고, 불명확하면 삭제해.
- output에는 여러 개의 Q&A를 넣지 말고 단일 답변 문단만 남겨.
"""
        critique_resp = model.generate_content(critique_prompt)
        critique_text = critique_resp.text.strip() if critique_resp.text else ""
        time.sleep(LLM_DELAY_SEC)
    except Exception as e:
        print(f"    ❌ Gemini 비평 실패: {e}")
        return None

    # 3. Qwen 최종 수정
    print(f"    [3/3] Qwen 최종 생성 중...")
    try:
        final_prompt = f"""다음 비평을 반영해 최종 Q&A를 완성해.
비평/수정안: {critique_text[:3000]}

반드시 JSON만 출력: {{"instruction": "질문", "output": "답변"}}
추가 설명, 머리말, 코드블록 금지.
- instruction은 질문 1문장만.
- output은 답변 1문단만.
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


def weekly_llm_debate_event(
    *,
    target_file: str | None = None,
    max_records: int | None = None,
    duration_sec: int = EVENT_DURATION_SEC,
) -> dict:
    """스케줄러가 월~금 02:00에 호출, 최대 2시간 동안 배치 처리"""
    _configure_utf8_stdio()
    start = time.time()
    print("\n" + "=" * 60)
    print(f"🚀 LLM 토론 배치 시작: {datetime.now().isoformat()}")
    print("=" * 60)

    processed_count = 0
    error_count = 0
    skipped_count = 0
    duplicate_skipped_count = 0
    processed_files: list[str] = []
    found_any_data = False
    debated_paper_ids = _load_debated_paper_ids()
    seen_in_this_run: set[str] = set()

    while (time.time() - start) < duration_sec:
        remaining = int(duration_sec - (time.time() - start))
        print(f"\n⏱️ 남은 시간: {remaining}초")

        result = get_unprocessed_raw_data(target_file=target_file)
        if result is None:
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
        for i, rec in enumerate(records):
            if (time.time() - start) >= duration_sec:
                print("  ⏰ 2시간 도달, 배치 종료")
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
        if processed_files:
            lines.append(f"처리 파일: {', '.join(processed_files[:5])}")
            if len(processed_files) > 5:
                lines.append(f"... 외 {len(processed_files) - 5}개 파일")
        _send_telegram_notification("\n".join(lines))

    return {
        "processed_count": processed_count,
        "skipped_count": skipped_count,
        "duplicate_skipped_count": duplicate_skipped_count,
        "error_count": error_count,
        "processed_files": processed_files,
        "found_any_data": found_any_data,
    }


def main() -> None:
    _configure_utf8_stdio()
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ .env에 GEMINI_API_KEY를 설정하세요.")
        return

    parser = argparse.ArgumentParser(description="LLM 토론 기반 파인튜닝 데이터 생성 배치")
    parser.add_argument("--test", action="store_true", help="배치를 즉시 1회 실행")
    parser.add_argument("--file", type=str, default=None, help="처리할 특정 JSONL 파일명 또는 경로")
    parser.add_argument("--max-records", type=int, default=None, help="테스트 시 최대 처리 레코드 수")
    parser.add_argument("--duration-sec", type=int, default=EVENT_DURATION_SEC, help="최대 실행 시간(초)")
    args = parser.parse_args()

    if args.test:
        print("🧪 테스트 모드: 배치 1회 즉시 실행")
        weekly_llm_debate_event(
            target_file=args.file,
            max_records=args.max_records,
            duration_sec=args.duration_sec,
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
