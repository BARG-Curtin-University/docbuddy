"""Document retrieval functions for Atari Assist."""
import difflib
from pathlib import Path
from typing import List, Dict, Any

def load_documents(source_dir: str) -> List[Dict[str, str]]:
    """Load all documents from the source directory.
    
    Args:
        source_dir: Directory containing the documents to load
        
    Returns:
        List of dictionaries with filename and content
    """
    docs = []
    for path in Path(source_dir).glob("*"):
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8")
                docs.append({"filename": path.name, "content": text})
            except UnicodeDecodeError:
                # Skip binary files
                pass
    return docs

def get_best_chunks(docs: List[Dict[str, str]], query: str, top_n: int = 4) -> List[Dict[str, Any]]:
    """Get the best matching chunks from the documents based on the query.
    
    Args:
        docs: List of documents to search
        query: Query string to match against
        top_n: Number of top matches to return
        
    Returns:
        List of the top matching documents
    """
    return sorted(
        docs, 
        key=lambda d: difflib.SequenceMatcher(None, query, d["content"]).ratio(), 
        reverse=True
    )[:top_n]