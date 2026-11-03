"""topic_split_1103 진단: 실사용 · dev 질문 중 번호 붙은 하위 주제(1. 2. …)가 있는 질문이 얼마나 되나 (코드 변경 없음)."""
import collections, glob, re, sqlite3

qs = {}
for i, t in sqlite3.connect(".bridge/agent_bridge.sqlite").execute("select id, user_text from bridge_jobs"):
    if t and t.strip():
        qs.setdefault(t.strip(), "실사용")
for f in sorted(glob.glob("docs/experiments/**/*.tsv", recursive=True)):
    name = f.split("/")[-1]
    if "heldout" in name and "heldout_open" not in name:
        continue  # held-out 은 판정 전용
    for l in open(f, encoding="utf-8"):
        p = l.rstrip("\n").split("\t")
        if len(p) >= 2 and re.search(r"[가-힣]", p[1]) and len(p[1]) >= 6 and not l.startswith("#"):
            qs.setdefault(p[1].strip(), f.split("/")[2])
NUM = re.compile(r"(?:^|[\s:：.?!])(?:([1-9])[.)]|[(]([1-9])[)]|([①-⑨]))\s*(?=\S)")
ORD = re.compile(r"첫째|둘째|셋째")
src = collections.Counter(qs.values())
print("질문", len(qs), "· 실사용", src["실사용"])
hits = collections.Counter()
for q, s in qs.items():
    nums = [int(a or b or (ord(c) - ord("①") + 1)) for a, b, c in NUM.findall(q)]
    seq = 1 in nums and 2 in nums and nums.index(1) < nums.index(2)
    if seq or ORD.search(q):
        hits[s] += 1
        print(f"[{s}] {len(q)}자 · 번호 {nums} · {q[:160]}")
print("번호 붙은 하위 주제 질문:", dict(hits))
L = sorted(((len(q), s, q) for q, s in qs.items() if s == "실사용"), reverse=True)[:8]
print("실사용 가장 긴 8:")
for n, s, q in L:
    print(f"  {n}자 · {q[:140]}")
