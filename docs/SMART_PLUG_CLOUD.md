# 스마트 플러그 — 클라우드 제어 모드

플러그가 **LAN TCP(6668 등)를 열지 않아** `tinytuya` 로컬 제어가 `Connection refused` / 901 인 경우, **앱과 같은 경로**로 IoT Open API를 쓸 수 있습니다.

## 전제

1. [Tuya IoT](https://iot.tuya.com) **Cloud 프로젝트**에 Smart Life 계정이 연동되어 있고  
2. **Device 리스트**에 기기가 보이며, 가능하면 상태가 **Online**  
3. 프로젝트 **Data Center**와 `TUYA_CLOUD_REGION`이 일치 (스크린에 **Western America** → `us`)

> 콘솔에만 **Offline**이고 앱은 되는 경우: 계정·리전 불일치, 연동 만료, 기기가 클라우드에 안 붙는 네트워크 문제 등을 먼저 점검하세요. **Offline이면 API도 실패할 수 있습니다.**

## `.env` 예시

```env
TUYA_CONTROL_MODE=cloud
TUYA_DEVICE_ID=ebcb91ucgoxlp8yy
TUYA_CLOUD_ACCESS_ID=여기에_Access_ID
TUYA_CLOUD_ACCESS_SECRET=여기에_Secret
TUYA_CLOUD_REGION=us
TUYA_CLOUD_DP_CODE=switch_1
```

- `TUYA_CLOUD_DP_CODE`: `devices.json`의 `mapping` → `code` (플러그 Air는 보통 `switch_1`)
- Access ID/Secret은 **IoT 콘솔 → 프로젝트 → Overview/Authorization** (위자드에 넣던 값과 동일)

## 테스트

```bash
cd "/Volumes/T7 Shield/mini"
.venv/bin/python -c "from agent_tools.smart_plug import run; print(run('스마트 플러그 켜줘'))"
```

## 로컬 vs 클라우드

| 모드 | 경로 | 조건 |
|------|------|------|
| `local` (기본) | 맥 → `플러그IP:6668` | 기기가 TCP 리슨 |
| `cloud` | 맥 → Tuya API → 클라우드 → 기기 | IoT 키 + 기기 Online |
