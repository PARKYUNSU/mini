import requests
from bs4 import BeautifulSoup
import sys

def get_hacker_news_titles():
    """
    Hacker News 메인 페이지에서 1위부터 5위까지 글 제목을 추출하여 반환합니다.
    """
    url = "https://news.ycombinator.com/"
    titles = []

    try:
        # 1단계: 다음 URL의 정적 HTML을 requests+BeautifulSoup으로 파싱
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        soup = BeautifulSoup(response.text, 'html.parser')

        # 2단계: 파싱된 HTML에서 1위부터 5위까지 글 제목을 추출합니다.
        # 'titlelink' 클래스를 가진 모든 <a> 태그를 찾습니다.
        title_elements = soup.find_all('a', class_='titlelink')

        # 상위 5개 제목만 추출
        for i, title_element in enumerate(title_elements):
            if i < 5:
                titles.append(title_element.get_text())
            else:
                break

        # 3단계: 추출한 글 제목들을 리스트로 반환합니다.
        return titles

    except requests.exceptions.RequestException as e:
        print(f"웹 요청 중 오류 발생: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"데이터 파싱 중 오류 발생: {e}", file=sys.stderr)
        return []

if __name__ == "__main__":
    # 5단계: 함수 호출
    hacker_news_top_titles = get_hacker_news_titles()
    print(hacker_news_top_titles)