# Ping Gemini (Vocareum) Models

Ping a set of Gemini models and report availability, latency, and a tiny response check.

## Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for env + deps management (recommended)

Install uv (one option):

```bash
pipx install uv
# or: curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup
1) Install dependencies (creates `.venv/`):

```bash
uv sync
```

2) Provide an API key via env var or `.env`:

```bash
# create a local .env from the example template
cp .env.example .env
# then open .env and set one of the keys, e.g.
# GEMINI_API_KEY=your-key
# or
# GOOGLE_API_KEY=your-key
```

## Run

```bash
uv run ping.py
```

This prints a per-model status with latency and a short reply, then a summary.

## Configuration
- Edit the model list in [ping.py](ping.py), variable `MODELS`.
- The script uses `dotenv` to auto-load `.env`.

## VS Code Tips
- Select the workspace interpreter so imports resolve:
  - Command Palette → "Python: Select Interpreter" → choose `.venv/bin/python` under this folder.
- If Pylance still shows missing imports, run `uv sync` and reload the window.

## Notes
- Lockfile `uv.lock` is included; commit it for reproducible installs.
- `.env` is git-ignored; a `.env.example` template is provided for convenience.
