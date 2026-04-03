import requests
from bs4 import BeautifulSoup
import sys

def investigate_github_repo(url: str):
    """
    GitHub 저장소 URL을 조사하여 주요 정보를 추출하고 요약합니다.

    Args:
        url (str): 조사할 GitHub 저장소의 URL.
    """
    try:
        # 1단계: requests와 BeautifulSoup을 사용해 주어진 URL의 HTML을 가져옵니다.
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

        html_content = response.text

        # 2단계: 가져온 HTML을 BeautifulSoup 객체로 변환하여 파싱합니다.
        soup = BeautifulSoup(html_content, 'html.parser')

        # 3단계: 파싱된 HTML에서 필요한 정보를 추출합니다.
        repo_name = ""
        repo_description = ""
        readme_content = ""

        # 저장소 이름 추출
        # GitHub는 보통 <strong itemprop="name"> 태그 안에 저장소 이름을 표시합니다.
        name_tag = soup.find('strong', itemprop='name')
        if name_tag:
            repo_name = name_tag.text.strip()
        else:
            # 특정 태그를 찾지 못했을 경우 URL에서 저장소 이름을 추정
            path_parts = url.strip('/').split('/')
            if len(path_parts) >= 2:
                repo_name = path_parts[-1] # 마지막 부분이 저장소 이름일 가능성이 높음

        # 저장소 설명 추출
        # GitHub는 보통 <p class="f4 my-3"> 또는 <p data-testid="description-content"> 태그 안에 설명을 표시합니다.
        description_tag = soup.find('p', class_='f4 my-3')
        if not description_tag:
            description_tag = soup.find('p', {'data-testid': 'description-content'})
        if description_tag:
            repo_description = description_tag.text.strip()

        # README 내용 추출
        # GitHub의 README는 보통 <article class="markdown-body entry-content container-lg"> 안에 있습니다.
        readme_article = soup.find('article', class_='markdown-body')
        if readme_article:
            # README 내용에서 텍스트를 추출하고 불필요한 공백/줄바꿈 정리
            readme_content = readme_article.get_text(separator='\n', strip=True)
            # 내용이 너무 길 경우 요약을 위해 일부만 표시
            if len(readme_content) > 1500:
                readme_content = readme_content[:1500] + "...\n(내용이 너무 길어 일부만 표시합니다.)"
        else:
            readme_content = "README 내용을 찾을 수 없습니다."

        # 4단계: 추출한 정보를 바탕으로 조사 결과를 작성합니다.
        investigation_result = f"--- GitHub 저장소 조사 결과 ---\n"
        investigation_result += f"URL: {url}\n"
        investigation_result += f"저장소 이름: {repo_name if repo_name else '찾을 수 없음'}\n"
        investigation_result += f"설명: {repo_description if repo_description else '찾을 수 없음'}\n\n"
        investigation_result += f"--- README 내용 ---\n"
        investigation_result += f"{readme_content}\n"
        investigation_result += f"--------------------------------\n"

        # 5단계: 조사 결과를 사용자에게 제공합니다.
        print(investigation_result)

    except requests.exceptions.RequestException as e:
        print(f"웹 페이지를 가져오는 중 오류가 발생했습니다: {e}")
    except Exception as e:
        print(f"데이터를 파싱하거나 처리하는 중 오류가 발생했습니다: {e}")

# 사용자 요청 URL
target_url = "https://github.com/asgeirtj/system_prompts_leaks"
investigate_github_repo(target_url)