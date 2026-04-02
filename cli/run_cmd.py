"""
cli/run_cmd.py — `janitor run` subcommand.

Starts the agent loop on a given task.
"""

import click
from rich.console import Console

console = Console()

@click.command()
@click.argument("task_id")
@click.option(
    "--tasks-dir",
    default="tasks",
    show_default=True,
    help="Path to the tasks library directory.",
)

@click.option(
    "--max-iterations",
    default=10,
    show_default=True,
    help="Maximum number of fix attempts before giving up.",
)

@click.option(
    "--model",
    default="claude-sonnet-4-20250514",
    show_default=True,
    help="LLM model to use for the agent.",
)

@click.option(
    "--provider",
    default="anthropic",
    show_default=True,
    help="LLM provider to use for the agent (anthropic or openai).",
)

@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Stream agent reasoning to stdout."
)
def run(task_id: str,
    tasks_dir: str,
    max_iterations: int,
    model: str,
    provider: str,
    verbose: bool) -> None:
    """Run the self-healing agent on TASK_ID."""
    from agent.loop import AgentLoop
    from utils.config import load_config

    config = load_config(
        tasks_dir=tasks_dir,
        max_iterations=max_iterations,
        model=model,
        provider=provider, 
        verbose=verbose
    )

    console.rule(f"[bold cyan]janitor run · {task_id}[/bold cyan]")

    loop = AgentLoop(config)
    result = loop.run(task_id)

    if result.success:
        console.print(f"\n[bold green]✔ Fixed in {result.iterations} iteration(s).[/bold green]")
    else:
        console.print(
            f"\n[bold red]✘ Gave up after {result.iterations} iteration(s).[/bold red]"
        )
    
    raise SystemExit(0 if result.success else 1)
    

