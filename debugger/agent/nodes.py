"""
LangGraph nodes for the ReAct Debugging Agent
"""

from langchain_core.messages import HumanMessage
from debugger.execution.runner import Runner
from debugger.analysis.issue_analyzer import IssueAnalyzer
from debugger.llm.llm import get_llm
from debugger.config.settings import settings

llm = get_llm()

# -------------------------
# Node 1: Execute Code
# -------------------------
def execute_code(state):
    """
    Executes the project inside the sandbox.
    """
    sandbox = state["sandbox"]
    entry_file = state["entry_file"]

    runner = Runner(sandbox)
    result = runner.run(entry_file)

    state["execution_result"] = result
    return state

# -------------------------
# Node 1: Execute Code
# -------------------------
def analyze_issue(state):
    """
    Analyzes execution output and detects issues.
    """
    analyzer = IssueAnalyzer()
    issue = analyzer.analyze(state["execution_result"])

    state["issue"] = issue

    if state["execution_result"].success:
        state["completed"] = True

    return state

# -------------------------
# Node 2: Analyze Issue
# -------------------------
def reason(state):
    """
    Uses the LLM to determine the next action.
    """
    issue = state.get("issue")

    if not issue:
        return state
    
    prompt = f"""
You are an expert Python debugging engineer.

Project Error:
{issue.message}

Issue Type:
{issue.type}

Suggested Hint:
{issue.fix_hint}

Provide the corrective action required to fix the issue.
"""
    
    response = llm.invoke([HumanMessage(content=prompt)])

    state.setdefault("messages", []).append(response)
    state.setdefault("fixes", []).append(response.content)

    return state

# -------------------------
# Node 4: Increment Counter
# -------------------------
def increment_iteration(state):
    """
    Increments iteration count to avoid infinite loops
    """
    state["iteration"] += 1
    return state