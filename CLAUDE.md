# Janitor — AI Agent Codebase Guide

## Project Overview

**Janitor** is a CLI tool that takes a broken Python script and a description of what it should do, then uses an LLM agent to iteratively fix and run it until hidden tests pass or a maximum iteration limit is reached.

## Architecture

```
janitor/
├── tasks/          # Task library (broken scripts, descriptions, tests, metadata)
├── agent/          # LLM agent loop (edit → run → observe → repeat)
├── grader/         # Hidden test runner + cheat detection
├── cli/            # CLI entry points (run, grade subcommands)
└── utils/          # Shared config, logging, file I/O
```

### Core Components

- **Agent Loop** (`agent/loop.py`): Drives the fix-and-test cycle, capped at `--max-iterations` (default 10). Calls the LLM, applies edits, runs visible tests, reads tracebacks, and decides next steps.
- **LLM Client** (`agent/llm_client.py`): Abstraction over Anthropic and OpenAI APIs. Provider and model are configurable via CLI flags or `.env`.
- **Runner** (`agent/runner.py`): Executes scripts and visible tests in a subprocess sandbox.
- **Grader** (`grader/grader.py`): Runs hidden tests against the final solution and produces a score.
- **Cheat Detector** (`grader/cheat_detector.py`): Flags hardcoded outputs, deleted tests, modified test files, and holdout test manipulation.

## CLI Usage

```bash
# Install in editable mode
pip install -e ".[dev]"

# Run the agent on a task
janitor run task_001
janitor run task_001 --max-iterations 5 --provider openai --model gpt-4o --verbose

# Grade a completed solution
janitor grade task_001
janitor grade task_001 --strict
```

## Task Structure

Each task lives in `tasks/<task_id>/` and contains:

| File | Purpose |
|---|---|
| `broken_script.py` | The script the agent must fix |
| `description.md` | Natural language spec of what the script should do |
| `tests_visible.py` | Tests the agent can run and read |
| `tests_hidden.py` | Holdout tests used only by the grader |
| `metadata.json` | Task name, difficulty, time limit, etc. |

## Environment Variables

Copy `.env.example` to `.env` and fill in your keys:

```bash
ANTHROPIC_API_KEY=sk-...
OPENAI_API_KEY=sk-...

# Optional overrides
JANITOR_MAX_ITERATIONS=10
JANITOR_DEFAULT_PROVIDER=anthropic
JANITOR_DEFAULT_MODEL=claude-sonnet-4-20250514
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .

# Type check
mypy .
```

## Key Design Decisions

- **Grader is isolated**: `grader/` is never imported by `agent/`. This maintains the trust boundary between the agent and the hidden tests.
- **Deferred imports in CLI**: `AgentLoop` and `Grader` are imported inside command functions so the CLI starts instantly even if dependencies aren't fully wired yet.
- **Provider abstraction**: `agent/llm_client.py` wraps both Anthropic and OpenAI so the rest of the codebase is provider-agnostic.
- **Exit codes**: `janitor run` and `janitor grade` exit `0` on success, `1` on failure — making them scriptable and CI-friendly.

## Stack

- **Python** ≥ 3.11
- **click** — CLI framework
- **rich** — terminal output
- **pytest** — test runner (visible and hidden tests)
- **subprocess** — sandboxed script execution
- **anthropic / openai** — LLM providers
- **python-dotenv** — environment config