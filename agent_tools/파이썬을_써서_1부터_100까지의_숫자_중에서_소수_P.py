import numpy as np

try:
    # 1단계: numpy 라이브러리로 1부터 100까지의 숫자를 생성합니다.
    numbers = np.arange(1, 101)

    # 2단계: 소수 판별 함수를 정의하여 각 숫자가 소수인지 확인합니다.
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(np.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    # 3단계: 소수인 숫자들을 리스트에 추가하고, 그 리스트를 출력합니다.
    prime_numbers = [num for num in numbers if is_prime(num)]

    print("1부터 100까지의 숫자 중 소수(Prime number) 목록:")
    print(prime_numbers)

except Exception as e:
    print(f"오류가 발생했습니다: {e}")