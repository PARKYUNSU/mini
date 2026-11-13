"""answer_issues_1113 기계 항목: 모순 · 개수. hr_rp1 120 답, Ollama 안 씀."""
import json, re
from collections import Counter

R = [json.loads(l) for l in open("docs/experiments/e2e_ko_1008/results/hr_rp1.jsonl", encoding="utf-8")]
Q = {l.split("\t")[0]: l.rstrip("\n").split("\t", 1)[1] for l in open("docs/experiments/judge_v2_1113/heldout120.tsv", encoding="utf-8") if "\t" in l}
NUM = {"한": 1, "하나": 1, "두": 2, "둘": 2, "세": 3, "셋": 3, "네": 4, "넷": 4, "다섯": 5}
NONE = re.compile(r"찾는 연구(는|가)?[^.\n]{0,30}(없|찾을 수 없)|찾을 수 없습니다|다루(지 않|는 연구는 없)|포함되어 있지 않|포함되지 않")


def hint(r):
    s = next(x for x in r["trace"] if x["stage"] == "judge")
    return "힌트" if s.get("pick") == "없음" else "비힌트"


def parts(a):
    b = a.split("📎")[0]
    sp = re.split(r"<b>(서론|본론|결론)</b>", b)
    d = {sp[i]: sp[i + 1] for i in range(1, len(sp) - 1, 2)}
    return d.get("서론", ""), d.get("본론", ""), d.get("결론", "")


def want(q):
    if re.search(r"하나만|딱 하나|한 편만|한 개만", q):
        return 1
    m = re.search(r"(\d+|한|두|세|네|다섯)\s*(편|개|가지)", q)
    if m:
        return int(m.group(1)) if m.group(1).isdigit() else NUM[m.group(1)]
    return None


out = []
for r in R:
    s, b, c = parts(r["answer"])
    items = re.findall(r"^\s*\d+\.\s", b, re.M)
    marked = len(re.findall(r"관련 연구", b))
    w = want(Q[r["id"]])
    out.append({"id": r["id"], "grp": hint(r), "n_items": len(items), "marked": marked,
                "concl_none": bool(NONE.search(c)), "intro_none": bool(NONE.search(s)),
                "want": w, "count_bad": (w is not None and len(items) != w)})
json.dump(out, open("docs/experiments/answer_issues_1113/auto.json", "w"), ensure_ascii=False, indent=0)
for g in ("힌트", "비힌트"):
    X = [o for o in out if o["grp"] == g]
    mo = [o["id"] for o in X if o["n_items"] and o["concl_none"] and o["marked"] < o["n_items"]]
    mo_marked = [o["id"] for o in X if o["n_items"] and o["concl_none"] and o["marked"] >= o["n_items"]]
    over2 = [o["id"] for o in X if g == "힌트" and o["n_items"] > 2]
    cnt = [o for o in X if o["want"]]
    print(g, len(X), "| 모순(표시 없는 항목 + 결론 없음)", len(mo), mo, "| 관련연구 표시하고 없음", len(mo_marked),
          "| 힌트인데 3항목+", len(over2), "| 개수 요청", len(cnt), "위반", [(o['id'], o['want'], o['n_items']) for o in cnt if o['count_bad']])
