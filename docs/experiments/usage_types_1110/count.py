"""usage_types_1110 집계: labels.tsv → 유형 수 · MU 비율(하한 · 상한) · 요소 수 · 기간별."""
import collections
import csv
import sqlite3

rows = list(csv.DictReader(open("docs/experiments/usage_types_1110/labels.tsv", encoding="utf-8"), delimiter="\t"))
jobs = {int(r["job_id"]) for r in rows} | {int(x) for r in rows for x in r["dup_jobs"].split(",") if x}
n_all = sqlite3.connect("file:.bridge/agent_bridge.sqlite?mode=ro", uri=True).execute("select count(*) from bridge_jobs").fetchone()[0]
assert len(jobs) == sum(1 + len([x for x in r["dup_jobs"].split(",") if x]) for r in rows), "작업 ID 겹침"


def report(name, rs):
    rs = [r for r in rs if r["type"] != "FU"]
    c = collections.Counter(r["type"] for r in rs)
    lo, hi = c["MU"], c["MU"] + c["MU?"]
    el = collections.Counter(r["elements"] for r in rs if r["type"] == "MU")
    print(f"{name}: 분모 {len(rs)} · {dict(sorted(c.items()))} · MU 하한 {lo}/{len(rs)}({lo / len(rs):.0%}) · 상한 {hi}/{len(rs)}({hi / len(rs):.0%}) · MU 요소 수 {dict(sorted(el.items()))}")


print(f"봇 큐 {n_all}건 중 학술 질문 작업 {len(jobs)}건 · 문구 기준 {len(rows)}개(이어지는 질문 FU {sum(r['type'] == 'FU' for r in rows)}) · 비학술 {n_all - len(jobs)}건")
report("문구 기준 전체", rows)
first = {}
for r in rows:
    if r["cluster"] != "-":
        first.setdefault(r["cluster"], r)
report("요청 기준 전체(고쳐 쓴 같은 요청 묶음)", list(first.values()))
report("문구 기준 10-08 이후(작업 102~)", [r for r in rows if int(r["job_id"]) >= 102])
report("문구 기준 10-30 이후(작업 137~)", [r for r in rows if int(r["job_id"]) >= 137])
