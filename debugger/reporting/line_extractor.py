import re
from typing import Optional

def extract_line_number(error_message: str) -> Optional[int]:
    """
    Extract line number from Python tracebacks.
    """
    match = re.search(r'File ".*?", line (\d+)', error_message)
    if match:
        return int(match.group(1))
    return None

def get_code_line(file_path: str, line_number: int) -> str:
    """
    Retrieve a specific line of code from a file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            return lines[line_number - 1].rstrip()
    except Exception:
        return "Unable to retrieve code."