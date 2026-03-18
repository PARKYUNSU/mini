#!/usr/bin/env python3
import json
import os
import sqlite3
import time
from pathlib import Path

os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

from dotenv import load_dotenv

load_dotenv()

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from agent_bot import (
    AgentSkillLibrary,
    build_graph,
    clear_session,
    direct_answer_node,
    router_node,
    use_existing_tool_node,
)


BASE_DIR = Path(__file__).resolve().parent
RESULT_PATH = BASE_DIR / "batch_test_results.json"


CATEGORY_1 = [
    ("A-01", "안녕! 오늘 하루 어땠어?", "A"),
    ("A-02", "넌 이름이 뭐야? 누가 널 만들었어?", "A"),
    ("A-03", "내가 방금 너한테 뭐라고 인사했지?", "A"),
    ("A-04", "나는 텍스트보다 시각적인 걸 잘 기억하는 사람이야. 기억해 둬.", "A"),
    ("A-05", "아까 내가 내 기억력에 대해 뭐라고 말했었지?", "A"),
    ("A-06", "나 지금 너무 피곤한데 위로 좀 해줘.", "A"),
    ("A-07", "넌 할 줄 아는 게 뭐야?", "A"),
    ("A-08", "(뜬금없이) 취소", "A"),
    ("A-09", "취소해 줘.", "A"),
    ("A-10", "/cancel", "A"),
    ("A-11", "재시작", "A"),
    ("A-12", "1 더하기 1은 뭐야?", "A"),
    ("A-13", "고마워, 수고했어!", "A"),
    ("A-14", "너 지금 어디 서버에서 돌아가고 있어?", "A"),
    ("A-15", "텔레그램 봇으로 나랑 대화하니까 기분이 어때?", "A"),
    ("A-16", "내가 제일 좋아하는 분야가 데이터 분석이랑 과학, 성경인데 알고 있어?", "A"),
    ("A-17", "아까 내가 좋아하는 분야 3가지 말해봐.", "A"),
    ("A-18", "넌 참 똑똑한 비서 같아.", "A"),
    ("A-19", "나 이제 잘 건데 내일 아침에 보자.", "A"),
    ("A-20", "좋은 아침! 어제 하던 얘기 계속해 볼까?", "A"),
]

CATEGORY_2 = [
    ("B-01", "우리 DB에 있는 논문 중에 CRAFT 핸드에 관한 논문 요약해 줘.", "B"),
    ("B-02", "CRAFT 핸드 논문에서 TPU 소재를 사용한 이유가 정확히 뭐야?", "B"),
    ("B-03", "방금 설명한 TPU 소재 부분만 더 길고 아주 상세하게 설명해 줘.", "B"),
    ("B-04", "Incremental Neural Network Verification 논문에서 제안한 핵심 알고리즘이 뭐야?", "B"),
    ("B-05", "Efficient Relational Context Perception 논문의 한계점(Limitation)은 뭐야?", "B"),
    ("B-06", "최근 수집된 논문들 중에서 LLM Agent와 관련된 논문이 있어?", "B"),
    ("B-07", "CRAFT 핸드 논문의 저자들은 어느 대학 소속이야?", "B"),
    ("B-08", "논문에서 제안한 모델의 성능 평가(Evaluation) 지표는 어떤 걸 썼어?", "B"),
    ("B-09", "지식 그래프 완성을 다룬 논문 내용을 초등학생도 이해할 수 있게 비유를 써서 설명해 줘.", "B"),
    ("B-10", "내가 아까 물어본 CRAFT 핸드랑 지식 그래프 논문의 차이점이 뭐야?", "B"),
    ("B-11", "우리 로컬 DB에 '양자 역학'과 관련된 논문이 있어?", "B"),
    ("B-12", "방금 네가 요약해 준 논문 내용에서 수학적 수식이 있었어?", "B"),
    ("B-13", "논문의 Abstract(초록) 부분만 한국어로 직역해서 보여줘.", "B"),
    ("B-14", "이 논문 우리 DB에 있어?", "B"),
    ("B-15", "최근 3일 동안 크롤링된 논문 중에 가장 흥미로운 거 하나 추천해 줘.", "B"),
    ("B-16", "이 논문들이 내 데이터 분석 업무에 어떻게 도움이 될까?", "B"),
    ("B-17", "제공된 문서에 없는 내용이면 절대 지어내지 말고 모른다고 해봐. 지구의 나이가 몇 살이야?", "B"),
    ("B-18", "논문의 Conclusion(결론)만 3줄로 요약해.", "B"),
    ("B-19", "CRAFT 핸드는 제작 비용이 얼마라고 나와 있어?", "B"),
    ("B-20", "지금까지 네가 요약해 준 논문 내용을 표(Table) 형태로 정리해 줘.", "B"),
]

