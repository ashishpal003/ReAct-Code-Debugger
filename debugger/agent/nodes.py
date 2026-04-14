"""
LangGraph nodes for the ReAct Debugging Agent
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from debugger.llm.llm import get_llm
from debugger.tools.registry import get_debugger_tools
from debugger.tools.sandbox_tools import configure_sandbox_tools
from debugger.analysis.issue_analyzer import IssueAnalyzer
from debugger.execution.runner import Runner

llm = get_llm()
tools = get_debugger_tools()
llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)


# -------------------------
# Node 1: Inject tools
# -------------------------
def setup_tools(state):
    """
    Inject sandbox into tools.
    """
    configure_sandbox_tools(state["sandbox"])
    return state

# -------------------------
# Node 2: Execute Code
# -------------------------
def execute_project(state):
    """
    Excute the project inside the sandbox.
    """
    sandbox = state["sandbox"]
    entry_file = state["entry_file"]

    runner = Runner(state["sandbox"])

    try:
        result = runner.run(entry_file)
    except Exception as e:
        # Create a fallback result
        from debugger.execution.runner import ExecutionResult
        result = ExecutionResult(
            stdout="",
            stderr=str(e),
            returncode=1,
        )

    state["execution_output"] = result.stdout + "\n" + result.stderr
    state["execution_result"] = result

    return state

# -------------------------
# Node 3: Analyze Issue
# -------------------------
def analyze_issue(state):
    """Analyze execution results.
    """
    result = state.get("execution_result")

    if result is None:
        state["issue"] = None
        state["completed"] = False
        return state
    
    analyzer = IssueAnalyzer()
    issue = analyzer.analyze(result)

    state["issue"] = issue
    state["completed"] = result.success

    return state

# -------------------------
# Node 4: Reason and Act
# -------------------------
def reason(state):
    """
    ReAct reasoning step with tool-calling support.
    """
    if state.get("completed", False):
        return state

    issue = state.get("issue")
    output = state.get("execution_output", "")

    system_message = SystemMessage(
        content=(
            "You are an expert Python debugging engineer."
            "Fix issues using the available tools."
            "Always rerun the project after applying fixes."
        )
    )

    human_message = HumanMessage(
        content=f"""
Execution Output:
{output}

Issue Type:
{getattr(issue, 'type', 'unknown')}

Hint:
{getattr(issue, 'fix_hint', 'No hint available')}

Fix the issue using the tools.
"""
    )

    messages = state.get("messages", [])

    if not any(isinstance(m, SystemMessage) for m in messages):
        messages.append(system_message)

    messages.append(human_message)

    response = llm_with_tools.invoke(messages)
    messages.append(response)
    
    state["messages"] = messages

    # Handle empty content when tool calls exist
    if response.tool_calls:
        for tool_call in response.tool_calls:
            state.setdefault("fixes", []).append(
                f"Tool called: {tool_call['name']} with args {tool_call['args']}"
            )
    else:
        state.setdefault("fixes", []).append(
            response.content or "No textual response generated."
        )

    return state

# -------------------------
# Node 5: Increment Counter
# -------------------------
def increment_iteration(state):
    """Increment iteration counter."""
    state["iteration"] += 1
    return state