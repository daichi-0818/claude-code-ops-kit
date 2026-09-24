---
name: analysis-sweep
description: Completion discipline for exhaustive analysis — auto-fires on "analyze the whole thing", "read everything", "every sheet/file", "full audit", "don't miss anything", or when reading a new repo/spreadsheet/log corpus for the first time. Prevents declaring victory on the first striking finding.
---
# Analysis Sweep (finish what you started reading)

## Why
Agents reliably fail exhaustive analysis in four ways:
1. **Early satisfaction** — a striking finding gets self-certified as "the
   main result" and the rest gets skimmed.
2. **Conclusion jumping** — the urge to report *now*, leaving regions unread.
3. **Weak tracking** — no record of what was actually covered; "read it all"
   without having read it all.
4. **Undefined "thorough"** — no self-imposed standard for what counts as
   read.

Real case: an audit of a 22-sheet workbook effectively stopped at sheet 9
after a dramatic finding; the next day's re-read surfaced three more issues
the first pass had skimmed past. A full day lost.

## The five required steps

### 1. DoD before starting
Write **≥5 explicit completion criteria** before touching the material
("every sheet gets a one-line summary", "every threshold checked for a
stated source", "≥3 disconfirming questions asked", …) and agree with the
requester when possible. The DoD doubles as a workload estimate — if it
looks too big, negotiate scope *now*; "can we narrow this?" up front beats
"ran out of time, half is unread" after.

### 2. Two passes, enforced
- **Pass 1 (skeleton)**: sweep everything fast, one line per unit
  (file / sheet / module).
- **Pass 2 (deep-dive)**: only then dig into the suspicious spots.

**No conclusions before Pass 2.** Finding something in Pass 1 does not
authorize skipping the rest of Pass 1.

### 3. No mid-run reporting
Striking findings go into notes; the report waits until every DoD item is
checked. Exception: stop-the-world issues only (security, data-loss risk).

### 4. Three disconfirming questions
Before finishing, ask at least three of: "what regions could I have
missed?", "what evidence points the other way?", "how could this logic/spec
be wrong?" Record the answers even when they are "probably none" — writing
"none" down is itself bias removal.

### 5. Declare the unverified
Anything not covered is listed as **unverified**, honestly ("ran out of
time", "no access", "file unreadable"). Reporting "done" without finishing
the DoD is forbidden.

## When it fires / when to skip
- Fires: "analyze / read closely / every / all / don't miss anything", and
  first contact with a new corpus (repo, workbook, log directory).
- Skip: explicitly narrowed scope ("just this file", "roughly"), narrow
  single-value lookups, or second-by-second incident response.
