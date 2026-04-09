"""
LangChain tools for the debugging agent.

These tools will be used by the React agent (Phase 3).
"""

from langchain_core.tools import tool
import subprocess
import os

# -------------------------
# File Tools
# -------------------------

@tool
def read_file(path: str) -> str:
    """
    Read file content
    """
    try:
        with open(path, "r") as f:
            return f.read()
    
    except Exception as e:
        return f"Error reading file: {str(e)}"
    
@tool
def write_file(path: str, content: str) -> str:
    """
    Write content to file
    """
    try:
        with open(path, "w") as f:
            f.write(content)
        return "File updated successfully"
    except Exception as e:
        return f"Error writing file: {str(e)}"
    

# -------------------------
# Dependency Tool
# -------------------------

@tool
def install_package(package: str) -> str:
    """
    Install a Python package using pip
    """
    try:
        subprocess.run(
            ["pip", "install", package],
            capture_output=True,
            text=True,
        )
        return f"Installed {package}"
    except Exception as e:
        return f"Error installing package: {str(e)}"


# -------------------------
# Code Execution Tool
# -------------------------

@tool
def run_python_file(path: str) -> str:
    """
    Execute a Python file
    """
    try:
        result = subprocess.run(
            ["python", path],
            capture_output=True,
            text=True,
        )
        return result.stdout + "\n" + result.stderr
    except Exception as e:
        return f"Execution error: {str(e)}"