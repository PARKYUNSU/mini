import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import sys
import re

def find_restaurants_google(location_query: str, group_size: int, min_rating: float = 4.0):
    """
    Google 검색을 통해 특정 위치 근처에서 특정 인원수에 적합한 식당을 찾아 추천합니다.
    [치명적 경고]에 따라 playwright 대신 requests와 BeautifulSoup을 사용합니다.

    Args:
        location_query (str): 검색할 위치 (예: '서울 지구촌교회 은혜채플').
        group_size (int): 모임 인원수 (예: 5).
        min_rating (float): 최소 평점 기준 (기본값 4.0).

    Returns:
        str: 추천 식당 정보 또는 결과를 찾지 못했다는 메시지.
    """
    try:
        # 1단계: 구글에서 '서울 지구촌교회 은혜채플 근처 5인 모임 적합 식당'을 검색합니다.
        # 검색어 구성
        search_query = f"{location_query} 근처 {group_size}인 모임 적합 식당"
        encoded_query = urllib.parse.quote(search_query)
        google_search_url = f"https://www.google.com/search?q={encoded_query}&hl=ko"

        # 2단계: Google 검색 결과 페이지의 HTML을 requests와 BeautifulSoup을 이용해 가져옵니다.
        # 🚨 [치명적 경고 - 샌드박스 제약]에 따라 playwright 대신 requests와 BeautifulSoup을 사용합니다.
        # 브라우저처럼 보이도록 User-Agent 헤더를 추가하여 차단될 가능성을 줄입니다.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(google_search_url, headers=headers, timeout=10)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3단계: 가져온 HTML에서 관련 식당 정보를 추출하여 필터링합니다 (평점 4.0 이상, 5인 모임 적합).
        # Google 검색 결과 페이지의 HTML 구조는 자주 변경될 수 있으므로,
        # 일반적인 패턴을 사용하여 식당 정보를 추출합니다.
        
        found_restaurants = []

        # Google Local Pack (지도 결과)에서 정보를 추출하는 시도
        # 클래스 이름은 Google UI 업데이트에 따라 변경될 수 있습니다.
        # 현재 관찰되는 Local Pack 컨테이너 클래스: 'VkpGBb', 'rllt__details'
        # 식당 이름: 'dbg0pd', 'OSrXXb'
        # 평점: 'Aq14fc'
        
        local_results_containers = soup.find_all('div', class_=['VkpGBb', 'rllt__details'])

        for container in local_results_containers:
            # 식당 이름 추출
            name_tag = container.find('div', class_='dbg0pd') or container.find('span', class_='OSrXXb')
            name = name_tag.text.strip() if name_tag else "이름 없음"

            # 평점 추출
            rating_tag = container.find('span', class_='Aq14fc')
            rating_text = rating_tag.text.strip().replace('평점', '').split('점')[0].strip() if rating_tag else "0.0"
            
            try:
                rating = float(rating_text)
            except ValueError:
                rating = 0.0

            # '5인 모임 적합'은 검색 결과 스니펫에서 직접적으로 찾기 어려우므로,
            # 평점 기준으로만 필터링하고, 검색어에 '5인 모임 적합'이 포함되었으므로
            # 결과 자체가 어느 정도 적합하다고 가정합니다.
            if rating >= min_rating:
                found_restaurants.append({
                    'name': name,
                    'rating': rating,
                    'source': 'Local Pack'
                })

        # Local Pack에서 충분한 결과를 찾지 못했거나, Local Pack이 없는 경우 일반 검색 결과 탐색
        if not found_restaurants or len(found_restaurants) < 3: # 최소 3개 미만이면 일반 검색 결과도 확인
            general_search_results = soup.find_all('div', class_='g') # 일반 검색 결과 컨테이너

            for result in general_search_results:
                title_tag = result.find('h3')
                snippet_tag = result.find('div', class_='VwiC3b') # 스니펫 텍스트

                name = title_tag.text.strip() if title_tag else "이름 없음"
                rating = 0.0
                
                if snippet_tag:
                    snippet_text = snippet_tag.text
                    # 스니펫에서 평점 패턴 찾기 (예: "평점 4.5")
                    rating_match = re.search(r'평점\s*(\d+\.?\d*)', snippet_text)
                    if rating_match:
                        try:
                            rating = float(rating_match.group(1))
                        except ValueError:
                            pass # 평점 변환 실패 시 0.0 유지

                if rating >= min_rating:
                    # 중복 방지 (Local Pack과 일반 검색 결과에서 같은 식당이 나올 수 있음)
                    if not any(res['name'] == name for res in found_restaurants):
                        found_restaurants.append({
                            'name': name,
                            'rating': rating,
                            'source': 'General Search'
                        })

        # 4단계: 추출된 식당 목록 중 가장 적합한 곳을 선택하여 사용자에게 추천합니다.
        # 평점이 가장 높은 식당을 우선 추천합니다.
        if found_restaurants:
            # 평점 기준으로 내림차순 정렬
            found_restaurants.sort(key=lambda x: x['rating'], reverse=True)
            best_restaurant = found_restaurants[0]
            return (f"'{location_query}' 근처 {group_size}인 모임에 적합한 식당을 찾았습니다:\n"
                    f"추천 식당: {best_restaurant['name']}\n"
                    f"평점: {best_restaurant['rating']}점")
        else:
            # 5단계: 만약 결과가 없으면, "해당 지역에서 적합한 식당을 찾지 못했습니다."라는 메시지를 출력합니다.
            return "해당 지역에서 적합한 식당을 찾지 못했습니다."

    except requests.exceptions.RequestException as e:
        return f"웹 요청 중 오류가 발생했습니다: {e}"
    except Exception as e:
        return f"식당 정보를 처리하는 중 오류가 발생했습니다: {e}"

# 스크립트 실행 시 함수 호출
if __name__ == "__main__":
    # 사용자 요청에 따른 검색어와 인원수 설정
    church_name = '서울 지구촌교회 은혜채플'
    group_size = 5
    
    result = find_restaurants_google(church_name, group_size)
    print(result)