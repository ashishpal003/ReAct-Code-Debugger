"""
Entry point to test Phase 1
"""

from debugger.config.settings import settings
from debugger.sandbox.sandbox import Sandbox
from debugger.execution.runner import Runner
from debugger.analysis.issue_analyzer import IssueAnalyzer


def main():
    with Sandbox(source_path="/Users/ashishpal/Documents/GenAI_Projects/for_testing/example_project", root_dir=settings.sandbox_root) as sandbox:

        # Step 1: Run code
        runner = Runner(sandbox)
        result = runner.run("main.py")

        print("\n--- STDOUT ---")
        print(result.stdout)

        print("\n--- STDERR ---")
        print(result.stderr)

        # Step 2: Analyze issues
        analyzer = IssueAnalyzer()
        issue = analyzer.analyze(result)

        print("\n--- ISSUE DETECTED ---")
        print(issue)


if __name__ == "__main__":
    main()