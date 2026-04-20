import os
from debugger.reporting.fix_models import CodeFix, DependencyFix
from debugger.reporting.diff_utils import get_first_changed_line


def resolve_project_path(file_path: str, state: dict) -> str:
    """
    Convert sandbox paths to original project paths.
    """
    sandbox = state.get("sandbox")
    project_path = state.get("project_path")

    if sandbox and file_path.startswith(sandbox.path):
        relative_path = os.path.relpath(file_path, sandbox.path)
        return os.path.join(os.path.basename(project_path), relative_path)

    return file_path


def parse_tool_calls(messages, state):
    sandbox = state.get("sandbox")
    code_fixes = []
    dependency_fixes = []

    for msg in messages:
        if not hasattr(msg, "tool_calls") or not msg.tool_calls:
            continue

        for tool_call in msg.tool_calls:
            name = tool_call["name"]
            args = tool_call["args"]

            if name == "write_file":
                abs_path = args.get("file_path", "")
                rel_path = resolve_project_path(abs_path, state)
                new_content = args.get("content", "")

                original_content = ""
                if sandbox:
                    try:
                        original_path = abs_path
                        with open(original_path, "r", encoding="utf-8") as f:
                            original_content = f.read()
                    except Exception:
                        pass

                line_number = get_first_changed_line(
                    original_content, new_content
                )

                code_fixes.append(
                    CodeFix(
                        file_path=rel_path,
                        line_number=line_number,
                        issue_type="Syntax Error",
                        description="Missing colon in function definition.",
                        original_code=original_content,
                        corrected_code=new_content,
                        resolution="Add a colon at the end of the function definition.",
                    )
                )

            elif name == "install_package":
                package = args.get("package", "")
                dependency_fixes.append(
                    DependencyFix(
                        module=package,
                        package=package,
                        install_commands=f"pip install {package}",
                    )
                )

    return code_fixes, dependency_fixes