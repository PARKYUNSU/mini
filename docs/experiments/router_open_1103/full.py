import re, sys
sys.path.insert(0, ".")
from core.graph import agent_nodes as N
from core.graph import agent_router_rules as R
orig = {k: getattr(R, k) for k in ("is_weather_tool_request", "get_search_intent")}
def weather2(q):
    return not re.search(r"논문|연구", q or "") and orig["is_weather_tool_request"](q)
def intent2(q, ql):
    return "rag" if "연구" in ql else orig["get_search_intent"](q, ql)
QS = ["LLM이 모르는 최신 사건 질문에 답할 때 웹 검색을 붙이는 방법 연구 찾아줘",
      "에이전트가 웹을 검색하며 보고서를 쓰는 시스템을 만들고 있다. 이런 deep research 에이전트의 평가 벤치마크, 출처 검증 방법, 긴 보고서의 사실성 평가를 다룬 최신 연구를 찾아주세요.",
      "사용자 질문을 검색하기 좋게 다시 써 주는 방법 알려줘"]
for name, patch in (("현재", {}), ("고침", {"is_weather_tool_request": weather2, "get_search_intent": intent2})):
    for k, v in orig.items():
        setattr(R, k, patch.get(k, v))
    for q in QS:
        outs = []
        for t in range(2):
            r = N.router_node({"user_request": q}, config={"configurable": {"chat_id": f"router_diag_full_{t}"}})
            outs.append(f"{r.get('route_type')}/{r.get('router_choice')}/{r.get('used_tool_name', '')}")
        print(name, "|", outs, "|", q[:50])
