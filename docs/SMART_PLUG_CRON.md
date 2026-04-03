# 스마트 플러그(Tuya) + 텔레그램 스케줄(cron)

## 동작 원리

1. **`tools/runtime/agent_tools/agent_tools/smart_plug.py`**
   - 기본: `tinytuya`로 LAN TCP에서 on/off.
   - **`TUYA_CONTROL_MODE=cloud`** 이면 IoT Open API(앱과 동일한 클라우드 경로).
   - 비밀 값은 **`.env`**의 `TUYA_*` 만 사용 (코드에 하드코딩 금지). 자세한 것은 **`SMART_PLUG_CLOUD.md`**.

2. **`apps.scheduler.run_scheduler`가 떠 있어야 함**
   - 1분마다 due job을 찾아 `apps.scheduler.agent_scheduled_runner.run_scheduled_job(prompt, chat_id)` 호출.
   - `is_scheduled=True`일 때도 **라우터 화이트리스트**가 `smart_plug`로 내려가면 Planner 없이 바로 도구 실행.

3. **`job_runs.jsonl`**
   - 작업이 **실행될 때마다** 한 줄씩 append되는 **로그**입니다.
   - 스케줄 “등록”은 **`jobs.json`** (또는 봇으로 `schedule_add_job`).

## 설정 순서

1. `pip install tinytuya` (또는 `pip install -r requirements.txt`)
2. `.env`에 채우기:
   - **로컬:** `TUYA_DEVICE_ID`, `TUYA_LOCAL_KEY`, `TUYA_PLUG_IP`, `TUYA_PROTOCOL_VERSION`
   - **클라우드(6668 거절 기기):** `TUYA_CONTROL_MODE=cloud`, `TUYA_CLOUD_ACCESS_ID`, `TUYA_CLOUD_ACCESS_SECRET`, `TUYA_CLOUD_REGION`(예: `us`)
3. 봇 재시작 → `tool_chroma_db`에 `smart_plug` 인덱싱(기동 시 sync).

## 스케줄 등록 예시 (텔레그램)

**켜기·끄기는 job을 각각 하나씩** 만드는 것이 단순합니다.

- 매일 07:30 켜기
  - 예: `매일 7시 30분에 스마트 플러그 켜줘`
  - **저장되는 prompt**에 반드시 **켜기** 의도가 들어가게 하세요.
  - (등록 UI가 `prompt`만 저장하면 그 문장이 그대로 실행 시 전달됩니다.)

- 매일 23:30 끄기
  - 예: `매일 23시 30분에 스마트 플러그 꺼줘`

실행 시 전달되는 `prompt` 예:

- `스마트 플러그 켜줘`
- `스탠드 불 꺼줘`
- `turn on smart plug` / `turn off`

## 트러블슈팅

- **프로토콜 버전**이 맞지 않으면 기기가 무반응 → `TUYA_PROTOCOL_VERSION` 변경.
- **로컬 키**는 클라우드와 오랫동안 동기화 안 되면 바뀔 수 있음 → tinytuya로 재스캔.
- 스케줄이 안 돌면 **`apps.scheduler.run_scheduler`** 프로세스가 살아 있는지 확인 (`ps aux | grep apps.scheduler` 또는 `grep run_scheduler`).
- 실행 기록: `.cron/job_runs.jsonl` / 다음 실행 시각: `.cron/jobs.json`의 `next_run_at`.
