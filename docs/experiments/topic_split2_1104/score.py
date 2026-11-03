"""topic_split2_1104 라벨 묶음 · 채점 (README §3 · §4). 1103 score.py 에서 대조 · 처리 · 정답 파일만 꼬리별로 나눴다.

  .venv/bin/python docs/experiments/topic_split2_1104/score.py packet [꼬리]  # 대조 · 처리 최종 문서 합집합 → label_packet_<꼬리>.md
  .venv/bin/python docs/experiments/topic_split2_1104/score.py score [꼬리]   # labels_<꼬리>.tsv (문항\t논문\t주제 번호 "1,3" 또는 "-")

묶음에는 어느 조건 문서인지 적지 않는다(섞어서 seed 1104). 기본 꼬리는 hu.
"""
import json, math, random, re, statistics, sys

R = "docs/experiments/e2e_ko_1008/results/"
D = "docs/experiments/topic_split2_1104/"
OLD = "docs/experiments/topic_split_1103/"
# 꼬리 → (대조, 처리, 정답). htd 는 dev — 이미 본 HT30 을 고친 추출기로 다시 잰 것
TAILS = {"hu": ("ts0_hu", "ts1_hu", D + "heldout_gold.jsonl"), "htd": ("ts0_ht", "ts1_htd", OLD + "heldout_topics_gold.jsonl")}
BLK = re.compile(r"\[문서 (\d+)\]\n(.*?)(?=\n\[문서 \d+\]\n|\Z)", re.S)
HEAD = re.compile(r"\[(\d{4}\.\d{4,5})(?:v\d+)?\]\s*([^\n]*)")


def rows(label):
    return {r["id"]: r for r in map(json.loads, open(R + label + ".jsonl", encoding="utf-8"))}


def docs(r):
    """최종 컨텍스트 문서 {논문 ID: (제목, 본문 앞부분)}."""
    out = {}
    for _, body in BLK.findall(r.get("numbered_context") or ""):
        m = HEAD.search(body)
        if m:
            rest = re.sub(r"\s+", " ", body[m.end():]).strip()
            out[m.group(1)] = (m.group(2).strip(), rest)
    return out


def sign_p(a, b):
    """양측 정확 부호 검정."""
    n, k = a + b, min(a, b)
    return 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def main():
    cmd, tail = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "hu")
    c, t = rows(TAILS[tail][0]), rows(TAILS[tail][1])
    gold = {g["id"]: g for g in map(json.loads, open(TAILS[tail][2], encoding="utf-8"))}
    if cmd == "packet":
        rnd = random.Random(1104)
        lines = []
        for qid in sorted(c):
            pool = {**docs(c[qid]), **docs(t[qid])}
            pids = sorted(pool)
            rnd.shuffle(pids)
            topics = gold.get(qid, {}).get("topics", [])
            lines.append(f"## {qid}\n\n**하위 주제** " + " · ".join(f"{k}. {x}" for k, x in enumerate(topics, 1)) + "\n")
            for p in pids:
                title, rest = pool[p]
                lines.append(f"- `{p}` **{title}** — {rest[:500]}")
            lines.append("")
        open(D + f"label_packet_{tail}.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print("문항", len(c), "· 문서", sum(len({**docs(c[q]), **docs(t[q])}) for q in c), "→", D + f"label_packet_{tail}.md")
        return
    lab = {}
    for l in open(D + f"labels_{tail}.tsv", encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            q, p, v = l.rstrip("\n").split("\t")[:3]
            lab[(q, p)] = set() if v.strip() == "-" else {int(x) for x in re.findall(r"\d+", v)}
    miss = [(q, p) for q in c for p in {**docs(c[q]), **docs(t[q])} if (q, p) not in lab]
    assert not miss, f"라벨 없음 {len(miss)}: {miss[:5]}"
    win = lose = tie = 0
    off_more = off_less = 0
    full = [0, 0]
    tot = [0, 0]
    ndoc = [0, 0]
    noff = [0, 0]
    shrink = 0
    per = []
    for q in sorted(c):
        k = len(gold[q]["topics"])
        cov, off = [], []
        for r in (c[q], t[q]):
            ls = [lab[(q, p)] for p in docs(r)]
            cov.append(len(set().union(*ls) & set(range(1, k + 1))) if ls else 0)
            off.append(sum(not x for x in ls))
        tot[0] += cov[0]
        tot[1] += cov[1]
        n = [len(docs(c[q])), len(docs(t[q]))]
        ndoc[0] += n[0]
        ndoc[1] += n[1]
        noff[0] += off[0]
        noff[1] += off[1]
        shrink += n[1] < 3 <= n[0]
        full[0] += cov[0] == k
        full[1] += cov[1] == k
        win += cov[1] > cov[0]
        lose += cov[1] < cov[0]
        tie += cov[1] == cov[0]
        off_more += off[1] > off[0]
        off_less += off[1] < off[0]
        topics = next((x.get("topics") for x in t[q].get("trace", []) if x.get("stage") == "search"), None)
        per.append(f"{q} 주제 {k} · 덮음 {cov[0]}→{cov[1]} · 주제 밖 {off[0]}→{off[1]} · 나뉨 {len(topics) if topics else 0}")
    print("\n".join(per))
    print(f"주: 덮은 주제 처리 많음 {win} : 적음 {lose} (동점 {tie}) · 부호 검정 p {sign_p(win, lose):.4f}")
    print(f"   덮은 주제 합계 {tot[0]} → {tot[1]} / {sum(len(gold[q]['topics']) for q in c)} · 다 덮은 문항 {full[0]} → {full[1]} / {len(c)}")
    r0, r1 = noff[0] / max(1, ndoc[0]), noff[1] / max(1, ndoc[1])
    print(f"보호 1: 주제 밖 문서 비율 {r0:.1%} → {r1:.1%} ({r1 - r0:+.1%}p, 기준 ≤ +10%p) · 편수 {ndoc[0]} → {ndoc[1]}"
          f" · 문항별 주제 밖 많음 {off_more} : 적음 {off_less}")
    print(f"보호 1b: 처리만 3편 미만으로 준 문항 {shrink} (기준 ≤ 3)")
    split = [q for q in t if next((x.get("topics") for x in t[q].get("trace", []) if x.get("stage") == "search"), None)]
    st = lambda r: sum(x.get("s", 0) for x in r.get("trace", []) if x.get("stage") in ("search", "select", "filter"))
    if split:
        d = [st(t[q]) - st(c[q]) for q in split]
        print(f"보호 3: 나뉜 {len(split)}문항 검색~거르기 증가 중앙 {statistics.median(d):+.1f}s (기준 ≤ +60s,"
              f" 대조 중앙 {statistics.median(st(c[q]) for q in split):.1f}s)")


if __name__ == "__main__":
    main()
