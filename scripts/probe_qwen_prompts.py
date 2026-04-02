#!/usr/bin/env python3
"""
Ollama(Qwen 등)에 JSON 프롬프트 목록을 순서대로 보내 응답·간단 기대값을 검사합니다.

  cp tests/fixtures/qwen_probe_prompts.example.json tests/fixtures/qwen_probe_prompts.json
  # 필요 시 qwen_probe_prompts.json 편집 후:
  python scripts/probe_qwen_prompts.py
  python scripts/probe_qwen_prompts.py --file tests/fixtures/qwen_probe_prompts.example.json
  python scripts/probe_qwen_prompts.py --timeout 120 --num-predict 256

환경: OLLAMA_HOST, LOCAL_LLM_MODEL (agent_bot과 동일), ollama serve 필요.
JSON 항목에 선택: "timeout_sec", "num_predict" (해당 프롬프트만 덮어씀).

무한 대기 방지: 기본 num_predict=384, 프롬프트당 timeout(기본 90s). 타임아웃 시에도 Ollama 쪽 생성은
백그라운드에서 이어질 수 있어 ollama ps / 재시작으로 정리할 수 있습니다.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")


def _load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "prompts" not in data:
        raise SystemExit("JSON 최상위에 'prompts' 배열이 있어야 합니다.")
    return data


def _check(item: dict, text: str) -> tuple[bool, str]:
    tid = item.get("id", "?")
    if item.get("expect_non_empty") and not (text or "").strip():
        return False, f"[{tid}] expect_non_empty 실패 (빈 응답)"
    min_c = item.get("min_chars")
    if min_c is not None and len((text or "").strip()) < int(min_c):
        return False, f"[{tid}] min_chars 미달 ({len(text)} < {min_c})"
    subs = item.get("expect_substrings_any")
    if subs:
        if not any(s in (text or "") for s in subs):
            return False, f"[{tid}] expect_substrings_any 불일치: 기대 {subs!r} 중 하나"
    return True, ""


def main() -> int:
    ap = argparse.ArgumentParser(description="Qwen/Ollama 프롬프트 프로브")
    ap.add_argument(
        "--file",
        "-f",
        type=Path,
        default=ROOT / "tests" / "fixtures" / "qwen_probe_prompts.json",
        help="프롬프트 JSON (없으면 example 경로 시도)",
    )
    ap.add_argument("--out", type=Path, default=None, help="JSONL 결과 저장 (선택)")
    ap.add_argument(
        "--timeout",
        type=float,
        default=float(os.getenv("PROBE_OLLAMA_TIMEOUT", "90")),
        help="프롬프트당 최대 대기 초 (기본 90, 환경변수 PROBE_OLLAMA_TIMEOUT)",
    )
    ap.add_argument(
        "--num-predict",
        type=int,
        default=int(os.getenv("PROBE_NUM_PREDICT", "384")),
        help="생성 토큰 상한(num_predict). 긴 답·thinking에 걸리면 줄이기 (기본 384)",
    )
    args = ap.parse_args()

    path = args.file
    if not path.is_file():
        ex = ROOT / "tests" / "fixtures" / "qwen_probe_prompts.example.json"
        if ex.is_file():
            print(f"경고: {path} 없음 → 예시 파일 사용: {ex}", file=sys.stderr)
            path = ex
        else:
            print(f"오류: 파일 없음 {args.file}", file=sys.stderr)
            return 2

    data = _load(path)
    prompts = data["prompts"]
    if not prompts:
        print("prompts 비어 있음")
        return 0

    from langchain_core.messages import HumanMessage
    from langchain_ollama import ChatOllama

    model = os.getenv("LOCAL_LLM_MODEL", "qwen3.5:9b")
    base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    out_lines: list[str] = []
    failed = 0
    for item in prompts:
        if not isinstance(item, dict):
            continue
        pid = item.get("id", "?")
        prompt = (item.get("prompt") or "").strip()
        if not prompt:
            print(f"[{pid}] SKIP: 빈 prompt")
            continue
        per_timeout = float(item.get("timeout_sec", args.timeout))
        num_pred = int(item.get("num_predict", args.num_predict))
        llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.1,
            num_predict=num_pred,
        )

        print(f"\n=== {pid} ===\nQ: {prompt[:200]}{'...' if len(prompt) > 200 else ''}")
        print(
            f"… 호출 중 (num_predict≤{num_pred}, 타임아웃 {per_timeout}s) …",
            flush=True,
        )
        msgs = [HumanMessage(content=prompt)]

        def _call():
            return llm.invoke(msgs)

        try:
            with ThreadPoolExecutor(max_workers=1) as pool:
                fut = pool.submit(_call)
                r = fut.result(timeout=per_timeout)
            text = (r.content or "").strip()
        except FuturesTimeout:
            err = f"타임아웃 ({per_timeout}s 초과) — Ctrl+C 후 --timeout·--num-predict 조정 또는 Ollama 로그 확인"
            print(f"FAIL: {err}")
            failed += 1
            out_lines.append(json.dumps({"id": pid, "ok": False, "error": err}, ensure_ascii=False))
            continue
        except Exception as e:  # noqa: BLE001
            print(f"FAIL invoke: {e}")
            failed += 1
            out_lines.append(json.dumps({"id": pid, "ok": False, "error": str(e)}, ensure_ascii=False))
            continue
        preview = text.replace("\n", " ")[:400]
        print(f"A: {preview}{'...' if len(text) > 400 else ''}")
        ok, reason = _check(item, text)
        if ok:
            print("→ OK")
        else:
            print(f"→ {reason}")
            failed += 1
        rec = {"id": pid, "ok": ok, "response_len": len(text), "notes": item.get("notes")}
        out_lines.append(json.dumps(rec, ensure_ascii=False))

    if args.out:
        args.out.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        print(f"\n결과 저장: {args.out}")

    print(f"\n요약: {'전부 통과' if failed == 0 else f'실패 {failed}건'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
