import requests
from bs4 import BeautifulSoup
import os

def get_busan_weather():
    """
    wttr.in 웹사이트에서 부산 날씨 정보를 가져와 출력합니다.
    """
    try:
        # 2단계: wttr.in의 URL을 정의하고, requests로 해당 URL에 GET 요청을 보내서 응답을 받습니다.
        # wttr.in은 기본적으로 터미널 친화적인 텍스트를 반환합니다.
        url = "https://wttr.in/Busan"
        
        # GET 요청 보내기
        response = requests.get(url)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생

        # 3단계: BeautifulSoup을 이용해 HTML 문서에서 날씨 정보를 추출합니다.
        # wttr.in은 주로 텍스트 기반의 출력을 제공하므로, BeautifulSoup은 전체 텍스트를 파싱하는 데 사용됩니다.
        # 실제로는 HTML 구조가 복잡하지 않아 전체 텍스트를 가져오는 것과 유사합니다.
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # wttr.in의 출력은 HTML 문서의 body에 직접 텍스트로 포함되거나 <pre> 태그 안에 있을 수 있습니다.
        # 여기서는 전체 문서의 텍스트 내용을 가져오는 방식으로 처리합니다.
        weather_info = soup.get_text()

        # 4단계: 추출된 날씨 정보를 사용자에게 출력합니다.
        print("--- 부산 날씨 정보 (wttr.in) ---")
        print(weather_info.strip()) # 불필요한 공백 제거
        print("---------------------------------")

    except requests.exceptions.RequestException as e:
        print(f"날씨 정보를 가져오는 중 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")
    finally:
        # 5단계: "[주의] .env 파일에 `WTTR_IN_API_KEY`를 추가한 뒤 승인해 주세요."라는 문구를 포함하여 완료합니다.
        print("[주의] .env 파일에 `WTTR_IN_API_KEY`를 추가한 뒤 승인해 주세요.")

# 함수 실행
if __name__ == "__main__":
    get_busan_weather()