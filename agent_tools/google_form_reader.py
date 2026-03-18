from playwright.sync_api import sync_playwright
import re


def run(user_request: str) -> str:
    """
    Host 실행용 표준 인터페이스. user_request에서 URL을 추출해 read_google_form 호출.
    """
    url_match = re.search(r"https?://[^\s\)\]\"']+", user_request)
    if not url_match:
        return "구글 폼 URL을 요청에 포함해 주세요. (예: https://docs.google.com/forms/...)"
    url = url_match.group(0).rstrip(".,;:!?)")
    return read_google_form(url)


def read_google_form(url: str):
    """
    이 도구는 Playwright를 사용하여 구글 폼(Google Forms) URL에 접속하고,
    화면에 렌더링된 실제 폼 제목과 질문(항목) 리스트를 텍스트로 긁어옵니다.
    사용자가 구글 폼 내용을 확인해 달라고 하면 무조건 이 도구를 사용하세요.
    """
    try:
        with sync_playwright() as p:
            # 샌드박스가 아닌 맥 미니 본체에서 브라우저를 띄움
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            # 페이지가 완전히 렌더링될 때까지 잠시 대기
            page.wait_for_timeout(2000)

            # 질문 항목들(role="heading") 긁어오기
            questions = page.locator('[role="heading"]').all_inner_texts()

            browser.close()

            # 쓸데없는 빈칸 제거하고 예쁘게 합치기
            clean_questions = [q for q in questions if q.strip()]
            return "구글 폼 내용 확인 성공:\n" + "\n".join(clean_questions)

    except Exception as e:
        return f"구글 폼 접근 중 에러 발생: {str(e)}"
