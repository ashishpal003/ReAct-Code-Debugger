"""
Defines the state for the LangGraph debugging agent.
"""

from typing import TypedDict, List, Optional
from debugger.analysis.issue_analyzer import Issue
from debugger.execution.runner import ExecutionResult

class DebuggerState(TypedDict, total=False):
    """
    Represents the shared state of the debugging workflow.
    """

    # Input
    project_path: str
    entry_file: str

    # Excution artifacts
    sandbox: object
    execution_result: ExecutionResult
    issue: Optional[Issue]

    # Iteration control
    iteration: int
    max_iterations: int

    # Agent reasoning trace
    message: List

    # Output
    fixes: List[str]
    completed: bool