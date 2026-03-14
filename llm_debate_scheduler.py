#!/usr/bin/env python3
"""
LLM 토론 기반 파인튜닝 데이터 생성 스케줄러
- 매주 토요일 02:00에 2시간 동안 배치 실행
- Qwen(초안) → Gemini(비평) → Qwen(최종) 파이프라인
"""

import os

os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

import json
import shutil
import time
from datetime import datetime
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.messages import HumanMessage
import schedule

load_dotenv()

# ============ 설정 ============
RAW_DATA_QUEUE = Path("./raw_data_queue")
PROCESSED_DATA_DIR = Path("./raw_data_queue/processed")
FINETUNE_OUTPUT = Path("./finetune_datasets/train_data.jsonl")
OLLAMA_MODEL = "qwen2.5:7b"
GEMINI_MODEL = "gemini-2.5-flash"
EVENT_DURATION_SEC = 7200  # 2시간
LLM_DELAY_SEC = 10
CONTENT_MAX_CHARS = 80000  # 논문 본문 최대 길이


def get_unprocessed_raw_data() -> tuple[Path, list[dict]] | None:
    """
    raw_data_queue/에서 미처리 JSONL 파일 하나를 읽어 반환.
    반환: (파일경로, [레코드 리스트]) 또는 None
    """
    RAW_DATA_QUEUE.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

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

    # 1. Qwen 초안
    print(f"    [1/3] Qwen 초안 생성 중...")
    try:
        llm_qwen = ChatOllama(model=OLLAMA_MODEL, temperature=0.2)
        draft_prompt = f"""다음 학술 논문 본문을 읽고, 핵심 내용을 묻고 답하는 Q&A 1세트를 작성해.
형식: 질문 1개 + 답변 1개. JSON 형태로 instruction과 output만 출력해.

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
"""
        final_resp = llm_qwen.invoke([HumanMessage(content=final_prompt)])
        final_text = final_resp.content.strip() if final_resp.content else critique_text
        time.sleep(LLM_DELAY_SEC)
    except Exception as e:
        print(f"    ❌ Qwen 최종 실패: {e}")
        final_text = critique_text

    # JSON 파싱
    try:
        for block in (final_text, critique_text, draft_qa):
            try:
                if "{" in block and "}" in block:
                    start = block.find("{")
                    end = block.rfind("}") + 1
                    parsed = json.loads(block[start:end])
                    instruction = parsed.get("instruction", "").strip()
                    output = parsed.get("output", "").strip()
                    if instruction and output:
                        return {
                            "system": "당신은 최신 AI 논문을 분석하는 수석 연구원입니다.",
                            "instruction": instruction,
                            "output": output,
                        }
            except json.JSONDecodeError:
                continue
        print("    ⚠️ 유효한 JSON 추출 실패")
        return None
    except Exception as e:
        print(f"    ❌ 파싱 오류: {e}")
        return None


def weekly_llm_debate_event() -> None:
    """매주 토요일 02:00에 실행, 2시간 동안 배치 처리"""
    start = time.time()
    print("\n" + "=" * 60)
    print(f"🚀 LLM 토론 배치 시작: {datetime.now().isoformat()}")
    print("=" * 60)

    processed_count = 0
    error_count = 0

    while (time.time() - start) < EVENT_DURATION_SEC:
        remaining = int(EVENT_DURATION_SEC - (time.time() - start))
        print(f"\n⏱️ 남은 시간: {remaining}초")

        result = get_unprocessed_raw_data()
        if result is None:
            print("  📭 처리할 원시 데이터 없음. 대기 중...")
            time.sleep(60)
            continue

        file_path, records = result
        print(f"  📄 처리 중: {file_path.name} ({len(records)}건)")

        success_in_file = 0
        for i, rec in enumerate(records):
            if (time.time() - start) >= EVENT_DURATION_SEC:
                print("  ⏰ 2시간 도달, 배치 종료")
                break

            try:
                qa = run_debate_pipeline(rec)
                if qa and save_to_finetune_jsonl(qa):
                    success_in_file += 1
                    processed_count += 1
                    print(f"    ✅ [{i+1}/{len(records)}] 저장 완료")
                else:
                    print(f"    ⏭️ [{i+1}/{len(records)}] 건너뜀")
            except Exception as e:
                error_count += 1
                print(f"    ❌ [{i+1}/{len(records)}] 오류: {e}")
                time.sleep(5)

        mark_file_processed(file_path)
        print(f"  📊 파일 처리 완료: {success_in_file}/{len(records)}건 저장")

    print("\n" + "=" * 60)
    print(f"🏁 배치 종료 | 성공: {processed_count}건 | 오류: {error_count}건")
    print("=" * 60 + "\n")


def main() -> None:
    import sys

    if not os.getenv("GEMINI_API_KEY"):
        print("❌ .env에 GEMINI_API_KEY를 설정하세요.")
        return

    if "--test" in sys.argv:
        print("🧪 테스트 모드: 배치 1회 즉시 실행 (2시간 제한 적용)")
        weekly_llm_debate_event()
        return

    schedule.every().saturday.at("02:00").do(weekly_llm_debate_event)

    print("📅 LLM 토론 스케줄러 시작 (매주 토요일 02:00)")
    print("   테스트: python llm_debate_scheduler.py --test")
    print("   Ctrl+C로 종료\n")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
