# AskDocs

A general-purpose document assistant for any documentation using RAG and LLMs like OpenAI, Claude, Gemini, Groq, and Ollama.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)

> **Note**: AskDocs is a general-purpose document assistant that can work with any type of documentation. It uses a Retrieval-Augmented Generation (RAG) architecture to provide accurate and contextual answers based on your documents.

## Features

- Ask questions about any documentation
- Choose from multiple LLM backends (OpenAI, Claude, Gemini, Groq, Ollama)
- Different prompt templates for varying control of LLM knowledge usage
- Knowledge base metrics and confidence scoring
- Preview matching documents before asking
- **Three interface options**:
  - Command-line interface (CLI)
  - Web application with FastHTML (100% server-side rendered)
  - Text User Interface (TUI) with Textual
- Advanced RAG (Retrieval-Augmented Generation) with semantic search
- Recursive document search to handle organized file structures
- Configurable document chunking for precise information retrieval
- Pre-compute and save embeddings for faster retrieval
- Comprehensive configuration system with JSON files and environment variables
- Simple and intuitive interface

## Overview

AskDocs is a general-purpose document assistant for any documentation. It works by:

1. Loading documentation from a specified directory (including subfolders)
2. Splitting documents into smaller chunks for precise retrieval with configurable size and overlap
3. Computing embeddings for semantic search (with fallback to lexical search)
4. Finding the most relevant document chunks for a user's question
5. Building prompts using configurable templates (isolation, complementary, or supplementary)
6. Sending the prompt to an LLM for an answer
7. Evaluating and displaying the result to the user

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/ask-docs.git
cd ask-docs

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
askdocs ask "How do I implement a REST API?"
```

### Use a different LLM backend
```bash
askdocs ask "What is dependency injection?" --model ollama
askdocs ask "How to write unit tests?" --model claude
askdocs ask "Explain Docker containers" --model gemini
askdocs ask "What is functional programming?" --model groq
```

### Use different prompt templates
```bash
# Use only document knowledge (isolation)
askdocs ask "What's in this documentation?" --template isolation

# Use documents first, fall back to model knowledge if needed (complementary)
askdocs ask "Compare React and Angular" --template complementary

# Combine document knowledge with model knowledge (supplementary)
askdocs ask "Explain microservices architecture" --template supplementary
```

### Preview top matching docs before asking
```bash
askdocs preview "authentication best practices"
```

### Build or rebuild the knowledge base
```bash
# Build with saved embeddings (recommended)
askdocs build-kb

# Build without saving embeddings
askdocs build-kb --no-save-embeddings

# Customize chunking parameters
askdocs build-kb --chunk-size 500 --chunk-overlap 100

# Use a different embedding model
askdocs build-kb --embedding-model all-mpnet-base-v2

# Force rebuild even if documents haven't changed
askdocs build-kb --force

# Use a custom source directory
askdocs build-kb --source-dir /path/to/your/docs
```

### View knowledge base information
```bash
askdocs kb-info
```

### View configuration information
```bash
askdocs config-info
```

### Check if embedding libraries are installed
```bash
askdocs check-embedding-libs
```

### List supported models and templates
```bash
askdocs list-models
askdocs list-templates
```

## Interface Options

AskDocs offers four different interfaces to suit your preferences and use cases.

### Python API (Importable)

The Python API allows you to use AskDocs programmatically in your own applications:

```python
from ask_docs.main import ask_question, preview_matches, get_kb_info

# Ask a question using the default model
answer = ask_question("How do I implement a REST API?")

# Preview matching documents
matches = preview_matches("authentication best practices")

# Get knowledge base information
kb_info = get_kb_info()
```

### Command-Line Interface (CLI)

The CLI provides a traditional command-line experience with rich text output:

```bash
askdocs ask "How do I implement a REST API?"
```

### Web Application

AskDocs includes a FastHTML web interface with a user-friendly UI and 100% server-side rendering.

```bash
# Start the web server
askdocs web
```

By default, the server runs on http://localhost:8000

#### Web Interface Features

- Ask questions with a simple form interface
- Select which LLM backend to use
- Choose prompt templates
- Preview matching documents
- View source information for answers
- No JavaScript required (100% server-side rendered)

### Text User Interface (TUI)

The TUI provides a rich terminal interface using the Textual framework:

```bash
# Start the TUI application
askdocs tui
```

#### TUI Features

- Full-screen interactive terminal interface
- Keyboard shortcuts for quick navigation
- Dark mode toggle
- Integrated knowledge base management
- Real-time status indicators
- Cross-platform compatibility

## Configuration

DocBuddy provides a comprehensive configuration system with multiple layers:

1. **Default configuration** (hardcoded defaults)
2. **Configuration files** (JSON format)
3. **Environment variables** (highest precedence)

### Configuration Files

DocBuddy looks for a `config.json` file in these locations (in order):
- Current working directory (`./config.json`)
- User's home directory (`~/.docbuddy/config.json`)
- Package directory

Create a configuration file based on the example:

```bash
cp config.json.example config.json
```

### Environment Variables

Set up your API keys and other configuration options in a `.env` file in the project root:

```
# LLM API keys
OPENAI_API_KEY=your_openai_key
CLAUDE_API_KEY=your_anthropic_key
GEMINI_API_KEY=your_google_key
GROQ_API_KEY=your_groq_key

