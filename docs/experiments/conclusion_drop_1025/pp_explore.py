import json,re,sys,collections,math
sys.path.insert(0,".")
from core.llm.answer_fix import _CITED
from core.llm.conclusion_rewrite import _OVERGEN
D="docs/experiments/conclusion_v3_1024/"
key=json.load(open(D+"blind_key.json")); res=[json.loads(l) for l in open(D+"results.jsonl")]
lab={l.split("\t")[0]:l.split("\t")[1] for l in open(D+"blind_judged.tsv").read().splitlines()[1:]}
txt={}
for l in open(D+"blind_judge.md"):
    m=re.match(r"(Q\d+[AB]\.\d+) (.*)",l)
    if m: txt[m.group(1)]=m.group(2)
rm=collections.Counter(); win=0; ans=0; tot=0
for q,arms in key.items():
    if res[int(q[1:])]["v2"]["why"]!="바꿈": continue
    side="AB"[arms.index("v2")]
    s=[(k,txt[k]) for k in txt if k.startswith(q+side+".") and k in lab]
    if not s: continue
    tot+=1
    drop=[k for k,t in s if len(set(_CITED.findall(t)))>=2 or _OVERGEN.search(t)]
    if not drop or not any(_CITED.search(t) for k,t in s if k not in drop): continue
    ans+=1; ex=sum(lab[k] in "EX" for k in drop); win+=ex>0
    for k in drop: rm[lab[k]]+=1
print("v2 바꿈 답",tot,"규칙 적용",ans,"E+X 줄어든 답",win,"지운 문장 라벨",dict(rm))
