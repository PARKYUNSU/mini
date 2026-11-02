"""qtype_1102: 실사용(브리지 DB) + 평가 질문 세트를 모아 같은 글은 하나로 (dev) · held-out 은 따로 (test)."""
import csv, glob, re, sqlite3, sys

E = "docs/experiments/"
TEST = {E + "foundation_1031/heldout.tsv", E + "foundation_1031/heldout_followup.tsv"}
files = sorted(set(glob.glob(E + "*/*questions*.tsv") + glob.glob(E + "*/heldout*.tsv") + glob.glob(E + "*/dev_*.tsv")
                   + [E + "compare_split_1015/g2.tsv", E + "compare_split_1015/r1_cmp.tsv", E + "compare_split_1015/r2_cmp.tsv",
                      E + "presence_gate_1014/gate162_4.tsv", E + "real_eval2_1015/g4.tsv", E + "corpus_seed_1020/discovery_q2.tsv"]))
norm = lambda q: re.sub(r"\s+", " ", q).strip()
rows = {}  # text -> [split, [srcs]]
for i, t in sqlite3.connect(".bridge/agent_bridge.sqlite").execute("select id, user_text from bridge_jobs order by id"):
    q = norm(t or "")
    if q:
        rows.setdefault(q, ["dev", []])[1].append(f"R_{i}")
for f in files:
    tag = f[len(E):].split("/")[0]
    for r in csv.reader(open(f), delimiter="\t"):
        if len(r) < 2 or r[0] == "id" or not r[-1].strip():
            continue
        q = norm(r[-1])
        ent = rows.setdefault(q, ["dev", []])
        ent[1].append(f"{tag}:{r[0]}")
        if f in TEST:
            ent[0] = "test"
out = csv.writer(open(sys.argv[1], "w"), delimiter="\t", lineterminator="\n")
out.writerow(["uid", "split", "srcs", "question"])
n = {"dev": 0, "test": 0}
for q, (split, srcs) in rows.items():
    n[split] += 1
    out.writerow([f"{split[0]}{n[split]:04d}", split, " ".join(srcs), q])
print(n, "files", len(files))
