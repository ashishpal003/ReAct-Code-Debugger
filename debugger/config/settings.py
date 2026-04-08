"""
Central configuration system for the debugger.

Why this matters:
- Avoid hardcoding values everywhere
- Easy to switch models / configs
- Works well with LangChain + LangGraph
"""

import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Settings(BaseModel):
    """
    Type-safe configuration using Pydantic v2
    """

    # ===== LLM SETTINGS =====
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")

    # ===== LANGSMITH =====
    langsmith_api_key: str | None = os.getenv("LANGCHAIN_API_KEY")
    tracking_enabled: bool = os.getenv("LANGCHAIN_TRACING_V2", "false") == "true"

    # ===== DEBUGGER =====
    max_iterations: int = 10
    sandbox_root: str = "/tmp/react_debugger"

    # ===== EXECUTION =====
    python_bin: str = "python3"

# Singleton config
settings = Settings()