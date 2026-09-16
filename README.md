# Website Time Machine ⏳

**Capture a public webpage today. Compare it with its future self.**

This project stores normalized page text snapshots, hashes each snapshot, and produces a lightweight change report on the next capture.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`.

## Current MVP

- Public HTTP(S) URL capture
- SQLite snapshot history
- SHA-256 content fingerprints
- Previous-vs-current word delta
- Simple similarity measurement
- Minimal browser UI

## Design direction

The long-term version will add screenshot snapshots, DOM-aware diffs, resource changes, and a visual timeline. The MVP deliberately starts with a reliable text snapshot primitive.
