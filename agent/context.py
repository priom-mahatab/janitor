"""
agent/context.py — Builds the prompt sent to the LLM on each iteration.

Keeps a rolling history of (script, test output) pairs so the model can
see what it already tried and what changed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


SYSTEM_PROMPT = """\
You are Janitor, an expert Python debugging agent.

Your job is to fix a broken Python script so that it correctly implements \
the described behavior and passes all visible tests.

On each turn you will receive:
- The task description
- The current state of the script
- The output from the last test run (stdout + stderr / traceback)
- A history of previous attempts

Respond with ONLY a fenced Python code block containing the complete fixed script.
Do not include any explanation outside the code block.
Do not add, remove, or modify test files.
Do not hardcode expected outputs/

Example response format:
```python
# fixed script here
```
"""

@dataclass
class Attempt:
    iteration: int
    script: str
    test_output: str
    passed: bool

@dataclass
class AgentContext:
    description: str
    history: list[Attempt] = field(default_factory=list)

    def add_attempt(self, iteration: int, script: str, test_output: str, passed: bool) -> None:
        self.history.append(Attempt(iteration, script, test_output, passed))

    def build_messages(self, current_script: str, last_output: str) -> list[dict]:
        """Return the messages list for the next LLM call"""
        user_content = _format_user_turn(
            description=self.description,
            current_script=current_script,
            last_output=last_output,
            history=self.history
        )
        return [{"role": "user", "content": user_content}]

# ── Prompt formatting ──────────────────────────────────────────────────────────

def _format_user_turn(
    description: str,
    current_script: str,
    last_output: str,
    history: list[Attempt],
) -> str:
    parts: list[str] = []
    parts.append(f"## Task Description\n{description.strip()}")

    if history:
        parts.append("## Previous Attempts")
        for a in history[-3:]: # show last 3 to keep prompt bounded
            status = "✔ passed" if a.passed else "✘ failed"
            parts.append(
                f"### Iteration {a.iteration} ({status})\n"
                f"```python\n{a.script.strip()}\n```\n"
                f"**Test output:**\n```\n{a.test_output.strip()}\n```"
            )
    
    parts.append(
        f"$$ Current Scripts\n```python\n{current_script.strip()}\n```"
    )
    parts.append(
        f"## Last Test Output\n```\n{last_output.strip()}\n```"
    )
    parts.append("Fix the script so all visible tests pass.")

    return "\n\n".join(parts)

# ── Parsing LLM response ───────────────────────────────────────────────────────
def extract_code(response: str) -> str | None:
    """
    Pull the first fenced Python code blo
    """
    import re
    match = re.search(r"```(?:python)?\n(.*?)```", response, re.DOTALL)
    return match.group(1).strip() if match else None

# ── Task loading ───────────────────────────────────────────────────────────────
def load_description(task_dir: Path) -> str:
    return (task_dir / "description.md").read_text()