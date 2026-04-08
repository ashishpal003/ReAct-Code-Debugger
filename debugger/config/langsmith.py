"""
LangSmith setup for observability.

This allows:
- Tracking agent decisions
- Debugging reasoning steps
- Visualizing LangGraph execution
"""

import os
from debugger.config.settings import settings

def setup_langsmith():
    """
    Configure LangSmith environment variables
    """

    if settings.tracking_enabled and settings.langsmith_api_key:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
        os.environ["LANGCHAIN_PROJECT"] = "react-debugger"

        print("LangSmith tracing enabled")
    else:
        print("LangSmith not configured")