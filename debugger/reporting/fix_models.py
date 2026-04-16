from dataclasses import dataclass
from typing import Optional

@dataclass
class CodeFix:
    file_path: str
    line_number: int
    issue_type: str
    description: str
    original_code: str
    corrected_code: str
    resolution: str

@dataclass
class DependencyFix:
    module: str
    package: str
    install_commands: str