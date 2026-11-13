"""bc_1113 결과 jsonl → results.md (채점 없음, 답 원문 그대로).

  python3 docs/experiments/blind_check_1113/make_results.py
"""
import json, re

D = "docs/experiments/blind_check_1113/"
Q = {l.split("\t")[0]: l.rstrip("\n").split("\t", 1)[1] for l in open(D + "questions.tsv", encoding="utf-8") if "\t" in l}
rows = [json.loads(l) for l in open("docs/experiments/e2e_ko_1008/results/bc_1113.jsonl", encoding="utf-8")]

# ollama ps 기록: 시각 → 올라온 모델. 운영 모델(yunsur_v13) 밖이 있으면 그 분.
other = set()
for l in open(D + "ollama_ps.log", encoding="utf-8"):
    t, _, models = l.strip().partition(" ")
    if any(m and not m.startswith("yunsur_v13") for m in models.split()):
        other.add(t[:5])


# 문항별 시작 · 끝 시각: 실행 시작(bc.out 의 start)부터 elapsed 누적 — 문항 사이 준비 시간은 빠져 약간 이르다
import datetime as _dt
_t = _dt.datetime.strptime(open(D + "start.txt").read().strip(), "%H:%M:%S")
for r in rows:
    r["_span"] = {(_t + _dt.timedelta(seconds=x)).strftime("%H:%M") for x in range(0, int(r["elapsed"]) + 61, 30)}
    _t += _dt.timedelta(seconds=r["elapsed"])


def judge(r):
    js = [s for s in r.get("trace") or [] if s.get("stage") == "judge"]
    if not js:
        return "판정 단계 없음"
    s = js[0]
    if s.get("gates"):
        return f"건너뜀(게이트: {', '.join(s['gates'])})"
    p = s.get("pick")
    if p is None:
        return "판정 실패(힌트 없이 진행)"
    return "없음" if p == "없음" else f"있음 — 문서 {p}"


def titles(ctx):
    out = []
    for m in re.finditer(r"\[문서 (\d+)\].*?\[(\d{4}\.\d{4,5})v?\d*\]\s*([^\n]*)", ctx or "", re.S):
        out.append(f"{m.group(1)}. {m.group(3).strip()} [{m.group(2)}]")
    return out


lines = ["# 논문 봇 점검 25 문항 — 운영 설정 재생 결과 (채점 없음)", "",
         "- 실행: `scripts/eval_e2e_ko.py --answer --save-context` (held-out 재생과 같은 경로, 대화 기록 없음), 운영 `.env` 그대로(`RAG_ANSWER_REPEAT_PENALTY=1.0` 포함). 코드 · `.env` · DB 변경 없음.",
         "- 답 생성은 temperature 0.2 라 같은 질문도 텔레그램에서 물을 때마다 문장이 조금씩 다를 수 있다(검색 · 판정은 같은 입력이면 같다).",
         "- 시간 옆 ⚠ = 그 문항이 도는 동안(시작 시각 + elapsed 누적으로 추정) 운영 모델(`yunsur_v13`) 밖 모델이 Ollama 에 올라와 있었음(`ollama_ps.log`).",
         "- 프롬프트 지문 = 답 LLM 입력(system + user) sha1 앞 12자.", ""]
for r in rows:
    st = " · ".join(f"{k} {v}s" for k, v in r.get("stages", []) if v)
    lines += [f"---", "", f"## {r['id']}. {Q[r['id']]}", "",
              f"- 판정: {judge(r)}",
              f"- 경로: `{r.get('route')}`" + (" — 라우터가 계획(planner) 경로로 보냄. 이 재생 스크립트는 RAG 경로만 돌려 답이 비어 있다. 텔레그램에서는 계획 경로 답이 나간다(재생 안 됨)" if str(r.get("route", "")).startswith("planner") else ""),
              f"- 시간: {r['elapsed']}s{' ⚠' if r['_span'] & other else ''}" + (f" (단계: {st})" if st else ""),
              f"- 답 길이: {r.get('answer_len')}자" + (" (평가 스크립트가 4000자에서 잘라 저장 — 뒤는 빠짐)" if (r.get("answer_len") or 0) > 4000 else ""),
              f"- 프롬프트 지문: `{r.get('answer_input') or '(답 LLM 호출 없음)'}`",
              f"- 오류: {r['error']}" if r.get("error") else "- 오류: 없음", "",
              "**검색된 문서**", ""] + [f"{t}" for t in titles(r.get("numbered_context"))] + (["(없음)"] if not titles(r.get("numbered_context")) else []) + \
             ["", "**최종 답 (원문)**", "", "````text", r.get("answer", ""), "````", ""]
open(D + "results.md", "w", encoding="utf-8").write("\n".join(lines))
print(len(rows), "문항 · 다른 모델 올라온 분", sorted(other))
