"""
utils/config.py - Loads environment variables and builds a Config object.

All runtime settings flow through Config so nothing reads os.environ directly.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "claude-sonnet-4-20250514"
DEFAULT_PROVIDER = "anthropic"
DEFAULT_MAX_ITERATIONS = 10
DEFAULT_TASKS_DIR = "tasks"

@dataclass
class Config:
    # Paths
    tasks_dir: Path

    # Agent
    max_iterations: int
    provider: str
    model: str
    verbose: bool

    # API keys (never logged or printed)
    anthropic_api_key: str = field(repr=False, default="")
    openai_api_key: str = field(repr=False, default="")

    def __post_init__(self) -> None:
        self.tasks_dir = Path(self.tasks_dir)
        self._validate()

    def _validate(self) -> None:
        if self.provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is not set. Add it to your .env file or environment."
            )
        
        if self.provider == "openai" and not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. Add it to your .env file or environment."
            )
        
        if not self.tasks_dir.exists():
            raise ValueError(f"Tasks directory not found: {self.tasks_dir}")
        if self.max_iterations < 1:
            raise ValueError("--max-iterations must be at least 1.")
        
    def task_path(self, task_id: str) -> Path:
        """Return the path to a task directory, raising if it does not exist"""
        p = self.tasks_dir / task_id
        if not p.exists():
            raise ValueError(f"Task '{task_id}' not found in {self.tasks_dir}")
        return p
    
def load_config(
        tasks_dir: str = DEFAULT_TASKS_DIR,
        max_iterations: int | None = None,
        model: str | None = None,
        provider: str | None = None,
        verbose: bool = False
) -> Config:
    """
    Build a Config from CLI flags + environment variables.

    CLI flags take precedence over environment variables, which take precedence over defaults.
    """
    return Config(
        tasks_dir=tasks_dir,
        max_iterations=max_iterations or int(os.getenv("JANITOR_MAX_ITERATIONS", DEFAULT_MAX_ITERATIONS)),
        provider=provider or os.getenv("JANITOR_DEFAULT_PROVIDER", DEFAULT_PROVIDER),
        model=model or os.getenv("JANITOR_DEFAULT_MODEL", DEFAULT_MODEL),
        verbose=verbose,
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        openai_api_key=os.getenv("OPENAI_API_KEY", "")
    )