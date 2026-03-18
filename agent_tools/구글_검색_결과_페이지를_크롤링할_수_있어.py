import requests
from bs4 import BeautifulSoup
import sys
import urllib.parse

def get_website_title(url: str):
    """
    주어진 URL의 웹사이트에서 HTML title 태그를 추출하여 반환합니다.
    """
    try:
        # 웹사이트의 HTML을 가져옵니다.
        # Google은 봇 접근을 차단할 수 있으므로 User-Agent를 설정합니다.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생

        # BeautifulSoup으로 HTML을 파싱합니다.
        soup = BeautifulSoup(response.text, 'html.parser')

        # title 태그를 찾아서 텍스트를 추출합니다.
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        else:
            return "Title tag not found."
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL {url}: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python your_script_name.py <search_query>")
        sys.exit(1)

    search_query = sys.argv[1]
    encoded_query = urllib.parse.quote_plus(search_query)
    google_search_url = f"https://www.google.com/search?q={encoded_query}"

    try:
        title = get_website_title(google_search_url)
        print(f"Google Search Result Page Title for '{search_query}': {title}")
    except Exception as e:
        print(f"An error occurred: {e}")