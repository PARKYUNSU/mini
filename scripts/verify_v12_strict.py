#!/usr/bin/env python3
"""v12 2차 엄격 검증 — 결론 과장·질문 묘사 끼워넣기·관련연구 귀속을 잡는다 (yunsur_v12 README §2.5).

  .venv/bin/python scripts/verify_v12_strict.py --base-url <vLLM /v1> --answers final_pass.jsonl --out verified_strict.jsonl [--ids a,b,...]

1차 근거 검증(verify_v12_llm.py)을 통과했지만 Claude 표본 감사에서 28% 가 결론 과장 등으로 틀렸다.
이 검증기는 Claude 판정 60건으로 먼저 보정한 뒤 쓴다.
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

D = Path(__file__).resolve().parent.parent / "finetune_datasets" / "v12"
MODEL = "openai/gpt-oss-120b"

PROMPT = """너는 학습 데이터 품질 검사관이다. [답변]이 [참고 문서]만으로 쓰였는지 아래 네 가지를 엄격히 검사하라.

A. 결론 과장: '### 결론'에 본론에 쓰지 않은 새 사실·평가·일반화가 있는가? 특히 "문서들이 질문의 방법/흐름을 구현한다", "모두 ~하도록 설계되었다", "~를 확인했다/입증했다"처럼 문서가 말하지 않은 연결·단정을 하는가?
B. 질문 묘사 끼워넣기: [사용자] 질문 문장에만 있고 참고 문서 블록에는 없는 표현·주장(방법 이름, 수치, 구성 요소, 효과)을 서론이 아닌 본론·결론에서 사실처럼 쓰는가? (서론에서 질문을 다시 말하는 것은 괜찮다)
C. 관련 연구 귀속: 문서 블록 중 관련 연구·참고문헌·다른 논문을 소개하는 부분(예: "X et al. proposed ...", 인용 목록)을 그 블록 논문의 기여인 것처럼 썼는가?
D. 가설·목표를 결과로: 문서가 가설·질문·계획으로 제시한 것을 연구 결과처럼 썼는가?

하나라도 해당하면 ok=false. JSON 하나만 출력하라:
{{"A": true|false, "B": true|false, "C": true|false, "D": true|false, "reason": "<해당 항목과 근거를 짧게>", "ok": true|false}}
(A~D 는 '문제가 있다' 면 true)

[참고 문서와 질문]
{user}

[답변]
{answer}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--answers", default="final_pass.jsonl")
    ap.add_argument("--out", default="verified_strict.jsonl")
    ap.add_argument("--ids", default="")
    ap.add_argument("--workers", type=int, default=32)
    args = ap.parse_args()
    url = args.base_url.rstrip("/") + "/chat/completions"

    P = {json.loads(l)["src_pid"]: json.loads(l) for l in (D / "prompts.jsonl").read_text().splitlines() if l.strip()}
    A = [json.loads(l) for l in (D / args.answers).read_text().splitlines() if l.strip()]
    if args.ids:
        want = set(args.ids.split(","))
        A = [a for a in A if a["src_pid"] in want]
    out_path = D / args.out
    done = set()
    if out_path.exists():
        done = {json.loads(l)["src_pid"] for l in out_path.read_text().splitlines() if l.strip()}
    todo = [a for a in A if a["src_pid"] not in done]
    lock = threading.Lock()
    print(f"엄격 검증 대상 {len(todo)}", flush=True)

    def one(a: dict) -> None:
        body = {"model": MODEL, "temperature": 0.0, "max_tokens": 4000, "reasoning_effort": "high",
                "messages": [{"role": "user", "content": PROMPT.format(user=P[a["src_pid"]]["user"], answer=a["answer"])}]}
        for attempt in range(4):
            try:
                r = requests.post(url, json=body, timeout=600)
                r.raise_for_status()
                txt = r.json()["choices"][0]["message"].get("content") or ""
                v = json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
                ok = not any(v.get(k) for k in "ABCD")
                with lock, out_path.open("a", encoding="utf-8") as w:
                    w.write(json.dumps({"src_pid": a["src_pid"], "ok": ok, "verdict": v}, ensure_ascii=False) + "\n")
                return
            except Exception as exc:
                print(f"  재시도 {a['src_pid']} ({attempt + 1}): {str(exc)[:120]}", flush=True)
                time.sleep(5 * (attempt + 1))

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        list(ex.map(one, todo))
    rows = [json.loads(l) for l in out_path.read_text().splitlines() if l.strip()]
    print(f"완료: {len(rows)} 중 통과 {sum(r['ok'] for r in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
