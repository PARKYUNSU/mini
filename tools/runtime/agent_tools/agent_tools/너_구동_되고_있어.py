import os

try:
    # 1. 현재 디렉토리와 파일 목록 확인
    current_directory = os.getcwd()
    print(f"현재 작업 디렉토리: {current_directory}")

    files_in_directory = os.listdir(current_directory)
    print("현재 디렉토리의 파일 목록:")
    for item in files_in_directory:
        print(f"- {item}")

    # 2. 사용자 요청 확인 (이미 주어진 요청: "너 구동 되고 있어?")
    user_request = "너 구동 되고 있어?"
    # print(f"\n사용자 요청: {user_request}") # 이 부분은 출력 계획에 없으므로 생략

    # 3. 응답 생성
    response = "네, 저는 정상적으로 작동하고 있습니다."

    # 4. 응답 출력
    print(f"\n{response}")

except Exception as e:
    print(f"오류가 발생했습니다: {e}")