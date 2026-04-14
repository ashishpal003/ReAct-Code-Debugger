"""
Defines the state for the LangGraph debugging agent.
"""

from typing import TypedDict, List, Any, Optional
from langchain_core.messages import BaseMessage
from debugger.execution.runner import ExecutionResult
from debugger.analysis.issue_analyzer import Issue


class DebuggerState(TypedDict, total=False):
    # Input
    project_path: str
    entry_file: str

    # Sandbox
    sandbox: Any

    # Execution Data
    execution_result: Optional[ExecutionResult]
    execution_output: Optional[str]
    issue: Optional[Issue]

    # Agent Memory
    messages: List[BaseMessage]
    fixes: List[str]

    # Iteration Control
    iteration: int
    max_iterations: int
    completed: bool