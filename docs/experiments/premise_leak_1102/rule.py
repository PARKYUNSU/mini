"""premise_leak_1102 §2.2: 전제 질문 30 dev 결론 문장에 R4 규칙을 댄다(맥미니, 읽기만). T = 새어 든 문장 · B = 경계 · N = '문서에 없음' 꼴."""
import collections, json, re, sys
from difflib import SequenceMatcher
sys.path.insert(0, ".")
sys.path.insert(0, "docs/experiments/conclusion_verify_1101")
import offline as OV
from core.llm.answer_fix import _CITED, _find
Q = dict(l.rstrip("\n").split("\t", 1) for l in open("docs/experiments/premise_leak_1102/dev_questions.tsv", encoding="utf-8") if "\t" in l)
T = {"P01": ["정도 떨어지는 것을 확인"], "P02": ["검색 없이도 반성 토큰만으로"], "P05": ["자기 선호 편향이 크게 감소한다는", "56.1 퍼센트 포인트까지 줄어들었"],
     "P07": ["급격히 감소하는 경계가 존재한다는 점은"], "P10": ["정확도가 크게 향상되지 않는 현상"], "P28": ["0.7 수준임을 확인"],
     "P30": ["응답이 길어질수록 정확도가 크게 저하"]}
B = {"P22": ["토크나이저가 숫자 비교 오류에 영향"], "P12": ["주장은 사실이 아닙니다"], "P24": ["검색 문서 수를 늘리는 것보다"]}
NOTICE = re.compile(r"찾을 수 없|제시하지 않|포함되어 있지 않|제시되지 않|다루지 않|알 수는 없|없습니다|않습니다|않는다|없다")
_END = re.compile(r"\n\s*(?:<b>|📎)")
_CIT = re.compile(r"\[\s*\d{4}\.\d{4,5}(?:v\d+)?\s*\]")
_PUN = re.compile(r"[^\w가-힣]+")
_NUM = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)?")
_LAT = re.compile(r"[A-Za-z][A-Za-z0-9\-]{2,}")
STOP = {"the", "and", "for", "with", "this", "that", "are", "from", "our", "llm", "llms", "rag", "model", "models", "based"}
norm = lambda s: _PUN.sub("", _CIT.sub("", s))
toks = lambda s: {n.replace(",", "") for n in _NUM.findall(_CIT.sub("", s))} | {w.lower() for w in _LAT.findall(_CIT.sub("", s)) if w.lower() not in STOP}
cnt = collections.Counter()
for r in map(json.loads, open("docs/experiments/e2e_ko_1008/results/pl0_dev.jsonl", encoding="utf-8")):
    a = r["answer"]; c = _find("결론", a)
    if not c:
        continue
    rest = a[c.end():]; m = _END.search(rest); concl = rest[:m.start()] if m else rest
    ss = OV.split(concl)
    bl = OV.blocks(r)
    allref = [re.sub(r"v\d+$", "", i) for i in dict.fromkeys(_CITED.findall(concl))]
    q = norm(Q[r["id"]])
    for s in ss:
        refs = [re.sub(r"v\d+$", "", i) for i in dict.fromkeys(_CITED.findall(s))] or allref or list(bl)
        ctx = "\n".join(bl.get(p, "") for p in refs)
        ns = norm(s)
        lcs = SequenceMatcher(None, ns, q, autojunk=False).find_longest_match(0, len(ns), 0, len(q)).size
        doc = len(toks(s) & toks(ctx))
        lab = "T" if any(k in s for k in T.get(r["id"], [])) else "B" if any(k in s for k in B.get(r["id"], [])) else "N" if NOTICE.search(s) else "-"
        fa = lcs >= 8 and doc == 0
        fb = fa and not NOTICE.search(s)
        cnt[(lab, "a")] += fa; cnt[(lab, "b")] += fb; cnt[(lab, "n")] += 1
        print(f"{r['id']} {lab} lcs{lcs:2d} doc{doc} {'A' if fa else ' '}{'B' if fb else ' '} | {s[:120]}")
print()
for lab in "TBN-":
    print(lab, "문장", cnt[(lab, "n")], "· 초안 규칙 걸림", cnt[(lab, "a")], "· 고지 뺀 규칙 걸림", cnt[(lab, "b")])
