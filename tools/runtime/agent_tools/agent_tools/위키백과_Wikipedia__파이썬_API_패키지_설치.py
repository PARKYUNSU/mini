import subprocess
import sys
import os

# 1단계: `wikipedia-api` 패키지를 설치합니다.
def ensure_package_installed(package_name):
    """
    Checks if a package is installed and installs it if not.
    """
    try:
        __import__(package_name)
    except ImportError:
        print(f"Package '{package_name}' not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"Package '{package_name}' installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing package '{package_name}': {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred during installation: {e}")
            sys.exit(1)

ensure_package_installed("wikipedia-api")

import wikipediaapi

def get_wikipedia_first_paragraph(page_title: str, lang: str = 'ko', user_agent: str = "MyWikipediaApp/1.0 (https://example.com/my-app)") -> str:
    """
    Wikipedia에서 특정 문서의 첫 문단을 가져옵니다.

    Args:
        page_title (str): 가져올 위키백과 문서의 제목.
        lang (str): 위키백과 언어 코드 (기본값: 'ko' 한국어).
        user_agent (str): 위키백과 API 요청 시 사용할 사용자 에이전트 문자열.
                          (예: "MyAwesomeApp/1.0 (contact@example.com)")

    Returns:
        str: 문서의 첫 문단 또는 오류 메시지.
    """
    try:
        # 이전 실행 에러: `user_agent` 인자 누락 수정
        wiki_wiki = wikipediaapi.Wikipedia(language=lang, user_agent=user_agent)
        page_py = wiki_wiki.page(page_title)

        if page_py.exists():
            # 2단계: `wikipedia-api` 패키지의 도움으로 '인공지능' 문서의 첫 문단을 가져옵니다.
            # wikipedia-api의 summary는 일반적으로 문서의 첫 문단에 해당하는 내용을 반환합니다.
            first_paragraph = page_py.summary
            return first_paragraph
        else:
            return f"'{page_title}' 문서를 찾을 수 없습니다."
    except Exception as e:
        return f"위키백과 문서를 가져오는 중 오류 발생: {e}"

if __name__ == "__main__":
    search_term = "인공지능"
    # 사용자 에이전트 설정 (환경 변수에서 가져오거나 기본값 사용)
    # 실제 사용 시에는 본인의 애플리케이션 이름과 연락처 정보를 포함하는 것이 좋습니다.
    my_user_agent = os.getenv("WIKIPEDIA_USER_AGENT", "MyWikipediaApp/1.0 (https://example.com/my-app)")

    result = get_wikipedia_first_paragraph(search_term, user_agent=my_user_agent)
    # 3단계: 가져온 첫 문단을 출력합니다.
    print(result)