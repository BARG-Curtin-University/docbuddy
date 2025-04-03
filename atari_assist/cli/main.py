"""Command-line interface for Atari Assist."""
import typer
from rich import print
from rich.panel import Panel

from atari_assist.core import ask_question, preview_matches
from atari_assist.config import DEFAULT_MODEL

app = typer.Typer()

@app.command()
def ask(question: str, model: str = DEFAULT_MODEL):
    """Ask about Atari 2600 development."""
    answer = ask_question(question, model)
    print("\n[yellow]Answer:[/yellow]\n")
    print(answer)

@app.command()
def list_models():
    """List available LLM models."""
    print("\n[yellow]Supported Models:[/yellow]")
    print("- openai")
    print("- ollama")
    print("- claude")
    print("- gemini")
    print("- groq")

@app.command()
def preview(question: str):
    """Preview the top matching documents for a question."""
    matches = preview_matches(question)
    print("\n[yellow]Top Matches:[/yellow]\n")
    for fname, snippet in matches:
        print(Panel(snippet.strip(), title=fname, expand=False))

if __name__ == "__main__":
    app()