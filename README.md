# Website Time Machine ⏳

A versioned observatory for the public web: capture a page over time, compare versions, and explain what changed.

## Product thesis

Screenshots preserve appearance, but a website is more than pixels. This project treats a page as a changing system of DOM structure, text, resources, metadata, and performance signals.

## Planned analysis

```text
Scheduled capture → snapshot → normalized representation → diff engine → visual timeline
```

A comparison can report:

- URL and redirect changes
- DOM structure changes
- text additions/removals
- image and script changes
- page-size/resource-count changes
- screenshot differences

## Build phases

- **Phase 1:** deterministic snapshots with Playwright
- **Phase 2:** structured DOM/text/resource diffing
- **Phase 3:** side-by-side visual comparison and timeline
- **Phase 4:** scheduled captures + exportable reports

## Intended stack

Python + Playwright + FastAPI + SQLite + browser-based visualization.

Only capture public pages you are authorized to analyze.
