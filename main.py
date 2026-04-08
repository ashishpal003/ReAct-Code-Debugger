"""
Entry point to test Phase 1
"""

from debugger.config.langsmith import setup_langsmith
from debugger.config.settings import settings
from debugger.llm.llm import get_llm
from debugger.sandbox.sandbox import Sandbox


def main():
    # Setup tracing
    setup_langsmith()

    # Initialize LLM
    llm = get_llm()

    print("Testing LLM...")
    response = llm.invoke("Say hello from the debugger agent")

    print("LLM Response: ", response.content)

    # Test Sandbox
    print("\nTesting Sandbox...")
    sandbox = Sandbox(source_path=".", root_dir=settings.sandbox_root)
    sandbox.setup()

    print("Sandbox ready at: ", sandbox.path)

if __name__ == "__main__":
    main()