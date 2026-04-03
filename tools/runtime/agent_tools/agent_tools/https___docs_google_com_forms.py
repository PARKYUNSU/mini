import subprocess
import sys
import requests
from bs4 import BeautifulSoup
import os

def ensure_package_installed(package_name):
    """
    Checks if a package is installed and installs it if not.
    """
    try:
        __import__(package_name)
    except ImportError:
        print(f"Package '{package_name}' not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"Package '{package_name}' installed successfully.")
        except Exception as e:
            print(f"Error installing package '{package_name}': {e}")
            sys.exit(1)

try:
    # 1단계: `requests`와 `beautifulsoup4` 라이브러리가 설치되어 있는지 확인하고 설치합니다.
    ensure_package_installed("requests")
    ensure_package_installed("beautifulsoup4")

    # 2단계: Google Forms URL에 접근합니다.
    url = "https://docs.google.com/forms/d/e/1FAIpQLSfAMBpyj_isjFieWxvMcwffrCvuz68cGnuHEWy5pCD2mG9Pkw/viewform"
    print(f"Google Forms URL에 접근 시도: {url}")
    response = requests.get(url)
    response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

    # 3단계: Google Forms의 HTML 소스코드를 가져와서 분석합니다.
    soup = BeautifulSoup(response.text, 'html.parser')

    # 4단계: 필요한 정보를 추출하여 출력합니다.
    print("\n--- Google Forms 정보 ---")

    # 폼 제목 추출 (페이지 타이틀)
    page_title = soup.find('title').text if soup.find('title') else "페이지 제목 없음"
    print(f"페이지 제목: {page_title}")

    # 폼의 메인 제목 추출 (페이지 내에 표시되는 제목)
    form_main_title_tag = soup.find('div', class_='freebirdFormviewerComponentsViewHeaderTitle')
    form_main_title = form_main_title_tag.text.strip() if form_main_title_tag else "폼 메인 제목 없음"
    print(f"폼 메인 제목: {form_main_title}")

    # 폼 설명 추출
    form_description_tag = soup.find('div', class_='freebirdFormviewerComponentsViewHeaderDescription')
    form_description = form_description_tag.text.strip() if form_description_tag else "폼 설명 없음"
    print(f"폼 설명: {form_description}")

    # 폼 질문 목록 추출
    questions = soup.find_all('div', class_='freebirdFormviewerComponentsQuestionBaseRoot')
    if questions:
        print("\n폼 질문 목록:")
        for i, question_div in enumerate(questions):
            question_text_tag = question_div.find('div', class_='freebirdFormviewerComponentsQuestionBaseTitle')
            question_text = question_text_tag.text.strip() if question_text_tag else f"질문 {i+1} (텍스트 없음)"
            print(f"- {question_text}")
            # 질문 유형이나 옵션 등 더 자세한 정보도 추출할 수 있지만, 여기서는 질문 텍스트만 추출합니다.
    else:
        print("\n폼 질문을 찾을 수 없습니다.")

    print(f"\nGoogle Forms URL 접근 및 정보 추출 성공.")

except requests.exceptions.RequestException as e:
    print(f"Google Forms URL 접근 중 네트워크 또는 HTTP 오류 발생: {e}")
except Exception as e:
    print(f"Google Forms 정보 추출 중 오류 발생: {e}")