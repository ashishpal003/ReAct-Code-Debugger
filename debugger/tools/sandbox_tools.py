"""
Sandbox-aware tools for the ReAct Debugger.
Compatible with LangChain's tool-calling interface.
"""

import os
import subprocess
from langchain_core.tools import tool

SANDBOX_PATH = None
VENV_PATH = None


def configure_sandbox_tools(sandbox):
    """Inject sandbox context into tools."""
    global SANDBOX_PATH, VENV_PATH
    SANDBOX_PATH = sandbox.path
    VENV_PATH = sandbox.venv_path


def _get_pip_path():
    return os.path.join(VENV_PATH, "bin", "pip")


def _get_python_path():
    return os.path.join(VENV_PATH, "bin", "python")


@tool
def read_file(file_path: str) -> str:
    """Read a file from the sandbox."""
    abs_path = os.path.join(SANDBOX_PATH, file_path)
    try:
        with open(abs_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


@tool
def write_file(file_path: str, content: str) -> str:
    """Write content to a file in the sandbox."""
    abs_path = os.path.join(SANDBOX_PATH, file_path)
    try:
        with open(abs_path, "w") as f:
            f.write(content)
        
        return f"Successfully updated {file_path}"
    except Exception as e:
        return f"Error writing file: {e}"


@tool
def install_package(package: str) -> str:
    """Install a Python package inside the sandbox."""
    try:
        result = subprocess.run(
            [_get_pip_path(), "install", package],
            cwd=SANDBOX_PATH,
            capture_output=True,
            text=True,
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Installation failed: {e}"


@tool
def run_project(entry_file: str) -> str:
    """Run the Python project inside the sandbox."""
    try:
        result = subprocess.run(
            [_get_python_path(), entry_file],
            cwd=SANDBOX_PATH,
            capture_output=True,
            text=True,
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Execution failed: {e}"