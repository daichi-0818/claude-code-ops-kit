# Global CLAUDE.md — starter template

<!-- Copy to ~/.claude/CLAUDE.md and edit the placeholders. Keep it short:
     every line here is loaded into every session. Per-repo detail belongs in
     that repo's own CLAUDE.md. -->

## Role
<!-- One paragraph: who the agent is for you, and the ground rules of this
     machine / engagement. -->

## Verification First
### Before writing
- Never assert an external API's field names, function signatures, or behavior
  from memory — check the official docs once before writing code against them.
  Mark anything unchecked as `[assumption]`.
- Before borrowing from existing code, confirm it really targets the same
  API/implementation. Same name does not mean same thing.

### After writing
- No deliverable without a verification means: run the test, hit the endpoint,
  compare the screenshot. If it cannot be verified, say so instead of shipping.

### In every report
- Split every claim into "verified (source)" or "guess" — explicitly, each
  time. Never let "should work" read as a fact.

## Completion discipline (the evidence rule)
- "Done" requires verifiable evidence: the deployed revision, the live URL or
  screenshot, the passing test output, the reconciled counts.
- Report completion in three distinct stages: **implemented** / **wired to
  production** / **proven in production**. Never let stage 1 read as stage 3.
- A completion claim without evidence is treated as not done.

## Generator/judge separation
- The author does not certify its own work. Before deploying an important
  change or submitting an important analysis, run `code-reviewer` (quality)
  and `adversarial-verifier` (read-only, ASSUME BROKEN) — see `agents/`.
- A CRITICAL finding blocks the deploy.

## Unattended runs (loop engineering)
- Before any long or unattended loop, write the limits down first: per-run cap,
  daily cap, and max retries before stopping to ask a human.
- Keep a human checkpoint: never auto-merge, never auto-deploy.
- Watch comprehension rot: when the share of code you have never read grows,
  schedule a reading pass to close the gap.

## Context hygiene
- Clear context between unrelated tasks; delegate bulk file reading to
  subagents to protect the main context.
- On compaction, preserve: the changed-file list, test commands, open tasks,
  and pending report items.

## Data boundaries
<!-- If you work multiple engagements, write the walls down explicitly, e.g.:
- This machine is for <CLIENT A> work only. Never bring material from other
  engagements onto it; never take <CLIENT A> internals off it.
- Credentials never go into notes or repos — password manager / secret
  manager only. -->

## Locations
<!-- Where things live on THIS machine, e.g.:
- Work root: ~/work/<project>/
- Scratch: ~/tmp/
- Session logs: <path> -->

## Project rules
<!-- Per-repo specifics live in that repo's CLAUDE.md. Link them here:
- <repo>: <one-line pointer> -->
