import requests
import os
import sys

# 2단계: get_busan_weather 함수를 기존 도구 agent_tools/폴더의 '서울_지금_현재_날씨_알려줘'에서 재사용합니다.
# '서울_지금_현재_날씨_알려줘' 도구의 코드를 기반으로 wttr.in에서 날씨를 가져오는 함수를 작성합니다.
# 단, wttr.in은 API 키를 필요로 하지 않습니다.

def get_weather_from_wttr(location: str, day: str = "today"):
    """
    wttr.in 웹사이트에서 특정 지역의 날씨 정보를 가져와 출력합니다.
    Args:
        location (str): 날씨 정보를 가져올 도시 이름 (예: "Busan", "Seoul").
        day (str): "today" 또는 "tomorrow" (wttr.in은 기본적으로 현재 날씨를 보여주며,
                   내일 날씨를 직접적으로 포맷팅하여 가져오기 어렵습니다.
                   여기서는 wttr.in의 기본 3일 예보 중 두 번째 날을 '내일'로 간주하여 파싱합니다.)
    Returns:
        str: 날씨 정보 문자열 또는 오류 메시지.
    """
    try:
        # wttr.in은 기본적으로 3일 예보를 ASCII 아트로 보여줍니다.
        # 내일 날씨를 정확히 파싱하기 위해 텍스트 모드와 특정 포맷을 사용합니다.
        # %l: Location, %t: Temperature, %C: Condition, %w: Wind, %h: Humidity, %P: Pressure
        # %D: Day of the week, %x: Date, %y: Year
        # wttr.in은 기본적으로 3일 예보를 보여주므로, 두 번째 블록을 '내일'로 간주합니다.
        # format=2을 사용하면 3일 예보를 간결하게 볼 수 있습니다.
        url = f"https://wttr.in/{location}?format=2"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

        weather_data = response.text.strip().split('\n')

        if not weather_data:
            return f"wttr.in에서 {location} 날씨 정보를 찾을 수 없습니다."

        # wttr.in?format=2는 보통 3줄로 나옵니다:
        # 1. Location: Current_Weather
        # 2. Tomorrow: Min_Temp..Max_Temp Condition
        # 3. Day_After_Tomorrow: Min_Temp..Max_Temp Condition
        
        if day == "today":
            if len(weather_data) >= 1:
                # 첫 번째 줄에서 현재 날씨 정보를 추출 (예: "Busan: +15°C Clear")
                today_info = weather_data[0]
                # "Location: " 부분을 제거하고 반환
                return today_info.replace(f"{location}: ", f"{location} 현재 날씨: ")
            else:
                return f"wttr.in에서 {location}의 현재 날씨 정보를 파싱할 수 없습니다."
        elif day == "tomorrow":
            if len(weather_data) >= 2:
                # 두 번째 줄에서 내일 날씨 정보를 추출 (예: "Tomorrow: +10..+18°C Partly cloudy")
                tomorrow_info = weather_data[1]
                # "Tomorrow: " 부분을 제거하고 반환
                return tomorrow_info.replace("Tomorrow: ", f"{location} 내일 날씨: ")
            else:
                return f"wttr.in에서 {location}의 내일 날씨 정보를 파싱할 수 없습니다."
        else:
            return "지원하지 않는 날짜입니다. 'today' 또는 'tomorrow'를 사용하세요."

    except requests.exceptions.RequestException as e:
        return f"날씨 정보를 가져오는 중 오류가 발생했습니다: {e}"
    except Exception as e:
        return f"예상치 못한 오류가 발생했습니다: {e}"

if __name__ == "__main__":
    # 1단계: wttr.in 웹사이트에서 부산 날씨 정보를 가져와 출력합니다. (현재 날씨)
    # 이 단계는 '내일 부산 날씨'를 위한 준비 단계로, 현재 부산 날씨를 먼저 가져와봅니다.
    print("1단계: wttr.in에서 부산 현재 날씨 정보를 가져와 출력합니다.")
    current_busan_weather = get_weather_from_wttr("Busan", "today")
    print(current_busan_weather)
    print("-" * 30)

    # 3단계: 함수 호출을 통해 내일 부산 날씨 정보를 얻습니다.
    print("3단계: 함수 호출을 통해 내일 부산 날씨 정보를 얻습니다.")
    tomorrow_busan_weather = get_weather_from_wttr("Busan", "tomorrow")

    # 4단계: 결과를 사용자에게 출력합니다.
    print("4단계: 결과를 사용자에게 출력합니다.")
    print(tomorrow_busan_weather)