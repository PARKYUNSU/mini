import sys

def greet_user(name="World"):
    """
    간단한 인사말을 출력하는 함수입니다.
    """
    try:
        message = f"Hello, {name}!"
        print(message)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        greet_user(sys.argv[1])
    else:
        greet_user()