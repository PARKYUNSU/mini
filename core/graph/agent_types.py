"""LangGraph 상태·공용 상수 (무거운 의존성 없음)."""

from typing import Literal, TypedDict

# graph.stream 예외 시 진행 메시지에 표시 (텔레그램 핸들러에서 편집)
STREAM_FAILURE_TELEGRAM_MSG = (
    "🚨 시스템 내부 오류로 답변 생성에 실패했습니다. /cancel 후 다시 시도해주세요."
)


class AgentState(TypedDict, total=False):
    user_request: str
    image_base64: str  # 직전 턴의 이미지(문맥용). Vision 라우팅은 message.photo 있을 때만.
    route_type: Literal["direct_answer", "use_existing_tool", "planner", "code_run"]
    router_choice: Literal["A", "B", "C"]  # A=일상, B=RAG, C=Plan&Code
    direct_response: str  # Router → Direct Answer 결과
    python_example_direct: bool  # True: 짧은 코드 예제만(승인·E2B 없음)
    light_monitor: bool  # code_run: 관련성 검수 생략·재시도 축소
    skip_tool_save: bool  # 성공해도 agent_tools 저장 안 함
    agent_fatal_error: str  # 노드 내부 치명 오류 시 상위에서 통합 알림
    plan: list[str]
    approval_status: Literal["pending", "approved", "rejected"]
    generated_code: str
    execution_result: str
    retry_count: int
    error_hint: str  # Monitor → Executor 재시도 시 힌트
    content_irrelevant: bool  # Monitor: 실행 결과가 user_request와 무관함(엉뚱한 결과)
    used_tool_name: str  # 선택 또는 기억에서 복구한 기존 도구명
