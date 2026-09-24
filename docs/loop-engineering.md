# Loop Engineering: operating discipline for autonomous coding agents

"Loop Engineering" is the practice of running an AI coding agent in a loop
(generate -> run -> observe -> correct) and engineering *the loop itself* so it
stays honest over long, semi-autonomous runs. The ideas below draw on the
broader practitioner community's ongoing discussion of agentic coding loops and
"keep the agent running" workflows. This doc distills four rules that this kit's
components enforce.

## 1. Separate the generator from the judge
Do not let the agent that wrote the code be the only one that verifies it. A
model grading its own work grades generously. Insert a **separate, skeptical
reviewer** whose only job is to try to disprove that the change works.

- In this kit: `agents/adversarial-verifier.md` (read-only, ASSUME BROKEN).
- It runs on a different premise than a normal code review: not "is this good
  code" but "here is how this is secretly broken".

## 2. Write the limits down before an unattended run
Any long-running or unattended job needs an explicit ceiling declared **before**
you start it: per-run cost, per-day cost, and a max-retry count. An
unsupervised loop with no built-in ceiling will happily burn budget or thrash on
the same failure forever.

- Minimum viable version: decide "after N retries, stop and ask a human" and say
  it out loud before you press go.
- The `systematic-debugging` skill hard-codes one such ceiling: **three failed
  fix attempts = stop and escalate to a human**, because a fix that fails three
  times is an architecture problem, not a wrong guess.

## 3. Always leave a human checkpoint (never auto-merge)
Judgment is the scarce resource. The largest risk of a fully automated loop is
not a bug — it is **cognitive offloading**: handing every decision to the loop
until you no longer hold an opinion about your own system. Keep a human approval
gate on anything irreversible (merge, deploy, production write). Never
auto-merge.

## 4. Watch for comprehension rot
As the share of code you did not write yourself grows, the gap between what
*exists* and what you *understand* widens. Left alone, it rots: you can no
longer debug or safely change your own system. Periodically stop and read the
code the agent generated to close the gap. Treat "I don't know how this works
anymore" as a stop sign, not a minor annoyance.

## How the kit maps to these rules
| Rule | Component |
|---|---|
| Separate generator from judge | `agents/adversarial-verifier.md` |
| Nail requirements before building | `skills/grilling` |
| Root cause before fix + 3-strike escalation | `skills/systematic-debugging` |
| No unbacked claims leave the loop | `skills/self-audit` |
| Detect silent death of automation | `scripts/launchd-watchdog.py` |
| Keep the workspace from rotting | `scripts/tidy.py` |