CATEGORY_3_1 = [
    ("C-01", "네이버 금융에서 현재 삼성전자 주가 크롤링해서 알려주는 도구 만들어 줘.", "C"),
    ("C-02", "구글 파이낸스에서 원/달러 환율 가져오는 도구 만들어 줘.", "C"),
    ("C-03", "Hacker News 메인 페이지에서 1위부터 5위까지 글 제목 긁어오는 도구 짜줘.", "C"),
    ("C-04", "내일 부산 날씨 알려주는 도구 만들어 줘.", "C"),
    ("C-05", "무료 성경 API를 써서 요한복음(John) 1장 1절 영어로 가져오는 도구 만들어 줘.", "C"),
    ("C-06", "가져온 영어 성경 구절을 deep-translator 패키지로 한국어로 번역하는 도구 만들어.", "C"),
    ("C-07", "네이버 뉴스 IT/과학 홈에서 제일 위에 있는 뉴스 제목 3개 긁어와 줘.", "C"),
    ("C-08", "위키백과(Wikipedia) 파이썬 API 패키지 설치하고, '인공지능' 문서의 첫 문단만 가져오는 도구 짜줘.", "C"),
    ("C-09", "코인마켓캡이나 업비트 API로 현재 비트코인(BTC) 가격 가져와.", "C"),
    ("C-10", "오늘 서울의 미세먼지 수치를 웹에서 크롤링해서 알려줘.", "C"),
    ("C-11", "GitHub API를 써서 'LangGraph' 레포지토리의 별(Star) 개수 가져오는 도구 만들어.", "C"),
    ("C-12", "공공데이터포털 같은 데서 오늘 날짜의 공휴일 여부를 확인하는 코드 짜봐.", "C"),
    ("C-13", "특정 웹사이트(예: example.com)의 HTML title 태그만 긁어오는 아주 가벼운 크롤러 만들어 줘.", "C"),
    ("C-14", "구글 검색 결과 페이지를 크롤링할 수 있어?", "C"),
    ("C-15", "특정 영단어('Agent')의 어원을 온라인 사전에서 긁어오는 도구 짜줘.", "C"),
    ("C-16", "로또 당첨 번호 최신 회차 결과를 크롤링해서 알려줘.", "C"),
    ("C-17", "아까 만든 환율 도구랑 주식 도구를 합쳐서, 삼성전자 주가를 달러로 환산해서 보여주는 도구 만들어 줘.", "C"),
]

CATEGORY_3_2 = [
    ("R-01", "모레 제주도 날씨는 어때?", "B"),
    ("R-02", "아까 만든 성경 도구로 창세기(Genesis) 1장 1절 가져와 줘.", "B"),
    ("R-03", "이더리움(ETH) 가격은 얼마야?", "B"),
]


