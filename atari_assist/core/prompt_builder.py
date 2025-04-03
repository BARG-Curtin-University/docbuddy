"""Prompt builder for Atari Assist."""
from typing import List, Dict, Any

def build_prompt(chunks: List[Dict[str, Any]], query: str) -> str:
    """Build a prompt to send to the LLM using the matched document chunks.
    
    Args:
        chunks: List of document chunks to include in the prompt
        query: The user's query
        
    Returns:
        A formatted prompt string
    """
    context = "\n\n".join(f"File: {c['filename']}\n{c['content']}" for c in chunks)
    return f"""
You are an Atari 2600 programming assistant. Use the following files to help answer the question.

{context}

Question: {query}
Answer:
"""