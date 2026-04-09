# Kraken Trading Backend

A small beginner-friendly Python backend for Kraken trading.

## Features

- FastAPI backend
- Kraken private API signing
- `/health` endpoint
- `/balance` endpoint
- `/order` endpoint
- Safety checks:
  - allowed pairs only
  - max order size
  - `DRY_RUN=true` by default

---

## Important Safety Notes

- Keep `DRY_RUN=true` until you fully understand what you are doing.
- Do **not** enable withdrawal permissions on your Kraken API key.
- Use a separate API key with minimum permissions.
- Never commit your real `.env` file to GitHub.

---

## 1. Create the project

Clone or download the repo, then open a terminal in the project folder.

---

## 2. Create a virtual environment

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
