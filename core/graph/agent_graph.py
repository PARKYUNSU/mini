"""LangGraph 워크플로우 조립 (Router → … → Monitor)."""

from __future__ import annotations

import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

from core.config.agent_config import CHECKPOINT_DB_PATH
from core.graph.agent_types import AgentState

from core.graph.agent_nodes import (
    direct_answer_node,
    executor_node,
    monitor_node,
    planner_debate_node,
    planner_node,
    route_after_monitor,
    route_after_planner,
    route_after_router,
    router_node,
    use_existing_tool_node,
)


def build_graph(checkpointer=None):
    """Router → Direct/Existing/Planner 분기"""
    workflow = StateGraph(AgentState)

    workflow.add_node("router", router_node)
    workflow.add_node("direct_answer", direct_answer_node)
    workflow.add_node("use_existing_tool", use_existing_tool_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("planner_debate", planner_debate_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("monitor", monitor_node)

    workflow.set_entry_point("router")
    workflow.add_conditional_edges(
        "router",
        route_after_router,
        {
            "direct_answer": "direct_answer",
            "use_existing_tool": "use_existing_tool",
            "planner": "planner",
            "executor": "executor",
        },
    )
    workflow.add_edge("direct_answer", END)
    workflow.add_edge("use_existing_tool", END)
    workflow.add_conditional_edges(
        "planner",
        route_after_planner,
        {"planner_debate": "planner_debate", "executor": "executor", "__end__": END},
    )
    workflow.add_edge("planner_debate", "executor")
    workflow.add_edge("executor", "monitor")
    workflow.add_conditional_edges(
        "monitor", route_after_monitor, {"executor": "executor", "__end__": END}
    )

    if checkpointer is None:
        conn = sqlite3.connect(CHECKPOINT_DB_PATH, check_same_thread=False)
        checkpointer = SqliteSaver(conn)
    return workflow.compile(checkpointer=checkpointer)
