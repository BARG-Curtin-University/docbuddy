import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
DEFAULT_API_KEY = OPENAI_API_KEY

# Set the default model to use
DEFAULT_MODEL = "openai"
OLLAMA_MODEL = "llama3"
OPENAI_MODEL = "gpt-3.5-turbo"
CLAUDE_MODEL = "claude-3-haiku-20240307"
GEMINI_MODEL = "models/gemini-pro"
GROQ_MODEL = "mixtral-8x7b-32768"