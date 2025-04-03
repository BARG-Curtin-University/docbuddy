# Atari Assist

A command-line and web assistant to help with Atari 2600 programming using AI models like OpenAI, Claude, Gemini, Groq, and Ollama.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)

## Features

- Ask questions about Atari 2600 programming
- Choose from multiple LLM backends (OpenAI, Claude, Gemini, Groq, Ollama)
- Preview matching documents before asking
- Use as a CLI tool or a web application with FastHTML
- Advanced RAG (Retrieval-Augmented Generation) with semantic search
- Recursive document search to handle organized file structures
- Document chunking for precise information retrieval
- Pre-compute and save embeddings for faster retrieval
- Simple and intuitive interface

## Overview

Atari Assist is a tool designed to help Atari 2600 programmers. It works by:

1. Loading Atari 2600 related documentation from a directory (including subfolders)
2. Splitting documents into smaller chunks for precise retrieval
3. Computing embeddings for semantic search (when supported libraries are available)
4. Finding the most relevant document chunks for a user's question
5. Constructing a prompt with these relevant chunks
6. Sending the prompt to an LLM for an answer
7. Displaying the result to the user

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/atari-assist.git
cd atari-assist

# Basic installation
pip install -e .

# With embedding support for semantic search (recommended)
pip install -e ".[embeddings]"

# Full installation with development dependencies
pip install -e ".[full]"
```

### Requirements

- Python 3.9 or higher
- Basic requirements (automatically installed):
  - typer, rich, openai, anthropic, requests, google-generativeai, groq, python-fasthtml, python-dotenv
- Optional embedding dependencies (for semantic search):
  - numpy, sentence-transformers

## Command-Line Usage

### Ask a question using OpenAI (default)
```bash
atari-assist ask "How to draw a missile?"
```

### Use a different LLM backend
```bash
atari-assist ask "How does WSYNC work?" --model ollama
atari-assist ask "How to handle collisions?" --model claude
atari-assist ask "What is a playfield?" --model gemini
atari-assist ask "How to use registers?" --model groq
```

### Preview top matching docs before asking
```bash
atari-assist preview "Detecting collisions"
```

### Build or rebuild the knowledge base
```bash
# Build with saved embeddings (recommended)
atari-assist build-kb

# Build without saving embeddings
atari-assist build-kb --no-save-embeddings

# Customize chunking parameters
atari-assist build-kb --chunk-size 500 --chunk-overlap 100

# Use a different embedding model
atari-assist build-kb --embedding-model all-mpnet-base-v2

# Force rebuild even if documents haven't changed
atari-assist build-kb --force
```

### View knowledge base information
```bash
atari-assist kb-info
```

### Check if embedding libraries are installed
```bash
atari-assist check-embedding-libs
```

### List supported models
```bash
atari-assist list-models
```

## Web Application

Atari Assist includes a FastHTML web interface that provides the same functionality with a user-friendly web interface.

### Starting the Web Server

```bash
atari-assist-web
```

By default, the server runs on http://localhost:8000

### Web Interface Features

- Ask questions with a simple form interface
- Select which LLM backend to use
- Preview matching documents
- View model information
- Interactive, responsive UI with real-time updates

## Configuration

### LLM API Keys

Set up your API keys in a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_key
CLAUDE_API_KEY=your_anthropic_key
GEMINI_API_KEY=your_google_key
GROQ_API_KEY=your_groq_key
```

For Ollama, make sure the Ollama service is running locally.

### Custom Configuration

Edit the `atari_assist/config.py` file to customize:

#### LLM Settings
- `DEFAULT_MODEL`: Set the default LLM provider (e.g., "openai", "ollama", "claude", etc.)
- `OPENAI_MODEL`: Specific OpenAI model to use (e.g., "gpt-3.5-turbo")
- `OLLAMA_MODEL`: Specific Ollama model to use (e.g., "llama3")
- `CLAUDE_MODEL`: Specific Claude model to use
- `GEMINI_MODEL`: Specific Gemini model to use
- `GROQ_MODEL`: Specific Groq model to use

#### RAG Settings
You can modify these in `core/document_retrieval.py`:
- `DEFAULT_CHUNK_SIZE`: Default size of document chunks (default: 1000 characters)
- `DEFAULT_CHUNK_OVERLAP`: Default overlap between chunks (default: 200 characters)

These can also be set via command line when building the knowledge base.

## RAG Implementation

Atari Assist implements a Retrieval-Augmented Generation (RAG) system with the following features:

### Document Loading
- Recursively searches directories for documentation files
- Supports any text-based document format
- Maintains file path information for better source tracking

### Document Chunking
- Splits documents into smaller, semantically meaningful chunks
- Preserves sentence boundaries for context
- Configurable chunk size and overlap

### Semantic Search (when available)
- Uses sentence-transformers for computing embeddings
- Falls back to lexical search when embedding libraries aren't available
- Pre-computes and caches embeddings for better performance

### Knowledge Base Management
- Builds and saves embeddings to disk
- Loads pre-built knowledge base for faster startup
- Command-line tools for managing the knowledge base

## Project Structure

```
atari_assist/
├── __init__.py
├── config.py
├── core/               # Core functionality
│   ├── __init__.py
│   ├── document_retrieval.py  # Advanced RAG implementation
│   ├── prompt_builder.py
│   └── query_processor.py
├── llm/                # LLM integrations
│   ├── __init__.py
│   ├── base.py
│   ├── openai_llm.py
│   ├── ollama_llm.py
│   ├── anthropic_llm.py
│   ├── gemini_llm.py
│   └── groq_llm.py
├── cli/                # CLI interface
│   ├── __init__.py
│   └── main.py
└── web/                # Web interface
    ├── __init__.py
    ├── app.py
    ├── handlers.py
    ├── templates/
    └── static/
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Full installation including embedding libraries
pip install -e ".[full]"
```

### Run Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=atari_assist

# Run specific test file
pytest tests/test_document_retrieval.py
```

### Formatting and Linting

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy atari_assist
```

## Documentation

- Detailed docstrings follow the Google Python Style Guide
- See the `CONTRIBUTING.md` file for contributor guidelines

## Adding Your Own Atari Documentation

Place your Atari 2600 documentation files in the `atari_docs` directory. You can organize files in subfolders as needed. The system will automatically load and index all documents.

After adding new documentation, rebuild the knowledge base:

```bash
atari-assist build-kb
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to contribute to this project.

## Acknowledgments

- Thanks to all contributors who have helped with this project
- Special thanks to the Atari 2600 programming community for their amazing resources