import numpy as np
import calendar # 월 이름을 가져오기 위해 사용

try:
    # 1단계: numpy 라이브러리로 2024년 각 월의 매출 데이터를 생성합니다.
    # 1월부터 12월까지 12개의 월별 매출 데이터 (100에서 500 사이의 랜덤 정수)
    sales_data = np.random.randint(100, 501, 12) # 501은 상한선 미포함이므로 500까지 포함

    print("2024년 월별 가상 매출 데이터:")
    for i, sales in enumerate(sales_data):
        month_name = calendar.month_name[i + 1] # 1월은 인덱스 1
        print(f"{month_name}: {sales}원")
    print("-" * 40)

    # 2단계: 생성된 매출 데이터를 ASCII 아트 막대그래프로 시각화합니다.
    # (요청에 따라 matplotlib 대신 텍스트 기호(ASCII 아트)를 직접 구현)
    print("\n2024년 월별 매출 ASCII 아트 막대그래프:")

    if sales_data.size > 0:
        max_sales = sales_data.max()
    else:
        max_sales = 1 # 데이터가 없을 경우 0으로 나누는 오류 방지

    max_bar_length = 50 # 콘솔에 적합한 최대 막대 길이

    for i, sales in enumerate(sales_data):
        month_name = calendar.month_name[i + 1]
        # 막대 길이 계산 (최대 매출에 비례하여 스케일링)
        if max_sales > 0:
            bar_length = int((sales / max_sales) * max_bar_length)
        else:
            bar_length = 0
        
        bar = '▇' * bar_length # 텍스트 기호로 막대 생성
        # 월 이름 정렬을 위해 패딩 추가
        print(f"{month_name:<10} | {bar} {sales}원")

    # 3단계: 생성된 데이터와 그래프를 출력합니다. (이미 위에서 출력됨)

except ModuleNotFoundError:
    print("필요한 라이브러리(numpy)가 설치되지 않았습니다. 'pip install numpy'를 실행하여 설치해 주세요.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")