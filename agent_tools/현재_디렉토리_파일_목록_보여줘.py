import os

try:
    current_directory = os.getcwd()
    print(f"현재 작업 디렉토리: {current_directory}")

    files_in_directory = os.listdir(current_directory)
    print("현재 디렉토리의 파일 목록:")
    for item in files_in_directory:
        print(item)

except Exception as e:
    print(f"오류 발생: {e}")