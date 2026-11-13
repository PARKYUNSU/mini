"""9B + v2 프롬프트 재생 (README §6). 맥미니에서:

  .venv/bin/python docs/experiments/judge_v2_1113/prompt_only.py

held-out 대조(hj_ctl) 의 판정이 돈 문항마다 같은 컨텍스트로 판정만 다시 돌린다:
v13+v1(운영 꼬리) · v13+v2 · 27b+v2. 결과는 prompt_only.jsonl 에 이어 쓴다.
"""
import json, os, sys, time

sys.path.insert(0, ".")
sys.path.insert(0, "docs/experiments/open_judge_1103")
import oj
import core.llm.presence_judge as pj
from core.llm.agent_prompts import DIRECT_ANSWER_RAG_SYSTEM_BASE as SYS

D = "docs/experiments/judge_v2_1113/"
OUT = D + "prompt_only.jsonl"
Q = {l.split("\t")[0]: l.rstrip("\n").split("\t", 1)[1] for l in open(D + "heldout120.tsv", encoding="utf-8") if "\t" in l}
rows = [json.loads(l) for l in open("docs/experiments/e2e_ko_1008/results/hj_ctl.jsonl", encoding="utf-8")]
seen = {json.loads(l)["id"] for l in open(OUT, encoding="utf-8")} if os.path.exists(OUT) else set()
with open(OUT, "a", encoding="utf-8") as w:
    for r in rows:
        js = [s for s in r.get("trace") or [] if s.get("stage") == "judge" and s.get("pick") is not None]
        if not js or r["id"] in seen:
            continue
        prompt = oj.rebuild(Q[r["id"]], r["numbered_context"], len(r["doc_ids"]))
        out = {"id": r["id"], "run_ctl": js[0]["pick"]}
        for name, fn, m in (("v13_v1", pj.judge_presence_shared, "yunsur_v13"),
                            ("v13_v2", pj.judge_presence_shared_v2, "yunsur_v13"),
                            ("27b_v2", pj.judge_presence_shared_v2, "qwen3.6:27b-q4_K_M")):
            t = time.time()
            out[name] = fn(SYS, prompt, Q[r["id"]], m)
            out[name + "_s"] = round(time.time() - t, 1)
        w.write(json.dumps(out, ensure_ascii=False) + "\n")
        w.flush()
        print(out, flush=True)
