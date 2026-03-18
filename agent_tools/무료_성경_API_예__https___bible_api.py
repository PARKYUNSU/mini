import subprocess
import sys
import os
import requests

# 1단계: `deep-translator` 패키지를 설치합니다.
def ensure_package_installed(package_name):
    """
    Checks if a package is installed and installs it if not.
    """
    try:
        __import__(package_name)
    except ImportError:
        print(f"'{package_name}' 패키지가 설치되어 있지 않습니다. 설치를 시도합니다...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"'{package_name}' 패키지가 성공적으로 설치되었습니다.")
        except Exception as e:
            print(f"'{package_name}' 패키지 설치 중 오류 발생: {e}")
            sys.exit(1) # 설치 실패 시 스크립트 종료

ensure_package_installed("deep_translator")

# deep_translator가 설치된 후 import
from deep_translator import GoogleTranslator

try:
    # 3단계: 사용자가 입력한 영어 성경 구절을 가져오는 함수를 정의합니다.
    def get_english_bible_verse(verse_reference):
        """
        Fetches an English Bible verse from bible-api.com.
        """
        # bible-api.com은 기본적으로 API 키를 요구하지 않습니다.
        # 따라서 os.getenv("XXX_API_KEY")를 사용할 필요가 없습니다.
        api_url = f"https://bible-api.com/{verse_reference}?translation=kjv"
        
        print(f"'{verse_reference}' 영어 성경 구절을 가져오는 중...")
        response = requests.get(api_url)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생

        data = response.json()

        if 'verses' in data and data['verses']:
            # 여러 구절이 있을 수 있으므로 모든 구절을 합칩니다.
            full_verse_text = " ".join([v['text'] for v in data['verses']])
            return full_verse_text
        elif 'error' in data:
            raise ValueError(f"API 오류: {data['error']}")
        else:
            raise ValueError("성경 구절을 찾을 수 없거나 응답 형식이 예상과 다릅니다.")

    # 4단계: 가져온 영어 텍스트를 한국어로 번역하는 함수를 정의합니다.
    def translate_text_to_korean(english_text):
        """
        Translates English text to Korean using deep-translator.
        """
        print("영어 텍스트를 한국어로 번역하는 중...")
        translator = GoogleTranslator(source='en', target='ko')
        translated_text = translator.translate(english_text)
        return translated_text

    # 5단계: 번역된 결과를 출력하는 함수를 정의합니다.
    def print_translated_verse(original_verse_ref, english_text, korean_text):
        """
        Prints the original English verse and its Korean translation.
        """
        print(f"\n--- 성경 구절 번역 결과 ({original_verse_ref}) ---")
        print(f"영어 원문: {english_text}")
        print(f"한국어 번역: {korean_text}")
        print("--------------------------------------------------")

    # 예시 사용: 'John 3:16' 구절을 번역합니다.
    verse_to_translate = 'John 3:16' # 사용자가 입력할 영어 성경 구절

    # 3단계 실행: 영어 성경 구절 가져오기
    english_verse_text = get_english_bible_verse(verse_to_translate)

    # 4단계 실행: 가져온 영어 텍스트를 한국어로 번역
    korean_translated_text = translate_text_to_korean(english_verse_text)

    # 5단계 실행: 번역된 결과 출력
    print_translated_verse(verse_to_translate, english_verse_text, korean_translated_text)

except requests.exceptions.RequestException as e:
    print(f"네트워크 또는 API 요청 오류 발생: {e}")
except ValueError as e:
    print(f"데이터 처리 오류 발생: {e}")
except Exception as e:
    print(f"예상치 못한 오류 발생: {e}")