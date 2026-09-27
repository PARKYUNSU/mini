#!/usr/bin/env python3
"""
레거시 진입점: LaunchAgent 등이 ``mini/run_scheduler.py`` 경로만 알고 있을 때 호환.

실제 구현은 ``apps.scheduler.run_scheduler`` 를 사용합니다.
"""
from apps.scheduler.run_scheduler import main

if __name__ == "__main__":
    main()
