"""Command-line interface for Atari Assist."""
import typer
from rich import print
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from atari_assist.core import ask_question, preview_matches, build_or_rebuild_kb
from atari_assist.config import DEFAULT_MODEL

app = typer.Typer()

@app.command()
def ask(
    question: str, 
    model: str = DEFAULT_MODEL, 
    rebuild: bool = typer.Option(False, "--rebuild", "-r", help="Rebuild knowledge base before answering")
):
    """Ask about Atari 2600 development."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing question...", total=None)
        answer = ask_question(question, model, rebuild_kb=rebuild)
    
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
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Finding matches...", total=None)
        matches = preview_matches(question)
    
    print("\n[yellow]Top Matches:[/yellow]\n")
    for fname, snippet in matches:
        print(Panel(snippet.strip(), title=fname, expand=False))

@app.command()
def build_kb(
    save_embeddings: bool = typer.Option(True, "--save-embeddings/--no-save-embeddings", help="Save embeddings for future use")
):
    """Build or rebuild the knowledge base."""
    print("[yellow]Building knowledge base...[/yellow]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
    ) as progress:
        task = progress.add_task(description="Processing documents...", total=None)
        num_chunks = build_or_rebuild_kb(save_embeddings=save_embeddings)
        progress.update(task, description="Knowledge base built successfully!")
    
    print(f"[green]Knowledge base built with {num_chunks} chunks.[/green]")
    
    # Explain what was done
    if save_embeddings:
        print("[cyan]Embeddings saved to disk. Future queries will be faster![/cyan]")
    else:
        print("[cyan]Embeddings were computed but not saved to disk.[/cyan]")
    
    # Print path info
    print(f"\n[yellow]Knowledge base location:[/yellow]")
    print(f"atari_docs/.kb/knowledge_base.json")

@app.command()
def check_embedding_libs():
    """Check if embedding libraries are installed."""
    libraries = []
    
    # Check for numpy
    try:
        import numpy
        libraries.append("[green]numpy: Installed[/green]")
    except ImportError:
        libraries.append("[red]numpy: Not installed[/red]")
    
    # Check for sentence-transformers
    try:
        import sentence_transformers
        libraries.append("[green]sentence-transformers: Installed[/green]")
    except ImportError:
        libraries.append("[red]sentence-transformers: Not installed[/red] (needed for semantic search)")
    
    print("\n[yellow]Embedding Libraries:[/yellow]")
    for lib in libraries:
        print(lib)
    
    if any("[red]" in lib for lib in libraries):
        print("\n[yellow]Install missing libraries with:[/yellow]")
        print("pip install numpy sentence-transformers")

if __name__ == "__main__":
    app()