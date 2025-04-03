from atari_assist.llm.openai_llm import OpenAI_LLM
from atari_assist.llm.ollama_llm import OllamaLLM
from atari_assist.llm.anthropic_llm import ClaudeLLM
from atari_assist.llm.gemini_llm import GeminiLLM
from atari_assist.llm.groq_llm import GroqLLM

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
