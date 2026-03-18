import requests
from bs4 import BeautifulSoup
import sys

def get_samsung_stock_price():
    """
    네이버 금융에서 삼성전자 주가 정보를 크롤링하여 반환합니다.
    [치명적 경고 - 샌드박스 제약]에 따라 playwright 대신 requests와 BeautifulSoup을 사용합니다.
    """
    url = 'https://finance.naver.com/sise/'
    samsung_stock_name = "삼성전자"

    try:
        # 1단계: requests와 BeautifulSoup 라이브러리 사용 (상단에 import)

        # 2단계: 'https://finance.naver.com/sise/' URL의 정적 HTML을 requests+BeautifulSoup으로 파싱
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

        soup = BeautifulSoup(response.text, 'html.parser')

        # 3단계: 추출된 주가 정보 중 삼성전자 관련 데이터를 정제하고, 필요에 따라 숫자형 데이터로 변환
        # 시가총액 상위 종목 테이블 찾기 (ID: siselist_tab_0)
        stock_table = soup.find('table', {'id': 'siselist_tab_0'})

        samsung_price = None
        if stock_table:
            # 테이블의 모든 행(tr)을 순회
            for row in stock_table.find_all('tr'):
                # 종목명(삼성전자)을 포함하는 td 찾기
                title_td = row.find('td', class_='tltle')
                if title_td and title_td.find('a', string=samsung_stock_name):
                    # 삼성전자 행을 찾았으면, 그 행에서 주가 정보를 포함하는 td 찾기
                    # 주가는 보통 종목명 다음의 'number' 클래스를 가진 td에 있습니다.
                    price_td = row.find('td', class_='number')
                    if price_td:
                        samsung_price_str = price_td.get_text(strip=True)
                        # 숫자형 데이터로 변환 (콤마 제거)
                        samsung_price = int(samsung_price_str.replace(',', ''))
                        break # 삼성전자 주가를 찾았으므로 루프 종료
        
        # 4단계: 크롤링한 주가 정보를 사용자에게 알림 메시지 형태로 반환
        if samsung_price is not None:
            message = f"현재 {samsung_stock_name} 주가: {samsung_price:,}원"
            print(message)
            return message
        else:
            # 5단계: 삼성전자 주가 정보를 찾지 못한 경우 에러 메시지 출력
            error_message = f"네이버 금융에서 {samsung_stock_name} 주가 정보를 찾을 수 없습니다."
            print(error_message, file=sys.stderr)
            return error_message

    except requests.exceptions.RequestException as e:
        # 5단계: 네트워크 또는 HTTP 요청 관련 에러 처리
        error_message = f"웹페이지에 접속하는 중 오류가 발생했습니다: {e}"
        print(error_message, file=sys.stderr)
        return error_message
    except Exception as e:
        # 5단계: 그 외 예상치 못한 에러 처리
        error_message = f"주가 정보를 크롤링하는 중 예상치 못한 오류가 발생했습니다: {e}"
        print(error_message, file=sys.stderr)
        return error_message

if __name__ == "__main__":
    get_samsung_stock_price()