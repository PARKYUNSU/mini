#!/usr/bin/env python3
"""RAG 답변 템플릿 준수·거짓 부정 비율 — yunsur_v12 README §4.5.

  python3 scripts/answer_format_stats.py ans_v12 ans_base ans_full
  python3 scripts/answer_format_stats.py --fix ans_v12   # core.llm.answer_fix 후처리를 적용한 뒤 센다
"""
import json,re,sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.llm.answer_fix import drop_contradicted_no_doc
FIX = '--fix' in sys.argv
R="docs/experiments/e2e_ko_1008/results/"
gold={json.loads(l)["id"]:set(json.loads(l)["relevant_papers"]) for l in open("docs/experiments/retrieval_eval_1007/eval_set.jsonl")}
DENY=re.compile(r"제공된 (문서|텍스트|정보)에는[^.]*?(없습니다|찾을 수 없습니다)")
for m in [x for x in sys.argv[1:] if x != '--fix']:
    rows=[json.loads(l) for l in open(R+m+".jsonl")]
    rag=[r for r in rows if r["route"]=="direct_answer/B" and r.get("answer")]
    c=dict(n=0,sec=0,items=0,cite=0,first=0,deny_g=0,g=0,ng=0,deny_ng=0)
    for r in rag:
        a=r["answer"]; c["n"]+=1
        if FIX: a=drop_contradicted_no_doc(a)[0]
        secs=re.findall(r"<b>(서론|본론|결론)</b>",a)
        c["sec"]+= secs==["서론","본론","결론"]
        body=a.split("<b>본론</b>",1)[-1].split("<b>결론</b>",1)[0]
        blocks=re.split(r"^\s*\d+\.\s",body,flags=re.M)[1:]
        c["items"]+= 1<=len(blocks)<=4
        c["cite"]+= bool(blocks) and all(re.search(r"\[\d{4}\.\d{4,5}v\d+\]",b) for b in blocks)
        intro=a.split("<b>본론</b>",1)[0]
        g=bool(gold[r["id"]] & set(r["context_papers"]))
        if g:
            c["g"]+=1; c["first"]+=bool(r.get("answer_first_ok")); c["deny_g"]+=bool(DENY.search(intro))
        else:
            c["ng"]+=1; c["deny_ng"]+=bool(DENY.search(intro))
    n=c["n"]
    print(f"{m+('+fix' if FIX else ''):13} RAG {n} | 섹션 {c['sec']/n:.2f} 본론1-4 {c['items']/n:.2f} 항목전부인용 {c['cite']/n:.2f} | 정답있음 {c['g']}: 첫항목정답 {c['first']/c['g']:.2f} 없다고함 {c['deny_g']/c['g']:.2f} | 정답없음 {c['ng']}: 없다고밝힘 {c['deny_ng']}/{c['ng']}")
