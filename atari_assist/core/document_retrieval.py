"""Document retrieval functions for Atari Assist.

This module provides functions for loading documents, chunking them, and retrieving
the most relevant chunks for a given query using semantic search when available,
with fallback to lexical search.
"""
import difflib
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

# Default chunk size and overlap for text splitting
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

def load_documents(source_dir: str, recursive: bool = True) -> List[Dict[str, str]]:
    """Load all documents from the source directory, including subdirectories.
    
    Args:
        source_dir: Directory containing the documents to load
        recursive: Whether to recursively search subdirectories (default: True)
        
    Returns:
        List of dictionaries with filename and content
    """
    docs = []
    # Use ** for recursive glob if recursive=True, otherwise use *
    glob_pattern = "**/*" if recursive else "*"
    
    for path in Path(source_dir).glob(glob_pattern):
        if path.is_file():
            try:
                # Get relative path from source_dir for better identification
                rel_path = path.relative_to(source_dir)
                text = path.read_text(encoding="utf-8")
                docs.append({
                    "filename": str(rel_path),
                    "content": text,
                    "filepath": str(path),
                    "file_type": path.suffix.lower()
                })
            except UnicodeDecodeError:
                # Skip binary files
                pass
    return docs

def split_text_into_chunks(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, 
                          chunk_overlap: int = DEFAULT_CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks of specified size.
    
    Args:
        text: Text to split
        chunk_size: Maximum size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        
        # Try to find a sentence break near the end
        if end < len(text):
            sentence_break = max(
                text.rfind('. ', start, end),
                text.rfind('? ', start, end),
                text.rfind('! ', start, end),
                text.rfind('\n', start, end)
            )
            
            if sentence_break != -1 and sentence_break > start + chunk_size // 2:
                end = sentence_break + 1
        
        chunks.append(text[start:end])
        
        # Move start to account for overlap
        start = start + chunk_size - chunk_overlap
    
    return chunks

def create_document_chunks(docs: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Split documents into chunks for more precise retrieval.
    
    Args:
        docs: List of document dictionaries
        
    Returns:
        List of document chunk dictionaries
    """
    chunked_docs = []
    
    for doc in docs:
        text = doc["content"]
        chunks = split_text_into_chunks(text)
        
        for i, chunk in enumerate(chunks):
            chunked_docs.append({
                "filename": doc["filename"],
                "content": chunk,
                "chunk_id": i,
                "filepath": doc.get("filepath", ""),
                "file_type": doc.get("file_type", "")
            })
    
    return chunked_docs

def get_best_chunks_lexical(docs: List[Dict[str, str]], query: str, top_n: int = 4) -> List[Dict[str, Any]]:
    """Get the best matching chunks from the documents based on lexical similarity.
    
    Args:
        docs: List of documents to search
        query: Query string to match against
        top_n: Number of top matches to return
        
    Returns:
        List of the top matching documents
    """
    # Use difflib's SequenceMatcher for lexical similarity
    return sorted(
        docs, 
        key=lambda d: difflib.SequenceMatcher(None, query.lower(), d["content"].lower()).ratio(), 
        reverse=True
    )[:top_n]

def get_best_chunks(docs: List[Dict[str, str]], query: str, top_n: int = 4) -> List[Dict[str, Any]]:
    """Get the best matching chunks from the documents for a given query.
    
    This is the main retrieval function that attempts to use semantic search 
    if possible, falling back to lexical search if not.
    
    Args:
        docs: List of documents to search
        query: Query string to match against
        top_n: Number of top matches to return
        
    Returns:
        List of the top matching documents
    """
    # If docs is empty, return empty list
    if not docs:
        return []
    
    # Check if documents are already chunked
    if not any("chunk_id" in doc for doc in docs):
        docs = create_document_chunks(docs)
    
    try:
        # Try to use semantic search if embeddings libraries are available
        import numpy as np
        
        try:
            # Try to use SentenceTransformers if available
            from sentence_transformers import SentenceTransformer
            
            model = SentenceTransformer('all-MiniLM-L6-v2')
            query_embedding = model.encode(query)
            
            # Compute embeddings for all docs if not already embedded
            if not any("embedding" in doc for doc in docs):
                contents = [doc["content"] for doc in docs]
                embeddings = model.encode(contents)
                for i, doc in enumerate(docs):
                    doc["embedding"] = embeddings[i]
            
            # Compute cosine similarity
            for doc in docs:
                doc_embedding = doc["embedding"]
                similarity = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
                )
                doc["similarity"] = similarity
            
            # Sort by similarity
            return sorted(docs, key=lambda d: d["similarity"], reverse=True)[:top_n]
            
        except ImportError:
            # Fall back to lexical search if no embedding library
            return get_best_chunks_lexical(docs, query, top_n)
    
    except ImportError:
        # Fall back to lexical search if numpy is not available
        return get_best_chunks_lexical(docs, query, top_n)
    
def build_knowledge_base(
    source_dir: str, 
    save_embeddings: bool = False, 
    embedding_model: str = "all-MiniLM-L6-v2",
    force: bool = False
) -> List[Dict[str, Any]]:
    """Build a knowledge base from documents in the source directory.
    
    Args:
        source_dir: Directory containing the documents to load
        save_embeddings: Whether to save embeddings for future use
        embedding_model: Name of the sentence-transformers model to use
        force: Force rebuild even if no changes detected
        
    Returns:
        List of document chunk dictionaries
    """
    import os
    import hashlib
    import json
    import time
    
    # Load documents
    docs = load_documents(source_dir, recursive=True)
    chunked_docs = create_document_chunks(docs)
    
    # Directory for KB files
    kb_dir = os.path.join(source_dir, ".kb")
    os.makedirs(kb_dir, exist_ok=True)
    
    # File paths
    kb_path = os.path.join(kb_dir, "knowledge_base.json")
    metadata_path = os.path.join(kb_dir, "metadata.json")
    
    # Check if we need to rebuild by comparing hashes of document contents
    if not force and os.path.exists(kb_path) and os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            
            # Compute new hash of all documents
            doc_hash = hashlib.md5()
            for doc in docs:
                doc_hash.update(doc["content"].encode())
                doc_hash.update(doc["filename"].encode())
            current_hash = doc_hash.hexdigest()
            
            # If hash matches and embedding model matches, we can reuse existing KB
            if (metadata.get("hash") == current_hash and 
                metadata.get("embedding_model") == embedding_model and
                metadata.get("chunk_size") == DEFAULT_CHUNK_SIZE and
                metadata.get("chunk_overlap") == DEFAULT_CHUNK_OVERLAP):
                
                print(f"No changes detected in documents. Using existing knowledge base.")
                with open(kb_path, "r") as f:
                    return json.load(f)
                
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            # If any error occurs, rebuild the knowledge base
            pass
    
    # Try to compute embeddings if available
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
        
        print(f"Computing embeddings using model: {embedding_model}")
        model = SentenceTransformer(embedding_model)
        
        # Compute embeddings for all chunks
        contents = [doc["content"] for doc in chunked_docs]
        embeddings = model.encode(contents)
        
        for i, doc in enumerate(chunked_docs):
            doc["embedding"] = embeddings[i].tolist()  # Convert to list for serialization
        
        # Save embeddings if requested
        if save_embeddings:
            # Save knowledge base
            with open(kb_path, "w") as f:
                json.dump(chunked_docs, f)
            
            # Compute hash of all documents for change detection
            doc_hash = hashlib.md5()
            for doc in docs:
                doc_hash.update(doc["content"].encode())
                doc_hash.update(doc["filename"].encode())
            
            # Save metadata
            metadata = {
                "hash": doc_hash.hexdigest(),
                "created_at": time.time(),
                "embedding_model": embedding_model,
                "chunk_size": DEFAULT_CHUNK_SIZE,
                "chunk_overlap": DEFAULT_CHUNK_OVERLAP,
                "num_docs": len(docs),
                "num_chunks": len(chunked_docs)
            }
            
            with open(metadata_path, "w") as f:
                json.dump(metadata, f)
    
    except ImportError:
        # Continue without embeddings if libraries not available
        print("Warning: sentence-transformers not installed. Using lexical search only.")
        
        # Still save the chunked documents if requested
        if save_embeddings:
            with open(kb_path, "w") as f:
                json.dump(chunked_docs, f)
            
            # Compute hash for change detection
            doc_hash = hashlib.md5()
            for doc in docs:
                doc_hash.update(doc["content"].encode())
                doc_hash.update(doc["filename"].encode())
            
            # Save metadata without embedding info
            metadata = {
                "hash": doc_hash.hexdigest(),
                "created_at": time.time(),
                "embedding_model": None,  # No embedding model used
                "chunk_size": DEFAULT_CHUNK_SIZE,
                "chunk_overlap": DEFAULT_CHUNK_OVERLAP,
                "num_docs": len(docs),
                "num_chunks": len(chunked_docs)
            }
            
            with open(metadata_path, "w") as f:
                json.dump(metadata, f)
    
    return chunked_docs

def load_knowledge_base(source_dir: str) -> List[Dict[str, Any]]:
    """Load a pre-built knowledge base if available, or build one if not.
    
    Args:
        source_dir: Directory containing the documents
        
    Returns:
        List of document chunk dictionaries
    """
    kb_path = os.path.join(source_dir, ".kb", "knowledge_base.json")
    metadata_path = os.path.join(source_dir, ".kb", "metadata.json")
    
    if os.path.exists(kb_path):
        try:
            import json
            import numpy as np
            
            # Load the knowledge base
            with open(kb_path, "r") as f:
                chunked_docs = json.load(f)
            
            # Load metadata if available
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                print(f"Using knowledge base with {metadata.get('num_chunks', len(chunked_docs))} chunks")
                print(f"Created at: {time.ctime(metadata.get('created_at', 0))}")
                
                if metadata.get('embedding_model'):
                    print(f"Embedding model: {metadata.get('embedding_model')}")
                else:
                    print("No embeddings - using lexical search only")
            
            # Convert embedding lists back to numpy arrays if needed
            try:
                from sentence_transformers import SentenceTransformer
                for doc in chunked_docs:
                    if "embedding" in doc:
                        doc["embedding"] = np.array(doc["embedding"])
            except ImportError:
                pass
            
            return chunked_docs
            
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            # Fall back to building knowledge base if loading fails
            return build_knowledge_base(source_dir)
    else:
        print("No existing knowledge base found. Building...")
        # Build knowledge base if not found
        return build_knowledge_base(source_dir)