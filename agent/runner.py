"""
agent/runner.py — Executes the script and visible tests in a subprocess sandbox.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

TIMEOUT_SECONDS = 30

@dataclass
class RunResult:
    passed: bool
    output: str
    returncode: int

def run_visible_tests(task_dir: Path, script_path: Path) -> RunResult:
    """
    Run pytest on tests_visible.py inside the task directory.

    The script under test is always loaded from `script_path`, which is the
    agent's working copy (may differ from the original broken_script.py).
    """
    test_file = task_dir / "tests_visible.py"
    
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            str(test_file),
            "--tb=short",
            "-q",
            "--no-header",
            f"--import-mode=importlib",
        ],
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
        cwd=task_dir,
        env=_safe_env(script_path)
    )

def run_script(script_path: Path) ->RunResult:
    """Run the script directly (no pytest) and capture output."""
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
        cwd=script_path.parent,
    )
    output = (result.stdout + result.stderr).strip()
    return RunResult(
        passed=result.returncode == 0,
        output=output,
        returncode=result.returncode
    )

def _safe_env(script_path: Path) -> dict:
    """
    Build a clean environment for the subprocess.
    Injects JANITOR_SCRIPT_PATH so tests can import the working copy by path.
    """
    import os
    env = os.environ.copy()
    env["JANITOR_SCRIPT_PATH"] = str(script_path)
    return env