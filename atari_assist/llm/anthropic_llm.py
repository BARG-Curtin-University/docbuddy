"""Anthropic (Claude) LLM implementation."""
from anthropic import Anthropic
from atari_assist.config import CLAUDE_API_KEY, CLAUDE_MODEL
from atari_assist.llm.base import BaseLLM

class ClaudeLLM(BaseLLM):
    """Anthropic Claude LLM implementation."""
    
    def __init__(self, model=None, api_key=None):
        """Initialize the Claude LLM.
        
        Args:
            model: The Claude model to use (defaults to config.CLAUDE_MODEL)
            api_key: The Anthropic API key (defaults to config.CLAUDE_API_KEY)
        """
        self.model = model or CLAUDE_MODEL
        self.api_key = api_key or CLAUDE_API_KEY
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None
    
    def ask(self, prompt: str) -> str:
        """Send a prompt to Claude and return the response.
        
        Args:
            prompt: The prompt to send to Claude
            
        Returns:
            The AI's response as a string
        """
        if not self.api_key or not self.client:
            return "Error: Claude API key is not configured."
            
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error with Claude API: {str(e)}"