"""
cli/main.py - Entry point for the `shrunner` CLI.

Usage:
    shrunner run <task_id> [options]
    shrunner grade <task_id> [options]
"""

import click
from cli.run_cmd import run
from cli.grade_cmd import grade

@click.group()
@click.version_option(package_name="janitor")
def main() -> None:
    """Janitor - fix broken Python scripts with an LLM agent."""

main.add_command(run)
main.add_command(grade)

if __name__ == "__main__":
    main()
