"""qtype_1102 §4.2 판정 묶음: 바뀐 문항마다 qt0 · qt1 답을 A/B 로 섞는다. 열쇠는 judge/key.json(판정 뒤 연다).

판정 전 결정: 답 끝 외부 검색 목록(📎 DB 밖에서 찾은 관련 논문 — 인용 · 요약 없음)은 두 답 모두 잘라 낸다
(survey_gate_1030 과 같음). 쌍 H_I02 는 바뀐 a 만 판정한다(§4.2).
"""
import json, os, random, re

R = "docs/experiments/e2e_ko_1008/results/"
D = "docs/experiments/qtype_1102/"
J = D + "judge/"
os.makedirs(J, exist_ok=True)
ids = [l.strip() for l in open(D + "stage2_ids.txt") if l.strip()]
Q = dict(l.rstrip("\n").split("\t", 1) for f in ("stage2_questions.tsv", "stage2_followup.tsv") for l in open(D + f) if l.strip())


def load(*labels):
    out = {}
    for lb in labels:
        out.update({j["id"]: j for j in map(json.loads, open(R + lb + ".jsonl"))})
    return out


c0, c1 = load("qt0_s2", "qt0_f2"), load("qt1_s2", "qt1_f2")
BLK = re.compile(r"\[문서 \d+\]\n(.*?)(?=\n\[문서 \d+\]\n|\Z)", re.S)
HEAD = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n]*)")
CITE = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]")


def blocks(ctx):
    out = {}
    for body in BLK.findall(ctx or ""):
        m = HEAD.search(body)
        if m and m.group(1) not in out:
            out[m.group(1)] = (m.group(2).strip(), re.sub(r"\s+", " ", body[m.end():]).strip())
    return out


rng = random.Random(1102)
key, items = {}, []
for i in ids:
    flip = rng.random() < 0.5
    A, B = (c1[i], c0[i]) if flip else (c0[i], c1[i])
    key[i] = "A" if flip else "B"  # 처리(qt1, 분류기) 쪽
    ans = {s: x["answer"].split("📎")[0].rstrip() for s, x in (("A", A), ("B", B))}
    bl = {s: blocks(x.get("numbered_context")) for s, x in (("A", A), ("B", B))}
    cited = {s: list(dict.fromkeys(CITE.findall(ans[s]))) for s in "AB"}
    out = [f"## {i}\n\n**질문** {Q[i]}"]
    for s in "AB":
        out.append(f"### 답 {s}\n\n{ans[s]}\n\n_{s} 컨텍스트 {len(bl[s])}편_: " +
                   " · ".join(f"{p} {t[:60]}" for p, (t, _) in bl[s].items()))
    out.append("### 인용 블록")
    for p in dict.fromkeys(cited["A"] + cited["B"]):
        who = "".join(s for s in "AB" if p in cited[s])
        src = bl["A"].get(p) or bl["B"].get(p)
        out.append(f"- **{p}** [인용 {who}] " + (f"{src[0]} — {src[1][:900]}" if src else "(컨텍스트에 없음)"))
    items.append("\n\n".join(out))
json.dump(key, open(J + "key.json", "w"), indent=0)
n = 4
for k in range(n):
    part = items[k::n]
    open(J + f"packets_{k + 1}.md", "w").write("\n\n---\n\n".join(part) + "\n")
print(len(items), "문항 →", n, "묶음")
