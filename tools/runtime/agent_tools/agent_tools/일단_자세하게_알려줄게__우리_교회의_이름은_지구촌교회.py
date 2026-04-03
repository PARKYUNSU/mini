import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys

def find_restaurants_near_church(church_name: str, search_term: str, group_size: int = 5):
    """
    네이버 검색을 통해 교회 근처 식당 정보를 찾아 출력합니다.
    정적 HTML 파싱에 의존하므로, 동적 콘텐츠는 처리하지 못할 수 있습니다.
    '5인 모임 적합' 및 '4시 이후 영업' 정보는 정적 HTML에서 직접 파싱하기 어렵습니다.

    Args:
        church_name (str): 교회의 이름 (예: '지구촌교회 은혜채플').
        search_term (str): 식당 검색어 (예: '4시 이후 가까운 식당').
        group_size (int): 모임 인원 (현재는 필터링에 직접 사용되지 않음, 정보 부족).
    """
    try:
        # 1단계: 네이버 일반 검색 URL을 생성합니다.
        # 네이버 일반 검색을 사용하여 '플레이스' 섹션의 정적 HTML을 파싱 시도합니다.
        base_url = "https://search.naver.com/search.naver"
        full_query = f"{church_name} {search_term}"
        encoded_query = urllib.parse.quote(full_query)
        search_url = f"{base_url}?query={encoded_query}"

        print(f"검색 URL: {search_url}")

        # 2단계: `requests` 라이브러리를 사용해 생성한 URL의 HTML을 가져옵니다.
        # User-Agent를 설정하여 봇으로 인식되는 것을 방지합니다.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

        # 3단계: `BeautifulSoup`를 이용해 가져온 HTML에서 관련 정보를 추출합니다.
        soup = BeautifulSoup(response.text, 'html.parser')

        restaurants = []
        # 네이버 검색 결과의 '플레이스' 섹션에서 식당 정보를 추출 시도합니다.
        # HTML 구조는 변경될 수 있으므로, 현재 시점의 구조를 기반으로 합니다.
        # '플레이스' 섹션은 보통 'section._place_base_' 또는 유사한 클래스를 가집니다.
        place_section = soup.find('section', class_='_place_base_')
        if not place_section:
            # 다른 일반적인 플레이스 섹션 클래스 시도
            place_section = soup.find('div', class_='_place_base_')
        
        if place_section:
            # 각 식당 항목을 찾습니다.
            # li 태그에 특정 클래스가 붙어있는 경우가 많습니다.
            # 예: li.UE_U8, li.VL_sP, li._item
            # 실제 HTML 구조를 확인하여 정확한 셀렉터를 찾아야 합니다.
            # 현재는 일반적인 패턴을 사용합니다.
            items = place_section.find_all('li', class_='_item')
            if not items: # 다른 일반적인 클래스 시도
                items = place_section.find_all('li', class_='VL_sP')
            if not items: # 또 다른 일반적인 클래스 시도
                items = place_section.find_all('li', class_='UE_U8')
            
            for item in items:
                # 식당 이름
                name_tag = item.find('a', class_='P7PO2')
                # 주소
                address_tag = item.find('span', class_='AD7Za')
                # 평점
                rating_tag = item.find('span', class_='PXMot')
                # 카테고리 (예: 한식)
                category_tag = item.find('span', class_='KCMnt')
                
                name = name_tag.get_text(strip=True) if name_tag else "이름 없음"
                address = address_tag.get_text(strip=True) if address_tag else "주소 없음"
                rating = rating_tag.get_text(strip=True) if rating_tag else "평점 없음"
                category = category_tag.get_text(strip=True) if category_tag else "카테고리 없음"

                restaurants.append({
                    "name": name,
                    "address": address,
                    "rating": rating,
                    "category": category
                })
        else:
            print("네이버 검색 결과에서 '플레이스' 섹션을 찾을 수 없습니다. HTML 구조가 변경되었거나 검색 결과가 없습니다.")
            print("일반 웹 페이지의 정적 HTML 파싱은 동적 콘텐츠를 처리하지 못할 수 있습니다.")
            return

        # 4단계: 추출된 정보 중 5인 모임에 적합하고, 교회로부터 가까운 식당들을 필터링합니다.
        # 현재 정적 HTML 파싱만으로는 '5인 모임 적합' 및 '정확한 거리' 필터링이 어렵습니다.
        # 네이버 검색 결과의 '플레이스' 섹션은 보통 관련성/거리 순으로 정렬되어 있으므로,
        # 상위 결과들을 '가까운 식당'으로 간주합니다.
        # '4시 이후' 정보도 일반적으로 검색 결과 스니펫에 포함되지 않습니다.
        
        filtered_restaurants = []
        print(f"\n--- '{church_name}' 근처 '{search_term}' 검색 결과 (상위 {min(len(restaurants), 5)}개) ---")
        print("참고: '5인 모임 적합' 및 '4시 이후 영업' 정보는 정적 HTML에서 파싱하기 어렵습니다.")
        print("      검색 결과는 네이버의 관련성/거리 순으로 정렬되어 있습니다.")

        # 상위 5개 또는 전체 결과 중 적은 수만큼 출력
        for i, restaurant in enumerate(restaurants[:5]):
            filtered_restaurants.append(restaurant)
            print(f"[{i+1}]")
            print(f"  이름: {restaurant['name']}")
            print(f"  주소: {restaurant['address']}")
            print(f"  평점: {restaurant['rating']}")
            print(f"  카테고리: {restaurant['category']}")
            print("-" * 20)

        # 5단계: 필터링된 결과를 사용자에게 출력합니다.
        if not filtered_restaurants:
            print("필터링된 식당이 없습니다.")

    except requests.exceptions.RequestException as e:
        print(f"웹 요청 중 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    # 사용자 요청에 따라 인자 설정
    church_name = '지구촌교회 은혜채플'
    search_term = '4시 이후 가까운 식당'
    group_size = 5 # 5인 모임

    # 함수 호출
    find_restaurants_near_church(church_name, search_term, group_size)