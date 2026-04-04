#!/usr/bin/env python3
"""
라우터 1단계 하드룰·파이썬 3단 분류 등 순수(또는 경로/콜백만 주입) 규칙.

agent_bot.py의 무거운 의존성(langchain, chromadb, telebot) 없이 import 가능.
테스트는 agent_config + 이 모듈만으로 라우팅 회귀 검증 가능.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal, Optional

# ----- 주입: 채팅별 논문 모드·최근 도구 (agent_bot에서 제공) -----


@dataclass(frozen=True)
class RouterStep1Deps:
    """router_step1_hard_rules에 필요한 런타임 의존성."""

    agent_tools_dir: Path
    get_paper_mode: Callable[[str], bool]
    resolve_recent_tool: Callable[[str, str], Optional[str]]


def user_wants_intentional_exec_error(user_request: str) -> bool:
    """
    사용자가 샌드박스에서 의도적 SyntaxError/오타 실행을 요청한 경우.
    """
    raw = user_request or ""
    u = raw.lower()
    compact = u.replace(" ", "")
    if "syntaxerror" in compact:
        return True
    if "syntaxerror" in raw:
        return True
    if "일부러" in raw or "의도적" in raw:
        if any(k in raw for k in ("오타", "에러", "오류", "문법")):
            return True
        if "syntax" in u:
            return True
    if "고의" in raw and ("오류" in raw or "에러" in raw):
        return True
    return False


def is_explicit_python_coding_request(user_request: str, req_lower: str) -> bool:
    """파이썬으로 코드를 짜거나 실행·문법 실험을 하라는 뜻이 분명한 요청."""
    if not (user_request or "").strip():
        return False
    u = req_lower or user_request.lower()
    if "파이썬" in user_request or "python" in u:
        if any(
            x in user_request or x in u
            for x in ("코드", "짜", "작성", "실행", "돌려", "문법", "syntax", "프로그램", "스크립트", "더하기", "for ", "while ")
        ):
            return True
    if "syntaxerror" in u.replace(" ", "") or "syntax error" in u:
        return True
    if "코드" in user_request and any(
        k in user_request
        for k in (
            "실행해",
            "실행 해",
            "실행해봐",
            "실행해 봐",
            "실행해줘",
            "실행해 줘",
            "돌려",
            "돌려줘",
            "돌려봐",
            "돌려 봐",
        )
    ):
        return True
    exec_markers = ("돌려봐", "돌려 봐", "실행해봐", "실행해 봐", "실행해줘", "실행해 줘")
    if any(m in user_request for m in exec_markers):
        if any(s in u for s in ("print", "hello world", "syntax")):
            return True
        if any(s in user_request for s in ("오타", "SyntaxError", "syntaxerror", "문법", "일부러", "의도적")):
            return True
    return False


def skip_planner_debate_for_fast_path(user_request: str) -> bool:
    """매우 가벼운 코딩 요청은 planner_debate 생략 휴리스틱."""
    r = (user_request or "").strip()
    if not r or len(r) > 220:
        return False
    low = r.lower()
    trivial = (
        "간단한 파이썬",
        "간단 파이썬",
        "간단한 코드",
        "간단 코드",
        "짧은 코드",
        "짧은 파이썬",
        "예제 코드",
        "샘플 코드",
        "헬로 월드",
    )
    if any(t in r for t in trivial):
        return True
    if "hello world" in low:
        return True
    if len(r) < 52 and "파이썬" in r and any(k in r for k in ("구문", "코드", "만들", "짜", "작성")):
        return True
    return False


def classify_python_pipeline_tier(user_request: str, req_lower: str) -> Literal["example", "run", "complex"]:
    """파이썬/코딩 요청을 예제형 / 실행형 / 복잡형으로 나눔."""
    r = user_request or ""
    compact_syn = req_lower.replace(" ", "")

    complex_kw = (
        "크롤링",
        "스크래핑",
        "도구 만들",
        "도구를 만들",
        "자동화",
        "파일 읽",
        "파일 쓰",
        "파일을 읽",
        "파일에 쓰",
        "데이터베이스",
        "mysql",
        "postgres",
        "mongodb",
        "beautifulsoup",
        "playwright",
        "selenium",
        "스케줄 등록",
        "예약 등록",
        "파이프라인",
        "여러 단계",
        "멀티 스텝",
    )
    if any(k in r for k in complex_kw):
        return "complex"
    if "http://" in r or "https://" in r:
        return "complex"
    if "api" in req_lower and any(k in r for k in ("호출", "연동", "키", "토큰", "openapi")):
        return "complex"
    if "github.com" in req_lower or "gitlab" in req_lower:
        return "complex"

    run_kw = (
        "실행해",
        "실행 해",
        "실행해봐",
        "실행해 봐",
        "돌려",
        "돌려봐",
        "돌려 봐",
        "돌려줘",
        "결과 보여",
        "출력해 줘",
        "출력해줘",
        "출력 보여",
        "syntaxerror",
        "오타를",
        "오타 넣",
        "오타를 넣",
        "에러 나",
        "에러내",
        "에러 내",
        "고의",
        "일부러",
        "샌드박스",
        "테스트 실행",
        "실행 결과",
        "실행하고",
        "실행해서",
    )
    if "syntaxerror" in compact_syn:
        return "run"
    if any(k in r for k in run_kw):
        return "run"

    ex_kw = (
        "예제",
        "구문",
        "샘플",
        "보여줘",
        "보여 줘",
        "어떻게 쓰",
        "간단한 파이썬",
        "간단한 코드",
        "간단 파이썬",
        "기본 문법",
        "문법 예제",
        "for문",
        "if문",
        "리스트 컴프리헨션",
        "comprehension",
        "배우고 싶",
        "입문",
    )
    if any(k in r for k in ex_kw):
        return "example"
    if len(r) < 72 and ("짜줘" in r or "만들어줘" in r or "작성해" in r) and "실행" not in r and "돌려" not in r:
        return "example"
    if len(r) < 56 and "파이썬" in r and "실행" not in r and "돌려" not in r and "파일" not in r:
        return "example"
    return "complex"


def router_python_three_tier(user_request: str, req_lower: str) -> Optional[dict]:
    """파이썬·코딩 하드룰: 예제 → direct_answer, 실행 → code_run, 복잡 → planner."""
    followup_indicators = ("더 자세히", "자세히", "그게", "그거", "그것", "그게 무슨", "무슨 뜻", "설명해 줘", "알려 줘")
    explicit = is_explicit_python_coding_request(user_request, req_lower)
    coding_keywords = (
        "도구 만들어",
        "도구 만들",
        "코드 짜",
        "코드 작성",
        "크롤링",
        "스크래핑",
        "계산",
        "파이썬",
        "스크립트",
        "자동화",
        "분석 도구",
        "데이터 분석",
        "API 호출",
        "파일 읽",
        "파일 쓰",
        "컴프리헨션",
        "for문",
    )
    has_kw = any(kw in user_request for kw in coding_keywords)
    if not explicit and not has_kw:
        return None
    if not explicit and any(f in user_request for f in followup_indicators) and len(user_request) <= 50:
        return None

    tier = classify_python_pipeline_tier(user_request, req_lower)
    print(f"[DEBUG] Router: 파이썬/코딩 3단 분류 → {tier} (explicit={explicit}, has_kw={has_kw})")
    if tier == "example":
        return {"route_type": "direct_answer", "router_choice": "A", "python_example_direct": True}
    if tier == "run":
        return {
            "route_type": "code_run",
            "router_choice": "C",
            "approval_status": "approved",
            "plan": ["사용자 요청에 맞게 파이썬 코드를 작성하고 print 등으로 실행 결과를 출력한다."],
            "light_monitor": True,
            "skip_tool_save": True,
        }
    return {"route_type": "planner", "router_choice": "C"}


def _is_followup_vague_query(user_request: str) -> bool:
    """이전 대화 맥락을 참조하는 후속/모호한 질의 (Tavily 부적합, RAG 적합)."""
    u = (user_request or "").strip()
    if len(u) > 60:
        return False
    vague = ("그거", "그게", "그것", "그건", "이거", "저거", "이게", "저게", "더 자세히", "자세히", "아까 그", "방금 그")
    return any(v in u for v in vague)


def is_factual_lookup(user_request: str) -> bool:
    """사실 조회 질문 (Tavily 적합). 후속/맥락 참조 질의는 제외."""
    r = (user_request or "").lower().strip()
    if len(r) < 5:
        return False
    if _is_followup_vague_query(user_request):
        return False
    if any(k in r for k in ("도구", "스케줄", "예약", "job", "chromadb", "논문 목록")):
        return False
    patterns = ("알고 있어", "알아?", "뭐야?", "뭐야 ", "설명해", "알려줘", "알려 줘")
    return any(p in r for p in patterns)


def _agent_tool_py_exists(agent_tools_dir: Path, stem: str) -> bool:
    """루트 또는 saved/ 아래에 <stem>.py 가 있는지 (langchain 없이 순수 Path)."""
    d = agent_tools_dir
    if (d / f"{stem}.py").is_file():
        return True
    return (d / "saved" / f"{stem}.py").is_file()


def resolve_recent_tool_from_snapshot(recent: list, user_request: str) -> Optional[str]:
    """_recent_tools 스냅샷으로 '아까 그 도구' 참조 해석 (락 없음)."""
    if not recent:
        return None

    req = user_request.lower()
    if any(k in req for k in ("성경", "bible", "genesis", "john")):
        for item in recent:
            if item.get("tag") == "bible":
                return item.get("tool_name")
    if any(k in req for k in ("환율", "달러", "usd", "krw")):
        for item in recent:
            if item.get("tag") == "exchange_rate":
                return item.get("tool_name")
    if any(k in req for k in ("주가", "삼성전자", "stock")):
        for item in recent:
            if item.get("tag") == "stock_price":
                return item.get("tool_name")
    if any(k in req for k in ("비트코인", "이더리움", "btc", "eth", "코인")):
        for item in recent:
            if item.get("tag") == "coin_price":
                return item.get("tool_name")
    weather_lookup_verbs = ("알려줘", "보여줘", "조회", "확인", "가져와", "예보", "몇 도", "온도")
    weather_smalltalk = ("날씨 좋네", "날씨 좋다", "오늘 날씨 좋네", "오늘 날씨 좋다", "기분", "좋네", "좋다")
    if any(k in req for k in ("날씨", "부산", "제주", "서울")) and any(v in user_request for v in weather_lookup_verbs) and not any(x in user_request for x in weather_smalltalk):
        for item in recent:
            if item.get("tag") == "weather":
                return item.get("tool_name")

    if any(k in user_request for k in ("아까 만든", "방금 만든", "그 도구", "그 툴", "그걸로", "그거로")):
        return recent[0].get("tool_name")
    return None


def _req_lower_for_ascii_greeting_scan(req_lower: str) -> str:
    """URL 경로 속 hello/hi 등이 인사로 오인되지 않게 URL 구간을 제거."""
    return re.sub(r"https?://\S+", " ", req_lower, flags=re.IGNORECASE)


def _ascii_greeting_in_smalltalk(req_lower: str) -> bool:
    """영문 인사(hi/hello)만 단어 경계·따옴표 밖에서 매칭.

    `len('hello')` 처럼 문자열 리터럴 안의 hello, `this` 속의 hi 오분류를 줄입니다.
    http(s) URL 안의 토큰은 스캔에서 제외합니다.
    """
    scan = _req_lower_for_ascii_greeting_scan(req_lower)
    if re.search(r"(?<![\w'])\bhi\b(?![\w'])", scan):
        return True
    if re.search(r"(?<![\w'])\bhello\b(?![\w'])", scan):
        return True
    return False


def is_smalltalk_or_memory_request(user_request: str, req_lower: str) -> bool:
    """A 경로 전용 하드룰: 일상 대화, 짧은 메모리 질의, 간단 산수."""
    # "print hello world 돌려봐" 등에서 hello만 보고 인사로 오분류하지 않음
    if ("hello world" in req_lower or "헬로 월드" in user_request) and any(
        k in user_request or k in req_lower for k in ("print", "돌려", "실행")
    ):
        return False
    greetings = ("안녕", "헬로", "반가", "굿모닝", "굿나잇", "하이", "좋은 아침")
    # "윤수르"는 호칭(윤수르, …)에 항상 들어가 오분류되므로 제외. "윤수르 누구야" 등은 다른 키워드로 잡힘.
    identity_q = ("누구야", "누구니", "누구세요", "자기소개", "정체", "이름이 뭐야", "뭐하는")
    thanks_farewell = ("고마워", "수고했어", "잘 자", "내일 보자", "좋은 밤", "안녕히")
    comfort = ("위로", "힘들어", "피곤", "지쳤어", "격려", "응원", "배고프", "출출", "졸려", "졸리", "심심해", "심심하")
    memory_q = ("아까", "방금", "기억", "말했었지", "말했지", "좋아하는 분야", "기억해 둬")
    capability = ("할 줄 아는 게 뭐야", "할 수 있어", "어디 서버", "기분이 어때", "기분은 어때", "너의 기분은 어때", "기분이 어떠니", "기분은 어떠니", "기분이 어떠냐고")
    memory_blockers = ("도구", "성경", "창세기", "요한복음", "환율", "가격", "주가", "날씨", "논문", "api", "비트코인", "이더리움")
    weather_smalltalk_markers = ("날씨 좋네", "날씨 좋다", "오늘 날씨 좋네", "오늘 날씨 좋다", "덥네", "춥네", "비 오네", "날씨가 좋네")
    weather_query_markers = ("알려줘", "어때", "조회", "확인", "가져와", "예보", "몇 도", "온도", "미세먼지")

    if _ascii_greeting_in_smalltalk(req_lower):
        return True
    if any(x in req_lower for x in greetings):
        return True
    if any(x in user_request for x in identity_q):
        return True
    if any(x in user_request for x in thanks_farewell):
        return True
    if any(x in user_request for x in comfort):
        return True
    if any(x in user_request for x in memory_q) and not any(b in req_lower for b in memory_blockers):
        return True
    if any(x in user_request for x in capability):
        return True
    if re.search(r"(너|넌|너는).*(어때|어떠니|어떠냐)", user_request):
        return True
    if "날씨" in user_request and any(x in user_request for x in weather_smalltalk_markers) and not any(x in user_request for x in weather_query_markers):
        return True

    if re.search(r"\d+\s*(더하기|\+)\s*\d+", user_request):
        return True
    return False


def get_search_intent(user_request: str, req_lower: str) -> Literal["web", "rag", "tool", "none"]:
    """검색 의도 분류."""
    rag_blockers = ("논문", "chromadb", "chroma", "paper")
    if any(b in req_lower for b in rag_blockers):
        return "rag"
    if "저장된" in req_lower and any(b in req_lower for b in ("논문", "paper")):
        return "rag"

    tool_blockers = ("도구 목록", "저장된 도구", "등록된 스케줄", "스케줄 목록", "예약 목록")
    if any(b in req_lower for b in tool_blockers):
        return "tool"
    if re.search(r"JOB-[A-Z0-9]+", user_request, re.I):
        return "tool"
    if ("스케줄" in req_lower or "job" in req_lower) and any(w in req_lower for w in ("검색", "보여", "조회", "리스트")):
        return "tool"
    if "목록" in req_lower and any(w in req_lower for w in ("검색", "보여", "조회", "리스트")):
        if any(b in req_lower for b in ("도구", "스케줄", "예약", "job")):
            return "tool"

    web_trigger_combos = (
        ("뉴스", "알려"),
        ("뉴스", "찾아"),
        ("뉴스", "요약"),
        ("뉴스", "검색"),
        ("웹", "검색"),
        ("인터넷", "검색"),
        ("인터넷", "찾아"),
        ("최신", "뉴스"),
        ("오늘", "뉴스"),
        ("실시간", "정보"),
        "뉴스 검색",
        "뉴스 요약",
        "IT 뉴스",
        "오늘 뉴스",
        "웹 검색",
        "인터넷 검색",
    )
    for combo in web_trigger_combos:
        if isinstance(combo, str):
            if combo in user_request:
                return "web"
        elif combo[0] in user_request and combo[1] in user_request:
            return "web"

    return "none"


def match_whitelisted_tool(user_request: str, req_lower: str, agent_tools_dir: Path) -> Optional[str]:
    """B 경로 화이트리스트: 목적이 명확히 일치하는 도구만 반환."""
    has_url = bool(re.search(r"https?://\S+", user_request))

    form_write_keywords = ("입력해", "기입해", "입력해 줘", "기입해 줘", "기입해 봐", "입력해 봐", "써 봐", "넣어")
    if has_url and any(kw in user_request for kw in form_write_keywords):
        tool = agent_tools_dir / "fill_google_form.py"
        if tool.exists():
            return "fill_google_form"

    form_read_keywords = ("구글 폼", "google form", "폼 내용", "폼 확인", "뭐 있어", "확인해 줘")
    if has_url and any(kw in req_lower for kw in form_read_keywords):
        tool = agent_tools_dir / "google_form_reader.py"
        if tool.exists():
            return "google_form_reader"

    if re.search(r"JOB-[A-Z0-9]+", user_request, re.I) and any(
        kw in user_request for kw in ("자세히", "보여", "상세", "조회", "알려")
    ):
        tool = agent_tools_dir / "schedule_show_job.py"
        if tool.exists():
            return "schedule_show_job"

    _sched_cmd = (user_request or "").strip()
    if re.match(r"(?i)^(?:delete|삭제)\s+JOB-[A-Z0-9]+\s*$", _sched_cmd):
        tool = agent_tools_dir / "schedule_delete_job.py"
        if tool.exists():
            return "schedule_delete_job"
    if re.match(r"(?i)^edit\s+JOB-[A-Z0-9]+\s+time\s+\d{1,2}:\d{2}\s*$", _sched_cmd):
        tool = agent_tools_dir / "schedule_edit_job.py"
        if tool.exists():
            return "schedule_edit_job"
    if re.match(r"(?i)^edit\s+JOB-[A-Z0-9]+\s+prompt\s+.+", _sched_cmd, re.DOTALL):
        tool = agent_tools_dir / "schedule_edit_job.py"
        if tool.exists():
            return "schedule_edit_job"

    tool_list_trigger = ("저장된 도구", "기존 도구", "등록된 도구", "agent_tools")
    tool_list_action = ("목록", "알려", "보여", "검색", "조회", "뭐 있어")
    if any(t in req_lower for t in tool_list_trigger) and any(a in req_lower for a in tool_list_action):
        tool = agent_tools_dir / "agent_tools_list.py"
        if tool.exists():
            return "agent_tools_list"

    schedule_list_keywords = ("스케줄 목록", "등록된 스케줄", "예약 목록", "스케줄 보여", "스케줄 조회", "스케줄 리스트", "스케줄 알려")
    if any(kw in req_lower for kw in schedule_list_keywords):
        tool = agent_tools_dir / "schedule_list_jobs.py"
        if tool.exists():
            return "schedule_list_jobs"

    if any(kw in user_request for kw in ("매일", "매주", "매월", "정기적으로", "예약", "알람", "리마인더")):
        tool = agent_tools_dir / "schedule_add_job.py"
        if tool.exists():
            return "schedule_add_job"

    # 주제 검색(찾아/검색 등)은 RAG — '목록+알려줘'만으로 인벤토리 화이트리스트에 걸리지 않게 함.
    _paper_topic_search = any(w in req_lower for w in ("검색", "요약", "설명", "찾아"))
    if (
        not _paper_topic_search
        and ("chromadb" in req_lower or "논문" in user_request or "db에" in req_lower or "db 목록" in req_lower)
        and any(w in req_lower for w in ("목록", "뭐 있어", "뭐있어", "조회", "알려줘", "보여"))
    ):
        tool = agent_tools_dir / "chromadb_db_inventory.py"
        if tool.exists():
            return "chromadb_db_inventory"

    search_intent = get_search_intent(user_request, req_lower)
    if search_intent == "web":
        tool = agent_tools_dir / "tavily_search_tool.py"
        if tool.exists():
            return "tavily_search_tool"

    weather_tool = agent_tools_dir / "서울_지금_현재_날씨_알려줘.py"
    if weather_tool.exists():
        if "서울" in user_request and "날씨" in user_request and "미세먼지" not in user_request:
            return "서울_지금_현재_날씨_알려줘"

    smart_plug_tool = agent_tools_dir / "smart_plug.py"
    if smart_plug_tool.exists():
        has_on = bool(re.search(r"켜|turn\s*on|power\s*on", req_lower))
        has_off = bool(re.search(r"꺼|끄|turn\s*off|power\s*off", req_lower))
        plug_ctx = (
            "플러그" in user_request
            or "스마트플러그" in req_lower.replace(" ", "")
            or "스마트 플러그" in user_request
            or "스탠드 불" in user_request
            or "스탠드조명" in req_lower.replace(" ", "")
            or "스탠드 조명" in user_request
            or ("스탠드" in user_request and "불" in user_request)
            or ("스탠드" in user_request and (has_on or has_off))
            or "tuya" in req_lower
            or "tinytuya" in req_lower
            or "아울렛" in user_request
            or ("스탠드" in user_request and ("조명" in user_request or "전원" in user_request))
        )
        if plug_ctx and (has_on or has_off):
            return "smart_plug"

    return None


def router_step1_hard_rules(
    user_request: str,
    req_lower: str,
    chat_id: str,
    deps: RouterStep1Deps,
) -> Optional[dict]:
    """1단계: 명백한 하드룰. 매칭 시 즉시 반환, None이면 2단계로."""
    d = deps.agent_tools_dir
    has_url = bool(re.search(r"https?://\S+", user_request))

    if is_smalltalk_or_memory_request(user_request, req_lower):
        return {"route_type": "direct_answer", "router_choice": "A"}
    whitelisted_tool = match_whitelisted_tool(user_request, req_lower, d)
    if whitelisted_tool:
        out = {"route_type": "use_existing_tool", "router_choice": "B", "used_tool_name": whitelisted_tool}
        if whitelisted_tool == "tavily_search_tool":
            out["search_intent"] = "web"
        return out
    if (
        not deps.get_paper_mode(chat_id)
        and is_factual_lookup(user_request)
        and get_search_intent(user_request, req_lower) != "rag"
        and (d / "tavily_search_tool.py").exists()
    ):
        return {"route_type": "use_existing_tool", "router_choice": "B", "used_tool_name": "tavily_search_tool"}
    recent_tool = deps.resolve_recent_tool(chat_id, user_request)
    if recent_tool and _agent_tool_py_exists(d, recent_tool):
        si = get_search_intent(user_request, req_lower)
        if recent_tool != "tavily_search_tool" or si not in ("rag", "tool"):
            return {"route_type": "use_existing_tool", "router_choice": "B", "used_tool_name": recent_tool}
    if has_url:
        return {"route_type": "planner", "router_choice": "C"}
    text_creation_markers = (
        "문자 메시지",
        "문자 메세지",
        "문자 ",
        "SMS",
        "초안 작성",
        "이메일 ",
        "이메일 작성",
        "메일 ",
        "인사말",
        "인사말 추천",
        "번역해 줘",
        "번역해줘",
        "글쓰기",
        "글 짜",
        "내용 만들어",
        "메시지 만들어",
        "메시지 내용",
        "메세지 만들어",
        "메세지 내용",
        "초안 만들어",
        "작성해 줘",
        "써 줘",
        "써줘",
    )
    if any(m in user_request for m in text_creation_markers):
        return {"route_type": "direct_answer", "router_choice": "A"}
    text_targets = ("문자", "이메일", "메일", "인사말", "글", "초안", "내용", "메시지")
    if ("만들어" in user_request or "써" in user_request or "작성" in user_request) and any(t in user_request for t in text_targets):
        if not any(c in user_request for c in ("코드", "크롤링", "스크래핑", "API", "파이썬", "스크립트", "도구")):
            return {"route_type": "direct_answer", "router_choice": "A"}
    action_keywords = (
        "도구를 만들어 줘",
        "도구 만들어 줘",
        "코드를 짜 줘",
        "코드 짜 줘",
        "코드 짜줘",
        "코드 짜달라",
        "크롤링해 줘",
        "크롤링 해 줘",
        "크롤링해달라",
        "스크래핑해 줘",
        "코드 작성해 줘",
        "스크립트 만들어 줘",
        "자동화해 줘",
    )
    if any(kw in user_request for kw in action_keywords):
        py_route = router_python_three_tier(user_request, req_lower)
        if py_route is not None:
            return py_route
        return {"route_type": "planner", "router_choice": "C"}
    existing_tool_keywords = ("기존 도구", "저장된 도구", "agent_tools", "이미 있는 도구", "만들어진 도구")
    if any(kw in user_request for kw in existing_tool_keywords) or ("도구" in user_request and "사용" in user_request):
        if any(kw in user_request for kw in existing_tool_keywords) and any(
            a in req_lower for a in ("목록", "검색", "조회", "보여", "알려", "뭐 있어", "뭐있어")
        ):
            if (d / "agent_tools_list.py").exists():
                return {"route_type": "use_existing_tool", "router_choice": "B", "used_tool_name": "agent_tools_list"}
        return {"route_type": "use_existing_tool", "router_choice": "B"}
    schedule_keywords = ("매일", "매주", "매월", "정기적으로", "스케줄", "예약", "알람", "리마인더")
    if any(kw in user_request for kw in schedule_keywords) and (d / "schedule_add_job.py").exists():
        return {"route_type": "use_existing_tool", "router_choice": "B", "used_tool_name": "schedule_add_job"}
    # 주제·조건이 있는 논문 찾기/검색은 RAG(B) — '목록으로 알려줘'만 있는 문장이 인벤토리보다 먼저 걸리지 않게 순서 우선.
    if ("chromadb" in req_lower or "논문" in user_request) and any(w in req_lower for w in ("검색", "요약", "설명", "찾아")):
        return {"route_type": "direct_answer", "router_choice": "B"}
    paper_list_actions = ("목록", "알려줘", "뭐 있어", "뭐있어", "조회", "보여")
    if ("chromadb" in req_lower or "논문" in user_request) and any(w in req_lower for w in paper_list_actions):
        tool = d / "chromadb_db_inventory.py"
        if tool.exists():
            return {"route_type": "use_existing_tool", "router_choice": "B", "used_tool_name": "chromadb_db_inventory"}
        return {"route_type": "direct_answer", "router_choice": "B"}
    if _is_followup_vague_query(user_request):
        return {"route_type": "direct_answer", "router_choice": "B"}
    knowledge_verbs = ("요약해 줘", "설명해 줘", "알려 줘", "번역해 줘", "자세히 설명", "요약해줘", "설명해줘", "알려줘")
    code_blockers = ("코드", "크롤링", "스크래핑", "API", "파이썬", "스크립트", "짜줘", "만들어 줘")
    if any(k in user_request for k in knowledge_verbs) and not any(c in user_request for c in code_blockers):
        return {"route_type": "direct_answer", "router_choice": "B"}
    py_route = router_python_three_tier(user_request, req_lower)
    if py_route is not None:
        return py_route
    return None


def router_step2_build_features(user_request: str, req_lower: str) -> dict:
    """2단계: LLM 분류용 feature dict."""
    has_url = bool(re.search(r"https?://\S+", user_request))
    return {
        "has_url": has_url,
        "has_text_creation": any(m in user_request for m in ("문자", "이메일", "번역", "인사말", "글쓰기", "초안")),
        "has_coding_keywords": any(k in user_request for k in ("코드", "크롤링", "스크래핑", "API", "파이썬", "스크립트")),
        "len": len(user_request),
    }
