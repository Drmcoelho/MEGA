import typer, json
from mega_common.config import CONFIG
try:
    from content_engine.src.pdf_ingest import batch_index
except ImportError:
    batch_index = None

pdf_app = typer.Typer(help="Ingestão de PDFs (robusta)")

@pdf_app.command("ingest")
def ingest(target: str):
    if not batch_index:
        typer.echo("Dependências de PDF não instaladas. pip install PyPDF2")
        raise typer.Exit(1)
    res = batch_index(target)
    typer.echo(json.dumps(res, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))