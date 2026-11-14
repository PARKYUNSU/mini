# 저장된 모든 답 중 '없음' 판정 답에 mark_related_items 를 적용해 ① 모순 수를 전후로 센다(Ollama 안 씀)
import glob, json, re, sys
sys.path.insert(0, ".")
from core.llm.answer_fix import mark_related_items
NONE = re.compile(r"찾는 연구(는|가)?[^.\n]{0,30}(없|찾을 수 없)|찾을 수 없습니다|다루(지 않|는 연구는 없)|포함되어 있지 않|포함되지 않")
def parts(a):
    b = a.split("📎")[0]
    sp = re.split(r"<b>(서론|본론|결론)</b>|^###\s*(서론|본론|결론)\s*$", b, flags=re.M)
    sp = [x for x in sp if x is not None]
    d = {sp[i]: sp[i + 1] for i in range(1, len(sp) - 1, 2)}
    return d.get("서론", ""), d.get("본론", ""), d.get("결론", "")
def contra(a):
    s, b, c = parts(a)
    n = len(re.findall(r"^\s*\d+\.\s", b, re.M))
    return n > 0 and bool(NONE.search(c)) and len(re.findall(r"관련 연구", b)) < n
tot = hint = before = after = changed = 0
ex = []
for f in glob.glob("docs/experiments/e2e_ko_1008/results/*.jsonl"):
    for l in open(f, encoding="utf-8"):
        try: r = json.loads(l)
        except Exception: continue
        a = r.get("answer") or ""
        if not a or not isinstance(r.get("trace"), list): continue
        tot += 1
        j = next((x for x in r["trace"] if x.get("stage") == "judge"), {})
        if j.get("pick") != "없음": continue
        hint += 1
        o, n = mark_related_items(a)
        before += contra(a); after += contra(o); changed += bool(n)
        if n and len(ex) < 2: ex.append((f.split("/")[-1], r["id"], o.split("📎")[0][:700]))
print("답", tot, "| '없음' 판정 답", hint, "| 고친 답", changed, "| ① 모순", before, "→", after)
for e in ex: print("-----", e[0], e[1]); print(e[2])
