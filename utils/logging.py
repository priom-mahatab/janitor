"""
utils/logging.py — Shared Rich console and structured logging helpers.

All agent output flows through these helpers so formatting stays consistent
and verbose mode is respected everywhere without threading it manually.
"""

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
    pass

# -- Script editing --
def log_patch_applied(verbose: bool) -> None:
    pass

def log_script(code: str, verbose: bool) -> None:
    pass

# -- Test execution --
def log_running_tests() -> None:
    pass

def log_test_result(passed: bool, output: str, verbose: bool) -> None:
    pass

# -- Agent outcome --
def log_success(iteration: int) -> None:
    pass

def log_give_up(iteration: int) -> None:
    pass

# -- Errors --
def log_error(msg: str) -> None:
    pass

# -- Helpers --
def _last_meaningful_line(output: str) -> str:
    pass