# AskDocs configuration
ASKDOCS_DEFAULT_MODEL=openai
ASKDOCS_SOURCE_DIR=docs

# Model-specific configuration (optional)
OPENAI_MODEL=gpt-3.5-turbo
CLAUDE_MODEL=claude-3-haiku-20240307
GEMINI_MODEL=models/gemini-pro
GROQ_MODEL=mixtral-8x7b-32768
OLLAMA_MODEL=llama3
```

For Ollama, make sure the Ollama service is running locally.

### Configuration Structure

The configuration file has these main sections:

#### LLM Settings
```json
"llm": {
  "default_model": "openai",
  "openai": {
    "model": "gpt-3.5-turbo"
  },
  "ollama": {
    "model": "llama3",
    "base_url": "http://localhost:11434"
  }
  // other providers...
}
```

#### RAG Settings
```json
"rag": {
  "source_dir": "docs",
  "chunk_size": 1000,
  "chunk_overlap": 200,
  "embedding_model": "all-MiniLM-L6-v2",
  "kb_dir": ".kb"
}
```

#### Prompt Templates
```json
"prompts": {
  "default_template": "isolation",
  "templates": {
    "isolation": "You are a helpful assistant...",
    "complementary": "You are a helpful assistant...",
    "supplementary": "You are a helpful assistant..."
  }
}
```

#### Web Interface Settings
```json
"web": {
  "title": "AskDocs",
  "host": "0.0.0.0",
  "port": 8000,
  "debug": true
}
```

Many of these settings can also be overridden via command-line parameters when using the CLI.

## RAG Implementation

DocBuddy implements an advanced Retrieval-Augmented Generation (RAG) system with the following features:

### Document Loading
- Recursively searches directories for documentation files
- Supports any text-based document format
- Maintains file path information for better source tracking
- Configurable source directory through config files or environment variables

### Document Chunking
- Splits documents into smaller, semantically meaningful chunks
- Preserves sentence boundaries for context
- Fully configurable chunk size and overlap
- Metadata tracking to avoid unnecessary rebuilds

### Semantic Search
- Uses sentence-transformers for computing embeddings
- Choice of different embedding models (all-MiniLM-L6-v2, all-mpnet-base-v2, etc.)
- Falls back to lexical search when embedding libraries aren't available
- Pre-computes and caches embeddings for better performance

### Prompt Templates
- Multiple built-in templates with different LLM knowledge utilization strategies:
  - **Isolation**: Uses only document knowledge (good for factual queries)
  - **Complementary**: Uses documents first, falls back to model knowledge if needed
  - **Supplementary**: Combines document knowledge with model knowledge
- Easily customizable through configuration files

### Knowledge Base Management
- Builds and saves embeddings to disk
- Loads pre-built knowledge base for faster startup
- Tracks changes to avoid unnecessary rebuilding
- Comprehensive command-line tools for managing the knowledge base

## Project Structure

```
ask_docs/
├── __init__.py
├── config.py           # Configuration system
├── main.py             # High-level API
├── core/               # Core functionality
│   ├── __init__.py
│   ├── document_retrieval.py  # Advanced RAG implementation
│   ├── prompt_builder.py      # Template rendering
│   └── query_processor.py     # Question answering
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
pytest --cov=ask_docs

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
mypy ask_docs
```

## Documentation

- Detailed docstrings follow the Google Python Style Guide
- See the `CONTRIBUTING.md` file for contributor guidelines
- Interface-specific documentation available in the docs/interfaces directory:
  - [Python API](docs/interfaces/python_api.md)
  - [Command-Line Interface](docs/interfaces/cli.md)
  - [Web Interface](docs/interfaces/web.md)
  - [Text User Interface](docs/interfaces/tui.md)

## Adding Your Own Documentation

Place your documentation files in the configured source directory (default is `docs/`). You can organize files in subfolders as needed. The system will automatically load and index all documents.

After adding new documentation, rebuild the knowledge base:

```bash
docbuddy build-kb
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to contribute to this project.

## Acknowledgments

- Thanks to all contributors who have helped with this project
- This project evolved from an earlier specialized document assistant
- Thanks to the open-source LLM and RAG communities for their excellent tools and libraries