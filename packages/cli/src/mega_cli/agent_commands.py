import typer

try:
    from multi_agent.session import MultiAgentSession
except ImportError:
    MultiAgentSession = None

agent_app = typer.Typer(help="Sessões multi-agente")


@agent_app.command("plan")
def plan(topic: str):
    if not MultiAgentSession:
        typer.echo("Multi-agent package não instalado.")
        raise typer.Exit(1)
    sess = MultiAgentSession()
    typer.echo(sess.run_plan(topic))


@agent_app.command("explain")
def explain(concept: str):
    if not MultiAgentSession:
        typer.echo("Multi-agent package não instalado.")
        raise typer.Exit(1)
    sess = MultiAgentSession()
    typer.echo(sess.explain_levels(concept))
