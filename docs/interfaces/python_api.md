# AskDocs Python API

The Python API allows you to integrate AskDocs's functionality directly into your own Python applications.

## Installation

Make sure AskDocs is installed:

```bash
pip install -e .  # from repository root
# or
pip install askdocs  # when published
```

## Basic Usage

Import the main functions from `askdocs.main`:

```python
from askdocs.main import ask_question, preview_matches, get_kb_info, build_knowledge_base
```

### Ask a Question

```python
answer = ask_question(
    "How do I implement a REST API?",
    model="openai",  # optional, defaults to config
    template="isolation"  # optional, defaults to config
)

print(answer["answer"])  # Display the answer text
print(answer["sources"])  # Display the source documents
```

### Preview Document Matches

```python
matches = preview_matches(
    "authentication best practices",
    limit=5  # optional, number of matches to return
)

for match in matches:
    print(f"Score: {match['score']}")
    print(f"Source: {match['metadata']['filename']}")
    print(f"Content: {match['text']}\n")
```

### Knowledge Base Management

```python
# Get information about the current knowledge base
kb_info = get_kb_info()
print(f"Total documents: {kb_info['total_documents']}")
print(f"Total chunks: {kb_info['total_chunks']}")
print(f"Using embeddings: {kb_info['using_embeddings']}")

# Build or rebuild the knowledge base
build_knowledge_base(
    source_dir="docs",  # optional
    chunk_size=1000,  # optional
    chunk_overlap=200,  # optional
    save_embeddings=True,  # optional
    force_rebuild=False  # optional
)
```

## Advanced Usage

### Custom Configuration

```python
from askdocs.config import get_config, set_config

# Get the current configuration
config = get_config()

# Modify configuration
config["llm"]["default_model"] = "claude"
config["rag"]["chunk_size"] = 800

# Set the updated configuration
set_config(config)
```

### Working with Multiple Knowledge Bases

```python
from askdocs.core.document_retrieval import DocumentRetrieval

# Create a document retrieval instance with custom settings
retriever = DocumentRetrieval(
    source_dir="custom_docs",
    kb_dir=".custom_kb",
    chunk_size=500,
    chunk_overlap=100
)

# Build the knowledge base
retriever.build_knowledge_base()

# Get best chunks for a query
chunks = retriever.get_best_chunks("What is authentication?", limit=3)

# Use the chunks with a custom prompt
from askdocs.core.prompt_builder import build_prompt
from askdocs.llm.factory import get_llm

prompt = build_prompt(chunks, "What is authentication?", template="isolation")
llm = get_llm("openai")
answer = llm.ask(prompt)
```

## Error Handling

```python
try:
    answer = ask_question("How do I implement a REST API?")
except Exception as e:
    print(f"Error: {e}")
```

## API Reference

| Function | Description |
| --- | --- |
| `ask_question(question, model=None, template=None)` | Ask a question using the specified model and template |
| `preview_matches(query, limit=5)` | Preview the top document matches for a query |
| `get_kb_info()` | Get information about the current knowledge base |
| `build_knowledge_base(...)` | Build or rebuild the knowledge base |