def save_results(rows):
    RESULT_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def test_direct(category_name, cases, chat_id):
    rows = []
    clear_session(chat_id)
    cfg = {"configurable": {"chat_id": chat_id, "bot": None}}
    for idx, question, expected in cases:
        started = time.time()
        route_info = router_node({"user_request": question}, config=cfg)
        actual = route_info.get("router_choice", "?")
        result_text = ""
        error = ""
        try:
            if route_info.get("route_type") == "direct_answer":
                out = direct_answer_node(
                    {
                        "user_request": question,
                        "router_choice": route_info.get("router_choice", "A"),
                    },
                    config=cfg,
                )
                result_text = out.get("direct_response", "")
            elif route_info.get("route_type") == "use_existing_tool":
                out = use_existing_tool_node({"user_request": question}, config=cfg)
                result_text = out.get("execution_result", "")
        except Exception as e:
            error = str(e)
        rows.append(
            {
                "category": category_name,
                "id": idx,
                "question": question,
                "expected": expected,
                "actual": actual,
                "passed": actual == expected and not error,
                "elapsed_sec": round(time.time() - started, 2),
                "error": error,
                "preview": (result_text or "")[:500],
            }
        )
        save_results(rows_all + rows)
    return rows


def run_graph_case(graph, question, chat_id, expected, idx):
    thread_id = f"batch_{idx}_{int(time.time() * 1000)}"
    cfg = {"configurable": {"thread_id": thread_id, "chat_id": chat_id, "bot": None}}
    started = time.time()
    error = ""
    preview = ""
    actual = "?"
    saved_tool = None
    try:
        for _ in graph.stream(
            {
                "user_request": question,
                "route_type": "",
                "direct_response": "",
                "plan": [],
                "approval_status": "pending",
                "generated_code": "",
                "execution_result": "",
                "retry_count": 0,
                "error_hint": "",
            },
            cfg,
            stream_mode="updates",
        ):
            pass
        state = graph.get_state(cfg)
        values = state.values if hasattr(state, "values") else {}
        actual = values.get("router_choice", "?")
        if state.next:
            for _ in graph.stream(Command(resume="승인"), cfg, stream_mode="updates"):
                pass
            state = graph.get_state(cfg)
            values = state.values if hasattr(state, "values") else {}
        actual = values.get("router_choice", actual)
        if values.get("route_type") == "planner":
            preview = values.get("execution_result", "")[:500]
            code = values.get("generated_code", "")
            result = values.get("execution_result", "")
            request = values.get("user_request", question)
            if code and result and not any(x in result for x in ("오류", "Error", "Exception", "Timeout")):
                saved_tool = AgentSkillLibrary().save_tool(code, request)
        elif values.get("route_type") == "use_existing_tool":
            preview = values.get("execution_result", "")[:500]
        elif values.get("route_type") == "direct_answer":
            preview = values.get("direct_response", "")[:500]
    except Exception as e:
        error = str(e)
    return {
        "id": idx,
        "question": question,
        "expected": expected,
        "actual": actual,
        "passed": actual == expected and not error,
        "elapsed_sec": round(time.time() - started, 2),
        "error": error,
        "preview": preview,
        "saved_tool": saved_tool,
    }


rows_all = []


def main():
    global rows_all
    conn = sqlite3.connect(str(BASE_DIR / "agent_checkpoints.db"), check_same_thread=False)
    graph = build_graph(checkpointer=SqliteSaver(conn))

    rows_all.extend(test_direct("Category 1", CATEGORY_1, "batch_cat1"))
    rows_all.extend(test_direct("Category 2", CATEGORY_2, "batch_cat2"))
    save_results(rows_all)

    clear_session("batch_cat3")
    for idx, question, expected in CATEGORY_3_1:
        row = run_graph_case(graph, question, "batch_cat3", expected, idx)
        row["category"] = "Category 3-1"
        rows_all.append(row)
        save_results(rows_all)

    for idx, question, expected in CATEGORY_3_2:
        row = run_graph_case(graph, question, "batch_cat3", expected, idx)
        row["category"] = "Category 3-2"
        rows_all.append(row)
        save_results(rows_all)

    print(json.dumps(rows_all, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
