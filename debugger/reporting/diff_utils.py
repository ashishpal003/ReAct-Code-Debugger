import difflib


def get_first_changed_line(original: str, modified: str) -> int:
    """
    Identify the first line where the code differs.
    """
    original_lines = original.splitlines()
    modified_lines = modified.splitlines()

    diff = difflib.ndiff(original_lines, modified_lines)

    line_number = 1
    for line in diff:
        if line.startswith("- ") or line.startswith("+ "):
            return line_number
        if not line.startswith("?"):
            line_number += 1

    return 0