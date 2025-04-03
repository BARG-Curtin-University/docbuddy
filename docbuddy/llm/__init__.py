from docbuddy.llm.openai_llm import OpenAI_LLM
from docbuddy.llm.ollama_llm import OllamaLLM
from docbuddy.llm.anthropic_llm import ClaudeLLM
from docbuddy.llm.gemini_llm import GeminiLLM
from docbuddy.llm.groq_llm import GroqLLM

def get_llm(model: str):
    if model == "openai":
        return OpenAI_LLM()
    elif model == "ollama":
        return OllamaLLM()
    elif model == "claude":
        return ClaudeLLM()
    elif model == "gemini":
        return GeminiLLM()
    elif model == "groq":
        return GroqLLM()
    else:
        raise ValueError(f"Unsupported model: {model}")