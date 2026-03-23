"""Vision: 이미지 다운로드·Base64·Ollama 분석"""

import base64
import tempfile
import time
from pathlib import Path

from langchain_core.messages import HumanMessage

from agent_config import ollama_kwargs

# Lazy import to avoid loading Ollama at module load
def _get_ollama_llm():
    from langchain_ollama import ChatOllama

    return ChatOllama(**ollama_kwargs(temperature=0.2))


def download_photo_to_base64(bot, message) -> tuple[str, str] | None:
    """텔레그램 사진 → (base64_str, user_request) 또는 None"""
    if not message.photo:
        return None
    t0 = time.perf_counter()
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_bytes = bot.download_file(file_info.file_path)
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        try:
            with open(tmp_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
        finally:
            Path(tmp_path).unlink(missing_ok=True)
        user_request = (message.caption or "").strip()
        if not user_request:
            user_request = "이 이미지를 자세히 분석하고 무엇인지 설명해 줘."
        elapsed = time.perf_counter() - t0
        print(f"[DEBUG] Vision: 사진 다운로드+Base64 {elapsed:.2f}s ({len(b64)//1024}KB)", flush=True)
        return (b64, user_request)
    except Exception as e:
        import traceback
        print(f"[DEBUG] 사진 다운로드/Base64 변환 오류: {e}\n{traceback.format_exc()}")
        return None


def build_message_content(text: str, image_base64: str | None):
    """텍스트만 또는 LangChain 멀티모달 리스트 포맷"""
    if not image_base64:
        return text
    return [
        {"type": "text", "text": text},
        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_base64}"},
    ]


def run_vision_analysis(bot, chat_id: str, user_request: str, base64_image: str, status_msg) -> str | None:
    """Qwen Vision으로 이미지 분석. 결과 문자열 반환, 실패 시 None."""
    t0 = time.perf_counter()
    try:
        llm = _get_ollama_llm()
        content = [
            {"type": "text", "text": user_request},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"},
        ]
        resp = llm.invoke([HumanMessage(content=content)])
        elapsed = time.perf_counter() - t0
        print(f"[DEBUG] Vision: Ollama 추론 {elapsed:.2f}s (응답 {len(resp.content or '')}자)", flush=True)
        return (resp.content or "").strip()
    except Exception as e:
        import traceback
        print(f"[DEBUG] Vision 분석 오류: {e}\n{traceback.format_exc()}")
        return None
