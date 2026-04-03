"""
Tuya 스마트 플러그(아울렛) 켜기/끄기 (tinytuya).

[제어 방식]
  TUYA_CONTROL_MODE=local (기본) — LAN TCP 6668 (기기가 포트를 열어야 함)
  TUYA_CONTROL_MODE=cloud — IoT Open API 경유 (앱과 같은 클라우드 경로; 6668 불필요)

[필수 환경 변수 — .env]
  TUYA_DEVICE_ID        기기 Device ID (Tuya IoT / tinytuya 스캔으로 확인)
  TUYA_LOCAL_KEY        local 모드일 때 필수. cloud 모드에서는 미사용 가능
  TUYA_PLUG_IP          플러그 LAN IP (예: 192.168.0.200) — 공유기 DHCP와 반드시 일치
  TUYA_PLUG_PORT        Tuya 로컬 TCP 포트 (기본 6668)
  TUYA_PROTOCOL_VERSION 프로토콜 버전 문자열 (기본 3.3, 기기에 따라 3.1 / 3.4)
  TUYA_SOCKET_TIMEOUT   TCP 타임아웃 초 (기본 8) — 응답 없을 때 터미널이 멈춘 것처럼 보이지 않게
  TUYA_SOCKET_RETRIES   tinytuya 재시도 횟수 (기본 2, 기본값 5면 최대 수십 초 대기)
  TUYA_PLUG_DPS         스위치 DPS 번호 (기본 1). 멀티 갱/다른 펌웨어는 2 등으로 변경
  TUYA_PLUG_STATUS_DELAY  제어 후 status() 전 대기 초 (기본 2). 901 방지용
  TUYA_PLUG_RELAX_VERIFY 1 이면 status 실패(901)여도 '명령 전송' 안내 (기본: 901이면 자동 완화)
  TUYA_PLUG_STRICT_VERIFY 1 이면 status 실패 시 반드시 오류로 처리 (901도 실패)

[클라우드 모드 전용 — TUYA_CONTROL_MODE=cloud]
  TUYA_CLOUD_ACCESS_ID     IoT 콘솔 Access ID (API Key)
  TUYA_CLOUD_ACCESS_SECRET IoT 콘솔 Access Secret
  TUYA_CLOUD_REGION        us / eu / cn … (Western America면 us)
  TUYA_CLOUD_DP_CODE       기본 switch_1 (devices.json mapping.code 와 동일)

[설치]
  pip install tinytuya

[스케줄 연동]
  run_scheduler.py + cron이 prompt를 그래프에 넣을 때, is_scheduled=True라도
  이 도구는 라우터 화이트리스트로 use_existing_tool 경로를 탑니다.
  예: job prompt = "스마트 플러그 켜줘" / "스탠드 불 꺼줘"
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path


def _load_project_dotenv() -> None:
    """mini/.env 로드. agent_bot 없이 `python -c`·스크립트로 호출해도 TUYA_* 가 보이게 함."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    mini_root = Path(__file__).resolve().parents[1]
    load_dotenv(mini_root / ".env")


def _parse_action(user_request: str) -> str | None:
    """user_request에서 on/off 추출. 못 찾으면 None."""
    r = (user_request or "").lower()
    # 영문
    if re.search(r"\b(on|turn\s*on|power\s*on)\b", r):
        return "on"
    if re.search(r"\b(off|turn\s*off|power\s*off)\b", r):
        return "off"
    # 한국어 (긴 패턴 우선)
    off_kw = ("꺼", "끄", "종료", "소등", "불 끄", "불꺼", "전원 끄")
    on_kw = ("켜", "켜줘", "켜 줘", "점등", "불 켜", "전원 켜", "가동")
    if any(k in user_request for k in off_kw):
        return "off"
    if any(k in user_request for k in on_kw):
        return "on"
    return None


