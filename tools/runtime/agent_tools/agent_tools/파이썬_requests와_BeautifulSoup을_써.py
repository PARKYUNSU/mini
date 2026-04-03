import subprocess
import sys
import requests
from bs4 import BeautifulSoup

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

try:
    # 1단계: `requests`와 `BeautifulSoup` 패키지를 사용하여 'Hacker News' 메인 페이지에 접속합니다.
    ensure_package_installed("requests")
    ensure_package_installed("bs4") # BeautifulSoup은 'bs4' 패키지에 포함되어 있습니다.

    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    response.raise_for_status() # HTTP 오류가 발생하면 예외를 발생시킵니다.

    # 2단계: BeautifulSoup을 이용해 HTML 문서에서 최신 글 제목 5개를 추출합니다.
    soup = BeautifulSoup(response.text, 'html.parser')

    # Hacker News의 글 제목은 일반적으로 'titleline' 클래스를 가진 span 태그 안에 있는 a 태그에 있습니다.
    # 모든 'titleline' 클래스를 가진 span 태그를 찾습니다.
    title_spans = soup.find_all('span', class_='titleline')

    print("Hacker News 최신 글 제목 (상위 5개):")
    # 3단계: 추출된 제목에 번호표를 붙여 출력합니다.
    for i, title_span in enumerate(title_spans[:5]): # 상위 5개만 처리
        # 각 title_span 안에서 첫 번째 'a' 태그를 찾습니다.
        link_tag = title_span.find('a')
        if link_tag:
            print(f"{i+1}. {link_tag.get_text()}")
        else:
            print(f"{i+1}. (제목을 찾을 수 없음)")

except requests.exceptions.RequestException as e:
    print(f"네트워크 요청 중 오류가 발생했습니다: {e}")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")