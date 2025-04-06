# AskDocs Command-Line Interface (CLI)

AskDocs provides a powerful command-line interface with various subcommands to interact with your documentation.

## Installation

```bash
pip install -e .  # from repository root
# or
pip install askdocs  # when published
```

## Basic Commands

### Ask a Question

```bash
askdocs ask "How do I implement a REST API?"
```

#### Options:
- `--model MODEL`: Choose a specific LLM provider (openai, claude, gemini, groq, ollama)
- `--template TEMPLATE`: Select a prompt template (isolation, complementary, supplementary)
- `--no-color`: Disable colored output

### Preview Matching Documents

```bash
askdocs preview "authentication best practices"
```

#### Options:
- `--limit LIMIT`: Number of document matches to display

### Build Knowledge Base

```bash
askdocs build-kb
```

#### Options:
- `--source-dir DIR`: Specify the documentation source directory
- `--kb-dir DIR`: Specify the knowledge base directory
- `--chunk-size SIZE`: Set the document chunk size (default: 1000)
- `--chunk-overlap OVERLAP`: Set the chunk overlap (default: 200)
- `--no-save-embeddings`: Don't save embeddings to disk
- `--embedding-model MODEL`: Specify the embedding model
- `--force`: Force rebuild even if no documents have changed

## Information Commands

### View Knowledge Base Info

```bash
askdocs kb-info
```

### View Configuration Info

```bash
askdocs config-info
```

### Check Embedding Libraries

```bash
askdocs check-embedding-libs
```

### List Available Models

```bash
askdocs list-models
```

### List Prompt Templates

```bash
askdocs list-templates
```

## Interface Launchers

### Launch Web Interface

```bash
askdocs web
```

#### Options:
- `--host HOST`: Bind to specific host (default: 0.0.0.0)
- `--port PORT`: Specify the port (default: 8000)
- `--debug`: Enable debug mode

### Launch TUI (Text User Interface)

```bash
askdocs tui
```

## Advanced Usage

### Using Configuration Files

AskDocs looks for a `config.json` file in these locations (in order):
- Current working directory (`./config.json`)
- User's home directory (`~/.askdocs/config.json`)
- Package directory

```bash
# Create a configuration file based on the example
cp config.json.example config.json

# Then edit as needed
nano config.json
```

### Using Environment Variables

Set up your API keys and other configuration options in a `.env` file in the project root.

Example:
```
OPENAI_API_KEY=your_openai_key
CLAUDE_API_KEY=your_anthropic_key
DOCBUDDY_DEFAULT_MODEL=openai
DOCBUDDY_SOURCE_DIR=docs
```

## Command Reference Table

| Command | Description |
| --- | --- |
| `ask QUESTION` | Ask a question about your documentation |
| `preview QUERY` | Preview the top matching documents for a query |
| `build-kb` | Build or rebuild the knowledge base |
| `kb-info` | Display information about the knowledge base |
| `config-info` | Display the current configuration |
| `check-embedding-libs` | Check if embedding libraries are installed |
| `list-models` | List available LLM models |
| `list-templates` | List available prompt templates |
| `web` | Launch the web interface |
| `tui` | Launch the text user interface |