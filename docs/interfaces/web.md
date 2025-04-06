# AskDocs Web Interface

AskDocs provides a web interface powered by FastHTML, offering a user-friendly way to interact with your documentation.

## Features

- Ask questions about your documentation
- Choose which LLM backend to use
- Select different prompt templates
- Preview matching documents
- View source information for answers
- 100% server-side rendered (no JavaScript required)
- Mobile-friendly interface with Pico CSS

## Starting the Web Server

```bash
# Start with default settings (host 0.0.0.0, port 8000)
askdocs web

# Specify a different host and port
askdocs web --host 127.0.0.1 --port 5000

# Enable debug mode
askdocs web --debug
```

## Web Interface Pages

### Main Page

The main page provides a simple form to ask questions about your documentation.

- Input field for your question
- Model selection dropdown
- Template selection dropdown
- Submit button

### Knowledge Base Status

View information about your knowledge base:

```
http://localhost:8000/kb-info
```

This page displays:
- Total documents in the knowledge base
- Total document chunks
- Whether semantic search (embeddings) is enabled
- When the knowledge base was last updated

### Model Information

View information about available LLM models:

```
http://localhost:8000/model-info
```

This page displays:
- Available LLM providers
- Default model
- Model configurations

## Configuration

The web interface can be configured through the main AskDocs configuration system:

### config.json
```json
{
  "web": {
    "title": "AskDocs",
    "host": "0.0.0.0",
    "port": 8000,
    "debug": false
  }
}
```

### Environment Variables
```
DOCBUDDY_WEB_TITLE=Custom AskDocs Title
DOCBUDDY_WEB_HOST=127.0.0.1
DOCBUDDY_WEB_PORT=5000
DOCBUDDY_WEB_DEBUG=true
```

## Advanced Usage

### Custom Templates

You can customize the web interface by modifying the templates in `askdocs/web/templates/`:

- `index.html`: Main page with the question form
- `kb_status.html`: Knowledge base status page
- `model_info.html`: Model information page
- `templates.html`: Contains reusable HTML components

### API Endpoints

The web interface provides several API endpoints:

- `GET /`: Main page
- `POST /ask`: Submit a question
- `GET /preview`: Preview document matches
- `GET /kb-info`: Knowledge base information
- `GET /model-info`: Model information

### Running Behind a Reverse Proxy

For production environments, it's recommended to run AskDocs behind a reverse proxy like Nginx:

```nginx
server {
    listen 80;
    server_name askdocs.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```