# Atari Assist

A command-line and web assistant to help with Atari 2600 programming using AI models like OpenAI, Claude, Gemini, Groq, and Ollama.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)

## Features

- Ask questions about Atari 2600 programming
- Choose from multiple LLM backends (OpenAI, Claude, Gemini, Groq, Ollama)
- Preview matching documents before asking
- Use as a CLI tool or a web application with FastHTML
- Fully tested and modular codebase
- Simple and intuitive interface

## Overview

Atari Assist is a tool designed to help Atari 2600 programmers. It works by:

1. Loading Atari 2600 related documentation from a directory
2. Finding the most relevant documents for a user's question
3. Constructing a prompt with these documents
4. Sending the prompt to an LLM for an answer
5. Displaying the result to the user

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/atari-assist.git
cd atari-assist

# Install the package
pip install -e .

# For development dependencies
pip install -e ".[dev]"
```

### Requirements

- Python 3.9 or higher
- Required Python packages (automatically installed):
  - typer
  - rich
  - openai
  - anthropic
  - requests
  - google-generativeai
  - groq
  - python-fasthtml
  - python-dotenv

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

- Default model
- Model specific configurations
- Source directory for Atari documentation

## Project Structure

```
atari_assist/
├── __init__.py
├── config.py
├── core/               # Core functionality
│   ├── __init__.py
│   ├── document_retrieval.py
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

Place your Atari 2600 documentation files in the `atari_docs` directory. The system will automatically load and index these documents for query matching.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to contribute to this project.

## Acknowledgments

- Thanks to all contributors who have helped with this project
- Special thanks to the Atari 2600 programming community for their amazing resources