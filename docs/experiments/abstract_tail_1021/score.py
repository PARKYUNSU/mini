"""abstract_tail_1021 §3 판정 (맥미니)."""
import glob, json, re, statistics as st, sys
from pathlib import Path
sys.path.insert(0, ".")
from scripts.score_real_eval import score

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"
SETS = {"real40": "real_eval_1013", "real2": "real_eval2_1015"}
SEP = "\n\n---\n\n"
AB = {}
for f in ["raw_data_queue/crawled_papers.jsonl"] + glob.glob("raw_data_queue/processed/*.jsonl"):
    for l in open(f):
        try:
            d = json.loads(l)
        except ValueError:
            continue
        AB.setdefault(re.sub(r"v\d+$", "", d.get("paper_id", "")), re.sub(r"\s+", " ", d.get("abstract") or "").strip())
CAP = 8000 + 5 * (2000 - 800)  # 운영 rag_max_chars (초록 2000자)


def pid(b):
    m = re.search(r"\[(\d{4}\.\d{4,5})v\d+\]", b)
    return m.group(1) if m else None


def missing(b):
    p = pid(b); a = AB.get(p, "")[:2000]
    return bool(p and a and "[초록]" not in b and a[-80:].lower() not in re.sub(r"\s+", " ", b).lower())


def tail_nums(p):
    a = AB.get(p, "")
    return {t for t in re.findall(r"\d+(?:\.\d+)?%?", a[len(a) // 2:]) if len(t.rstrip("%")) >= 2 or "%" in t}


rows = {arm: {} for arm in ("at0", "at1")}
for arm in rows:
    for tag in SETS:
        for l in open(R / f"{arm}_{tag}.jsonl"):
            r = json.loads(l); rows[arm][(tag, r["id"])] = r
keys = [k for k in rows["at0"] if k in rows["at1"]]
for arm in ("at0", "at1"):
    blocks = [b for k in keys for b in (rows[arm][k].get("numbered_context") or "").split(SEP) if pid(b)]
    past = sum(len((rows[arm][k].get("numbered_context") or "")[:CAP].split(SEP)) < len((rows[arm][k].get("numbered_context") or "").split(SEP)) for k in keys)
    print(f"{arm}: 블록 {len(blocks)} · 초록 끝 누락 블록 {sum(missing(b) for b in blocks)} · 상한({CAP}자) 넘어 잘린 블록이 있는 문항 {past} · 응답 시간 중앙 {st.median(rows[arm][k]['elapsed'] for k in keys):.1f}s")
aff = [k for k in keys if any(missing(b) for b in (rows["at0"][k].get("numbered_context") or "").split(SEP))]
print(f"영향 문항 {len(aff)}: {[f'{t}:{i}' for t, i in aff]}")
for arm in ("at0", "at1"):
    hit = 0
    for k in aff:
        ps = {pid(b) for b in (rows["at0"][k].get("numbered_context") or "").split(SEP) if missing(b)}
        ans = rows[arm][k].get("answer") or ""
        hit += any(t in ans for p in ps for t in tail_nums(p))
    print(f"   주(효과) {arm}: 초록 끝 결과 숫자를 쓴 영향 문항 {hit}/{len(aff)}")
for tag, d in SETS.items():
    s = {arm: score(f"{arm}_{tag}", EXP / d) for arm in ("at0", "at1")}
    f = lambda x: (sum(r["ok"] for r in x["N"]), sum(r["both_cited"] for r in x["C"]), sum(r["gold_cited"] >= 3 for r in x["T"]))
    ok = {arm: sum(rows[arm][k]["ok"] for k in keys if k[0] == tag) for arm in ("at0", "at1")}
    print(f"   {tag}: 검색 ok {ok['at0']} → {ok['at1']} · N 정답 · C 두 편 · T≥3 {f(s['at0'])} → {f(s['at1'])}")
