"""Gemini 다중 API 키·429(Rate limit) 시 다음 키로 순환."""

from __future__ import annotations

import time
from typing import Any, Optional

import httpx
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

try:
    from google.api_core.exceptions import ResourceExhausted as _ResourceExhausted
except ImportError:
    _ResourceExhausted = None


def is_gemini_rate_limit_error(exc: BaseException) -> bool:
    """Gemini/게이트웨이 429·쿼터·ResourceExhausted 계열."""
    if _ResourceExhausted is not None and isinstance(exc, _ResourceExhausted):
        return True
    sc = getattr(exc, "status_code", None)
    if sc == 429:
        return True
    response = getattr(exc, "response", None)
    if response is not None and getattr(response, "status_code", None) == 429:
        return True
    if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 429:
        return True
    name = type(exc).__name__
    if "ResourceExhausted" in name or "TooManyRequests" in name:
        return True
    msg = str(exc).lower()
    if "resource_exhausted" in msg or "resource exhausted" in msg:
        return True
    if "429" in msg and any(x in msg for x in ("quota", "rate", "limit", "exhausted", "throttl")):
        return True
    return False


class RotatingGeminiChat:
    """LangChain ChatGoogleGenerativeAI 호환: invoke 시 429면 다음 키로 재시도."""

    def __init__(self, keys: list[str], model: str, temperature: float) -> None:
        self._keys = [k.strip() for k in keys if k and str(k).strip()]
        self._model = model
        self._temperature = temperature

    def invoke(
        self,
        input: Any,
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ):
        if not self._keys:
            raise ValueError("Gemini API 키가 없습니다. GEMINI_API_KEY 또는 GEMINI_API_KEYS를 설정하세요.")
        last: BaseException | None = None
        for idx, key in enumerate(self._keys):
            llm = ChatGoogleGenerativeAI(
                model=self._model,
                api_key=key,
                temperature=self._temperature,
            )
            try:
                return llm.invoke(input, config=config, **kwargs)
            except Exception as e:
                last = e
                if is_gemini_rate_limit_error(e) and idx < len(self._keys) - 1:
                    print(
                        f"[Gemini] {idx + 1}번 키 Rate limit → "
                        f"{idx + 2}번 키로 전환해 같은 요청을 다시 호출합니다. (총 {len(self._keys)}개 키)",
                        flush=True,
                    )
                    time.sleep(1.5)
                    continue
                if is_gemini_rate_limit_error(e) and idx == len(self._keys) - 1:
                    print(
                        "[Gemini] 마지막 키도 Rate limit — 추가 키 없음, 이 호출은 여기서 중단합니다.",
                        flush=True,
                    )
                raise
        if last:
            raise last
        raise RuntimeError("Gemini invoke: unexpected empty key list")


def gemini_sdk_generate_json(keys: list[str], model_name: str, prompt: str) -> str:
    """google.generativeai SDK로 JSON MIME 생성. 429 시 키 순환."""
    import google.generativeai as genai

    clean = [k.strip() for k in keys if k and str(k).strip()]
    if not clean:
        raise ValueError("Gemini API 키가 없습니다.")
    gen_cfg = genai.types.GenerationConfig(response_mime_type="application/json")
    last: BaseException | None = None
    for idx, key in enumerate(clean):
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(
                model_name,
                generation_config=gen_cfg,
            )
            resp = model.generate_content(prompt)
            return (resp.text or "").strip()
        except Exception as e:
            last = e
            if is_gemini_rate_limit_error(e) and idx < len(clean) - 1:
                print(
                    f"    [Gemini] {idx + 1}번 키 Rate limit → "
                    f"{idx + 2}번 키로 전환 후 비평 요청을 다시 보냅니다. (키 {len(clean)}개)",
                    flush=True,
                )
                time.sleep(1.5)
                continue
            if is_gemini_rate_limit_error(e) and idx == len(clean) - 1:
                print(
                    "    ⚠️ Gemini: 마지막 키까지 Rate limit — 이번 논문 토론(비평 단계)은 여기서 중단합니다.",
                    flush=True,
                )
            raise
    if last:
        raise last
    return ""
