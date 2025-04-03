"""Query processor for Atari Assist."""
from typing import List, Tuple
from atari_assist.llm import get_llm
from atari_assist.core.document_retrieval import load_documents, get_best_chunks
from atari_assist.core.prompt_builder import build_prompt
from atari_assist.config import DEFAULT_MODEL

# Default source directory for the Atari documentation
SOURCE_DIR = "atari_docs"

def ask_question(question: str, model: str = DEFAULT_MODEL) -> str:
    """Ask a question about Atari 2600 development.
    
    Args:
        question: The question to ask
        model: The LLM model to use
        
    Returns:
        The answer from the LLM
    """
    docs = load_documents(SOURCE_DIR)
    chunks = get_best_chunks(docs, question)
    prompt = build_prompt(chunks, question)
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
    docs = load_documents(SOURCE_DIR)
    chunks = get_best_chunks(docs, question, top_n)
    return [(c["filename"], c["content"][:200]) for c in chunks]