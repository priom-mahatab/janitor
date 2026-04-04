"""
utils/logging.py — Shared Rich console and structured logging helpers.

All agent output flows through these helpers so formatting stays consistent
and verbose mode is respected everywhere without threading it manually.
"""

from __future__ import annotations

from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text

# single instance of console - import everywhere instead of instantiating per module
console = Console()
err_console = Console(stderr=True)

# -- iteration banner --
def log_iteration(n: int, max_n: int) -> None:
    console.rule(f"[bold blue]Iteration {n} / {max_n}[/bold blue]")

# -- LLM interaction --
def log_llm_prompt(prompt: str, verbose: bool):
    if not verbose:
        return
    console.print(Panel(prompt, title="[dim]Prompt[/dim]", border_style="dim"))

def log_llm_response(response: str, verbose: bool) -> None:
    if not verbose:
        return
    console.print(Panel(response, title="[dim]LLM Response[/dim]", border_style="cyan"))

# -- Script editing --
def log_patch_applied(verbose: bool) -> None:
    if not verbose:
        return
    console.print("[green]✔ Patch applied.[/green]")

def log_script(code: str, verbose: bool) -> None:
    if not verbose:
        return
    console.print(Syntax(code, "python", theme="monokai", line_numbers=True))

# -- Test execution --
def log_running_tests() -> None:
    console.print("[dim]Running visible tests..[/dim]")

def log_test_result(passed: bool, output: str, verbose: bool) -> None:
    if passed:
        console.print("[bold green]✔ All visible tests passed.[/bold green]")
    else:
        console.print("[bold red]✘ Tests failed.[/bold red]")
        if verbose:
            console.print(
                Panel(output, title="[red]Test Output[/red]", border_style="red")
            )
        else:
            # Shows the last traceback line even in non-verbose mode
            last_line = _last_meaningful_line(output)
            if last_line:
                console.print(f" [red]{last_line}[/red]")

# -- Agent outcome --
def log_success(iterations: int) -> None:
    console.print(
        f"\n[bold green]✔ Fixed in {iterations} iteration(s).[/bold green]"
    )

def log_give_up(iterations: int) -> None:
    console.print(
        f"\n[bold red]✘ Gave up after {iterations} iteration(s).[/bold red]"
    )

# -- Errors --
def log_error(msg: str) -> None:
    err_console.print(f"[bold red]Error:[/bold red] {msg}")

# -- Helpers --
def _last_meaningful_line(output: str) -> str:
    """Return the last non-empty line from test output (usually the error summary)."""
    lines = [l.strip() for l in output.splitlines() if l.strip()]
    return lines[-1] if lines else ""