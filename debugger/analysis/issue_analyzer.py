"""
Issue Analyzer

Transforms raw execution errors into structured issues.
"""

import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class Issue:
    """
    Represents a detected issue in the code
    """
    type: str
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    fix_hint: Optional[str] = None

class IssueAnalyzer:
    """
    Analyzes execution results and extracts issues
    """
    
    def analyze(self, result) -> Issue:
        stderr = result.stderr

        # -------------------------
        # Missing Dependency
        # -------------------------
        if "ModuleNotFoundError" in stderr:
            match = re.search(r"No module named '(.+?)'", stderr)
            module = match.group(1) if match else None

            return Issue(
                type="missing_dependency",
                message=stderr,
                fix_hint=f"Install package: {module}"
            )
        
        # -------------------------
        # Syntax Error
        # -------------------------
        if "SyntaxError" in stderr:
            return Issue(
                type="syntax_error",
                message=stderr,
                fix_hint="Fix syntax error in code",
            )

        # -------------------------
        # Import Error
        # -------------------------
        if "ImportError" in stderr:
            return Issue(
                type="import_error",
                message=stderr,
                fix_hint="Check module paths or missing __init__.py",
            )

        # -------------------------
        # Attribute Error
        # -------------------------
        if "AttributeError" in stderr:
            return Issue(
                type="attribute_error",
                message=stderr,
                fix_hint="Check object attributes or method names",
            )

        # -------------------------
        # Type Error
        # -------------------------
        if "TypeError" in stderr:
            return Issue(
                type="type_error",
                message=stderr,
                fix_hint="Check function arguments or types",
            )

        # -------------------------
        # Default Case
        # -------------------------
        return Issue(
            type="unknown",
            message=stderr,
            fix_hint="Analyze error manually",
        )