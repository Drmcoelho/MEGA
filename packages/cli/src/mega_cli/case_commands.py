import typer, json
from case_generator.core import compose_case
from mega_common.config import CONFIG

case_app = typer.Typer(help="Geração de casos clínicos (robusto)")

@case_app.command("generate")
def generate(topic: str, markdown: bool = typer.Option(False, help="Saída em Markdown")):
    case = compose_case(topic)
    if markdown:
        typer.echo(case.to_markdown())
    else:
        if CONFIG.cli.json_pretty:
            typer.echo(json.dumps(case.to_dict(), ensure_ascii=False, indent=2))
        else:
            typer.echo(json.dumps(case.to_dict(), ensure_ascii=False))