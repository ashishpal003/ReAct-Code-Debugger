"""
Defines the LangGraph workflow for the debugging agent.
"""

from langgraph.graph import StateGraph, END
from debugger.agent.state import DebuggerState
from debugger.agent.nodes import (
    execute_code,
    analyze_issue,
    reason,
    increment_iteration,
)

def should_continue(state: DebuggerState):
    """
    Determines whether the agent should continue debugging.
    """
    if state.get("completed", False):
        return "end"
    
    if state["iteration"] >= state["max_iterations"]:
        return "end"
    
    return "continue"

def build_debugger_graph():
    """
    Constructs and compiles the LangGraph debugger workflow.
    """
    workflow = StateGraph(DebuggerState)

    # Add nodes
    workflow.add_node("execute", execute_code)
    workflow.add_node("analyze", analyze_issue)
    workflow.add_node("reason", reason)
    workflow.add_node("increment", increment_iteration)

    # Define edges
    workflow.set_entry_point("execute")
    workflow.add_edge("execute", "analyze")
    workflow.add_edge("analyze", "reason")
    workflow.add_edge("reason", "increment")

    # Conditional routing
    workflow.add_conditional_edges(
        "increment",
        should_continue,
        {
            "continue": "execute",
            "end": END
        },
    )

    return workflow.compile()