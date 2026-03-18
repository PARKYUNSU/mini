import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys
import os

def find_restaurants_for_church_group(church_name: str, group_size: int, search_term: str = "식당", min_rating: float = 4.0):
    """
    지정된 교회 근처에서 특정 인원수에 적합하고 평점이 높은 식당을 찾아 추천합니다.
    네이버 검색을 활용하여 정보를 수집합니다.

    Args:
        church_name (str): 검색할 교회의 이름.
        group_size (int): 모임 인원 수.
        search_term (str): 식당 검색 시 사용할 추가 검색어 (기본값: "식당").
        min_rating (float): 필터링할 최소 평점 (기본값: 4.0).
    """
    print(f"'{church_name}' 근처 {group_size}인 모임에 적합한 식당을 찾고 있습니다.")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 1단계: 구글 검색 (또는 네이버 검색)을 통해 교회 위치 정보 수집
    # 샌드박스 제약으로 인해 구글 검색 결과 직접 파싱은 어려우며, 네이버 검색이 더 효과적일 수 있습니다.
    # 네이버 검색을 통해 교회 위치를 간접적으로 파악하고, 이를 기반으로 식당 검색을 진행합니다.
    # 이 부분은 네이버 검색 UI 변경에 매우 취약할 수 있습니다.

    # 1-1. 교회 주소 검색 시도 (네이버 검색 활용)
    encoded_church_location_query = urllib.parse.quote(f"{church_name} 위치")
    naver_location_search_url = f"https://search.naver.com/search.naver?query={encoded_church_location_query}"

    church_address = None
    print(f"네이버에서 '{church_name}'의 위치 정보를 검색합니다...")
    try:
        response = requests.get(naver_location_search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 네이버 검색 결과에서 '장소' 섹션의 주소 추출 시도
        # 셀렉터는 네이버 UI 변경에 따라 달라질 수 있습니다.
        address_element = soup.find('span', class_='addr')
        if address_element:
            church_address = address_element.get_text(strip=True)
        else:
            # 다른 형태의 주소 정보 탐색 (예: 'place_area' 내의 주소)
            place_area = soup.find('div', class_='place_area')
            if place_area:
                address_element_alt = place_area.find('span', class_='addr')
                if address_element_alt:
                    church_address = address_element_alt.get_text(strip=True)

        if church_address:
            print(f"'{church_name}'의 예상 주소: {church_address}")
            # 2단계: 네이버지도에서 지구촌교회 은혜채플 주변의 식당 목록을 가져오기 위한 검색어 구성
            final_search_query = f"{church_address} {search_term} {group_size}인 모임"
        else:
            print(f"'{church_name}'의 정확한 주소를 찾기 어려워, 교회 이름과 검색어를 조합하여 검색합니다.")
            final_search_query = f"{church_name} {search_term} {group_size}인 모임"

    except requests.exceptions.RequestException as e:
        print(f"교회 위치 검색 중 웹 요청 오류가 발생했습니다: {e}")
        final_search_query = f"{church_name} {search_term} {group_size}인 모임" # Fallback
    except Exception as e:
        print(f"교회 위치 정보 파싱 중 오류가 발생했습니다: {e}")
        final_search_query = f"{church_name} {search_term} {group_size}인 모임" # Fallback

    encoded_final_search_query = urllib.parse.quote(final_search_query)
    naver_restaurant_search_url = f"https://search.naver.com/search.naver?query={encoded_final_search_query}&where=nexearch&sm=top_hty&fbm=0&ie=utf8"

    print(f"네이버에서 '{final_search_query}' 식당 정보를 검색합니다...")
    restaurants = []
    try:
        response = requests.get(naver_restaurant_search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 네이버 검색 결과에서 '장소' 섹션의 식당 목록을 파싱 시도
        # 이 셀렉터는 네이버 검색 UI 변경에 따라 매우 취약할 수 있습니다.
        # 다양한 형태의 장소 아이템을 고려하여 셀렉터를 시도합니다.
        place_items = soup.select('li.sp_place_item') # 일반적인 장소 검색 결과 아이템
        if not place_items:
            place_items = soup.select('div.place_item') # 다른 형태의 장소 검색 결과 아이템
        if not place_items:
            place_items = soup.select('div.search_result_item') # 또 다른 형태

        for item in place_items:
            name_element = item.find('a', class_='_title') or item.find('span', class_='_title') or item.find('a', class_='name')
            name = name_element.get_text(strip=True) if name_element else "이름 없음"

            # 평점 추출 시도
            rating_element = item.find('span', class_='_grade') or item.find('em', class_='_grade') or item.find('span', class_='score')
            rating_text = rating_element.get_text(strip=True) if rating_element else "0.0"
            try:
                rating = float(rating_text)
            except ValueError:
                rating = 0.0

            # 주소 추출 시도
            addr_element = item.find('span', class_='addr') or item.find('div', class_='address')
            address_rest = addr_element.get_text(strip=True) if addr_element else "주소 없음"

            # 카테고리/메뉴 정보 (선택 사항)
            category_element = item.find('span', class_='_category') or item.find('span', class_='category')
            category = category_element.get_text(strip=True) if category_element else "카테고리 없음"

            restaurants.append({
                'name': name,
                'rating': rating,
                'address': address_rest,
                'category': category
            })

        # 3단계: 가져온 식당 목록 중 인원 5명에 적합하고 평점이 높은 곳들을 필터링
        # '5인 모임'은 검색어에 포함하여 간접적으로 필터링을 시도합니다.
        # 직접적인 인원 수용 정보는 웹 스크래핑으로 얻기 어려우므로, 평점 기준으로 필터링합니다.
        filtered_restaurants = [
            rest for rest in restaurants if rest['rating'] >= min_rating
        ]

        if filtered_restaurants:
            # 평점 높은 순으로 정렬
            restaurants_sorted = sorted(filtered_restaurants, key=lambda x: x['rating'], reverse=True)

            # 4단계: 필터링된 결과를 사용자에게 안내
            print(f"\n'{church_name}' 근처 {group_size}인 모임에 적합한 식당 추천 (평점 {min_rating} 이상):")
            for i, rest in enumerate(restaurants_sorted[:5]): # 상위 5개만 출력
                print(f"{i+1}. {rest['name']} (평점: {rest['rating']}) - {rest['category']} - {rest['address']}")
        else:
            print(f"'{church_name}' 근처에서 {group_size}인 모임에 적합한 식당을 찾지 못했습니다.")

    except requests.exceptions.RequestException as e:
        print(f"식당 정보 검색 중 웹 요청 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"식당 정보 파싱 중 오류가 발생했습니다: {e}")

# 사용자 요청에 따른 실행
if __name__ == "__main__":
    church_name_input = "서울 지구촌교회 은혜채플"
    group_size_input = 5
    find_restaurants_for_church_group(church_name_input, group_size_input)