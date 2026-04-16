from debugger.config.langsmith import setup_langsmith
from debugger.config.settings import settings
from debugger.sandbox.sandbox import Sandbox
from debugger.agent.graph import build_debugger_graph
from debugger.reporting.report_generator import generate_report


def main():
    setup_langsmith()

    project_path = "/Users/ashishpal/Documents/GenAI_Projects/for_testing/example_project"
    entry_file = "main.py"

    print(f"Using model: {settings.ollama_model}")
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

        final_state = graph.invoke(initial_state)

        # print("\n✅ Debugging Complete!")
        # print("\n🔧 Fixes Suggested:\n")
        # for i, fix in enumerate(final_state.get("fixes", []), 1):
        #     print(f"{i}. {fix}")

        final_state["model_name"] = settings.ollama_model
        print(generate_report(final_state))


if __name__ == "__main__":
    main()