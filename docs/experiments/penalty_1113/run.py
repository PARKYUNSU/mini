"""반복 억제 설정이 한국어 깨짐을 만드는지 (README). 맥미니에서:

  .venv/bin/python docs/experiments/penalty_1113/run.py

held-out 대조(hj_ctl) 의 답 입력을 다시 만들어, 운영 샘플링(temperature 0.2 · top_p 0.8)에
반복 억제만 바꿔 v13 으로 답을 다시 낸다. 조건마다 seed 0~2 세 번(temperature 0.2 라 seed 가 답을 바꾼다).
"""
import json, os, sys

sys.path.insert(0, ".")
sys.path.insert(0, "docs/experiments/open_judge_1103")
import hashlib, oj, requests
import core.llm.presence_judge as pj
from core.llm.agent_prompts import DIRECT_ANSWER_RAG_SYSTEM_BASE as SYS

D = "docs/experiments/penalty_1113/"
IDS = sys.argv[1:] or ["H_D11", "H_A28", "H_H06", "G06", "G19",  # 깨짐 있던 5
                       "G01", "G07", "G12", "H_A02"]          # 멀쩡했던 4(부작용 확인)
COND = {"ops": {"repeat_penalty": 1.18},                       # 운영: 모델 파일의 presence_penalty 1.5 도 그대로 적용
        "rp1": {"repeat_penalty": 1.0},                        # repeat 만 끔
        "pp0": {"repeat_penalty": 1.18, "presence_penalty": 0}, # presence 만 끔(핵심)
        "off": {"repeat_penalty": 1.0, "presence_penalty": 0}}  # 둘 다 끔
Q = {l.split("\t")[0]: l.rstrip("\n").split("\t", 1)[1] for l in open("docs/experiments/judge_v2_1113/heldout120.tsv", encoding="utf-8") if "\t" in l}
rows = {json.loads(l)["id"]: json.loads(l) for l in open("docs/experiments/e2e_ko_1008/results/hj_ctl.jsonl", encoding="utf-8")}
with open(D + "answers_fixed.jsonl", "a", encoding="utf-8") as w:
    for i in IDS:
        r = rows[i]
        prompt = oj.rebuild(Q[i], r["numbered_context"], len(r["doc_ids"]))
        # 운영과 같은 system: 대조 판정이 '없음' 이면 NO_DOC_HINT 가 붙는다 — 답 입력 지문으로 확인
        nodoc = any(s.get("stage") == "judge" and s.get("pick") == "없음" for s in r["trace"])
        sys_p = SYS + (pj.NO_DOC_HINT if nodoc else "")
        assert hashlib.sha1((sys_p + "\n" + prompt).encode()).hexdigest()[:12] == r["answer_input"], i
        for name, extra in COND.items():
            for seed in range(3):
                opt = {"temperature": 0.2, "top_p": 0.8, "num_predict": 1500, "num_ctx": 4096, "seed": seed, **extra}
                res = requests.post("http://127.0.0.1:11434/api/chat", timeout=600, json={
                    "model": "yunsur_v13", "stream": False, "think": False, "options": opt, "keep_alive": "30m",
                    "messages": [{"role": "system", "content": sys_p}, {"role": "user", "content": prompt}]}).json()
                w.write(json.dumps({"id": i, "cond": name, "seed": seed, "answer": res["message"]["content"]}, ensure_ascii=False) + "\n")
                w.flush()
                print(i, name, seed, len(res["message"]["content"]), flush=True)
