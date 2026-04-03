#!/usr/bin/env python3
"""Tavily 검색 + Qwen/Gemini 요약 테스트"""
import sys
sys.path.insert(0, ".")
from tools.runtime.agent_tools.agent_tools.tavily_search_tool import run as tavily_run
from core.llm.agent_llm import get_executor_llm, get_planner_llm
from langchain_core.messages import HumanMessage

OUT = []

def log(s):
    print(s, flush=True)
    OUT.append(str(s))

# 1. Tavily 검색
log("=== 1. Tavily 검색 실행 ===")
raw = tavily_run("오늘 최신 IT 뉴스 검색해 줘")
log(raw[:1500] + "\n...")
log(f"[총 {len(raw)}자]\n")

# 2. Qwen → Gemini 순으로 요약 시도
prompt = f"""아래 검색 결과를 한국어로 요약해 줘.
- 각 뉴스별로 2~3문장으로 핵심만 전달
- 5개 뉴스 모두 포함 (일부 누락 금지)
- 제목·출처·링크는 생략하고 내용 요약만

[검색 결과]
{raw[:6000]}"""

# Gemini 먼저 (빠름), 실패 시 Qwen
for name, llm_getter in [("Gemini", get_executor_llm), ("Qwen", get_planner_llm)]:
    log(f"=== 2. {name} 요약 시도 ===")
    try:
        resp = llm_getter().invoke([HumanMessage(content=prompt)])
        summary = (resp.content or "").strip()
        if summary and len(summary) > 50:
            log(summary)
            log(f"\n[요약 성공 ({name}): {len(summary)}자]")
            break
    except Exception as e:
        log(f"[{name} 실패] {e}")
else:
    log("[모든 LLM 요약 실패]")

# 결과 파일 저장
with open("test_tavily_qwen_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
log("\n→ test_tavily_qwen_result.txt 에 저장됨")
