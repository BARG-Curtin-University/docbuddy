"""Groq LLM implementation."""
from groq import Groq
from atari_assist.config import GROQ_API_KEY, GROQ_MODEL
from atari_assist.llm.base import BaseLLM

class GroqLLM(BaseLLM):
    """Groq LLM implementation."""
    
    def __init__(self, model=None, api_key=None):
        """Initialize the Groq LLM.
        
        Args:
            model: The Groq model to use (defaults to config.GROQ_MODEL)
            api_key: The Groq API key (defaults to config.GROQ_API_KEY)
        """
        self.model = model or GROQ_MODEL
        self.api_key = api_key or GROQ_API_KEY
        self.client = Groq(api_key=self.api_key) if self.api_key else None
    
    def ask(self, prompt: str) -> str:
        """Send a prompt to Groq and return the response.
        
        Args:
            prompt: The prompt to send to Groq
            
        Returns:
            The AI's response as a string
        """
        if not self.api_key or not self.client:
            return "Error: Groq API key is not configured."
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with Groq API: {str(e)}"