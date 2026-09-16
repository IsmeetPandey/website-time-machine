# Contributing to Website Time Machine

Website Time Machine captures public web pages and compares snapshots over time.

## Development flow

1. Create a focused branch for one change.
2. Keep snapshot and comparison behavior deterministic and explainable.
3. Add tests when changing capture, hashing, parsing, or comparison logic.
4. Run the test suite locally before opening a pull request.
5. Include verification notes and a short explanation of the user-facing effect.

## Safety and scope

Only use the tool with pages you are authorized to access. Do not commit credentials, cookies, private snapshots, or other sensitive data. Keep network behavior limited to the project's documented public HTTP(S) use case.

## Pull requests

Good pull requests are focused, testable, and easy to review. Documentation, tests, reliability improvements, and small usability fixes are welcome when they make snapshot capture or change reporting clearer.
