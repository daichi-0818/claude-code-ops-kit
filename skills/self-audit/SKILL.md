---
name: self-audit
description: Pre-submission audit that fires right before you hand a report, analysis, or conclusion to a human or another system. Machine-checks for unbacked claims, silent "it's zero / it's stopped" misdiagnoses, and unverified API assumptions. Also triggers on "audit this" or "check for guesses".
---
# Pre-Submission Self-Audit (Guess Check)

Run this mechanically **right before** you submit any report, analysis, or conclusion. If even one item is NG, do not submit — fix it first.

## Checklist

### 1. Claim-to-source table
- For every number and factual claim in the output, can you name the exact source (query result / API response / file / log) where you verified it, one-to-one?
- For anything you cannot: (a) go verify it at the source, (b) cut it, or (c) tag it `[unverified]`.

### 2. "It's zero / it's missing / it's stopped" assertions (the most frequent failure mode)
- "The data is zero" has two readings: *actually zero* and *the fetch failed and it looks like zero*. Did you check both?
- "It's stopped" has two readings: *actually halted* and *the copy I'm looking at is stale*. (Real example: a "backup stopped" alarm that was just a local checkout that had not pulled.)
- Never assert "does not exist / no prior art / nobody has done this". Stop at "not found within the range I searched" — proving nonexistence is impossible.

### 3. External API / library behavior
- Any place you assert a field name, function signature, or behavior: is it confirmed against official docs? Tag unconfirmed spots `[unverified]`.

### 4. Explicit split between fact and guess
- Is every claim classified as either "verified (source named)" or "guess"? Do not leave mushy hedges ("should be", "probably", "seems to") standing in for one or the other.

### 5. Per-recipient rules
- Different audiences need different framing. Keep a short table of your own recipient rules here and check against it before sending. Template:
  - `<recipient A>`: <the specific basis / unit / framing they always expect; the mistake they always catch>
  - `<recipient B>`: <plain text only, no Markdown tables, no nesting — paste-safe>
  - `<daily report>`: <the fixed format your reader expects>

### 6. Three disconfirming questions
- List three ways "this conclusion could be wrong" and show you closed each one. Anything you cannot close, state as a stated limitation.

## Output
- All checks pass -> no footnote needed. Submit as-is.
- Something was NG -> fix before submitting, and add one line noting what you changed (e.g. "note: added source verification for X during pre-submission audit").
