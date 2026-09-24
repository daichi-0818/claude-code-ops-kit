---
name: pre-deploy
description: Quality gate that auto-fires before "deploy", "push", "ship it", "release", or "put it in production" — runs static analysis, import/dependency checks, and tests, and only then allows the deploy.
---
# Pre-Deploy Checklist

Pass every gate below before any deploy/push/release. One failure = stop the
deploy and fix first.

## 1. Static analysis, per language
- **Python**: `python -m py_compile` on every changed file, plus a smoke
  import of the changed modules.
- **TypeScript/JavaScript**: `npx tsc --noEmit` (TS) and/or the project
  linter.
- **Match the production runtime version.** Syntax that parses on your local
  interpreter can be a SyntaxError on the production one — compile-check with
  the version production actually runs.

## 2. Imports and dependencies
- Is every newly added import actually installed?
- Are `requirements.txt` / `package.json` consistent with the code?
- Watch for missing *standard-library* imports (`sys`, `os`, …) — the classic
  cause of a redeploy that a green linter did not catch.

## 3. Tests
- Run the unit tests if they exist.
- If they don't: call the changed function at least once; for an API
  endpoint, hit it locally with curl/httpie.

## 4. Env vars and secrets
- `.env` complete for the target environment?
- Platform wiring present (secret-manager entries, runtime service config)?

## 5. Final diff review
- `git diff --stat`: no unintended files in the change.
- The commit message actually describes the change.

## Project-specific runner
If the project ships an integrated pre-deploy script (lint+test+build in
one), run that — it supersedes gates 1–3. Never bypass pre-push hooks.

## After all gates pass
Report "pre-deploy checks passed" first, then deploy. Never interleave the
two.
