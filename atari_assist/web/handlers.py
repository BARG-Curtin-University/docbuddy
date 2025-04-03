"""FastHTML handlers for Atari Assist."""
from dataclasses import dataclass
from fasthtml.common import *
from atari_assist.core import ask_question, preview_matches
from atari_assist.config import DEFAULT_MODEL

@dataclass
class Question:
    query: str
    model: str = DEFAULT_MODEL

def get_index():
    """Render the main index page."""
    header = Grid(
        H1("Atari Assist"),
        P("Ask questions about Atari 2600 development"),
        cols=1
    )
    
    # Create a form for submitting questions
    question_form = Form(
        Grid(
            Label("Question", Input(id="query", name="query", placeholder="How does WSYNC work?")),
            Label("Model", 
                  Select(
                      Option("OpenAI", value="openai", selected=(DEFAULT_MODEL == "openai")),
                      Option("Ollama", value="ollama", selected=(DEFAULT_MODEL == "ollama")),
                      Option("Claude", value="claude", selected=(DEFAULT_MODEL == "claude")),
                      Option("Gemini", value="gemini", selected=(DEFAULT_MODEL == "gemini")),
                      Option("Groq", value="groq", selected=(DEFAULT_MODEL == "groq")),
                      id="model", name="model"
                  )
            ),
            cols=1
        ),
        Grid(
            Button("Ask", type="submit", hx_post="/ask", hx_target="#result", hx_indicator="#loading"),
            Button("Preview Matches", type="button", hx_post="/preview", hx_target="#result", hx_indicator="#loading"),
            Button("Model Info", type="button", hx_get="/model-info", hx_target="#result", hx_indicator="#loading"),
            cols=3
        )
    )
    
    # Create loading indicator and result div
    loading_indicator = Div(
        "Loading...",
        id="loading", 
        cls="htmx-indicator",
        style="display:none;"
    )
    
    result_div = Div(id="result")
    
    # Main content
    content = Container(
        header,
        question_form,
        loading_indicator,
        result_div
    )
    
    return Titled("Atari Assist", content)

def post_question(question: Question):
    """Handle question submission."""
    answer = ask_question(question.query, question.model)
    return Card(
        Div(question.query, cls="question"),
        P(answer, cls="answer"),
        H3(f"Model: {question.model}", cls="model-info")
    )

def get_preview(question: Question):
    """Preview matching documents."""
    matches = preview_matches(question.query)
    
    if not matches:
        return Div(P("No matches found for your query."))
    
    match_divs = []
    for fname, snippet in matches:
        match_divs.append(
            Card(
                H3(fname, cls="filename"),
                P(snippet, cls="snippet")
            )
        )
    
    return Div(
        H2("Top Matching Documents"),
        *match_divs
    )

def get_model_info():
    """Display information about available models."""
    return Card(
        H2("Available Models"),
        Grid(
            Card(H3("OpenAI"), P("Uses OpenAI API (requires API key)")),
            Card(H3("Ollama"), P("Uses local Ollama instance")),
            Card(H3("Claude"), P("Uses Anthropic's Claude API (requires API key)")),
            Card(H3("Gemini"), P("Uses Google's Gemini API (requires API key)")),
            Card(H3("Groq"), P("Uses Groq API (requires API key)")),
            cols=2
        )
    )