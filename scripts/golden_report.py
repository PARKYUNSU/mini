"""golden set 리포트 — 회귀 실행 결과에서 꼭 들어가야 할 논문 · 서술이 빠졌는지, 빠졌으면 어느 단계에서 빠졌는지.

사용: python scripts/golden_report.py GOLDEN.json RESULT1.jsonl [RESULT2.jsonl ...]
GOLDEN.json: {"W02": {"papers": ["2502.05239"], "must": ["Scott"]}, ...}  ("must" 는 답 본문에 있어야 할 문자열, 대소문자 무시)
여러 결과 파일 = 같은 질문을 여러 번 돌린 것(실행 간 흔들림을 본다).
"""
from __future__ import annotations

import json
import re
import sys


def _stage(r: dict, name: str) -> dict:
    return next((s for s in r.get("trace") or [] if isinstance(s, dict) and s.get("stage") == name), {})


def _base(pid: str) -> str:
    return re.sub(r"v\d+$", "", str(pid))


def why_missing(r: dict, pid: str) -> str:
    """빠진 단계: 검색 · 선별 · 거르기 · 27B 판정 · 답 모델 · 외부 검색."""
    ids = lambda name, key: {_base(x) for x in _stage(r, name).get(key) or []}
    if pid in {p["arxiv"] for p in _stage(r, "ext_promote").get("promoted") or []}:
        return "외부 승격됨 · 답 모델이 안 씀"
    if pid not in ids("search", "ids") | ids("router", "ids"):
        agg = _stage(r, "judge").get("agg")
        return f"DB 검색에 안 나옴(판정 {agg or '안 함'}{' — 직접 있음이라 외부 검색 안 돎' if agg == 'a' else ''})"
    if pid not in ids("select", "ids"):
        return "선별(15→5)에서 빠짐"
    if pid not in ids("filter", "docs"):
        return "관련도 거르기에서 빠짐"
    ctx = r.get("numbered_context") or ""
    num = {_base(p): n for n, p in re.findall(r"\[문서 (\d+)\]\n(?:\[[^\]]*\]\n)*?\[(\d{4}\.\d{4,5}(?:v\d+)?)", ctx)}
    lab = (_stage(r, "judge").get("doc_labels") or {}).get(num.get(pid, ""))
    if lab == "N":
        return "27B 무관 판정 → 답 칸 없음"
    return f"컨텍스트에 있음(판정 {lab or '-'}) · 답 모델이 안 씀"


def main(golden_path: str, results: list[str]) -> None:
    golden = json.load(open(golden_path))
    runs = [{json.loads(l)["id"]: json.loads(l) for l in open(f)} for f in results]
    miss_total = 0
    print(f"# golden 리포트 — 실행 {len(runs)} 번")
    for qid, g in golden.items():
        cells = []
        for k, run in enumerate(runs, 1):
            r = run.get(qid)
            if not r:
                cells.append(f"  실행{k}: 결과 없음")
                continue
            body = re.sub(r"<[^>]+>", "", r.get("answer") or "").split("📎")[0]
            bad = [f"{p}: {why_missing(r, p)}" for p in g.get("papers", []) if p not in body]
            bad += [f"서술 '{m}' 없음" for m in g.get("must", []) if m.lower() not in body.lower()]
            miss_total += len(bad)
            cells.append(f"  실행{k}: " + ("통과" if not bad else " / ".join(bad)))
        print(f"- {qid}\n" + "\n".join(cells))
    print(f"\n누락 합계 {miss_total}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
