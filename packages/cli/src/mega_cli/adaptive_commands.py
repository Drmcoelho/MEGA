import typer, json
from adaptive.engine import AdaptiveEngine
from mega_common.config import CONFIG
from adaptive.exceptions import InvalidRatingError

adaptive_app = typer.Typer(help="Comandos do motor adaptativo persistente")
_engine = AdaptiveEngine()


@adaptive_app.command("rate")
def rate(item_id: str, rating: int = typer.Argument(..., min=0, max=2)):
    try:
        result = _engine.rate_item(item_id, rating)
        payload = {
            "item": result.item_id,
            "previous_interval": result.previous_interval,
            "next_interval": result.next_interval,
            "rating": result.rating,
        }
        typer.echo(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2 if CONFIG.cli.json_pretty else None,
            )
        )
    except InvalidRatingError as e:
        typer.echo(f"Rating inválido: {e}")
        raise typer.Exit(1)


@adaptive_app.command("mastery")
def mastery(subskill: str, rating: int):
    resp = _engine.update_mastery(subskill, rating)
    typer.echo(
        json.dumps(
            resp, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None
        )
    )


@adaptive_app.command("due")
def due():
    typer.echo(
        json.dumps(
            {"due": _engine.due()},
            ensure_ascii=False,
            indent=2 if CONFIG.cli.json_pretty else None,
        )
    )


@adaptive_app.command("snapshot")
def snapshot():
    typer.echo(
        json.dumps(
            {"mastery": _engine.snapshot()},
            ensure_ascii=False,
            indent=2 if CONFIG.cli.json_pretty else None,
        )
    )
