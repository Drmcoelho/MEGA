"""
MEGA CLI - Command line interface for Medical Education with Generative AI
"""
import os
import sys
from pathlib import Path
from typing import List, Optional

import typer
import yaml
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="mega",
    help="MEGA CLI - Medical Education with Generative AI",
    add_completion=False
)
console = Console()

__version__ = "0.1.0"

@app.command()
def version():
    """Show version information"""
    console.print(f"MEGA CLI version {__version__}")
    console.print("Medical Education with Generative AI")

@app.command()  
def ingest(
    content_path: Optional[Path] = typer.Option(None, help="Path to content directory")
):
    """Ingest educational content and list available modules"""
    if content_path is None:
        # Try to find content/modules relative to current directory
        content_path = Path.cwd() / "content" / "modules"
        
    if not content_path.exists():
        console.print(f"[red]Content path not found: {content_path}[/red]")
        console.print("Try specifying --content-path or run from project root")
        raise typer.Exit(1)
    
    console.print(f"[blue]Scanning modules in: {content_path}[/blue]")
    
    modules = []
    for module_dir in content_path.iterdir():
        if module_dir.is_dir():
            manifest_path = module_dir / "manifest.yaml"
            if manifest_path.exists():
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        manifest = yaml.safe_load(f)
                    modules.append((module_dir.name, manifest))
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not load {manifest_path}: {e}[/yellow]")
    
    if not modules:
        console.print("[yellow]No modules found with valid manifest.yaml files[/yellow]")
        return
    
    # Display modules in a nice table
    table = Table(title="Available Educational Modules")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Version", style="green")
    table.add_column("Duration", style="yellow")
    table.add_column("Objectives", style="blue")
    
    for module_dir, manifest in modules:
        objectives_summary = ""
        if "objectives" in manifest and manifest["objectives"]:
            objectives_summary = f"{len(manifest['objectives'])} objectives"
        
        table.add_row(
            manifest.get("id", module_dir),
            manifest.get("title", "Unknown"),
            manifest.get("version", "1.0.0"),
            f"{manifest.get('estimated_time_hours', '?')}h",
            objectives_summary
        )
    
    console.print(table)
    console.print(f"\n[green]Found {len(modules)} modules ready for use![/green]")

@app.command()
def draft_case(
    module_id: str = typer.Argument(..., help="Module ID to create case for"),
    difficulty: str = typer.Option("intermediate", help="Case difficulty level")
):
    """Draft a new clinical case for a module (placeholder)"""
    console.print(f"[blue]Drafting case for module: {module_id}[/blue]")
    console.print(f"[blue]Difficulty level: {difficulty}[/blue]")
    console.print("[yellow]Note: This is a placeholder command. Case generation will be implemented later.[/yellow]")

if __name__ == "__main__":
    app()