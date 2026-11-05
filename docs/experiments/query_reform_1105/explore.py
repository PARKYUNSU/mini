"""사후 탐색(관문 판정에 안 씀): 어떤 문항에서 '2' 비율이 묽어졌나."""
import collections, json, math, re

rows = [json.loads(l) for l in open("docs/experiments/e2e_ko_1008/results/qr_dev.jsonl", encoding="utf-8")]
lab = {}
for path in ("docs/experiments/filter_input_1104/labels.tsv", "docs/experiments/query_reform_1105/labels.tsv"):
    for l in open(path, encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            q, p, v = l.rstrip("\n").split("\t")[:3]
            lab[(q, p)] = int(v)


def sign_p(a, b):
    n, k = a + b, min(a, b)
    return 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def changed(x):
    return [p for p in x["final1"] if p not in x["final0"]]


on = [x for x in rows if x["reform"].get("on")]
ch = [x for x in on if changed(x)]


def show(name, keep):
    sub = [x for x in ch if keep(x)]
    fired = sum(keep(x) for x in on)
    base = collections.Counter(lab[(x["id"], p)] for x in sub for p in x["final0"])
    add = collections.Counter(lab[(x["id"], p)] for x in sub for p in changed(x))
    win = lose = gained = 0
    for x in sub:
        got = [lab[(x["id"], p)] for p in changed(x)]
        g, b = got.count(2), got.count(0)
        win += g > b
        lose += g < b
        gained += g > 0
    n0, n1 = sum(base.values()), sum(base.values()) + sum(add.values())
    r0, r1 = base[2] / max(1, n0), (base[2] + add[2]) / max(1, n1)
    print(f"{name:26s} 발동 {fired:2d} · 바뀜 {len(sub):2d} · 이김:짐 {win}:{lose} (p {sign_p(win, lose):.3f}) · 얻음 {gained} ({gained / max(1, fired):.0%}) · '2' 비율 {r0:.1%} → {r1:.1%} ({(r1 - r0) * 100:+.1f}%p) · 추가 {dict(sorted(add.items()))} · '0' {add[0] / max(1, sum(add.values())):.0%}")


show("전체", lambda x: True)
for k in (1, 2, 3, 4):
    show(f"거른 뒤 {k}편", lambda x, k=k: len(x["final0"]) == k)
show("거른 뒤 2~4편", lambda x: len(x["final0"]) >= 2)
show("JN · real", lambda x: x["id"].split(":")[0] in ("JN", "real40", "real2"))
show("그 밖", lambda x: x["id"].split(":")[0] not in ("JN", "real40", "real2"))
print()
print("거른 뒤 1편인 바뀐 문항:")
for x in ch:
    if len(x["final0"]) == 1:
        got = [lab[(x["id"], p)] for p in changed(x)]
        print(" ", x["id"], lab[(x["id"], x["final0"][0])], got, x["question"][:46].replace("\n", " "))
print()
print("JN 바뀐 문항:")
for x in ch:
    if x["id"].startswith("JN:"):
        got = [lab[(x["id"], p)] for p in changed(x)]
        print(" ", x["id"], len(x["final0"]), got, x["question"][:46].replace("\n", " "))
print()
print("새 검색어 예시(짐 문항):")
for x in ch:
    got = [lab[(x["id"], p)] for p in changed(x)]
    if got.count(2) < got.count(0):
        print(" ", x["id"], got, "|", x["query"][:60], "|", x["reform"]["query"][:70])
