#!/usr/bin/env python3
"""v12 RAG 학습 정답을 강한 교사(Groq gpt-oss-120b)로 만든다 — yunsur_v12 README §2.3.

  .venv/bin/python scripts/teacher_v12.py [--limit N]

- 입력은 capture_v12_prompts.py 가 저장한 **운영 메시지 그대로** + 교사 전용 지시(시스템 끝에 덧붙임).
  학습 데이터에는 교사 전용 지시를 넣지 않는다.
- 하루 한도(TPD)에 걸리면 Groq 이 알려준 시간만큼 기다렸다가 이어서 한다 — 며칠 동안 켜 둘 수 있다.
- 이어서 하기: 이미 답한 src_pid 는 건너뛴다.
출력: finetune_datasets/v12/teacher.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = Path(__file__).resolve().parent.parent
PIN = ROOT / "finetune_datasets" / "v12" / "prompts.jsonl"
OUT = ROOT / "finetune_datasets" / "v12" / "teacher.jsonl"
MODEL = "openai/gpt-oss-120b"

TEACHER_RULES = """

[교사 전용 추가 규칙 — 학습 정답의 품질 기준. 아래를 어기면 답이 버려진다]
1. 본론 각 항목의 **모든 문장**은 그 항목 끝에 단 `[문서 N]` 블록의 본문(제목 포함)에서 직접 확인할 수 있어야 한다. 확인할 수 없는 내용은 쓰지 않는다 — 항목이 짧아져도 된다.
2. **질문 문장에 들어 있는 묘사를 문서 내용인 것처럼 옮겨 쓰지 않는다.** 질문이 "두 모듈로 나누어 도구를 호출한다"고 해도, 문서 블록에 그 말이 없으면 쓰지 않는다.
3. 같은 논문이 여러 `[문서 N]` 에 나뉘어 있으면 문장 근거가 있는 번호를 모두 단다(예: `[문서 1][문서 4]`). 다른 논문의 내용을 섞지 않는다.
4. 아래 [정답 힌트]를 따른다 (힌트 문구 자체는 답에 쓰지 않는다):
   - 정답 문서가 주어지면: 본론 1번 항목을 그 논문으로 하고 발췌에 있는 내용만 쓴다. 질문이 묻는 세부가 발췌에 없으면 "제공된 발췌에는 그 세부가 나오지 않습니다" 정도로 짧게 밝힌다 — **그 논문이 질문의 연구라는 사실은 부정하지 않는다.** 관련 있는 다른 문서는 0~2개 더 쓸 수 있다.
   - 정답 문서가 없다고 하면: 서론 첫 문장에 "제공된 문서에는 질문이 찾는 연구가 없습니다."라고 쓰고, 본론에는 주제가 가장 가까운 문서만(최대 2개) 그 문서 내용대로 적으며, 결론에서도 문서가 질문에 답한다고 말하지 않는다.
