#!/usr/bin/env python3
"""v12 교사 답변의 내용 근거 검증(LLM) — yunsur_v12 README §2.4.

  .venv/bin/python scripts/verify_v12_llm.py --base-url <vLLM /v1>

자동 검증(verify_v12.py)을 통과한 답만 본다. 본론 각 항목의 문장이 그 항목이 인용한 [문서 N] 블록에서
확인되는지 항목별로 판정한다. 하나라도 아니면 탈락. Claude 가 무작위 표본으로 이 판정기의 정확도를 따로 잰다.
출력: finetune_datasets/v12/verified_llm.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "finetune_datasets" / "v12"
MODEL = "openai/gpt-oss-120b"

PROMPT = """너는 엄격한 사실 검증자다. 아래 [참고 문서]와 [답변]을 비교하라.

[답변]의 '### 본론' 각 번호 항목에 대해: 그 항목의 모든 주장(방법·구성·결과·숫자·이름)이 **그 항목 끝에 인용된 [문서 N] 블록의 본문에서 직접 확인되는가**?
- 다른 문서 블록에만 있는 내용, 문서에 없는 내용, 질문 문장에서만 온 묘사가 하나라도 있으면 supported=false.
- 표현을 바꾼 요약은 괜찮다. 일반적인 연결 문장("기존 대비 차별화된다" 같은 평가)은 문서가 그런 대비를 말할 때만 허용한다.
'### 결론'도 본론에 없는 새 사실 주장을 하면 conclusion_ok=false.

JSON 하나만 출력하라:
{{"items": [{{"n": 1, "supported": true|false, "issue": "<짧게>"}}, ...], "conclusion_ok": true|false}}

[참고 문서와 질문]
{user}

[답변]
{answer}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--workers", type=int, default=32)
    args = ap.parse_args()
    url = args.base_url.rstrip("/") + "/chat/completions"

    P = {json.loads(l)["src_pid"]: json.loads(l) for l in (D / "prompts.jsonl").read_text().splitlines() if l.strip()}
    T = {json.loads(l)["src_pid"]: json.loads(l) for l in (D / "teacher.jsonl").read_text().splitlines() if l.strip()}
    A = [json.loads(l) for l in (D / "verified_auto.jsonl").read_text().splitlines() if l.strip()]
    todo = [a["src_pid"] for a in A if a["ok"]]
    out_path = D / "verified_llm.jsonl"
    done = set()
    if out_path.exists():
        done = {json.loads(l)["src_pid"] for l in out_path.read_text().splitlines() if l.strip()}
    todo = [p for p in todo if p not in done]
    lock = threading.Lock()
    print(f"검증 대상 {len(todo)}", flush=True)

    def one(pid: str) -> None:
        body = {"model": MODEL, "temperature": 0.0, "max_tokens": 4000, "reasoning_effort": "medium",
                "messages": [{"role": "user", "content": PROMPT.format(user=P[pid]["user"], answer=T[pid]["answer"])}]}
        for attempt in range(4):
            try:
                r = requests.post(url, json=body, timeout=600)
                r.raise_for_status()
                txt = r.json()["choices"][0]["message"].get("content") or ""
                m = re.search(r"\{.*\}", txt, re.S)
                v = json.loads(m.group(0))
                ok = bool(v.get("items")) and all(i.get("supported") for i in v["items"]) and bool(v.get("conclusion_ok"))
                with lock, out_path.open("a", encoding="utf-8") as w:
                    w.write(json.dumps({"src_pid": pid, "ok": ok, "verdict": v}, ensure_ascii=False) + "\n")
                print(f"  {pid} ok={ok}", flush=True)
                return
            except Exception as exc:
                print(f"  재시도 {pid} ({attempt + 1}): {str(exc)[:120]}", flush=True)
                time.sleep(5 * (attempt + 1))

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        list(ex.map(one, todo))
    rows = [json.loads(l) for l in out_path.read_text().splitlines() if l.strip()]
    print(f"완료: {len(rows)} 중 통과 {sum(r['ok'] for r in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
