import requests
from bs4 import BeautifulSoup
import os
import sys

def get_latest_lotto_numbers():
    """
    동행복권 웹사이트에서 최신 로또 당첨 번호를 크롤링하여 반환합니다.
    [치명적 경고 - 샌드박스 제약]에 따라 requests와 BeautifulSoup을 사용합니다.
    """
    # 1단계: 로또 당첨 번호를 제공하는 웹사이트의 URL
    # 최신 회차 결과를 제공하는 HTML 페이지 URL
    LOTTO_URL = "https://www.dhlottery.co.kr/gameResult.do?method=byWin"

    # 2단계: .env 파일에서 LOTTO_API_KEY를 가져옵니다.
    # 이 웹사이트는 API 키를 직접 사용하지 않지만, 지시사항에 따라 포함합니다.
    lotto_api_key = os.getenv("LOTTO_API_KEY")
    if lotto_api_key:
        # 실제 사용되지 않더라도, 지시사항 준수를 위해 변수에 할당합니다.
        pass 

    try:
        # 3단계: 제공된 URL에서 로또 당첨 번호 정보를 크롤링합니다.
        response = requests.get(LOTTO_URL)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 4단계: 크롤링한 데이터 중 로또 당첨 번호를 추출합니다.
        # 회차 정보 추출
        drw_no_element = soup.find('h4', class_='tit_result')
        drw_no_text = drw_no_element.find('strong').get_text(strip=True) if drw_no_element else "회차 정보 없음"

        # 당첨 번호 추출
        win_numbers_div = soup.find('div', class_='num win')
        winning_numbers = []
        if win_numbers_div:
            for span in win_numbers_div.find_all('span', class_='ball_645'):
                winning_numbers.append(span.get_text(strip=True))
        else:
            winning_numbers = ["당첨 번호 없음"]

        # 보너스 번호 추출
        bonus_number_div = soup.find('div', class_='num bonus')
        bonus_number = ""
        if bonus_number_div:
            bonus_span = bonus_number_div.find('span', class_='ball_645')
            if bonus_span:
                bonus_number = bonus_span.get_text(strip=True)
            else:
                bonus_number = "보너스 번호 없음"
        else:
            bonus_number = "보너스 번호 없음"

        # 5단계: 추출된 로또 당첨 번호를 사용자에게 제공합니다.
        print(f"[{drw_no_text}] 로또 당첨 결과:")
        print(f"당첨 번호: {', '.join(winning_numbers)}")
        print(f"보너스 번호: {bonus_number}")

    except requests.exceptions.RequestException as e:
        print(f"웹사이트에 접속하는 중 오류가 발생했습니다: {e}", file=sys.stderr)
    except AttributeError:
        print("필요한 정보를 찾을 수 없습니다. 웹사이트 구조가 변경되었을 수 있습니다.", file=sys.stderr)
    except Exception as e:
        print(f"데이터를 처리하는 중 예기치 않은 오류가 발생했습니다: {e}", file=sys.stderr)

if __name__ == "__main__":
    get_latest_lotto_numbers()