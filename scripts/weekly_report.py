"""주간 점검 한 줄 (docs/experiments/foundation_1031 §6) — `weekly_check.sh` 가 부른다.

eval_e2e_ko 결과(`results/<label>.jsonl`)에서 사람 판정 없이 셀 수 있는 지표만 뽑아
`docs/experiments/foundation_1031/weekly.md` 표에 붙일 마크다운 한 줄을 출력한다.
인용은 답 **본문**(📎 외부 검색 목록 앞)만 센다 — 외부 목록의 ID 가 정답과 겹쳐도 답이 찾은 게 아니다.
"""
from __future__ import annotations

import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "docs/experiments/e2e_ko_1008/results"
GOLD = ROOT / "docs/experiments/real_eval_1013/gold.jsonl"
STAGES = ("router", "query", "search", "select", "judge", "answer", "rewrite")
HEADER = ("| 날짜 | 커밋 | 문항 | 검색 정답 | 답 정답 인용 | '없음' 답 | 컨텍스트 밖 인용 | 시간 중앙 | "
          + " · ".join(STAGES) + " 중앙(s) | 오류 |\n|" + "---|" * 10)
_ID = re.compile(r"\b(\d{4}\.\d{4,5})(?:v\d+)?\b")
_NODOC = ("찾을 수 없", "질문이 찾는 연구가 없")


def row(label: str) -> str:
    rows = [json.loads(l) for l in (RES / f"{label}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    gold = {g["id"]: set(g.get("relevant_papers") or []) for g in map(json.loads, GOLD.read_text(encoding="utf-8").splitlines())}
    has_gold = [r for r in rows if gold.get(r["id"])]
    body = {r["id"]: (r.get("answer") or "").split("📎")[0] for r in rows}
    cites = {i: set(_ID.findall(b)) for i, b in body.items()}
    ans_ok = sum(bool(cites[r["id"]] & gold[r["id"]]) for r in has_gold)
    out_ctx = sum(len(cites[r["id"]] - set(r.get("doc_ids") or r.get("context_papers") or [])) for r in rows)
    nodoc = sum(any(s in body[r["id"]] for s in _NODOC) for r in rows)
    per = {s: [] for s in STAGES}
    for r in rows:
        for name, sec in r.get("stages") or []:
            if name in per:
                per[name].append(sec)
    med = lambda xs: f"{statistics.median(xs):.1f}" if xs else "–"
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    errs = sum(bool(r.get("error")) for r in rows)
    return (f"| {label.removeprefix('weekly_')} | {commit} | {len(rows)} | {sum(r['ok'] for r in has_gold)}/{len(has_gold)} | "
            f"{ans_ok}/{len(has_gold)} | {nodoc} | {out_ctx} | {med([r['elapsed'] for r in rows])}s | "
            f"{' · '.join(med(per[s]) for s in STAGES)} | {errs} |")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--header":
        print(HEADER)
    else:
        print(row(sys.argv[1]))
