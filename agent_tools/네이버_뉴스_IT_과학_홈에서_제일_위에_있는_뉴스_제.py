import requests
from bs4 import BeautifulSoup
import sys

def get_naver_it_science_news_titles(num_titles: int = 3):
    """
    네이버 뉴스 IT/과학 홈에서 제일 위에 있는 뉴스 제목을 추출하여 반환합니다.

    Args:
        num_titles (int): 추출할 뉴스 제목의 개수. 기본값은 3입니다.

    Returns:
        list: 추출된 뉴스 제목 문자열 리스트.
    """
    # 1단계: 네이버 뉴스 IT/과학 홈의 URL을 정의합니다.
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105"
    news_titles = []

    try:
        # 2단계: requests와 BeautifulSoup 모듈을 이용해 해당 URL의 HTML을 가져옵니다.
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3단계: BeautifulSoup을 통해 제일 위에 있는 뉴스 제목을 추출합니다.
        # 'cluster_text_headline' 클래스를 가진 <a> 태그를 찾아 뉴스 제목을 추출합니다.
        # 이 클래스는 주요 뉴스 기사의 제목을 포함하는 것으로 확인됩니다.
        headlines = soup.find_all('a', class_='cluster_text_headline')

        for i, headline in enumerate(headlines):
            if i >= num_titles:
                break
            title = headline.get_text(strip=True)
            news_titles.append(title)

    except requests.exceptions.RequestException as e:
        print(f"웹 페이지를 가져오는 중 오류 발생: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"뉴스 제목을 파싱하는 중 오류 발생: {e}", file=sys.stderr)
        return []

    return news_titles

if __name__ == "__main__":
    try:
        # 4단계: 추출된 뉴스 제목들을 출력합니다.
        top_news = get_naver_it_science_news_titles(num_titles=3)

        if top_news:
            print("네이버 뉴스 IT/과학 상위 3개 뉴스 제목:")
            for i, title in enumerate(top_news):
                print(f"{i+1}. {title}")
            # 5단계: 출력할 뉴스 제목이 정확한지 확인합니다. (코드 실행 후 수동 확인)
        else:
            print("뉴스 제목을 가져오지 못했습니다.")
    except Exception as e:
        print(f"스크립트 실행 중 오류 발생: {e}", file=sys.stderr)