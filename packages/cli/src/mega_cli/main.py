import typer, json, os, yaml
from mega_common.config import CONFIG
from .adaptive_commands import adaptive_app
from .agent_commands import agent_app
from .case_commands import case_app
from .pdf_commands import pdf_app

app = typer.Typer(help="CLI MEGA (robusta)")
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
MODULES_DIR = os.path.join(BASE, "content", "modules")

@app.command()
def version():
    typer.echo("mega-cli 0.2.0")

@app.command()
def ingest():
    if not os.path.isdir(MODULES_DIR):
        typer.echo("Nenhum módulo encontrado")
        raise typer.Exit(code=0)
    mods = []
    for d in sorted(os.listdir(MODULES_DIR)):
        mpath = os.path.join(MODULES_DIR, d, "manifest.yaml")
        if os.path.isfile(mpath):
            with open(mpath, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    mods.append({"id": data.get("id"), "title": data.get("title"), "version": data.get("version")})
                except Exception as e:
                    typer.echo(f"Erro lendo {mpath}: {e}")
    typer.echo(json.dumps(mods, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))

@app.command()
def draft_case(topic: str = typer.Argument(..., help="Tópico para caso clínico (placeholder)")):
    typer.echo(json.dumps({"topic": topic, "status": "placeholder"}, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))

app.add_typer(adaptive_app, name="adaptive")
app.add_typer(agent_app, name="agent")
app.add_typer(case_app, name="case")
app.add_typer(pdf_app, name="pdf")

if __name__ == "__main__":
    app()