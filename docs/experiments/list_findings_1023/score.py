"""list_findings_1023 §3 판정 (맥미니) — 자동 지표 + 눈가림 판정용 표본 파일."""
import glob, json, random, re, statistics as st, sys
from math import comb
from pathlib import Path
sys.path.insert(0, ".")
from scripts.score_real_eval import score

EXP = Path("docs/experiments"); R = EXP / "e2e_ko_1008/results"; D = EXP / "list_findings_1023"
A = ("lf0", "lf1"); SETS = ("real40", "real2", "new")
AB = {}
for f in ["raw_data_queue/crawled_papers.jsonl"] + glob.glob("raw_data_queue/processed/*.jsonl"):
    for l in open(f):
        try:
            d = json.loads(l)
        except ValueError:
            continue
        AB.setdefault(re.sub(r"v\d+$", "", d.get("paper_id", "")), re.sub(r"\s+", " ", d.get("abstract") or "").replace("\\%", "%"))
_CITE = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]")


def items(ans):
    body = (ans or "").split("본론", 1)[-1].split("결론", 1)[0]
    return [x.strip() for x in re.split(r"\n\s*\d+\.\s", "\n" + body)[1:] if x.strip()]


def nums(text):
    t = re.sub(r"\[[^\]]*\]|<[^>]+>|\b(19|20)\d{2}\b", " ", text)
    return {n for n in re.findall(r"\d+(?:[.,]\d+)?", t) if not (len(n) == 1 and n in "123456789")}


def grade(it):
    src = " ".join(AB.get(p, "") for p in _CITE.findall(it))
    ns = nums(it)
    ok = {n for n in ns if re.search(rf"(?<![\d.,]){re.escape(n)}(?![\d])", src)}
    return bool(ok), bool(ns - ok)


rows = {a: {(t, json.loads(l)["id"]): json.loads(l) for t in SETS for l in open(R / f"{a}_{t}.jsonl")} for a in A}
keys = [k for k in rows["lf0"] if k in rows["lf1"]]
per = {a: {k: [grade(i) for i in items(rows[a][k].get("answer"))] for k in keys} for a in A}
g = {a: {k: sum(x[0] for x in per[a][k]) for k in keys} for a in A}
b = sum(g["lf1"][k] > g["lf0"][k] for k in keys); c = sum(g["lf1"][k] < g["lf0"][k] for k in keys); n = b + c
p = 1.0 if n == 0 else min(1, 2 * sum(comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)
for a in A:
    tot = sum(len(v) for v in per[a].values())
    print(f"{a}: 본론 항목 {tot} · 근거 수치 항목 {sum(g[a].values())} · 초록에 없는 숫자 항목 {sum(x[1] for v in per[a].values() for x in v)} · "
          f"응답 시간 중앙 {st.median(rows[a][k]['elapsed'] for k in keys):.1f}s")
print(f"주(자동): 근거 수치 항목 처리가 많은 문항 {b} : 적은 문항 {c}, p={p:.4f}")
for t, d in (("real40", "real_eval_1013"), ("real2", "real_eval2_1015")):
    s = {a: score(f"{a}_{t}", EXP / d) for a in A}
    ok = {a: sum(rows[a][k]["ok"] for k in keys if k[0] == t) for a in A}
    print(f"   보호 {t}: 검색 ok {ok['lf0']} → {ok['lf1']} · T 정답 인용≥3 {sum(x['gold_cited'] >= 3 for x in s['lf0']['T'])} → {sum(x['gold_cited'] >= 3 for x in s['lf1']['T'])}")
# 눈가림 표본: 조건별 25 항목, 섞고 조건 표시는 따로
rnd = random.Random(1023); pool = []
for a in A:
    its = [(a, k, i) for k in keys for i in items(rows[a][k].get("answer")) if _CITE.search(i)]
    pool += rnd.sample(its, min(25, len(its)))
rnd.shuffle(pool)
with open(D / "blind.md", "w") as w, open(D / "blind_key.json", "w") as kf:
    for j, (a, k, it) in enumerate(pool):
        w.write(f"## B{j:02d} ({k[0]} {k[1]})\n항목: {it}\n")
        for pid in dict.fromkeys(_CITE.findall(it)):
            w.write(f"초록[{pid}]: {AB.get(pid, '')[:1500]}\n")
        w.write("\n")
    json.dump({f"B{j:02d}": a for j, (a, k, it) in enumerate(pool)}, kf)
print("눈가림 표본", len(pool), "→ blind.md (조건은 blind_key.json)")
