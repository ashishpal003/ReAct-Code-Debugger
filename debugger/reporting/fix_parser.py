import os
from debugger.reporting.fix_models import CodeFix, DependencyFix


def parse_tool_calls(messages, sandbox_path):
    """
    Convert tool calls into structured fixes.
    """
    code_fixes = []
    dependency_fixes = []

    for msg in messages:
        if not hasattr(msg, "tool_calls"):
            continue

        for tool_call in msg.tool_calls:
            name = tool_call["name"]
            args = tool_call["args"]

            if name == "write_file":
                file_path = args.get("file_path", "")
                content = args.get("content", "")
                rel_path = os.path.relpath(file_path, sandbox_path)

                code_fixes.append(
                    CodeFix(
                        file_path=rel_path,
                        line_number=0,
                        issue_type="Code Fix",
                        description="File was modified to resolve errors.",
                        original_code="Refer to previous version.",
                        corrected_code=content,
                        resolution="Update the file with the corrected implementation.",
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