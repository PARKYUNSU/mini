"""topic_split_1103 dev: 1단계 후보(번호 항목 · 쉼표 목록) → 2단계 하위 주제 뽑기(LLM)가 몇 문항에서 나뉘나.

  .venv/bin/python docs/experiments/topic_split_1103/gate_check.py count      # 후보 수만 (LLM 없음)
  .venv/bin/python docs/experiments/topic_split_1103/gate_check.py run [tsv]  # 후보마다 뽑기 → gate_dev.jsonl (이어 하기)
"""
import collections, glob, json, os, re, sqlite3, sys, time
sys.path.insert(0, ".")
from core.graph import agent_nodes as N

D = "docs/experiments/topic_split_1103/"


def dev_questions():
    qs = {}
    for i, t in sqlite3.connect(".bridge/agent_bridge.sqlite").execute("select id, user_text from bridge_jobs"):
        if t and t.strip():
            qs.setdefault(t.strip(), f"실사용:{i}")
    for f in sorted(glob.glob("docs/experiments/**/*.tsv", recursive=True)):
        name = f.split("/")[-1]
        if ("heldout" in name and "heldout_open" not in name) or "topic_split_1103" in f:
            continue  # held-out 은 판정 전용 · 이 라운드 문항은 따로
        for l in open(f, encoding="utf-8"):
            p = l.rstrip("\n").split("\t")
            if len(p) >= 2 and re.search(r"[가-힣]", p[1]) and len(p[1]) >= 6 and not l.startswith("#"):
                qs.setdefault(p[1].strip().replace("\\n", "\n"), f.split("/")[2])
    return qs


def main():
    cmd = sys.argv[1]
    if len(sys.argv) > 2:  # 라운드 문항 TSV (id\t질문)
        qs = {l.split("\t", 1)[1].rstrip("\n").replace("\\n", "\n"): l.split("\t", 1)[0]
              for l in open(sys.argv[2], encoding="utf-8") if l.strip() and not l.startswith("#")}
        out = D + "gate_" + os.path.basename(sys.argv[2]).rsplit(".", 1)[0] + ".jsonl"
    else:
        qs, out = dev_questions(), D + "gate_dev.jsonl"
    cand = {q: s for q, s in qs.items() if N.topic_split_candidate(q)}
    src = collections.Counter(s.split(":")[0] for s in qs.values())
    csrc = collections.Counter(s.split(":")[0] for s in cand.values())
    print(f"질문 {len(qs)} · 1단계 후보 {len(cand)} ({len(cand) / len(qs):.1%})")
    print("  출처별 후보/전체:", {k: f"{csrc[k]}/{v}" for k, v in src.most_common() if csrc[k]})
    if cmd == "count":
        return
    out = out.replace(".jsonl", os.getenv("TAG", "") + ".jsonl")
    done = {json.loads(l)["q"] for l in open(out, encoding="utf-8")} if os.path.exists(out) else set()
    with open(out, "a", encoding="utf-8") as w:
        for k, (q, s) in enumerate(cand.items(), 1):
            if q in done:
                continue
            t0 = time.time()
            topics = N._extract_subtopics(q)
            row = {"src": s, "q": q, "topics": topics, "s": round(time.time() - t0, 1)}
            w.write(json.dumps(row, ensure_ascii=False) + "\n")
            w.flush()
            print(f"[{k}/{len(cand)}] {s} 나뉨 {len(topics)} ({row['s']}s) · {q[:60]!r} → {topics}", flush=True)
    rows = [json.loads(l) for l in open(out, encoding="utf-8")]
    split = [r for r in rows if r["topics"]]
    print(f"2단계 나뉨 {len(split)}/{len(rows)} · 시간 중앙 {sorted(r['s'] for r in rows)[len(rows) // 2]}s")


if __name__ == "__main__":
    main()
