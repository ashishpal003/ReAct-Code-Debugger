"""
Entry point for the ReAct Code Debugger.
"""

from debugger.config.langsmith import setup_langsmith
from debugger.config.settings import settings
from debugger.sandbox.sandbox import Sandbox
from debugger.agent.graph import build_debugger_graph


def main():
    # Enable LangSmith tracing
    setup_langsmith()

    project_path = "/Users/ashishpal/Documents/GenAI_Projects/for_testing/example_project"  # Replace with your project
    entry_file = "main.py"

    print("🚀 Starting ReAct Debugger...\n")

    with Sandbox(
        source_path=project_path,
        root_dir=settings.sandbox_root,
        auto_cleanup=True,
    ) as sandbox:

        graph = build_debugger_graph()

        initial_state = {
            "project_path": project_path,
            "entry_file": entry_file,
            "sandbox": sandbox,
            "iteration": 0,
            "max_iterations": settings.max_iterations,
            "messages": [],
            "fixes": [],
            "completed": False,
        }

        result = graph.invoke(initial_state)

        print("\n✅ Debugging Complete!")
        print("\n🔧 Suggested Fixes:\n")

        for i, fix in enumerate(result.get("fixes", []), start=1):
            print(f"{i}. {fix}\n")


if __name__ == "__main__":
    main()