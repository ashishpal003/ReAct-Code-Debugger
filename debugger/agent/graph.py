from langgraph.graph import StateGraph, END
from debugger.agent.state import DebuggerState
from debugger.agent.nodes import (
    setup_tools,
    execute_project,
    analyze_issue,
    reason,
    increment_iteration,
    tool_node,
)


def route_after_analyze(state: DebuggerState):
    """Route based on execution success."""
    if state.get("completed", False):
        return END
    return "reason"


def route_after_reason(state: DebuggerState):
    """Route to tools if tool calls exist."""
    messages = state.get("messages", [])
    
    if not messages:
        return "increment"

    last_message = messages[-1]
    
    if getattr(last_message, "tool_calls", None):
        return "tools"
    
    return "increment"


def should_continue(state: DebuggerState):
    """Determine whether to continue debugging."""
    if state.get("iteration", 0) >= state.get("max_iterations", 5):
        return END
    return "execute"


def build_debugger_graph():
    workflow = StateGraph(DebuggerState)

    # Nodes
    workflow.add_node("setup_tools", setup_tools)
    workflow.add_node("execute", execute_project)
    workflow.add_node("analyze", analyze_issue)
    workflow.add_node("reason", reason)
    workflow.add_node("tools", tool_node)
    workflow.add_node("increment", increment_iteration)

    # Entry point
    workflow.set_entry_point("setup_tools")

    # Edges
    workflow.add_edge("setup_tools", "execute")
    workflow.add_edge("execute", "analyze")

    workflow.add_conditional_edges(
        "analyze",
        route_after_analyze,
        {
            "reason": "reason",
            END: END,
        },
    )

    workflow.add_conditional_edges(
        "reason",
        route_after_reason,
        {
            "tools": "tools",
            "increment": "increment",
        },
    )

    workflow.add_edge("tools", "increment")
    workflow.add_edge("increment", "execute")

    return workflow.compile()