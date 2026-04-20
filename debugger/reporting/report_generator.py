"""
Generates a structured debugging report.
"""

from datetime import datetime
from debugger.reporting.fix_parser import parse_tool_calls


def generate_report(state: dict) -> str:
    sandbox = state.get("sandbox")
    messages = state.get("messages", [])
    execution_result = state.get("execution_result")

    code_fixes, dependency_fixes = parse_tool_calls(messages, state)

    report = []
    report.append("\n=== ReAct Code Debugger Report ===\n")
    report.append(f"Project Path: {state.get('project_path')}")
    report.append(
        f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    report.append(f"Model Used: {state.get('model_name')}")
    report.append(f"Iterations: {state.get('iteration', 0)}")
    report.append(
        f"Execution Status: {'SUCCESS' if state.get('completed') else 'FAILED'}"
    )

    report.append("\n" + "─" * 48)

    # Code Fixes
    for i, fix in enumerate(code_fixes, start=1):
        report.append(f"\n🔴 Issue {i}: {fix.issue_type}")
        report.append(f"File: {fix.file_path}")
        if fix.line_number:
            report.append(f"Line: {fix.line_number}")
        report.append(f"\nDescription:\n{fix.description}")
        report.append(f"\nCorrected Code:\n{fix.corrected_code}")
        report.append(f"\nResolution:\n{fix.resolution}")
        report.append("\n" + "─" * 48)

    # Dependency Fixes
    offset = len(code_fixes)
    for i, dep in enumerate(dependency_fixes, start=1):
        report.append(f"\n🟡 Issue {offset + i}: Missing Dependency")
        report.append(f"Module: {dep.module}")
        report.append(f"Install Command: {dep.install_commands}")
        report.append("\n" + "─" * 48)

    # Execution Output
    if execution_result:
        report.append("\n✅ Execution Output")
        report.append(execution_result.stdout.strip())

    report.append("\n" + "─" * 48)
    report.append("\n🧹 Sandbox Cleanup Completed Successfully.")

    return "\n".join(report)