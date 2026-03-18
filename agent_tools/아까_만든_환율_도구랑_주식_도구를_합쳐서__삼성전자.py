import requests
from bs4 import BeautifulSoup
import os
import sys

def get_krw_usd_exchange_rate():
    """
    Google Finance 웹페이지에서 원/달러 환율 정보를 크롤링하여 반환합니다.
    [치명적 경고 - 샌드박스 제약]에 따라 playwright 대신 requests와 BeautifulSoup을 사용합니다.
    """
    url = "https://www.google.com/finance/quote/KRW-USD"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        soup = BeautifulSoup(response.text, 'html.parser')

        exchange_rate_tag = soup.find('div', class_='YMlKec fxKbKc')
        if exchange_rate_tag:
            exchange_rate_text = exchange_rate_tag.text.strip()
            exchange_rate = float(exchange_rate_text.replace(',', ''))
            return exchange_rate
        else:
            print("환율 정보를 찾을 수 없습니다. 웹사이트 구조가 변경되었을 수 있습니다.", file=sys.stderr)
            return None
    except requests.exceptions.RequestException as e:
        print(f"웹 요청 중 오류 발생: {e}", file=sys.stderr)
        return None
    except ValueError as e:
        print(f"환율 값 변환 중 오류 발생: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}", file=sys.stderr)
        return None

def get_samsung_stock_price():
    """
    네이버 금융에서 삼성전자 주가 정보를 크롤링하여 반환합니다.
    [치명적 경고 - 샌드박스 제약]에 따라 playwright 대신 requests와 BeautifulSoup을 사용합니다.
    """
    url = "https://finance.naver.com/item/main.naver?code=005930" # 삼성전자 종목 코드
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생
        soup = BeautifulSoup(response.text, 'html.parser')

        current_price_span = soup.find('span', class_='blind', string='현재가')
        if current_price_span:
            price_element = current_price_span.find_next_sibling(string=True)
            if price_element:
                price_text = price_element.strip()
            else:
                price_element = current_price_span.find_next_sibling('span')
                if price_element:
                    price_text = price_element.text.strip()
                else:
                    print("주가 텍스트를 찾을 수 없습니다. 웹사이트 구조가 변경되었을 수 있습니다.", file=sys.stderr)
                    return None

            stock_price = int(price_text.replace(',', ''))
            return stock_price
        else:
            print("삼성전자 주가 정보를 찾을 수 없습니다. 웹사이트 구조가 변경되었을 수 있습니다.", file=sys.stderr)
            return None
    except requests.exceptions.RequestException as e:
        print(f"웹 요청 중 오류 발생: {e}", file=sys.stderr)
        return None
    except ValueError as e:
        print(f"주가 값 변환 중 오류 발생: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    try:
        # 1단계: 기존 도구 `get_exchange_rate`를 사용하여 환율 정보를 가져옵니다.
        exchange_rate = get_krw_usd_exchange_rate()

        # 2단계: 기존 도구 `get_samsung_stock_price`를 사용하여 삼성전자 주가 정보를 가져옵니다.
        samsung_stock_price_krw = get_samsung_stock_price()

        if exchange_rate is not None and samsung_stock_price_krw is not None:
            # 3단계: 얻은 환율과 주가 정보를 바탕으로, 삼성전자의 주가를 달러로 환산합니다.
            samsung_stock_price_usd = samsung_stock_price_krw / exchange_rate

            # 4단계: 결과를 출력합니다.
            print(f"현재 원/달러 환율: 1 USD = {exchange_rate:.2f} KRW")
            print(f"현재 삼성전자 주가: {samsung_stock_price_krw:,} KRW")
            print(f"삼성전자 주가 (달러 환산): {samsung_stock_price_usd:.2f} USD")
        else:
            print("환율 또는 삼성전자 주가 정보를 가져오는 데 실패했습니다.")

    except Exception as e:
        print(f"스크립트 실행 중 오류 발생: {e}", file=sys.stderr)
    finally:
        # 5단계: "[주의] .env 파일에 EXCHANGE_RATE_API_KEY와 SAMSUNG_STOCK_API_KEY를 추가한 뒤 승인해 주세요." 포함.
        print("[주의] .env 파일에 EXCHANGE_RATE_API_KEY와 SAMSUNG_STOCK_API_KEY를 추가한 뒤 승인해 주세요.")