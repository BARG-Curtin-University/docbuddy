"""Core functionality for Atari Assist.

This package contains the core retrieval and query processing logic.
"""

from atari_assist.core.document_retrieval import load_documents, get_best_chunks
from atari_assist.core.prompt_builder import build_prompt
from atari_assist.core.query_processor import ask_question, preview_matches

__all__ = ["load_documents", "get_best_chunks", "build_prompt", "ask_question", "preview_matches"]