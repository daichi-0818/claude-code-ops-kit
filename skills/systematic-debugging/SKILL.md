---
name: systematic-debugging
description: A disciplined debugging protocol to use the moment you hit a bug, test failure, unexpected behavior, or job failure — BEFORE proposing any fix. Iron rule = no fix until the root cause investigation is done. The trigger is the instant you think "let me just try this". Auto-fires on "there's an error", "it's not working", "it's failing".
---
# Systematic Debugging (Root Cause Before Fix)

**Iron rule: do not fix without investigating the root cause.** Guess-fixes aimed at symptoms melt time and spawn new bugs. If Phase 1 is not done, you have not earned the right to name a fix.

Use this discipline *most* under pressure (panic invites guessing; systematic is faster in the end: measured 15-30 min vs. 2-3 hours of flailing).

## Phase 1: Root Cause Investigation (no fix proposals yet)
1. **Read the error message to the end** (full stack trace, line numbers, error code — the answer is often written there).
2. **Reproduce reliably** (if you cannot reproduce, the next move is data collection, not a fix).
3. **Suspect the most recent change** (git diff, recent commits, dependencies, config, environment differences).
4. **In multi-layer systems, instrument the boundaries before judging** (log the input/output of each component, run once, get evidence for *which layer* breaks, then dig only there). A gap in the logs is itself evidence.
5. **Trace bad values back to their source** (fix at the origin, not where the symptom surfaces).

## Phase 2: Pattern Analysis
- Find a **working** similar case in the same codebase and enumerate every difference from the broken one ("that can't be relevant" is banned).
- If there is a reference implementation, **read all of it**. Skimming to "borrow the pattern" is how bugs are born.

## Phase 3: Hypothesis and Minimal Test
- State each hypothesis in one sentence ("I think X is the cause, because Y").
- Verify with the **smallest** change. Do not fix several things at once (you lose track of what worked).
- Wrong guess -> new hypothesis. **Do not stack fixes** on top of each other.
- If you do not know, say "I don't know". Do not fix while bluffing.

## Phase 4: Implementation
1. **Write the failing reproduction test first** (a fix without a test does not stick).
2. Make **one** fix, aimed at the root cause (no "while I'm here" refactors mixed in).
3. Turn the test green and confirm no other tests broke.
4. **If a fix fails three times, stop.** That is not a wrong guess, it is an architecture problem. Consult a human on the design before attempt #4 (this is your human checkpoint — see the Loop Engineering doc).

## Stop signs (think any one of these -> go back to Phase 1)
"Just fix it and investigate later", "let me change X and see", "change several things and test together", "probably X so let me just fix it", "not fully sure but this might work", "just one more fix attempt (already failed twice)".

## Excuses vs. reality
| Excuse | Reality |
|---|---|
| It's a simple bug, no protocol needed | Simple bugs have root causes too. If it's simple, the protocol is fast |
| It's urgent, skip the protocol | Systematic beats trial-and-error on wall-clock time |
| I'll investigate after it's fixed | The first move sets the shape. Do it right from the start |
| I'll write the test later | A fix without a test recurs |

## If the investigation concludes "no root cause"
If it truly is environmental or timing-related: record the investigation, add proper handling (retry/timeout), and add monitoring/logging for the future. **But 95% of "no root cause" is insufficient investigation.**
