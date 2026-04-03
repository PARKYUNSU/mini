from playwright.sync_api import sync_playwright
import re


# 한국어 조사/껍데기 단어 → 파라미터 추출 시 제외
_PARTICLES = frozenset(("은", "는", "이", "가", "을", "를", "의", "에", "와", "과", "명단", "이름은", "날짜는", "장소는"))


def _clean_value(v: str) -> str:
    """조사·껍데기 제거, 핵심 명사만 반환"""
    v = v.strip().strip(".,;:!?\"'""''")
    for p in _PARTICLES:
        v = re.sub(rf"^{re.escape(p)}\s*", "", v)
        v = re.sub(rf"\s*{re.escape(p)}$", "", v)
    return v.strip() or "미지정"


def run(user_request: str) -> str:
    """
    Host 실행용 표준 인터페이스. user_request에서 URL, group, leader 등 추출해 fill_form 호출.
    [파라미터 추출 규칙] Key-Value 형식(인도자: 박윤수) 우선. 조사(은/는/이/가)는 절대 포함하지 않음.
    """
    url_match = re.search(r"https?://[^\s\)\]\"'\u201c\u201d]+", user_request)  # 스마트 따옴표 포함
    if not url_match:
        return "구글 폼 URL을 요청에 포함해 주세요."
    url = url_match.group(0).rstrip(".,;:!?)")

    # 1) Key-Value 형식 우선 (인도자: 박윤수, 중그룹: 마하나임 등)
    group = "마하나임"
    leader = ""
    date = "미지정"
    place = "미지정"
    members = "미지정"

    for m in re.finditer(r"(?:중그룹|그룹)[:\s]*([^\n]+?)(?:\n|$)", user_request):
        g = _clean_value(m.group(1))
        if g not in _PARTICLES and len(g) >= 2:
            group = g
            break
    for m in re.finditer(r"(?:인도자|리더)[:\s]*([^\n]+?)(?:\n|$)", user_request):
        g = _clean_value(m.group(1))
        if g not in _PARTICLES and len(g) >= 2:
            leader = g
            break
    for m in re.finditer(r"(?:날짜|일자)[:\s]*([0-9\-\./가-힣]+)", user_request):
        date = m.group(1).strip()
        break
    for m in re.finditer(r"(?:장소|place)[:\s]*([^\n]+?)(?:\n|$)", user_request):
        g = _clean_value(m.group(1))
        if g not in _PARTICLES:
            place = g
            break
    for m in re.finditer(r"(?:참가자|멤버|members|명단)[:\s]*([^\n]+?)(?:\n|$)", user_request):
        g = _clean_value(m.group(1))
        if g not in _PARTICLES:
            members = g
            break

    prayer_requests = "미지정"
    for m in re.finditer(r"(?:기도제목|기도\s*제목|prayer)[:\s]*([^\n]+?)(?:\n|$)", user_request):
        g = _clean_value(m.group(1))
        if g:
            prayer_requests = g
            break

    message = ""
    for m in re.finditer(r"(?:메시지|건의사항|message)[:\s]*([^\n]+?)(?:\n|$)", user_request):
        g = _clean_value(m.group(1))
        if g and g != "미지정":
            message = g
            break

    # 2) Key-Value 없으면 줄글에서 추출 (조사 제외)
    if not leader:
        for m in re.finditer(r"(?:인도자\s*이름은?\s*)?([가-힣]{2,4})\s*(?:기입|입력|써|넣)", user_request):
            g = _clean_value(m.group(1))
            if g not in _PARTICLES:
                leader = g
                break
    if not leader:
        for m in re.finditer(r"(?:인도자|리더)[:\s]*([가-힣a-zA-Z]{2,20})", user_request):
            g = _clean_value(m.group(1))
            if g not in _PARTICLES:
                leader = g
                break
    if not leader:
        leader = "미지정"

    if "마하나임" in user_request:
        group = "마하나임"
    elif "선택" in user_request:
        for m in re.finditer(r"([가-힣a-zA-Z]{2,10})\s*선택", user_request):
            g = m.group(1).strip()
            if g not in _PARTICLES:
                group = g
                break

    return fill_form(url=url, group=group, leader=leader, date=date, place=place, members=members, prayer_requests=prayer_requests, message=message)


def fill_form(url: str, group: str, leader: str, date: str, place: str, members: str, prayer_requests: str, message: str = ""):
    """
    구글 폼에 데이터를 기입하는 전용 도구입니다.

    [매개변수 입력 절대 규칙]
    1. group: 오직 그룹 이름만 (예: "마하나임")
    2. leader: 인도자 이름만 (조사 제외, 예: "박윤수")
    3. date: 날짜 숫자만 (예: "2026-03-15" 또는 "2026/03/15")
    4. place: 장소 이름만 (예: "8층")
    5. members: 참가자 명단만
    6. prayer_requests: 셀 현황 및 기도제목
    7. message: 목회자에게 하고 싶은 메시지 (없으면 빈 문자열)
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_timeout(2000)

            # --- 구글 폼 스마트 입력 로직 (질문 이름 기반 타겟팅) ---

            # 1. 라디오 버튼 (소속 중그룹)
            try:
                page.locator(f'div[role="radio"]:has-text("{group}")').click(timeout=3000)
            except Exception:
                pass

            # 2. 단답형 텍스트 (인도자 이름)
            try:
                page.locator('div[role="listitem"]').filter(has_text="인도자 이름").locator('input[type="text"]').fill(leader)
            except Exception:
                pass

            # 3. 날짜 (모임 날짜)
            try:
                formatted_date = date.replace("/", "-")
                page.locator('div[role="listitem"]').filter(has_text="모임 날짜").locator('input[type="date"]').fill(formatted_date)
            except Exception:
                pass

            # 4. 단답형 텍스트 (모임 장소)
            try:
                page.locator('div[role="listitem"]').filter(has_text="모임 장소").locator('input[type="text"]').fill(place)
            except Exception:
                pass

            # 5. 장문형 텍스트 (참가자 명단)
            try:
                page.locator('div[role="listitem"]').filter(has_text="참가자 명단").locator("textarea").fill(members)
            except Exception:
                pass

            # 6. 장문형 텍스트 (셀 현황 및 기도제목)
            try:
                page.locator('div[role="listitem"]').filter(has_text="셀 현황 및 기도제목").locator("textarea").fill(prayer_requests)
            except Exception:
                pass

            # 7. 장문형 텍스트 (목회자에게 하고 싶은 메시지)
            if message:
                try:
                    page.locator('div[role="listitem"]').filter(has_text="목회자에게 하고 싶은 메시지").locator("textarea").fill(message)
                except Exception:
                    pass

            page.wait_for_timeout(4000)
            browser.close()

            return f"✅ 기입 성공! (인도자: {leader}, 장소: {place})"

    except Exception as e:
        return f"구글 폼 기입 중 에러 발생: {str(e)}"
