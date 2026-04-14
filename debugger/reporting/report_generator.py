"""
Generates a structured debugging report.
"""

from datetime import datetime

def generate_report(state):
    report = []
    report.append("=== ReAct Debugger Report ===")
    report.append(f"Timestamp: {datetime.now()}")
    report.append(f"Iterations: {state.get('iteration')}")
    report.append(f"Completed: {state.get('completed')}\n")

    report.append("Fixes Applied:")
    for idx, fix in enumerate(state.get("fixes", []), 1):
        report.append(f"{idx}. {fix}")

    return "\n".join(report)