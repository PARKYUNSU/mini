"""pdf_decimal_1107 채점 (README §3).

  .venv/bin/python docs/experiments/pdf_decimal_1107/score.py packet  # 조각 오류 후보 눈가림 묶음 → label_packet.md · key.json
  .venv/bin/python docs/experiments/pdf_decimal_1107/score.py score   # labels.tsv 와 함께 집계
"""
import json, random, re, statistics, sys

sys.path.insert(0, ".")
from core.llm.answer_fix import _CITED

D = "docs/experiments/pdf_decimal_1107/"
R = "docs/experiments/e2e_ko_1008/results/"
BROKEN = re.compile(r"(\d+) *_\._ *(\d+)")
UNIT = {"%": r"%|퍼센트", "×": r"배|×|x(?![A-Za-z])", "x": r"배|×|x(?![A-Za-z])", "ms": r"ms|밀리초", "s": r"s(?![A-Za-z])|초", "k": r"[kK]|천", "M": r"M|백만"}


def rows(label):
    return {r["id"]: r for r in map(json.loads, open(R + label + ".jsonl", encoding="utf-8"))}


def unit_after(text):
    t = re.sub(r"^[ _*]+", "", text[:8])
    for k in UNIT:
        if t.startswith(k):
            return UNIT[k]
    return None


def fragments(answer, ctx0):
    """대조 컨텍스트의 깨진 소수를 답이 쪼개거나 잘라 쓴 자리. ``[(소수, 답 구절, 원문 구절)]``."""
    out = []
    seen = set()
    for m in BROKEN.finditer(ctx0):
        a, b = m.group(1), m.group(2)
        v = f"{a}.{b}"
        if v in seen:
            continue
        seen.add(v)
        if re.search(rf"(?<![\d.]){re.escape(v)}(?!\d)", answer):
            continue
        src = ctx0[max(0, m.start() - 90):m.end() + 50].replace("\n", " ")
        pats = [rf"(?<![\d.]){a}[\s ]*[×x·,_ ][\s ]*{b}(?!\d)"]
        u = unit_after(ctx0[m.end():])
        if u:
            pats += [rf"(?<![\d.,]){a}(?![\d.,])\s*(?:{u})", rf"(?<![\d.,]){b}(?![\d.,])\s*(?:{u})"]
        for p in pats:
            f = re.search(p, answer)
            if f:
                out.append((v, answer[max(0, f.start() - 70):f.end() + 40].replace("\n", " "), src))
                break
    return out


def right_uses(answer, ctx0):
    vs = {f"{m.group(1)}.{m.group(2)}" for m in BROKEN.finditer(ctx0)}
    return sum(bool(re.search(rf"(?<![\d.]){re.escape(v)}(?!\d)", answer)) for v in vs)


def packet():
    a, b = rows("pd0"), rows("pd1")
    items = []
    for i in sorted(set(a) & set(b)):
        ctx0 = a[i].get("numbered_context") or ""
        for arm, r in (("pd0", a[i]), ("pd1", b[i])):
            for v, line, src in fragments(r.get("answer") or "", ctx0):
                items.append({"id": i, "arm": arm, "v": v, "line": line, "src": src})
    random.Random(1107).shuffle(items)
    with open(D + "label_packet.md", "w", encoding="utf-8") as w:
        w.write("# 조각 오류 후보 (대조 · 처리를 섞었고 어느 쪽인지 적지 않았다)\n\n각 항목: T 답이 원문 소수를 쪼개거나 잘라 틀리게 말함 · F 아님 · ? 못 가림\n\n")
        for k, it in enumerate(items, 1):
            w.write(f"## {k} ({it['id']}) 원문 소수 {it['v']}\n- 답: {it['line']}\n- 원문: {it['src']}\n\n")
    json.dump(items, open(D + "key.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("후보", len(items))


def stat(rs):
    def none(r):
        return any(x.get("stage") == "judge" and x.get("pick") == "없음" for x in r.get("trace") or [])

    def outside(r):
        ids = {re.sub(r"v\d+$", "", str(x)) for x in (r.get("doc_ids") or [])}
        return sum(c not in ids for c in _CITED.findall(r.get("answer") or ""))
    return {"오류": sum(bool(r.get("error")) for r in rs.values()), "검색 ok": sum(bool(r.get("ok")) for r in rs.values()),
            "컨텍스트 밖 인용": sum(outside(r) for r in rs.values()), "판정 없음": sum(none(r) for r in rs.values()),
            "시간 중앙": round(statistics.median(r["elapsed"] for r in rs.values()), 1)}


def score():
    a, b = rows("pd0"), rows("pd1")
    ids = sorted(set(a) & set(b))
    print("문항", len(ids))
    n0 = sum(len(BROKEN.findall(a[i].get("numbered_context") or "")) for i in ids)
    n1 = sum(len(BROKEN.findall(b[i].get("numbered_context") or "")) for i in ids)
    q0 = sum(bool(BROKEN.search(a[i].get("numbered_context") or "")) for i in ids)
    print(f"주(기계): 깨진 소수점 대조 {n0}곳({q0}문항) → 처리 {n1}곳 · {'통과' if n1 == 0 else '미달'}")
    s0, s1 = stat(a), stat(b)
    print("대조", s0)
    print("처리", s1)
    print("보호:", "오류", "통과" if s1["오류"] == 0 else "미달", "· 검색 ok", "통과" if s1["검색 ok"] >= s0["검색 ok"] - 1 else "미달",
          "· 컨텍스트 밖", "통과" if s1["컨텍스트 밖 인용"] <= s0["컨텍스트 밖 인용"] + 1 else "미달",
          "· 판정 없음", "통과" if abs(s1["판정 없음"] - s0["판정 없음"]) <= 2 else "미달",
          "· 시간", "통과" if s1["시간 중앙"] <= s0["시간 중앙"] + 5 else "미달")
    print("보고: 답 입력 같은 문항", sum(a[i].get("answer_input") == b[i].get("answer_input") for i in ids),
          "· doc_ids 같은 문항", sum(a[i].get("doc_ids") == b[i].get("doc_ids") for i in ids),
          "· 소수를 맞게 쓴 자리 대조", sum(right_uses(a[i].get("answer") or "", a[i].get("numbered_context") or "") for i in ids),
          "· 처리", sum(right_uses(b[i].get("answer") or "", a[i].get("numbered_context") or "") for i in ids))
    try:
        key = json.load(open(D + "key.json", encoding="utf-8"))
        lab = {int(l.split("\t")[0]): l.split("\t")[1].strip() for l in open(D + "labels.tsv", encoding="utf-8") if l.strip() and not l.startswith("#")}
    except OSError:
        print("라벨 없음 — 조각 오류 집계 건너뜀")
        return
    t = {"pd0": set(), "pd1": set()}
    for k, it in enumerate(key, 1):
        if lab.get(k) == "T":
            t[it["arm"]].add(it["id"])
    only0, only1 = t["pd0"] - t["pd1"], t["pd1"] - t["pd0"]
    print(f"주(효과): 조각 오류 문항 대조 {len(t['pd0'])} {sorted(t['pd0'])} → 처리 {len(t['pd1'])} {sorted(t['pd1'])} · 대조만 {len(only0)} : 처리만 {len(only1)} · 후보 {len(key)} · 라벨 {len(lab)}")
    print("판정:", "재현 안 됨(대조 T 0)" if not t["pd0"] else ("통과" if len(t["pd1"]) < len(t["pd0"]) and not only1 else "미달"))


if __name__ == "__main__":
    {"packet": packet, "score": score}[sys.argv[1]]()
