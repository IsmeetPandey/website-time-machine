# Website Time Machine ⏳

> Capture a public webpage today. Compare it with its future self.

Website Time Machine stores normalized webpage text snapshots, fingerprints each capture, and produces a lightweight change report when the same URL is captured again.

## What it does

- Captures public HTTP(S) pages
- Stores snapshot history in SQLite
- Creates SHA-256 content fingerprints
- Calculates previous-vs-current word deltas
- Reports a simple similarity measurement
- Provides a minimal browser UI

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`.

## Engineering principles

- **Deterministic core:** normalize content before hashing so comparisons are less sensitive to irrelevant markup.
- **Evidence first:** a change report describes measurable differences; it does not infer why a page changed.
- **Small MVP:** reliable text snapshots come before expensive visual or DOM-aware analysis.

## Quality & maintenance

- Dependency updates are managed with Dependabot.
- CI performs a Python compilation/smoke check on pushes and pull requests.
- Contributions are documented in `CONTRIBUTING.md`.
- Security reports should follow `SECURITY.md`.

## Roadmap

- [ ] Screenshot snapshots
- [ ] DOM-aware diffs
- [ ] Resource-level change tracking
- [ ] Visual timeline
- [ ] Exportable change reports

## Scope

Use this project for ordinary public HTTP(S) pages. Respect the target site's terms, access controls, and rate limits.
