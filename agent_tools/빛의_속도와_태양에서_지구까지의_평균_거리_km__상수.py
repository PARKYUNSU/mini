try:
    # 1단계: 빛의 속도와 태양에서 지구까지의 평균 거리 상수를 정의합니다.
    SPEED_OF_LIGHT_KM_PER_SEC = 299792.458  # 빛의 속도 (km/s)
    DISTANCE_SUN_TO_EARTH_KM = 149600000  # 태양에서 지구까지의 평균 거리 (km)

    # 2단계: 빛이 지구에 도달하는 시간을 초로 계산합니다.
    time_in_seconds = DISTANCE_SUN_TO_EARTH_KM / SPEED_OF_LIGHT_KM_PER_SEC

    # 3단계: 초를 분과 초로 변환하여 정확한 시간을 출력합니다.
    minutes = int(time_in_seconds // 60)
    seconds = time_in_seconds % 60

    print(f"빛의 속도: {SPEED_OF_LIGHT_KM_PER_SEC} km/s")
    print(f"태양에서 지구까지의 평균 거리: {DISTANCE_SUN_TO_EARTH_KM} km")
    print(f"태양에서 출발한 빛이 지구에 도달하는 데 걸리는 시간:")
    print(f"{minutes}분 {seconds:.2f}초")

except Exception as e:
    print(f"오류가 발생했습니다: {e}")