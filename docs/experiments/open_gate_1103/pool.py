"""open_gate_1103 §4.2 판정 묶음: 두 조건의 answer_input 이 다른 문항만 qt 처럼 A/B 로 섞는다. 열쇠 judge/key.json 은 판정 뒤 연다.

판정 전 결정: 답 끝 외부 검색 목록(📎)은 두 답 모두 잘라 낸다(R6 와 같음). 쌍 H_I04 는 b 만 본다. 인용 블록은 두 쪽 컨텍스트 중 그 논문의 가장 긴 블록 앞 900자.
"""
import json, os, random, re

R = "docs/experiments/e2e_ko_1008/results/"
D = "docs/experiments/open_gate_1103/"
J = D + "judge/"
os.makedirs(J, exist_ok=True)
Q = dict(l.rstrip("\n").split("\t", 1) for l in open(D + "stage2_questions.tsv", encoding="utf-8") if l.strip())
Q.update(dict(l.rstrip("\n").split("\t", 1) for l in open("docs/experiments/foundation_1031/heldout_followup.tsv", encoding="utf-8") if l.strip()))


def load(*labels):
    out = {}
    for lb in labels:
        out.update({j["id"]: j for j in map(json.loads, open(R + lb + ".jsonl", encoding="utf-8"))})
    return out


c0, c1 = load("og0_s2", "og0_f2"), load("og1_s2", "og1_f2")
ids = [i for i in c0 if i in c1 and i != "H_I04a"]
same = [i for i in ids if c0[i].get("answer_input") and c0[i]["answer_input"] == c1[i].get("answer_input")]
ids = [i for i in ids if i not in same]
BLK = re.compile(r"\[문서 \d+\]\n(.*?)(?=\n\[문서 \d+\]\n|\Z)", re.S)
HEAD = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n]*)")
CITE = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]")


def blocks(ctx):
    out = {}
    for body in BLK.findall(ctx or ""):
        m = HEAD.search(body)
        if m:
            t, b = m.group(2).strip(), re.sub(r"\s+", " ", body[m.end():]).strip()
            if len(b) > len(out.get(m.group(1), ("", ""))[1]):
                out[m.group(1)] = (t, b)
    return out


rng = random.Random(1103)
key, items = {}, []
for i in ids:
    flip = rng.random() < 0.5
    A, B = (c1[i], c0[i]) if flip else (c0[i], c1[i])
    key[i] = "A" if flip else "B"  # 처리(og1, 판정 건너뜀) 쪽
    ans = {s: x["answer"].split("📎")[0].rstrip() for s, x in (("A", A), ("B", B))}
    bl = {s: blocks(x.get("numbered_context")) for s, x in (("A", A), ("B", B))}
    allb = {**bl["A"]}
    for p, v in bl["B"].items():
        if len(v[1]) > len(allb.get(p, ("", ""))[1]):
            allb[p] = v
    cited = {s: list(dict.fromkeys(CITE.findall(ans[s]))) for s in "AB"}
    out = [f"## {i}\n\n**질문** {Q[i]}"]
    for s in "AB":
        out.append(f"### 답 {s}\n\n{ans[s]}\n\n_{s} 컨텍스트 {len(bl[s])}편_: " + " · ".join(f"{p} {t[:60]}" for p, (t, _) in bl[s].items()))
    out.append("### 인용 블록")
    for p in dict.fromkeys(cited["A"] + cited["B"]):
        who = "".join(s for s in "AB" if p in cited[s])
        src = allb.get(p)
        out.append(f"- **{p}** [인용 {who}] " + (f"{src[0]} — {src[1][:900]}" if src else "(컨텍스트에 없음)"))
    items.append("\n\n".join(out))
json.dump(key, open(J + "key.json", "w"), indent=0)
n = max(1, (len(items) + 10) // 11)
for k in range(n):
    open(J + f"packets_{k + 1}.md", "w", encoding="utf-8").write("\n\n---\n\n".join(items[k::n]) + "\n")
print(len(items), "문항 →", n, "묶음 · 답 입력 같아 뺀 문항", len(same), same)
