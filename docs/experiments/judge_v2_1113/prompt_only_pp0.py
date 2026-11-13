"""§6 재생을 presence_penalty 0 으로 다시 (README §7). v13 모델 파일 기본 pp 1.5 를 덮는다.

  .venv/bin/python docs/experiments/judge_v2_1113/prompt_only_pp0.py
"""
import json, sys

sys.path.insert(0, ".")
sys.path.insert(0, "docs/experiments/open_judge_1103")
import oj, requests
import core.llm.presence_judge as pj
from core.llm.agent_prompts import DIRECT_ANSWER_RAG_SYSTEM_BASE as SYS

D = "docs/experiments/judge_v2_1113/"
Q = {l.split("\t")[0]: l.rstrip("\n").split("\t", 1)[1] for l in open(D + "heldout120.tsv", encoding="utf-8") if "\t" in l}
rows = {json.loads(l)["id"]: json.loads(l) for l in open("docs/experiments/e2e_ko_1008/results/hj_ctl.jsonl", encoding="utf-8")}
ids = [json.loads(l)["id"] for l in open(D + "prompt_only.jsonl", encoding="utf-8")]


def call(prompt, q, tail, parse, pp):
    cut = prompt.rfind(pj._USER_MARK)
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": prompt[:cut] + "\n" + tail.format(question=q)}]
    opt = {"temperature": 0, "seed": 0, "num_predict": 64, "num_ctx": 4096}
    if pp is not None:
        opt["presence_penalty"] = pp
    raw = requests.post("http://127.0.0.1:11434/api/chat", timeout=300, json={
        "model": "yunsur_v13", "stream": False, "think": False, "keep_alive": "30m", "options": opt, "messages": msgs}).json()["message"]["content"]
    return parse(raw), raw


with open(D + "prompt_only_pp0.jsonl", "w", encoding="utf-8") as w:
    for i in ids:
        r = rows[i]
        prompt = oj.rebuild(Q[i], r["numbered_context"], len(r["doc_ids"]))
        out = {"id": i}
        for name, tail, parse, pp in (("v1_pp15", pj.SHARED_TAIL, pj.parse_pick, None),   # 재생 일치 확인용
                                      ("v1_pp0", pj.SHARED_TAIL, pj.parse_pick, 0),
                                      ("v2_pp0", pj.SHARED_TAIL_V2, pj.parse_pick_v2, 0)):
            out[name], out[name + "_raw"] = call(prompt, Q[i], tail, parse, pp)
        w.write(json.dumps(out, ensure_ascii=False) + "\n")
        print(i, out["v1_pp15"], out["v1_pp0"], out["v2_pp0"], flush=True)
