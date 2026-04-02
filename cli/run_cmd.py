"""
cli/run_cmd.py — `shrunner run` subcommand.

Starts the agent loop on a given task.
"""

import click
from rich.console import Console

console = Console()

@click.command()
@click.argument("task_id")
@click.option(
    "--task-dir",
    default="tasks",
    show_default=True,
    help="Path to the tasks library directory.",
)

@click.option(
    "--max-iterations",
    default=10,
    show_default=True,
    help="Maximum number of fix attempets before giving up.",
)

@click.option(
    "--model",
    default="claude-sonnet-4-20250514",
    show_default=True,
    help="LLM model to use for the agent.",
)

def run() -> None:
    pass
