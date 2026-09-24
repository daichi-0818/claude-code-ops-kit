# Contributing

This kit is deliberately small: real operating practices that came out of actual
failures, not a philosophy collection. Contributions are welcome in that spirit.

- **Prefer real scars over theory.** If you add or change a component, say which
  concrete failure it prevents.
- **Keep scripts dependency-free.** Standard library only, and all paths passed
  as arguments — no hard-coded locations, no company- or user-specific values.
- **Check before you push.** `python3 -m py_compile scripts/*.py`, and run each
  script with `--dry-run` / `--help`.
- **Skills:** keep the frontmatter `description` in English (it is the
  auto-invocation signal) and keep each skill to a single, mechanical checklist.
- **No private data.** Do not commit real names, hostnames, paths, project IDs,
  or internal business logic. Use `<placeholders>` and `com.example.*`.

Open an issue to discuss larger changes first.
