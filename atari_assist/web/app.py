"""FastHTML web app for Atari Assist."""
from fasthtml.common import *
from atari_assist.config import DEFAULT_MODEL
from atari_assist.web.handlers import (
    get_index, 
    post_question, 
    get_model_info,
    get_preview
)

# Initialize FastHTML app
app, rt = fast_app(
    title="Atari Assist",
    pico=True,  # Use Pico CSS for styling
    debug=True, # Enable debug mode
)

# Routes
rt("/")(get_index)
rt("/ask")(post_question)
rt("/model-info")(get_model_info)
rt("/preview")(get_preview)

def serve_app(host="0.0.0.0", port=8000):
    """Serve the FastHTML app.
    
    Args:
        host: Host to serve on
        port: Port to serve on
    """
    serve(app=app, host=host, port=port)

if __name__ == "__main__":
    serve_app()