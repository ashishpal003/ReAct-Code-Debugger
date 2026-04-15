"""
Generates a structured debugging report.
"""

from datetime import datetime
from debugger.llm.llm import get_llm


def generate_report(state: dict) -> str:
    """Generate a detailed debugging report."""
    report = []
    report.append("\n=== ReAct Debugger Report ===")
    report.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Iterations: {state.get('iteration', 0)}")
    report.append(f"Completed: {state.get('completed', False)}\n")

    report.append("Fixes Applied:")
    fixes = state.get("fixes", [])

    if not fixes:
        report.append("No fixes were required.")
    else:
        for i, fix in enumerate(fixes, start=1):
            report.append(f"{i}. {fix}")

    return "\n".join(report)

def summarise_report(report: str):
    """Summarises the report that can be read."""
    llm = get_llm()

    response = llm.invoke(f"""
Covert the given python code report into a resolution format
- Extract just the file name and the code changes applied.
- Extract the packages installed and let of the packges installed as pip install <package_name>

# Report:   
{report}
"""
    )

    return response.content
