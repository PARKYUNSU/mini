import requests
from bs4 import BeautifulSoup
import sys

def find_restaurants_for_group(search_query: str, group_size: int, min_rating: float = 4.0):
    """
    교회 셀 모임 인원에게 적합한 외부 식당을 찾아 추천합니다.
    Google 검색을 시뮬레이션하고, 평점 및 인원 수에 따라 필터링합니다.

    Args:
        search_query (str): Google 검색에 사용할 쿼리 (예: "교회 셀 모임 식당").
        group_size (int): 모임 인원 수.
        min_rating (float): 식당을 추천하기 위한 최소 평점 기준.

    Returns:
        dict: 추천된 식당의 상세 정보 (이름, 주소, 평점) 딕셔너리,
              적합한 식당을 찾지 못한 경우 None을 반환합니다.
    """
    print(f"1단계: 구글 검색을 통해 '{search_query}' 식당 목록을 찾아보겠습니다.")

    # Google 검색 URL 구성
    google_search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"

    try:
        # User-Agent를 설정하여 봇으로 인식될 가능성을 줄입니다.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(google_search_url, headers=headers, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        soup = BeautifulSoup(response.text, 'html.parser')

        print(f"Google 검색 URL: {google_search_url}")
        print("Google 검색 결과 HTML을 가져왔습니다. (실제 파싱은 제한적)")

        # --- CRITICAL LIMITATION EXPLANATION ---
        print("\n🚨 [중요 알림]:")
        print("   Google 검색 결과 페이지는 동적으로 로드되는 콘텐츠가 많고,")
        print("   Google의 봇 차단 정책으로 인해 `requests`와 `BeautifulSoup`만으로는")
        print("   식당 이름, 주소, 평점과 같은 구조화된 데이터를 안정적으로 추출하기 매우 어렵습니다.")
        print("   따라서, 다음 단계 진행을 위해 실제 검색 결과 대신 예시 데이터를 활용하겠습니다.")
        print("   이는 [실행 계획]의 1단계를 시뮬레이션하기 위한 불가피한 조치입니다.")
        # --- END OF LIMITATION EXPLANATION ---

        # 실제 검색 결과 대신 예시 식당 데이터를 사용하여 다음 단계를 진행합니다.
        # 이 데이터는 '구글 검색을 통해 찾은' 식당 정보를 시뮬레이션합니다.
        example_restaurants = [
            {"name": "더 플레이스 다이닝", "address": "서울 중구 소공로 112", "rating": 4.5, "min_capacity": 4, "max_capacity": 10},
            {"name": "봉추찜닭 명동점", "address": "서울 중구 명동10길 19-27", "rating": 4.2, "min_capacity": 2, "max_capacity": 8},
            {"name": "매드포갈릭 강남점", "address": "서울 서초구 서초대로77길 3", "rating": 4.3, "min_capacity": 4, "max_capacity": 12},
            {"name": "아웃백 스테이크하우스 종로점", "address": "서울 종로구 종로 51", "rating": 4.6, "min_capacity": 4, "max_capacity": 15},
            {"name": "미즈컨테이너 강남점", "address": "서울 강남구 강남대로102길 33", "rating": 3.8, "min_capacity": 2, "max_capacity": 6}, # 낮은 평점
            {"name": "파스타집", "address": "서울 마포구 독막로 76-1", "rating": 4.1, "min_capacity": 2, "max_capacity": 6},
            {"name": "한정식집", "address": "서울 종로구 인사동길 12", "rating": 4.7, "min_capacity": 5, "max_capacity": 20},
        ]

    except requests.exceptions.RequestException as e:
        print(f"웹 페이지를 가져오는 중 오류 발생: {e}")
        print("네트워크 문제 또는 Google의 봇 차단으로 인해 검색 결과를 가져오지 못했습니다.")
        print("예시 데이터를 사용하여 다음 단계를 진행합니다.")
        # 오류 발생 시에도 예시 데이터를 사용하여 다음 단계 진행
        example_restaurants = [
            {"name": "더 플레이스 다이닝", "address": "서울 중구 소공로 112", "rating": 4.5, "min_capacity": 4, "max_capacity": 10},
            {"name": "봉추찜닭 명동점", "address": "서울 중구 명동10길 19-27", "rating": 4.2, "min_capacity": 2, "max_capacity": 8},
            {"name": "매드포갈릭 강남점", "address": "서울 서초구 서초대로77길 3", "rating": 4.3, "min_capacity": 4, "max_capacity": 12},
            {"name": "아웃백 스테이크하우스 종로점", "address": "서울 종로구 종로 51", "rating": 4.6, "min_capacity": 4, "max_capacity": 15},
            {"name": "미즈컨테이너 강남점", "address": "서울 강남구 강남대로102길 33", "rating": 3.8, "min_capacity": 2, "max_capacity": 6},
            {"name": "파스타집", "address": "서울 마포구 독막로 76-1", "rating": 4.1, "min_capacity": 2, "max_capacity": 6},
            {"name": "한정식집", "address": "서울 종로구 인사동길 12", "rating": 4.7, "min_capacity": 5, "max_capacity": 20},
        ]

    print(f"\n2단계: 찾은 식당 정보 중 평점이 높고({min_rating}점 이상), {group_size}명 인원에 적합하며, 위치가 편리한 곳들을 필터링하겠습니다.")
    filtered_restaurants = []
    for restaurant in example_restaurants:
        # 평점 필터링
        if restaurant["rating"] >= min_rating:
            # 인원 수 적합성 필터링 (최소/최대 수용 인원 기준)
            if restaurant["min_capacity"] <= group_size <= restaurant["max_capacity"]:
                filtered_restaurants.append(restaurant)

    if not filtered_restaurants:
        print("필터링 조건에 맞는 식당을 찾지 못했습니다.")
        return None

    print(f"필터링된 식당 목록 ({len(filtered_restaurants)}개):")
    for r in filtered_restaurants:
        print(f"  - {r['name']} (평점: {r['rating']} / 5.0, 수용 인원: {r['min_capacity']}~{r['max_capacity']}명)")

    print("\n3단계: 필터링된 식당 목록에서 사용자에게 추천할 적합한 장소를 선택하겠습니다.")
    # 필터링된 식당 중 평점이 가장 높은 식당을 추천합니다.
    recommended_restaurant = max(filtered_restaurants, key=lambda x: x["rating"])

    print("\n4단계: 선택된 장소에 대한 상세 정보를 출력하겠습니다.")
    print("\n--- 추천 식당 정보 ---")
    print(f"이름: {recommended_restaurant['name']}")
    print(f"주소: {recommended_restaurant['address']}")
    print(f"평점: {recommended_restaurant['rating']} / 5.0")
    print("--------------------")

    return recommended_restaurant

if __name__ == "__main__":
    # 사용자 요청에 따른 매개변수 설정
    # "교회 셀 모임 인원들이 이제 밖으로 가서 식사하고 교제하는 건데 인원이 한 5명이라고 해 혹 추천하는 장소가 있을까?"
    search_term = "서울 5인 모임 식당 추천" # 구글 검색 시뮬레이션에 사용할 검색어
    group_size = 5                     # 모임 인원
    min_rating_threshold = 4.0         # 최소 평점 기준

    try:
        find_restaurants_for_group(search_term, group_size, min_rating_threshold)
    except Exception as e:
        print(f"스크립트 실행 중 오류 발생: {e}")