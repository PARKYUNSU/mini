import requests
from bs4 import BeautifulSoup
import sys

def get_website_title(url: str):
    """
    주어진 URL의 웹사이트에서 HTML title 태그를 추출하여 반환합니다.
    """
    try:
        # 3단계: 웹사이트의 HTML을 가져옵니다.
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

        # 4단계: BeautifulSoup을 사용해 HTML을 파싱하고, title 태그를 추출합니다.
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')

        # 5단계: 추출된 title 태그를 출력하거나 다른 작업에 사용합니다.
        if title_tag:
            print(f"'{url}'의 HTML Title: {title_tag.text.strip()}")
        else:
            print(f"'{url}'에서 title 태그를 찾을 수 없습니다.")

    except requests.exceptions.RequestException as e:
        print(f"웹사이트에 접속하는 중 오류가 발생했습니다: {e}", file=sys.stderr)
    except Exception as e:
        print(f"HTML 파싱 중 오류가 발생했습니다: {e}", file=sys.stderr)

if __name__ == "__main__":
    # 1단계: `example.com` 웹사이트의 HTML title 태그만 긁어오기 위한 크롤러를 만듭니다.
    # 3단계: `example.com` 웹사이트의 HTML을 가져옵니다.
    target_url = "http://example.com"
    get_website_title(target_url)