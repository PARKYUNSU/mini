"""설치 점검(본 뒤 추가, README §7): jeff 저자 공개 자료 sst2 · boolq 를 우리 서버로 돌려 저자 저장 결과와 문항별로 비교한다.

  .venv/bin/python docs/experiments/jeff_1105/repro.py ~/dev/jeff_1105/src_jeff/bench
"""
import collections, json, statistics, sys, urllib.request

B = sys.argv[1].rstrip("/")
URL, KEY = "http://127.0.0.1:8090/v1/systemone", "devkey"


def auroc(pairs):
    pos = [p for p, g in pairs if g]
    neg = [p for p, g in pairs if not g]
    return sum((a > b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg))


def pearson(a, b):
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den if den else float("nan")


stored = [json.loads(l) for l in open(B + "/results/accuracy.jsonl", encoding="utf-8")]
runs = collections.Counter(r["run"] for r in stored if r["task"] in ("sst2", "boolq") and r["kind"] == "noul")
print("저자 run:", runs.most_common(12))
ours = {}
for task in ("sst2", "boolq"):
    for l in open(f"{B}/data/{task}.jsonl", encoding="utf-8"):
        it = json.loads(l)
        body = {"model": "jev-latest", "state": it["state"], "questions": it["questions"]}
        req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as r:
            ours[it["id"]] = (task, json.load(r)["answers"]["q"]["noul"], it["gold"])
for task in ("sst2", "boolq"):
    mine = {k: v for k, v in ours.items() if v[0] == task}
    print(f"[{task}] 우리 서버: {len(mine)}건 · AUROC {auroc([(v[1], v[2]) for v in mine.values()]):.3f} · 평균 noul {statistics.fmean(v[1] for v in mine.values()):.3f} · 0.5 이상 {sum(v[1] >= .5 for v in mine.values())}")
    for run in sorted(runs):
        rows = {r["id"]: r for r in stored if r["run"] == run and r["task"] == task}
        common = [k for k in mine if k in rows]
        if not common:
            continue
        a = [mine[k][1] for k in common]
        b = [rows[k]["answer"]["noul"] for k in common]
        print(f"   {run}: 문항 {len(common)} · 저자 AUROC {auroc([(rows[k]['answer']['noul'], mine[k][2]) for k in common]):.3f} · 평균 noul {statistics.fmean(b):.3f} · 우리와 상관 {pearson(a, b):.4f} · 0.5 일치 {sum((x >= .5) == (y >= .5) for x, y in zip(a, b))}/{len(common)} · 평균 차 {statistics.fmean(abs(x - y) for x, y in zip(a, b)):.4f}")
