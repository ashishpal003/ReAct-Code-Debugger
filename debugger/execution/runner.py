"""
Execution engine for running Python code inside sandbox.

Key responsibilities:
- Run Python files safely
- Capture stdout, stderr
- Return structured result
"""

import subprocess
import os
from dataclasses import dataclass

@dataclass
class ExecutionResult:
    """
    Structured result of code execution
    """
    stdout: str
    stderr: str
    returncode: int

    @property
    def success(self) -> bool:
        """
        True if execution succeeded
        """
        return self.returncode == 0
    
class Runner:
    def __init__(self, sandbox):
        self.sandbox = sandbox

    def _get_python_bin(self):
        """
        Get Python executable inside virtual environment
        """
        return os.path.join(self.sandbox.venv_path, "bin", "python")
    
    def run(self, entry_file: str = "main.py") -> ExecutionResult:
        """
        Run a Python file inside sandbox
        """

        python_bin = self._get_python_bin()

        print(f"▶️ Running: {entry_file}")

        process = subprocess.run(
            [python_bin, entry_file],
            cwd=self.sandbox.path,
            capture_output=True,
            text=True
        )

        return ExecutionResult(
            stdout=process.stdout,
            stderr=process.stderr,
            returncode=process.returncode
        )
