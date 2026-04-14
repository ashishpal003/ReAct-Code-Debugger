"""
LLM initialization using Ollama + LangChain

We use langchain-community's ChatOllama.
"""

from langchain_ollama.chat_models import ChatOllama
from debugger.config.settings import settings

def get_llm():
    """
    Returns a configured Ollama LLM instance.

    Why ChatOllama>
    - Native LangChain integration
    - Supports tool calling (important later)
    - Works locally (no API cost)
    """
    print("Using model:", settings.ollama_model)

    llm = ChatOllama(
        model=settings.ollama_model,
        temperature=0,
    )

    return llm