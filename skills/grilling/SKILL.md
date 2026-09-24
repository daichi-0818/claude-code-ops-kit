---
name: grilling
description: Pre-build requirements grill (an exhaustive interview). Before writing any plan, design, or deliverable, interrogate one question at a time until you and the requester share a common understanding. Triggers on "grill me", "nail down the requirements", "pin this down before building", "check before starting". Also auto-fires when a sizable implementation, document, or automation request arrives with fuzzy requirements.
---
# Pre-Build Grill (Exhaustive Requirements Interview)

Before you start building, interview the requester about every side of the plan **until you reach shared understanding**. Walk down each branch of the design tree one at a time, resolving the dependencies between decisions one by one.

## Rules
1. **One question at a time.** Batching several questions confuses the requester. Wait for the answer before the next one.
2. **Attach your own recommended answer to each question** ("my recommendation is A, because ..."). Never dump a blank slate on the requester.
3. **Anything you can answer from the codebase, memory, or real data, answer yourself — do not ask.** Only ask the human about things that genuinely need their judgment.
4. **Before the first question, verify the current state:** is this request actually still unsolved? Spend one minute confirming via git log, memory, and real data. (A real failure mode: re-dispatching an already-solved task off a stale note.)
5. **Exit condition:** once inputs, processing, outputs, human decision points, and out-of-scope items (what you will NOT do) are all articulated, read back the agreed requirements as a bullet list before you start.

## Why this works
Rework from "discovered a requirements mismatch after building" always costs more than the five questions up front. This is the **entry-side gate**, paired with the self-audit skill (the exit-side guess check).
