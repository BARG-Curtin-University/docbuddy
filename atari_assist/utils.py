import difflib
from pathlib import Path

def load_documents(source_dir):
    docs = []
    for path in Path(source_dir).glob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            docs.append({"filename": path.name, "content": text})
    return docs

def get_best_chunks(docs, query, top_n=4):
    return sorted(docs, key=lambda d: difflib.SequenceMatcher(None, query, d["content"]).ratio(), reverse=True)[:top_n]

def build_prompt(chunks, query):
    context = "\n\n".join(f"File: {c['filename']}\n{c['content']}" for c in chunks)
    return f"""
You are an Atari 2600 programming assistant. Use the following files to help answer the question.

{context}

Question: {query}
Answer:
"""