5. 결론은 본론에 쓴 내용만 종합한다. 새 주장·평가·일반론을 더하지 않는다.
6. 인용은 `[문서 N]` 형식만 쓴다. arXiv ID 를 쓰지 않는다. 출력 템플릿(### 서론 / ### 본론 / ### 결론)을 그대로 따른다."""


def wait_hint(msg: str) -> float:
    m = re.search(r"try again in (?:(\d+)h)?(?:(\d+)m)?([\d.]+)s", msg)
    if not m:
        return 600.0
    h, mi, s = (float(x) if x else 0.0 for x in m.groups())
    return h * 3600 + mi * 60 + s + 15


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--pace", type=float, default=25.0, help="호출 사이 대기(초) — 분당 8K 토큰 한도")
    ap.add_argument("--base-url", default="", help="OpenAI 호환 서버(vLLM 등). 주면 Groq 대신 이것을 쓴다")
    ap.add_argument("--key-file", default="", help="서버 API 키가 든 파일 경로(키를 명령줄에 남기지 않는다)")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--follow", action="store_true", help="캡처가 끝날 때까지 새 프롬프트를 따라가며 처리")
    args = ap.parse_args()
    if args.base_url:
        return run_openai(args)

    import core.config.agent_config  # noqa: F401  (.env 로드)
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_groq import ChatGroq

    llm = ChatGroq(model=MODEL, api_key=os.getenv("GROQ_API_KEY"), temperature=0.3, max_retries=0)
    rows = [json.loads(l) for l in PIN.read_text().splitlines() if l.strip()]
    rows = [r for r in rows if r.get("route") == "direct_answer/B" and r.get("user") and not r.get("eval_leak")]
    done = set()
    if OUT.exists():
        done = {json.loads(l)["src_pid"] for l in OUT.read_text().splitlines() if l.strip()}
    todo = [r for r in rows if r["src_pid"] not in done]
    if args.limit:
        todo = todo[: args.limit]
    print(f"teacher={MODEL} 대상 {len(rows)} · 남음 {len(todo)}", flush=True)

    with OUT.open("a", encoding="utf-8") as w:
        for k, r in enumerate(todo, 1):
            gold_nums = [i + 1 for i, p in enumerate(r["context_pids"]) if p == r["src_pid"]]
            hint = (f"\n\n[정답 힌트] 질문이 찾는 논문은 {''.join(f'[문서 {n}]' for n in gold_nums)} 이다."
                    if gold_nums else "\n\n[정답 힌트] 질문이 찾는 논문은 제공된 문서에 없다.")
            msgs = [SystemMessage(content=r["system"] + TEACHER_RULES + hint), HumanMessage(content=r["user"])]
            while True:
                try:
                    t0 = time.time()
                    resp = llm.invoke(msgs)
                    break
                except Exception as exc:
                    s = str(exc)
                    if "rate_limit" in s or "429" in s:
                        wt = wait_hint(s) if ("per day" in s or "TPD" in s) else 60.0
                        print(f"  한도 대기 {wt / 60:.1f}분: {s[:140]}", flush=True)
                        time.sleep(wt)
                        continue
                    print(f"  오류 {r['src_pid']}: {s[:200]}", flush=True)
                    resp = None
                    break
            if resp is None:
                continue
            text = str(resp.content or "").strip()
            usage = (getattr(resp, "response_metadata", {}) or {}).get("token_usage", {})
            w.write(json.dumps({"src_pid": r["src_pid"], "gold_nums": gold_nums, "answer": text, "tokens": usage.get("total_tokens"),
                                "elapsed": round(time.time() - t0, 1)}, ensure_ascii=False) + "\n")
            w.flush()
            print(f"[{k}/{len(todo)}] {r['src_pid']} tok={usage.get('total_tokens')} len={len(text)}", flush=True)
            time.sleep(args.pace)
    return 0


def build_messages(r: dict) -> tuple[list[dict], list[int]]:
    gold_nums = [i + 1 for i, p in enumerate(r["context_pids"]) if p == r["src_pid"]]
    hint = (f"\n\n[정답 힌트] 질문이 찾는 논문은 {''.join(f'[문서 {n}]' for n in gold_nums)} 이다."
            if gold_nums else "\n\n[정답 힌트] 질문이 찾는 논문은 제공된 문서에 없다.")
    return [{"role": "system", "content": r["system"] + TEACHER_RULES + hint},
            {"role": "user", "content": r["user"]}], gold_nums


def run_openai(args) -> int:
    """vLLM 등 OpenAI 호환 서버로 병렬 생성 (RunPod H100 gpt-oss-120b)."""
    import subprocess
    import threading
    from concurrent.futures import ThreadPoolExecutor

    import requests

    key = Path(args.key_file).read_text().strip() if args.key_file else ""
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    url = args.base_url.rstrip("/") + "/chat/completions"
    lock = threading.Lock()

    def done_ids() -> set:
        if not OUT.exists():
            return set()
        return {json.loads(l)["src_pid"] for l in OUT.read_text().splitlines() if l.strip()}

    def one(r: dict) -> None:
        msgs, gold_nums = build_messages(r)
        body = {"model": MODEL, "messages": msgs, "temperature": 0.3, "max_tokens": 6000, "reasoning_effort": "medium"}
        for attempt in range(4):
            try:
                t0 = time.time()
                resp = requests.post(url, json=body, headers=headers, timeout=600)
                resp.raise_for_status()
                j = resp.json()
                msg = j["choices"][0]["message"]
                text = (msg.get("content") or "").strip()
                if not text:
                    raise ValueError(f"빈 응답 finish={j['choices'][0].get('finish_reason')}")
                row = {"src_pid": r["src_pid"], "gold_nums": gold_nums, "answer": text,
                       "tokens": (j.get("usage") or {}).get("total_tokens"),
                       "elapsed": round(time.time() - t0, 1), "teacher": f"{MODEL}@vllm"}
                with lock:
                    with OUT.open("a", encoding="utf-8") as w:
                        w.write(json.dumps(row, ensure_ascii=False) + "\n")
                print(f"  {r['src_pid']} tok={row['tokens']} {row['elapsed']}s", flush=True)
                return
            except Exception as exc:
                print(f"  재시도 {r['src_pid']} ({attempt + 1}): {str(exc)[:160]}", flush=True)
                time.sleep(10 * (attempt + 1))

    while True:
        rows = [json.loads(l) for l in PIN.read_text().splitlines() if l.strip()]
        rows = [r for r in rows if r.get("route") == "direct_answer/B" and r.get("user") and not r.get("eval_leak")]
        have = done_ids()
        todo = [r for r in rows if r["src_pid"] not in have]
        if args.limit:
            todo = todo[: args.limit]
        capturing = subprocess.run(["pgrep", "-f", "capture_v12_prompts"], capture_output=True).returncode == 0
        print(f"[{time.strftime('%H:%M:%S')}] 대상 {len(rows)} · 완료 {len(have)} · 이번 {len(todo)} · 캡처중={capturing}", flush=True)
        if todo:
            with ThreadPoolExecutor(max_workers=args.workers) as ex:
                list(ex.map(one, todo))
        if not args.follow or (not capturing and not todo):
            break
        if not todo:
            time.sleep(60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
