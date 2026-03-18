import requests
import os
import sys

def get_github_repo_stars(owner: str, repo_name: str) -> str:
    """
    GitHub API를 사용하여 특정 레포지토리의 별(Star) 개수를 가져옵니다.

    Args:
        owner (str): 레포지토리 소유자의 사용자명 또는 조직명.
        repo_name (str): 레포지토리 이름.

    Returns:
        str: 레포지토리의 별 개수 또는 오류 메시지.
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Python-GitHub-Star-Counter" # GitHub API 요청 시 User-Agent 권장
    }

    # GitHub Personal Access Token이 필요한 경우 (rate limit 회피 등)
    # GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    # if GITHUB_TOKEN:
    #     headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

        data = response.json()
        stars = data.get("stargazers_count")

        if stars is not None:
            return f"'{owner}/{repo_name}' 레포지토리의 별 개수: {stars}"
        else:
            return f"'{owner}/{repo_name}' 레포지토리의 별 개수를 찾을 수 없습니다."

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return f"오류: 레포지토리 '{owner}/{repo_name}'를 찾을 수 없습니다. (HTTP 404)"
        elif response.status_code == 403:
            return f"오류: API 요청 제한에 도달했거나 권한이 없습니다. (HTTP 403) - User-Agent 또는 GITHUB_TOKEN 확인 필요."
        else:
            return f"HTTP 오류 발생: {http_err}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"연결 오류 발생: {conn_err} - 네트워크 연결을 확인하세요."
    except requests.exceptions.Timeout as timeout_err:
        return f"요청 시간 초과: {timeout_err}"
    except requests.exceptions.RequestException as req_err:
        return f"요청 중 알 수 없는 오류 발생: {req_err}"
    except Exception as e:
        return f"예상치 못한 오류 발생: {e}"

if __name__ == "__main__":
    repo_owner = "langchain-ai"
    repo_name = "langgraph"
    result = get_github_repo_stars(repo_owner, repo_name)
    print(result)