"""
Registers all tools available to the agent.
"""

from debugger.tools.sandbox_tools import (
    read_file,
    write_file,
    install_package,
    run_project
)

def get_debugger_tools():
    """
    Return the list of debugger tools.
    """
    return [
        read_file,
        write_file,
        install_package,
        run_project,
    ]