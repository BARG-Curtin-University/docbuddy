"""Query processor for Atari Assist."""
import os
from typing import List, Tuple, Dict, Any, Optional
from atari_assist.llm import get_llm
from atari_assist.core.document_retrieval import (
    load_documents,
    get_best_chunks,
    build_knowledge_base,
    load_knowledge_base
)
from atari_assist.core.prompt_builder import build_prompt
from atari_assist.config import DEFAULT_MODEL

# Default source directory for the Atari documentation
SOURCE_DIR = "atari_docs"

# Knowledge base cache to avoid reloading for multiple queries
_knowledge_base_cache = None

def get_knowledge_base(rebuild: bool = False) -> List[Dict[str, Any]]:
    """Get the knowledge base, loading or building it if necessary.
    
    Args:
        rebuild: Force rebuilding the knowledge base
        
    Returns:
        The knowledge base as a list of document chunks
    """
    global _knowledge_base_cache
    
    if _knowledge_base_cache is None or rebuild:
        try:
            # Try to load pre-built knowledge base first
            _knowledge_base_cache = load_knowledge_base(SOURCE_DIR)
        except Exception:
            # Fall back to building on the fly
            docs = load_documents(SOURCE_DIR, recursive=True)
            _knowledge_base_cache = get_best_chunks(docs, "")  # Empty query to just chunk documents
    
    return _knowledge_base_cache

def ask_question(question: str, model: str = DEFAULT_MODEL, rebuild_kb: bool = False) -> str:
    """Ask a question about Atari 2600 development.
    
    Args:
        question: The question to ask
        model: The LLM model to use
        rebuild_kb: Whether to rebuild the knowledge base
        
    Returns:
        The answer from the LLM
    """
    # Get knowledge base
    kb = get_knowledge_base(rebuild=rebuild_kb)
    
    # Get best chunks for this question
    chunks = get_best_chunks(kb, question)
    
    # Build prompt with the best chunks
    prompt = build_prompt(chunks, question)
    
    # Get LLM and ask the question
    llm = get_llm(model)
    return llm.ask(prompt)

def preview_matches(question: str, top_n: int = 4) -> List[Tuple[str, str]]:
    """Preview the top matching documents for a question.
    
    Args:
        question: The question to match against
        top_n: Number of top matches to return
        
    Returns:
        List of (filename, snippet) tuples
    """
    # Get knowledge base
    kb = get_knowledge_base()
    
    # Get best chunks for this question
    chunks = get_best_chunks(kb, question, top_n)
    
    # Format the results
    return [
        (c["filename"], c["content"][:200] + ("..." if len(c["content"]) > 200 else "")) 
        for c in chunks
    ]

def build_or_rebuild_kb(save_embeddings: bool = True) -> None:
    """Build or rebuild the knowledge base.
    
    This function is useful for CLI commands or scheduled tasks
    to rebuild the knowledge base from scratch.
    
    Args:
        save_embeddings: Whether to save embeddings to disk
    """
    global _knowledge_base_cache
    
    # Force rebuild
    _knowledge_base_cache = None
    
    # Build knowledge base with embeddings if available
    kb = build_knowledge_base(SOURCE_DIR, save_embeddings=save_embeddings)
    
    # Update cache
    _knowledge_base_cache = kb
    
    return len(kb)