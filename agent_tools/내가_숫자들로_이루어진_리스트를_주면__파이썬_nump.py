import subprocess
import sys

def ensure_package_installed(package_name):
    """
    Checks if a package is installed and installs it if not.
    """
    try:
        __import__(package_name)
    except ImportError:
        print(f"Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"Successfully installed {package_name}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package_name}: {e}")
            sys.exit(1) # Exit if essential package installation fails

try:
    # 1단계: numpy와 pandas 패키지를 설치합니다.
    # 이전에 발생한 input() 에러를 수정하기 위해, 사용자 입력을 받는 대신
    # 미리 정의된 숫자 리스트를 사용합니다.
    # 필요한 패키지가 설치되어 있지 않을 경우를 대비하여 설치를 시도합니다.
    ensure_package_installed("numpy")
    ensure_package_installed("pandas")

    import numpy as np
    import pandas as pd

    # 2단계: 사용자가 제공한 숫자 리스트를 입력받는 대신, 미리 정의된 리스트를 사용합니다.
    # 실제 사용 시에는 이 부분을 함수 인자 등으로 대체할 수 있습니다.
    numbers = [10, 20, 30, 40, 50, 10, 20, 30, 10, 60, 70, 70, 70]
    print(f"입력된 숫자 리스트: {numbers}")

    # 3단계: 입력받은 리스트를 numpy나 pandas로 변환하고, 평균, 중앙값, 최빈값, 표준편차를 계산합니다.
    # Pandas Series를 사용하여 계산하는 것이 편리합니다.
    s = pd.Series(numbers)

    mean_val = s.mean()
    median_val = s.median()
    # Pandas Series의 mode() 메서드는 여러 최빈값이 있을 경우 모두 반환합니다.
    mode_val = s.mode().tolist()
    std_dev_val = s.std()

    # 4단계: 계산된 결과를 출력합니다.
    print(f"평균: {mean_val}")
    print(f"중앙값: {median_val}")
    print(f"최빈값: {mode_val}")
    print(f"표준편차: {std_dev_val}")

except ImportError as e:
    print(f"필요한 라이브러리를 임포트하는 데 실패했습니다: {e}")
    print("numpy, pandas 패키지가 올바르게 설치되었는지 확인해주세요.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")