"""고친 안을 코드 수정 없이 덮어씌워(monkeypatch) 라우터 1단계 결과가 어떻게 바뀌는지 본다."""
import json, re, sys
sys.path.insert(0, ".")
from core.graph import agent_nodes as N
from core.graph import agent_router_rules as R
from core.rag.topic_gate import is_academic_query_full

D = "docs/experiments/router_open_1103/"
corpus = {r["q"]: r["src"] for r in json.load(open(D + "step1_nonrag.json", encoding="utf-8"))}
# 1단계에서 RAG(B)로 가던 질문도 함께 본다(새로 RAG 밖으로 새면 안 됨)
import glob, sqlite3
for i, t in sqlite3.connect(".bridge/agent_bridge.sqlite").execute("select id, user_text from bridge_jobs"):
    if t and t.strip():
        corpus.setdefault(t.strip(), "실사용")
for f in sorted(glob.glob("docs/experiments/**/*.tsv", recursive=True)):
    name = f.split("/")[-1]
    if "heldout" in name and "heldout_open" not in name:
        continue
    for l in open(f, encoding="utf-8"):
        p = l.rstrip("\n").split("\t")
        if len(p) >= 2 and re.search(r"[가-힣]", p[1]) and len(p[1]) >= 6 and not l.startswith("#") and re.match(r"^[A-Za-z]{1,3}_?\d|^d\d{4}|^[A-Z]_[A-Z]\d", p[0]):
            corpus.setdefault(p[1].strip(), f.split("/")[2])
NEG = ["최근 논문 알려줘", "최신 논문 알려줘", "DB에 논문 뭐 있어?", "저장된 논문 목록 보여줘", "논문 몇 편 있어?",
       "크로마DB에 저장된 논문 개수 알려줘", "요즘 들어온 논문 뭐 있어", "논문 목록 알려줘", "어떤 논문이 저장되어 있어?",
       "DB에 무슨 논문 있어?", "저장된 논문 보여줘", "내일 부산 날씨 어때?", "오늘 IT 뉴스 알려줘",
       "웹 검색해서 엔비디아 주가 알려줘", "인터넷에서 맛집 찾아줘", "최신 뉴스 요약해줘", "오늘 뉴스 알려줘"]
POS = ["LLM 양자화 최신 논문 두 편 알려줘", "음성 인식 논문 중 재밌는 거 알려줘", "그래프 신경망 괜찮은 논문 있으면 알려줘",
       "강화학습 보상 설계 연구 중 볼만한 논문 하나 알려줘", "기상 예측 딥러닝 논문 알려줘", "날씨 데이터로 전력 수요를 예측하는 연구 알려줘",
       "뉴스 기사를 요약하는 LLM 연구 알려줘", "웹 검색을 쓰는 에이전트 연구 알려줘"]
for q in NEG: corpus.setdefault(q, "합성-유지")
for q in POS: corpus.setdefault(q, "합성-RAG")

orig = {k: getattr(R, k) for k in ("_names_paper_topic", "is_weather_tool_request", "get_search_intent")}
_P_END = re.compile(r"(에서|에|의|은|는|이|가|을|를|들)(?=\s|$|[?.!])")
_FILL2 = re.compile(r"(db|저장된|저장돼\s*있는|저장되어|최근|최신|요즘|목록|리스트|알려\s*줘|보여\s*줘|뭐\s*있어|있어|조회|좀|해줘|어떤|무슨|몇\s*(개|편)|개수|하나)")

def topic_llm(q):
    stripped = re.sub(r"(논문|연구|paper|chromadb)", " ", q or "", flags=re.IGNORECASE)
    return is_academic_query_full(stripped) or orig["_names_paper_topic"](q)

def topic_regex(q):
    stripped = re.sub(r"(논문|연구|paper|chromadb)", " ", q or "", flags=re.IGNORECASE)
    if R.is_academic_query(stripped):
        return True
    content = _FILL2.sub(" ", _P_END.sub(" ", stripped.lower()))
    return len(re.sub(r"[^가-힣a-z0-9]", "", content)) >= 5

def weather2(q):
    return not re.search(r"논문|연구", q or "") and orig["is_weather_tool_request"](q)

def intent2(q, ql):
    return "rag" if "연구" in ql else orig["get_search_intent"](q, ql)

VARIANTS = {"현재": {}, "1a 주제 LLM": {"_names_paper_topic": topic_llm}, "1b 주제 정규식": {"_names_paper_topic": topic_regex},
            "2 날씨 막기": {"is_weather_tool_request": weather2}, "3 연구→rag": {"get_search_intent": intent2},
            "1b+2+3": {"_names_paper_topic": topic_regex, "is_weather_tool_request": weather2, "get_search_intent": intent2}}

def route(q):
    r = N.router_step1_hard_rules(q, q.lower(), "router_diag_1103") or {}
    t = r.get("route_type", "2단계")
    return t + ("/" + r.get("used_tool_name", "") if t == "use_existing_tool" else "/" + r.get("router_choice", "") if r else "")

res = {}
for name, patch in VARIANTS.items():
    for k, v in orig.items():
        setattr(R, k, patch.get(k, v))
    res[name] = {q: route(q) for q in corpus}
for k, v in orig.items():
    setattr(R, k, v)
base = res["현재"]
print("질문", len(corpus))
for name in VARIANTS:
    if name == "현재":
        continue
    ch = [(corpus[q], base[q], res[name][q], q) for q in corpus if res[name][q] != base[q]]
    print(f"\n== {name}: 바뀜 {len(ch)}")
    for s, a, b, q in sorted(ch):
        print(f"  [{s}] {a} → {b} | {q[:70]}")
print("\n== 합성 유지(현재 경로)")
for q in NEG:
    print(f"  {base[q]} | 1b+2+3 {res['1b+2+3'][q]} | {q}")
json.dump({k: v for k, v in res.items()}, open(D + "proto_routes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