def _dps_switch_value(dps: dict, switch_dps: int):
    """dps 키가 str/int 혼용일 수 있음."""
    if not dps:
        return None
    k_str = str(switch_dps)
    if k_str in dps:
        return dps[k_str]
    if switch_dps in dps:
        return dps[switch_dps]
    return None


def _dps_from_response(msg: dict | None) -> dict | None:
    """CONTROL/STATUS 응답에서 dps dict 추출 (3.4는 data.dps)."""
    if not isinstance(msg, dict) or msg.get("Err"):
        return None
    dps = msg.get("dps")
    if isinstance(dps, dict):
        return dps
    data = msg.get("data")
    if isinstance(data, dict) and isinstance(data.get("dps"), dict):
        return data["dps"]
    return None


def _coerce_on_off(v) -> bool | None:
    """DPS 값을 켜짐/꺼짐으로 해석. 알 수 없으면 None."""
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(int(v))
    s = str(v).strip().lower()
    if s in ("true", "1", "on", "yes"):
        return True
    if s in ("false", "0", "off", "no"):
        return False
    return None


def _run_tuya_cloud_control(device_id: str, want_on: bool) -> str:
    """IoT Open API로 스위치 명령 전송 (LAN TCP 없이 앱과 유사 경로)."""
    import tinytuya

    key = os.getenv("TUYA_CLOUD_ACCESS_ID", "").strip()
    secret = os.getenv("TUYA_CLOUD_ACCESS_SECRET", "").strip()
    if not key or not secret:
        return (
            "도구 오류: TUYA_CONTROL_MODE=cloud 일 때 .env에 "
            "TUYA_CLOUD_ACCESS_ID, TUYA_CLOUD_ACCESS_SECRET "
            "(IoT 개발 콘솔 Access ID / Secret)를 넣으세요."
        )
    region = (os.getenv("TUYA_CLOUD_REGION", "us").strip().lower() or "us")
    dp_code = (os.getenv("TUYA_CLOUD_DP_CODE", "switch_1").strip() or "switch_1")

    try:
        cloud = tinytuya.Cloud(
            apiRegion=region,
            apiKey=key,
            apiSecret=secret,
            apiDeviceID=device_id,
        )
    except TypeError as e:
        return f"스마트 플러그(클라우드) 초기화 오류: {e}"

    err = getattr(cloud, "error", None)
    if err:
        return f"스마트 플러그(클라우드) 토큰/연결 오류: {err}"

    payload = {"commands": [{"code": dp_code, "value": bool(want_on)}]}
    r = cloud.sendcommand(device_id, payload)
    if not isinstance(r, dict):
        return f"스마트 플러그(클라우드) 응답 이상: {r!r}"
    if r.get("success"):
        if want_on:
            return "스마트 플러그(클라우드) 전원 켜기 요청을 보냈습니다."
        return "스마트 플러그(클라우드) 전원 끄기 요청을 보냈습니다."
    msg = r.get("msg") or r.get("code") or r
    return (
        f"스마트 플러그(클라우드) 제어 실패: {msg}. "
        "IoT 콘솔에서 기기가 **Online**인지, 프로젝트 **Data Center**(예: Western America → us)와 "
        "Smart Life 계정 연동이 맞는지 확인하세요."
    )


