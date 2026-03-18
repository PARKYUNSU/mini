import requests
import sys
import os

def get_bible_verse(book: str, chapter: int, verse: int) -> str:
    """
    bible-api.com에서 특정 성경 구절을 가져옵니다.

    Args:
        book (str): 성경 책 이름 (예: "Genesis", "John").
        chapter (int): 장 번호.
        verse (int): 절 번호.

    Returns:
        str: 요청된 성경 구절 텍스트.
    """
    base_url = "https://bible-api.com/"
    query = f"{book} {chapter}:{verse}"
    url = f"{base_url}{query}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        data = response.json()

        if data and 'verses' in data and data['verses']:
            verse_text = data['verses'][0]['text']
            return f"{book} {chapter}:{verse}: {verse_text}"
        elif 'error' in data:
            return f"Error from API: {data['error']}"
        else:
            return "Verse not found or unexpected API response."
    except requests.exceptions.RequestException as e:
        return f"Network or API request error: {e}"
    except ValueError as e:
        return f"JSON decoding error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

try:
    book_name = "Genesis"
    chapter_num = 1
    verse_num = 1
    result = get_bible_verse(book_name, chapter_num, verse_num)
    print(result)
except Exception as e:
    print(f"An error occurred during execution: {e}")