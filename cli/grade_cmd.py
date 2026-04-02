"""
cli/grade_cmd.py - `shrunner grade` subcommand.

Runs the hidden test grader on the current state of a task's script.
"""

import click
from rich.console import Console
from rich.table import Table

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
    "--strict",
    is_flag=True,
    help="Fail immediately on any cheat detection hit.",
)
def grade(task_id: str, tasks_dir: str, strict: bool) -> None:
    """Grade the solution for TASK_ID using hidden tests."""
    from grader.grader import Grader
    from utils.config import load_config

    config = load_config(tasks_dir=tasks_dir)

    console.rule(f"[bold cyan]shrunner grade · {task_id}[/bold cyan]")

    grader = Grader(config)
    result = grader.grade(task_id, strict=strict)

    # Results table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Test", style="dim")
    table.add_column("Result")

    table.add_row("Hidden tests passed", f"{result.passed}/{result.total}")
    table.add_row(
        "Cheat detected",
        "[bold red]YES[/bold red]" if result.cheat_detected else "[green]no[/green]"
    )
    table.add_row("Score", f"[bold]{result.score:.0%}[/bold]")

    console.print(table)

    if result.cheat_detected:
        console.print(f"\n[bold red]Cheat reason[/bold red] {result.cheat_reason}")

    raise SystemExit(0 if result.passed == result.total and not result.cheat_detected else 1)