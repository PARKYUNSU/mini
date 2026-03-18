import requests
from bs4 import BeautifulSoup
import os
import sys

def get_samsung_stock_price():
    """
    네이버 금융에서 삼성전자 주가 정보를 크롤링하여 반환합니다.
    [치명적 경고 - 샌드박스 제약]에 따라 playwright 대신 requests와 BeautifulSoup을 사용합니다.
    """
    samsung_stock_code = "005930"
    url = f"https://finance.naver.com/item/main.naver?code={samsung_stock_code}"

    try:
        # 2단계: requests를 이용하여 네이버 금융 웹페이지에 접속합니다.
        response = requests.get(url)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생

        soup = BeautifulSoup(response.text, 'html.parser')

        # 3단계: 페이지에서 삼성전자 주가 정보를 추출합니다.
        # 현재 주가는 <div class="today"> 아래 <p class="no_today"> 안에 있는 <em> 태그의 <span class="blind"> 에 있습니다.
        today_price_div = soup.find('div', class_='today')
        if not today_price_div:
            return "주가 정보를 찾을 수 없습니다: 'today' div를 찾지 못했습니다."

        no_today_p = today_price_div.find('p', class_='no_today')
        if not no_today_p:
            return "주가 정보를 찾을 수 없습니다: 'no_today' p 태그를 찾지 못했습니다."

        # <em> 태그는 no_up, no_down, no_0 등 여러 클래스를 가질 수 있으므로, 단순히 <em> 태그를 찾습니다.
        price_em = no_today_p.find('em')
        if not price_em:
            return "주가 정보를 찾을 수 없습니다: 주가 <em> 태그를 찾지 못했습니다."

        # 실제 주가 숫자는 <em> 태그 안의 <span class="blind"> 에 있습니다.
        stock_price_span = price_em.find('span', class_='blind')
        if stock_price_span:
            stock_price = stock_price_span.get_text(strip=True)
            return f"삼성전자 현재 주가: {stock_price}원"
        else:
            # Fallback: If span.blind is not found, try to get text directly from em
            stock_price = price_em.get_text(strip=True)
            if stock_price:
                return f"삼성전자 현재 주가: {stock_price}원 (span.blind 태그 없음)"
            else:
                return "주가 정보를 찾을 수 없습니다: 주가 텍스트를 추출하지 못했습니다."

    except requests.exceptions.RequestException as e:
        return f"웹페이지 접속 중 오류 발생: {e}"
    except Exception as e:
        return f"주가 정보 파싱 중 오류 발생: {e}"

if __name__ == "__main__":
    # 1단계: requests와 BeautifulSoup 라이브러리를 사용해 네이버 금융 웹페이지를 크롤링할 수 있는 도구를 만듭니다.
    # (위 get_samsung_stock_price 함수로 구현)

    result = get_samsung_stock_price()
    # 4단계: 추출한 주가 정보를 사용자에게 출력합니다.
    print(result)

    # 5단계: "[주의] .env 파일에 `NAVER_FINANCE_API_KEY`를 추가한 뒤 승인해 주세요." 문구를 포함하여 완료합니다.
    print("[주의] .env 파일에 `NAVER_FINANCE_API_KEY`를 추가한 뒤 승인해 주세요.")