import numpy as np
import calendar # 월 이름을 가져오기 위해 사용

try:
    # 1단계: numpy 라이브러리로 2024년 각 월의 매출 데이터를 생성합니다.
    # 1월부터 12월까지 12개의 월별 매출 데이터 (100에서 500 사이의 랜덤 정수)
    sales_data = np.random.randint(100, 501, size=12)

    # 2단계: 각 월의 매출 데이터를 출력합니다.
    print("2024년 월별 가상 매출 데이터:")
    for i, sales in enumerate(sales_data):
        month_name = calendar.month_name[i + 1] # 1월은 인덱스 1
        print(f"{month_name}: {sales}만원")

    # 3단계: 총 매출, 평균 매출, 최대 매출, 최소 매출을 계산하고 출력합니다.
    total_sales = np.sum(sales_data)
    average_sales = np.mean(sales_data)
    max_sales = np.max(sales_data)
    min_sales = np.min(sales_data)

    print(f"\n총 매출: {total_sales}만원")
    print(f"평균 매출: {average_sales:.2f}만원")
    print(f"최대 매출: {max_sales}만원")
    print(f"최소 매출: {min_sales}만원")

except Exception as e:
    print(f"오류 발생: {e}")