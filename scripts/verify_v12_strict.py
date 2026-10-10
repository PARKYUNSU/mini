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

PROMPT = """너는 학습 데이터 품질 검사관이다. [답변]이 [참고 문서]에 근거했는지 아래 네 가지 '심각한 문제'만 검사하라.
가벼운 마무리 문장("~에 기여한다", "유용한 기반을 제공한다", "중요하다"), 질문의 일반 주제어를 다시 쓰는 것, 본론 항목 제목을 짧게 붙인 라벨은 문제로 보지 않는다.

A. 결론의 잘못된 사실·연결: 결론이 본론·문서에 없는 **구체적 사실**(방법 구성, 수치, 실험 결과, '~을 확인/입증했다')을 주장하거나, 문서가 질문이 찾는 그 방법을 다루지 않는데 "문서들이 질문의 방법/흐름을 구현한다", "모두 ~하도록 설계되었다"처럼 **잘못 연결**하는가?
B. 질문 속 기술 내용의 이식: 질문 문장에만 있고 문서 블록에 없는 **구체적 기술 내용**(특정 모듈·기법·수치·효과)을 본론·결론에서 문서의 사실처럼 쓰는가?
C. 관련 연구 귀속: 문서 블록이 다른 논문을 소개하는 부분(관련 연구, "X et al. proposed", 참고문헌)을 그 블록 논문의 기여처럼 썼는가?
D. 가설·목표를 결과로: 문서가 가설·질문·계획으로 제시한 것을 연구 결과처럼 썼는가?
E. 억지 연결: 질문과 주제가 다른 문서(예: 의사결정 아키텍처 논문을 '심성' 질문에)를 질문의 답인 것처럼 본론·결론에서 엮는가? 또는 결론이 한 문서(예: 다른 논문 Vul-RAG)의 내용을 다른 문서(예: 리뷰 논문)의 내용인 것처럼 섞는가?
F. 빈 블록 채우기: 제목·저자·참고문헌 줄뿐이라 내용이 거의 없는 문서 블록을 인용하면서, 질문 문장에 있던 기술 내용(예: '순위 재조정', '두 모듈')으로 그 논문을 설명하는가? (제목에 있는 말은 써도 된다)

JSON 하나만 출력하라 (A~F 는 '심각한 문제가 있다' 면 true):
{{"A": true|false, "B": true|false, "C": true|false, "D": true|false, "E": true|false, "F": true|false, "reason": "<해당 항목과 근거를 짧게>", "ok": true|false}}

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
        body = {"model": MODEL, "temperature": 0.0, "max_tokens": 4000, "reasoning_effort": "medium",
                "messages": [{"role": "user", "content": PROMPT.format(user=P[a["src_pid"]]["user"], answer=a["answer"])}]}
        for attempt in range(4):
            try:
                r = requests.post(url, json=body, timeout=600)
                r.raise_for_status()
                txt = r.json()["choices"][0]["message"].get("content") or ""
                m = re.search(r"\{.*\}", txt, re.S)
                if not m:
                    raise ValueError("JSON 없음")
                v = json.loads(m.group(0))
                ok = not any(v.get(k) for k in "ABCDEF")
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
