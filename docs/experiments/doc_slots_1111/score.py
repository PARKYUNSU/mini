"""doc_slots_1111 채점.

    .venv/bin/python docs/experiments/doc_slots_1111/score.py pool   # 판정 풀(조건 없음) + judge_packet.md
    .venv/bin/python docs/experiments/doc_slots_1111/score.py        # judged.txt(k<공백>0|1|2)를 다 단 뒤 채점

주 지표는 canon 40 의 질문별 '본론이 인용한 2 논문 수'(처리 > 대조, 부호 검정). canon_1110 에서 이미
조건 모른 채 단 (질문, 논문) 라벨은 그대로 쓰고, 없는 쌍만 새로 판정한다.
"""
import importlib.util
import json
import random
import re
import statistics
import sys
from pathlib import Path

D = Path("docs/experiments/doc_slots_1111")
spec = importlib.util.spec_from_file_location("canon_score", "docs/experiments/canon_1110/score.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
CAN = Path("docs/experiments/canon_1110")


def body(t):
    m = re.search(r"본론\s*(?:</b>)?(.*?)(?:<b>\s*결론|###\s*결론|$)", t or "", re.S)
    return m.group(1) if m else (t or "")


def cited(t):
    return {S.norm(x) for x in re.findall(r"\d{4}\.\d{4,5}(?:v\d+)?", t or "")}


def items(t):
    return len(re.findall(r"(?m)^\s*\d+\.\s", body(t)))


def cut_off(t):
    """답이 문장 중간에서 끝났는가 — 마침표 · 닫는 괄호 · 인용으로 끝나지 않으면 잘린 것으로 본다."""
    s = re.sub(r"<[^>]+>", "", t or "").strip()
    return bool(s) and not re.search(r"[.!?。)\]]\s*$", s)


assert cited("a [2412.18004v1] b 2601.06519") == {"2412.18004", "2601.06519"}
assert items("<b>본론</b>\n1. a\n2. b\n<b>결론</b>\n1. x") == 2 and cut_off("끝나지 않은 문") and not cut_off("끝났다.[2412.18004v1]")


def known():
    """canon_1110 에서 단 (질문, 논문) 라벨."""
    P = {x["k"]: x for x in json.loads((CAN / "pool.json").read_text(encoding="utf-8"))}
    out = {}
    for l in (CAN / "judged.txt").read_text(encoding="utf-8").splitlines():
        if l.strip():
            k, v = l.split()
            if P[int(k)]["set"] == "canon":
                out[(P[int(k)]["q"], P[int(k)]["p"])] = int(v)
    return out


def pool():
    qs = S.tsv(CAN / "questions.tsv")
    a, b = S.rows("ds0_canon"), S.rows("ds1_canon")
    K = known()
    pairs = sorted({(q, p) for q in qs for r in (a[q], b[q]) for p in cited(body(r.get("answer")))} - set(K))
    random.Random(1111).shuffle(pairs)
    meta = S.corpus()
    out = [{"k": k, "q": q, "question": qs[q], "p": p, "title": meta.get(p, ("", ""))[0], "abstract": meta.get(p, ("", ""))[1]}
           for k, (q, p) in enumerate(pairs)]
    (D / "pool.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    by = {}
    for x in out:
        by.setdefault(x["q"], []).append(x)
    w = ["# doc_slots_1111 판정 묶음 — 조건 · 논문 ID 없음. 2 직접 다룸 · 1 관련(직접 아님) · 0 관련 없음\n"]
    for q, xs in by.items():
        w.append(f"\n## {q} — {xs[0]['question']}\n")
        w += [f"\n**[{x['k']}]** {re.sub(r'\s+', ' ', x['title'])}\n> {re.sub(r'\s+', ' ', x['abstract'])}\n" for x in xs]
    (D / "judge_packet.md").write_text("".join(w), encoding="utf-8")
    print(f"새로 판정할 쌍 {len(out)} · canon_1110 라벨 재사용 {len({(q, p) for q in qs for r in (a[q], b[q]) for p in cited(body(r.get('answer')))} & set(K))} · 제목 없음 {sum(not x['title'] for x in out)}")


def main():
    J = known()
    P = {x["k"]: x for x in json.loads((D / "pool.json").read_text(encoding="utf-8"))}
    for l in (D / "judged.txt").read_text(encoding="utf-8").splitlines():
        if l.strip():
            k, v = l.split()
            J[(P[int(k)]["q"], P[int(k)]["p"])] = int(v)
    a, b = S.rows("ds0_canon"), S.rows("ds1_canon")
    win = lose = 0
    tot = {n: [0, 0] for n in ("2", "1", "0", "항목", "본론 인용", "컨텍스트 밖 인용", "잘림", "칸 틀 적용")}
    for q in a:
        n2 = []
        for i, r in enumerate((a[q], b[q])):
            cs = cited(body(r.get("answer")))
            lab = [J[(q, p)] for p in cs]  # 빠진 판정이 있으면 여기서 멈춘다
            n2.append(lab.count(2))
            for v in (2, 1, 0):
                tot[str(v)][i] += lab.count(v)
            tot["항목"][i] += items(r.get("answer"))
            tot["본론 인용"][i] += len(cs)
            tot["컨텍스트 밖 인용"][i] += len(cited(r.get("answer")) - S.ctx(r))
            tot["잘림"][i] += cut_off(r.get("answer"))
            tot["칸 틀 적용"][i] += any(isinstance(x, dict) and x.get("doc_slots") for x in (r.get("trace") or []))
        win += n2[1] > n2[0]
        lose += n2[1] < n2[0]
    p = S.sign_p(win, lose)
    print(f"주: canon {len(a)}문항 — 본론 '2' 늘어남 {win} : 줄어듦 {lose} (동점 {len(a) - win - lose}) · p {p:.4g} → {'통과' if win > lose and p < 0.05 else '미달'}")
    z0, z1 = tot["0"]
    print(f"보호 1: 본론 인용 '0' 합 {z0} → {z1} → {'통과' if z1 <= max(z0 * 1.5, z0 + 2) else '미달'}")
    for k, (x, y) in tot.items():
        print(f"  {k}: {x} → {y}")
    t = [statistics.median(r["elapsed"] for r in rs.values()) for rs in (a, b)]
    print(f"보호 5: 응답 시간 중앙 {t[0]:.1f} → {t[1]:.1f}s → {'통과' if t[1] <= t[0] + 20 else '미달'}")
    print(f"보호 4: 컨텍스트 밖 인용 → {'통과' if tot['컨텍스트 밖 인용'][1] <= tot['컨텍스트 밖 인용'][0] + 1 else '미달'} · 보호 6: 잘림 → {'통과' if tot['잘림'][1] <= tot['잘림'][0] + 2 else '미달'}")
    # 보호 2: 162 표본 — 답이 정답 논문을 인용
    a, b = S.rows("ds0_162s"), S.rows("ds1_162s")
    ok = [sum(bool(r.get("answer_ok")) for r in rs.values()) for rs in (a, b)]
    print(f"보호 2: 162 표본 {len(a)} answer_ok {ok[0]} → {ok[1]} → {'통과' if ok[1] >= ok[0] - 2 else '미달'} · 칸 틀 적용 {sum(any(isinstance(x, dict) and x.get('doc_slots') for x in (r.get('trace') or [])) for r in b.values())}")
    # 보호 3: real40 수치 · 비교
    sp = {json.loads(l)["id"]: json.loads(l) for l in open("docs/experiments/real_eval_1013/spec.jsonl", encoding="utf-8")}
    a, b = S.rows("ds0_realnc"), S.rows("ds1_realnc")
    num = [sum(all(n in (r.get("answer") or "") for n in sp[q]["numbers"]) for q, r in rs.items() if sp[q]["type"] == "N") for rs in (a, b)]
    cmp_ = [sum({S.norm(p) for p in sp[q]["papers"]} <= cited(r.get("answer")) for q, r in rs.items() if sp[q]["type"] == "C") for rs in (a, b)]
    print(f"보호 3: 수치 기대값 포함 {num[0]} → {num[1]} / {sum(sp[q]['type'] == 'N' for q in a)} · 비교 두 편 인용 {cmp_[0]} → {cmp_[1]} / {sum(sp[q]['type'] == 'C' for q in a)}"
          f" → {'통과' if num[1] >= num[0] - 1 and cmp_[1] >= cmp_[0] - 1 else '미달'}")


if __name__ == "__main__":
    pool() if sys.argv[1:] == ["pool"] else main()
