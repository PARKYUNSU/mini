import requests
from bs4 import BeautifulSoup
import sys

def get_krw_usd_exchange_rate():
    """
    Google Finance 웹페이지에서 원/달러 환율 정보를 크롤링하여 반환합니다.
    [치명적 경고 - 샌드박스 제약]에 따라 playwright 대신 requests와 BeautifulSoup을 사용합니다.
    """
    # 2단계: 다음 URL의 정적 HTML을 requests+BeautifulSoup으로 파싱합니다.
    # 참고: 실행 계획에 명시된 'https://www.google.com/finance' URL은 원/달러 환율 정보를
    # 직접적으로 포함하지 않으므로, 해당 정보를 명확하게 제공하는 특정 환율 페이지 URL을 사용합니다.
    # 이는 '원/달러 환율 정보를 추출합니다'라는 실행 계획 3단계의 목표를 달성하기 위함입니다.
    url = "https://www.google.com/finance/quote/USD-KRW?hl=en"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

        soup = BeautifulSoup(response.text, 'html.parser')

        # 3단계: 파싱된 HTML에서 원/달러 환율 정보를 추출합니다.
        # Google Finance 페이지 구조에 따라 환율 정보가 담긴 요소를 찾습니다.
        # 현재는 'YMlKec fxKbKc' 클래스를 가진 div 태그에 환율 정보가 있습니다.
        exchange_rate_element = soup.find('div', class_='YMlKec fxKbKc')

        if exchange_rate_element:
            exchange_rate = exchange_rate_element.get_text(strip=True)
            # 4단계: 추출한 환율 정보를 문자열로 반환합니다.
            return f"현재 원/달러 환율 (USD to KRW): {exchange_rate} KRW"
        else:
            return "원/달러 환율 정보를 찾을 수 없습니다."

    except requests.exceptions.RequestException as e:
        return f"웹페이지에 접근하는 중 오류가 발생했습니다: {e}"
    except Exception as e:
        return f"환율 정보를 파싱하는 중 오류가 발생했습니다: {e}"

# 6단계: 함수 테스트:
# 7단계: 함수가 제대로 작동하는지 확인합니다.
if __name__ == "__main__":
    result = get_krw_usd_exchange_rate()
    print(result)