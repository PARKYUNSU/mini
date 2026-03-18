import requests
import os

try:
    # 1단계: requests 라이브러리 import (상단에 이미 포함)

    # 2단계: 날씨 정보를 제공하는 외부 API 키가 필요합니다.
    # "[주의] 맥 미니의 `.env` 파일에 `WEATHER_API_KEY`를 추가한 뒤 승인해 주세요." 문구를 참고하세요.
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        print("오류: WEATHER_API_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인해 주세요.")
    else:
        city = "Seoul"
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        
        # 3단계: requests 모듈을 사용하여 날씨 API 요청을 보내고, 응답을 받아옵니다.
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric", # 섭씨 온도를 위해 metric 단위 사용
            "lang": "kr" # 한국어 설명을 위해 lang 파라미터 추가
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생
        
        # 4단계: 응답의 JSON 형식으로 변환된 데이터에서 서울의 현재 날씨 정보를 추출합니다.
        weather_data = response.json()
        
        if weather_data and weather_data.get("main") and weather_data.get("weather"):
            temperature = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            description = weather_data["weather"][0]["description"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]
            
            # 5단계: 추출한 날씨 정보를 사용자에게 출력합니다.
            print(f"현재 {city}의 날씨 정보:")
            print(f"  온도: {temperature}°C (체감 온도: {feels_like}°C)")
            print(f"  날씨: {description}")
            print(f"  습도: {humidity}%")
            print(f"  바람: {wind_speed} m/s")
        else:
            print(f"오류: {city}의 날씨 정보를 가져오는 데 실패했습니다. 응답 데이터가 올바르지 않습니다.")

except requests.exceptions.RequestException as e:
    print(f"날씨 정보를 가져오는 중 네트워크 또는 API 요청 오류 발생: {e}")
except KeyError as e:
    print(f"날씨 데이터 파싱 중 오류 발생: 필요한 키가 없습니다. {e}")
except Exception as e:
    print(f"예상치 못한 오류 발생: {e}")