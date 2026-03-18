import requests
from bs4 import BeautifulSoup
import os
import sys

def get_krw_usd_exchange_rate():
    """
    Google Finance 웹페이지에서 원/달러 환율 정보를 크롤링하여 반환합니다.
    [치명적 경고 - 샌드박스 제약]에 따라 playwright 대신 requests와 BeautifulSoup을 사용합니다.
    """
    try:
        # 1단계 및 2단계: Playwright 기반 도구 검색 및 사용 불가 (샌드박스 제약)
        # 3단계: Playwright 대신 requests와 BeautifulSoup을 사용하여 구글 파이낸스 웹페이지 접속 및 환율 추출
        # KRW-USD 환율 정보를 제공하는 Google Finance 페이지 URL
        url = "https://www.google.com/finance/quote/KRW-USD"
        
        # 웹사이트에서 봇으로 인식되지 않도록 User-Agent 헤더를 추가합니다.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생

        soup = BeautifulSoup(response.text, 'html.parser')

        # Google Finance 페이지에서 환율 정보가 포함된 요소를 찾습니다.
        # 현재 Google Finance 페이지 구조에서 환율 값은 'YMlKec fxKbKc' 클래스를 가진 div 태그에 있습니다.
        exchange_rate_element = soup.find('div', class_='YMlKec fxKbKc')
        
        if exchange_rate_element:
            exchange_rate_str = exchange_rate_element.text.strip()
            # 쉼표 제거 및 float으로 변환
            exchange_rate = float(exchange_rate_str.replace(',', ''))
            return exchange_rate
        else:
            print("오류: 환율 정보를 찾을 수 없습니다. 웹페이지 구조가 변경되었을 수 있습니다.", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"네트워크 또는 HTTP 요청 오류 발생: {e}", file=sys.stderr)
        return None
    except ValueError as e:
        print(f"환율 값 파싱 오류 발생: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"예기치 않은 오류 발생: {e}", file=sys.stderr)
        return None

if __name__ == '__main__':
    try:
        krw_usd_rate = get_krw_usd_exchange_rate()

        # 4단계: 추출한 환율 정보를 처리하여 사용자에게 제공합니다.
        if krw_usd_rate is not None:
            print(f"현재 구글 파이낸스 원/달러 환율: 1 USD = {krw_usd_rate:.2f} KRW")
        else:
            print("원/달러 환율 정보를 가져오는 데 실패했습니다.")

        # 5단계: "[주의] .env 파일에 `GOOGLE_FINANCE_API_KEY`를 추가한 뒤 승인해 주세요." 문구를 포함하여 완료합니다.
        print("[주의] .env 파일에 `GOOGLE_FINANCE_API_KEY`를 추가한 뒤 승인해 주세요.")

    except Exception as e:
        print(f"스크립트 실행 중 오류 발생: {e}", file=sys.stderr)