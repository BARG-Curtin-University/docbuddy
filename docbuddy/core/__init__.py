"""Core functionality for DocBuddy."""

from docbuddy.core.document_retrieval import (
    build_knowledge_base,
    get_matching_documents,
    kb_info
)
from docbuddy.core.query_processor import process_query
from docbuddy.core.prompt_builder import build_prompt

__all__ = [
    "build_knowledge_base",
    "get_matching_documents",
    "process_query",
    "build_prompt",
    "kb_info"
]