#!/usr/bin/env python3
"""v12 교사 답변 자동 검증(형식·인용·정답 힌트 반영) — yunsur_v12 README §2.4.

  python3 scripts/verify_v12.py

내용 검증(문장이 인용 문서에 실제로 있는가)은 이 다음에 사람/Claude 가 한다.
출력: finetune_datasets/v12/verified_auto.jsonl (행마다 ok·reasons)
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "finetune_datasets" / "v12"
NO_DOC = "제공된 문서에는 질문이 찾는 연구가 없습니다"


def check(ans: str, gold_nums: list[int], n_docs: int) -> list[str]:
    bad = []
    secs = re.findall(r"^###\s*(서론|본론|결론)\s*$", ans, re.M)
    if secs != ["서론", "본론", "결론"]:
        bad.append(f"섹션:{secs}")
    body = ans.split("### 본론", 1)[-1].split("### 결론", 1)[0] if "### 본론" in ans else ""
    items = re.findall(r"^\s*(\d+)\.\s", body, re.M)
    if not (1 <= len(items) <= 4):
        bad.append(f"본론항목:{len(items)}")
    cites = [int(x) for x in re.findall(r"\[문서\s*(\d+)\]", ans)]
    if any(c < 1 or c > n_docs for c in cites):
        bad.append("인용범위")
    # 본론 각 항목에 인용이 있어야 한다
    blocks = re.split(r"^\s*\d+\.\s", body, flags=re.M)[1:]
    if any(not re.search(r"\[문서\s*\d+\]", b) for b in blocks):
        bad.append("항목무인용")
    if re.search(r"\b\d{4}\.\d{4,5}(v\d+)?\b", ans):
        bad.append("arXivID")
    if re.search(r"[{}]|정답 힌트|교사 전용", ans):
        bad.append("플레이스홀더/힌트누출")
    intro = ans.split("### 본론", 1)[0]
    if gold_nums:
        first = blocks[0] if blocks else ""
        if not any(re.search(rf"\[문서\s*{g}\]", first) for g in gold_nums):
            bad.append("정답이1번아님")
        if NO_DOC in intro:
            bad.append("정답있는데없다고함")
    else:
        if NO_DOC not in intro:
            bad.append("정답없는데안밝힘")
    return bad


def main() -> int:
    P = {json.loads(l)["src_pid"]: json.loads(l) for l in (D / "prompts.jsonl").read_text().splitlines() if l.strip()}
    T = [json.loads(l) for l in (D / "teacher.jsonl").read_text().splitlines() if l.strip()]
    out, why = [], Counter()
    for t in T:
        p = P[t["src_pid"]]
        n_docs = len(p["context_pids"])
        bad = check(t["answer"], t.get("gold_nums") or [], n_docs)
        why.update(b.split(":")[0] for b in bad)
        out.append({"src_pid": t["src_pid"], "ok": not bad, "reasons": bad, "gold": bool(t.get("gold_nums"))})
    (D / "verified_auto.jsonl").write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out))
    n_ok = sum(o["ok"] for o in out)
    print(f"교사 {len(out)} · 자동 통과 {n_ok} · 정답 있음 {sum(o['gold'] for o in out)}")
    print("탈락 사유:", dict(why))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
