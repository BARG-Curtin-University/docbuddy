"""Ollama LLM implementation."""
import requests
from atari_assist.config import OLLAMA_MODEL
from atari_assist.llm.base import BaseLLM

class OllamaLLM(BaseLLM):
    """Ollama LLM implementation."""
    
    def __init__(self, model=None, base_url="http://localhost:11434"):
        """Initialize the Ollama LLM.
        
        Args:
            model: The Ollama model to use (defaults to config.OLLAMA_MODEL)
            base_url: The base URL for the Ollama API
        """
        self.model = model or OLLAMA_MODEL
        self.base_url = base_url
        self.api_url = f"{self.base_url}/api/generate"
    
    def ask(self, prompt: str) -> str:
        """Send a prompt to Ollama and return the response.
        
        Args:
            prompt: The prompt to send to Ollama
            
        Returns:
            The AI's response as a string
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
        except requests.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"
        except Exception as e:
            return f"Error with Ollama API: {str(e)}"