def run(user_request: str = "") -> str:
    """
    스마트 플러그 on/off. user_request 문맥에서 켜기/끄기를 추론합니다.

    매개변수:
        user_request: 예) "스탠드 불 켜줘", "스마트 플러그 꺼줘", "turn off the plug"
    """
    _load_project_dotenv()

    try:
        import tinytuya
    except ImportError:
        return (
            "도구 오류: tinytuya 패키지가 없습니다. "
            "맥 미니에서 `pip install tinytuya` 후 다시 시도하세요."
        )

    device_id = os.getenv("TUYA_DEVICE_ID", "").strip()
    local_key = os.getenv("TUYA_LOCAL_KEY", "").strip()
    ip = os.getenv("TUYA_PLUG_IP", os.getenv("TUYA_IP", "192.168.0.200")).strip()
    ver_raw = os.getenv("TUYA_PROTOCOL_VERSION", "3.3").strip()
    try:
        sock_timeout = float(os.getenv("TUYA_SOCKET_TIMEOUT", "8").strip() or "8")
    except ValueError:
        sock_timeout = 8.0
    try:
        sock_retries = int(os.getenv("TUYA_SOCKET_RETRIES", "2").strip() or "2")
    except ValueError:
        sock_retries = 2
    sock_retries = max(1, min(sock_retries, 10))
    try:
        switch_dps = int(os.getenv("TUYA_PLUG_DPS", "1").strip() or "1")
    except ValueError:
        switch_dps = 1
    try:
        plug_port = int(os.getenv("TUYA_PLUG_PORT", "6668").strip() or "6668")
    except ValueError:
        plug_port = 6668

    action = _parse_action(user_request or "")
    if not action:
        return (
            "스마트 플러그: 요청에서 켜기/끄기를 알 수 없습니다. "
            "예: '스마트 플러그 켜줘', '스탠드 불 꺼줘', 'turn on'."
        )

    control_mode = os.getenv("TUYA_CONTROL_MODE", "local").strip().lower()
    if control_mode == "cloud":
        if not device_id:
            return "도구 오류: TUYA_CONTROL_MODE=cloud 일 때도 TUYA_DEVICE_ID 가 필요합니다."
        return _run_tuya_cloud_control(device_id, action == "on")

    if not device_id or not local_key:
        return (
            "도구 오류: .env에 TUYA_DEVICE_ID, TUYA_LOCAL_KEY 를 설정하세요. "
            "(로컬 TCP가 안 되면 TUYA_CONTROL_MODE=cloud 로 전환 가능)"
        )

    try:
        ver = float(ver_raw)
    except ValueError:
        ver = 3.3

    try:
        try:
            status_delay = float(os.getenv("TUYA_PLUG_STATUS_DELAY", "2").strip() or "2")
        except ValueError:
            status_delay = 2.0
        strict_verify = os.getenv("TUYA_PLUG_STRICT_VERIFY", "").strip().lower() in (
            "1",
            "true",
            "yes",
        )
        relax = os.getenv("TUYA_PLUG_RELAX_VERIFY", "").strip().lower() in (
            "1",
            "true",
            "yes",
        )

        def _make_outlet():
            dev = tinytuya.OutletDevice(
                device_id,
                ip,
                local_key,
                connection_timeout=sock_timeout,
                port=plug_port,
            )
            dev.set_version(ver)
            dev.set_socketRetryLimit(sock_retries)
            dev.set_socketRetryDelay(1)
            dev.set_socketTimeout(sock_timeout)
            dev.set_socketPersistent(False)
            return dev

        def _verify_dps(dps: dict, want: bool) -> str | None:
            raw = _dps_switch_value(dps, switch_dps)
            got = _coerce_on_off(raw)
            if got is None:
                return (
                    "스마트 플러그: 기기 응답은 있으나 전원 상태를 해석할 수 없습니다. "
                    f"dps={dps!r} (스위치 DPS가 1이 아니면 .env에 TUYA_PLUG_DPS=번호 설정)"
                )
            if got != want:
                return (
                    f"스마트 플러그: 기기가 요청대로 바뀌지 않았습니다. "
                    f"요청={'ON' if want else 'OFF'}, dps[{switch_dps}]={raw!r}. "
                    f"TUYA_PROTOCOL_VERSION·TUYA_PLUG_DPS·IP를 확인하세요."
                )
            return None

        want_on = action == "on"

        # 1) 제어만 (연결 종료) — 응답에 dps가 오는 기기는 여기서 검증
        d = _make_outlet()
        ctrl = None
        try:
            ctrl = d.turn_on(switch=switch_dps) if want_on else d.turn_off(switch=switch_dps)
        finally:
            try:
                d.close()
            except Exception:
                pass

        if isinstance(ctrl, dict) and ctrl.get("Err"):
            if str(ctrl.get("Err")) == "901":
                return (
                    f"스마트 플러그: 맥에서 `{ip}:{plug_port}`(Tuya 로컬 TCP)로 **연결 자체가 안 됩니다**. "
                    f"(3.1/3.3/3.4와 무관하게 **IP·네트워크** 문제일 때가 많습니다.)\n"
                    f"① 공유기에서 '플러그' 기기의 **지금 사설 IP**를 보고 `.env`의 TUYA_PLUG_IP와 똑같이 맞추기\n"
                    f"② 터미널: `ping -c 2 {ip}` / `nc -vz {ip} {plug_port}`\n"
                    f"③ 맥이 플러그와 **같은 서브넷**(예: 둘 다 192.168.0.x)·**게스트 Wi-Fi 아님** 확인"
                )
            return f"스마트 플러그 제어 실패 — {ctrl}"

        dps_c = _dps_from_response(ctrl)
        if dps_c:
            err = _verify_dps(dps_c, want_on)
            if err:
                return err
            if want_on:
                return "스마트 플러그(스탠드 등) 전원을 켰습니다."
            return "스마트 플러그(스탠드 등) 전원을 껐습니다."

        # 2) 별도 연결로 status (일부 기기는 첫 연결 직후 두 번째 쿼리만 901 → 쉬었다가 재접속)
        time.sleep(max(0.0, status_delay))
        d2 = _make_outlet()
        st = None
        try:
            st = d2.status()
        finally:
            try:
                d2.close()
            except Exception:
                pass

        err901 = isinstance(st, dict) and str(st.get("Err")) == "901"
        if isinstance(st, dict) and st.get("Err") and not err901:
            return (
                f"스마트 플러그: 명령은 보냈지만 상태 조회 실패 — {st}. "
                f"IP·TUYA_PROTOCOL_VERSION·local_key를 확인하세요."
            )

        if isinstance(st, dict) and not st.get("Err"):
            dps = _dps_from_response(st) or {}
            err = _verify_dps(dps, want_on)
            if err:
                return err
            if want_on:
                return "스마트 플러그(스탠드 등) 전원을 켰습니다."
            return "스마트 플러그(스탠드 등) 전원을 껐습니다."

        # status None / 901 등: 일부 기기는 DP_QUERY만 거부하고 CONTROL은 동작
        if st is None or err901:
            if strict_verify and not relax:
                return (
                    f"스마트 플러그: 상태 조회 불가 — {st!r}. "
                    f"명령은 이미 전송됐을 수 있습니다. Smart Life로 확인하거나 "
                    f"TUYA_PLUG_STATUS_DELAY=3~5, TUYA_PLUG_RELAX_VERIFY=1 을 시도하세요."
                )
            act = "켜기" if want_on else "끄기"
            return (
                f"스마트 플러그: {act} 명령은 LAN으로 전송했습니다. "
                f"이 모델은 로컬 상태 조회가 901로 실패하는 경우가 있어, 실제 전원은 Smart Life 앱으로 확인해 주세요. "
                f"(오류로만 보고 싶으면 TUYA_PLUG_STRICT_VERIFY=1)"
            )

        return (
            "스마트 플러그: 제어 후 상태를 받지 못했습니다. "
            "TUYA_PROTOCOL_VERSION·IP·TUYA_PLUG_STATUS_DELAY 를 조정해 보세요."
        )
    except Exception as e:
        return f"스마트 플러그 제어 오류: {type(e).__name__}: {e}"


if __name__ == "__main__":
    import sys

    req = os.environ.get("USER_REQUEST", " ".join(sys.argv[1:]) or "")
    print(run(req))
