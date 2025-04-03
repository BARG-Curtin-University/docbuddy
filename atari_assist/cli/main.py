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
    save_embeddings: bool = typer.Option(True, "--save-embeddings/--no-save-embeddings", 
                                        help="Save embeddings for future use"),
    chunk_size: int = typer.Option(1000, "--chunk-size", "-c", 
                                  help="Size of document chunks"),
    chunk_overlap: int = typer.Option(200, "--chunk-overlap", "-o", 
                                     help="Overlap between chunks"),
    embedding_model: str = typer.Option("all-MiniLM-L6-v2", "--embedding-model", "-m", 
                                       help="Embedding model to use for semantic search"),
    force: bool = typer.Option(False, "--force", "-f", 
                              help="Force rebuild even if no changes detected")
):
    """Build or rebuild the knowledge base.
    
    This command processes all documents in the atari_docs directory, 
    splits them into chunks, and optionally computes embeddings for semantic search.
    """
    print("[yellow]Building knowledge base...[/yellow]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
    ) as progress:
        task = progress.add_task(description="Processing documents...", total=None)
        
        # Show configuration
        progress.console.print(f"[cyan]Configuration:[/cyan]")
        progress.console.print(f"  Chunk size: {chunk_size}")
        progress.console.print(f"  Chunk overlap: {chunk_overlap}")
        progress.console.print(f"  Embedding model: {embedding_model}")
        progress.console.print("")
        
        num_chunks = build_or_rebuild_kb(
            save_embeddings=save_embeddings,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            embedding_model=embedding_model,
            force=force
        )
        
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
        
@app.command()
def kb_info():
    """Show information about the current knowledge base."""
    import os
    import json
    import time
    from atari_assist.core.query_processor import SOURCE_DIR
    
    kb_path = os.path.join(SOURCE_DIR, ".kb", "knowledge_base.json")
    metadata_path = os.path.join(SOURCE_DIR, ".kb", "metadata.json")
    
    if not os.path.exists(kb_path):
        print("[yellow]No knowledge base found.[/yellow]")
        print("Run 'atari-assist build-kb' to build a knowledge base.")
        return
    
    kb_size = os.path.getsize(kb_path) / (1024 * 1024)  # Size in MB
    
    print(f"[green]Knowledge base exists at:[/green] {kb_path}")
    print(f"[green]Size:[/green] {kb_size:.2f} MB")
    
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            
            print("\n[yellow]Knowledge Base Metadata:[/yellow]")
            print(f"Created: {time.ctime(metadata.get('created_at', 0))}")
            print(f"Documents: {metadata.get('num_docs', 'Unknown')}")
            print(f"Chunks: {metadata.get('num_chunks', 'Unknown')}")
            print(f"Chunk size: {metadata.get('chunk_size', 'Unknown')}")
            print(f"Chunk overlap: {metadata.get('chunk_overlap', 'Unknown')}")
            
            if metadata.get('embedding_model'):
                print(f"Embedding model: {metadata.get('embedding_model')}")
            else:
                print("[yellow]No embeddings - using lexical search only[/yellow]")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"[red]Error reading metadata: {e}[/red]")
    else:
        print("[yellow]No metadata file found for the knowledge base.[/yellow]")
        print("This may be an older format knowledge base. Rebuild recommended.")
    
    # Show documents directory information
    print("\n[yellow]Documents Directory:[/yellow]")
    
    # Count documents
    doc_count = 0
    for root, _, files in os.walk(SOURCE_DIR):
        if ".kb" in root:  # Skip .kb directory
            continue
        for file in files:
            if file.startswith("."):  # Skip hidden files
                continue
            doc_count += 1
    
    print(f"Total documents: {doc_count}")
    
    # List some sample documents
    print("\n[yellow]Sample Documents:[/yellow]")
    sample_docs = []
    for root, _, files in os.walk(SOURCE_DIR):
        if ".kb" in root or len(sample_docs) >= 5:  # Skip .kb directory and limit to 5 samples
            continue
        for file in files:
            if file.startswith("."):  # Skip hidden files
                continue
            rel_path = os.path.relpath(os.path.join(root, file), SOURCE_DIR)
            sample_docs.append(rel_path)
            if len(sample_docs) >= 5:
                break
    
    for doc in sample_docs:
        print(f"- {doc}")
    
    if doc_count > 5:
        print(f"... and {doc_count - 5} more")
        
    # Show available models if sentence-transformers is installed
    try:
        from sentence_transformers import SentenceTransformer
        print("\n[yellow]Available Embedding Models (sample):[/yellow]")
        print("- all-MiniLM-L6-v2 (default, fast)")
        print("- all-mpnet-base-v2 (more accurate, slower)")
        print("- paraphrase-multilingual-MiniLM-L12-v2 (multilingual)")
        print("\nUse with: atari-assist build-kb --embedding-model MODEL_NAME")
    except ImportError:
        pass

if __name__ == "__main__":
    app()