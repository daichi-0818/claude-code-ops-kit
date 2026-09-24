# claude-code-ops-kit

**A practical kit for the way AI coding agents (Claude Code and friends) *silently
break* when you run them for a long time, semi-autonomously.**

This is not a manifesto or a list of principles. Every piece here came out of an
actual failure during real, day-in-day-out agent operation — an automated job
that quietly stopped firing, a "the data is zero" report that was really a failed
fetch, a fix piled on a fix until nobody understood the code anymore. The kit is
the *actual operating machinery* that now prevents each of those. That is the
whole point: running an agent for five minutes is easy; running one for months
without it rotting is the hard part, and these are the parts that hold.

## The failure each component prevents

| Component | The silent failure it stops |
|---|---|
| `skills/grilling` | Building the wrong thing because requirements were never nailed down (and re-doing solved work off a stale note) |
| `skills/systematic-debugging` | Guess-fixes stacked on guess-fixes; three-strike escalation to a human instead of thrashing forever |
| `skills/self-audit` | Shipping a report with unbacked numbers, or a "it's zero / it's stopped" claim that's really a fetch failure or a stale checkout |
| `skills/pre-deploy` | Shipping with a missing import or a syntax error that only the production runtime catches |
| `skills/tdd` | Tests that cannot fail (tautologies, implementation-coupled) and fixes that don't stick because no failing test ever existed |
| `skills/analysis-sweep` | "Read everything" that quietly stopped at the first dramatic finding |
| `skills/cloud-run-job-deploy` | A batch job that exits 0 without doing the work, or overlaps its own schedule until failures hide |
| `agents/adversarial-verifier` | The author grading its own homework — a separate, read-only "assume broken" judge |
| `agents/code-reviewer` | Shipping without any second review pass when no human reviewer is around |
| `scripts/launchd-watchdog.py` | A scheduled automation dying quietly and nobody noticing for weeks |
| `scripts/tidy.py` | An unbounded notes file and a hand-maintained index drifting away from reality |
| `templates/CLAUDE.global.md` | Re-deriving your operating rules from scratch on every new machine — and forgetting one |

## The components

**Skills** (`skills/`) — auto-firing discipline:

1. **`grilling`** — a pre-build requirements interview. One question at a
   time, each with your own recommended answer, until inputs / outputs / human
   decision points / out-of-scope are all written down. The entry-side gate.
2. **`systematic-debugging`** — no fix until the root cause is found. Read
   the whole error, reproduce, instrument the boundaries, one minimal change at
   a time, and **stop after three failed attempts** to escalate to a human.
3. **`self-audit`** — a mechanical pre-submission check for guesses:
   claim-to-source table, the "zero / stopped / missing" double-check, fact-vs-
   guess split, and three disconfirming questions.
4. **`pre-deploy`** — the gate before any deploy/push: per-language static
   analysis (checked against the *production* runtime version),
   import/dependency check, tests, env/secret wiring, final diff review. One
   failure stops the deploy.
5. **`tdd`** — seam-based red→green: agree on the public boundary to test
   before writing anything; ban implementation-coupled tests, tautologies, and
   horizontal slicing.
6. **`analysis-sweep`** — completion discipline for "read everything" tasks: a
   DoD of ≥5 criteria up front, two enforced passes, no mid-run conclusions,
   three disconfirming questions, unverified regions declared.
7. **`cloud-run-job-deploy`** — the job-specific steps that stop silent batch
   failures: rollback pin first, image-only update, log-content verification
   (exit 0 ≠ did the work), monitoring registration, timeout-vs-interval check.

**Agents** (`agents/`) — separate judges:

- **`adversarial-verifier`** — a read-only subagent that treats the work as
  **ASSUME BROKEN** and tries to disprove it. Separate from a quality review;
  this is the skeptical "No".
- **`code-reviewer`** — a senior-engineer quality pass (security / edge cases /
  performance / consistency / platform constraints), findings ranked
  CRITICAL/WARNING/INFO with `file:line`; CRITICAL blocks the deploy.

**Scripts** (`scripts/`):

- **`launchd-watchdog.py`** — a macOS watchdog that scans your launchd
  jobs each morning (loaded? last exit 0? resident daemon alive? script exists?
  label matches? TCC-safe paths?) and notifies you on any anomaly. Read-only.
- **`tidy.py`** — idempotent daily housekeeping:
  month-archive a running notes file, regenerate INDEX.md, rotate dated logs.
  Keeps the workspace from silently rotting.

**Template** (`templates/`):

- **`CLAUDE.global.md`** — a starter global CLAUDE.md that wires the discipline
  together: verification-first, the evidence rule for "done", generator/judge
  separation, unattended-run limits, context hygiene, and explicit data
  boundaries for multi-engagement machines.

The reasoning that ties these together — separate the generator from the judge,
write the limits down before an unattended run, always keep a human checkpoint,
watch for comprehension rot — is in [`docs/loop-engineering.md`](docs/loop-engineering.md).

## Install

Everything is independent; take only what you want.

```sh
# skills + agents (user-level; use .claude/ for project-level)
cp -R skills/* ~/.claude/skills/
cp agents/*.md ~/.claude/agents/

# starter global CLAUDE.md — new machines only; merge by hand if one exists
cp -n templates/CLAUDE.global.md ~/.claude/CLAUDE.md

# watchdog (macOS)
python3 scripts/launchd-watchdog.py --prefix com.example.

# tidy (any OS) — always dry-run first
python3 scripts/tidy.py --notes ~/notes/DAILY.md --archive-dir ~/notes/archive \
    --index-dir ~/notes --log-dir ~/notes/logs --dry-run
```

Full steps, including scheduling the watchdog via launchd, are in
[`docs/install.md`](docs/install.md).

The scripts are standard-library-only Python 3 and take every path as an
argument — no hard-coded locations. Skills use an English `description`
frontmatter (the auto-invocation signal). The per-recipient table in
`self-audit` is a template to fill in with your own audiences.

## Why this exists

The kit was extracted and fully genericized from one operator's real Claude Code
setup. The names, paths, and business logic are stripped; the machinery is not.
It is shared for other practitioners who have felt the same thing — that the
danger of a coding agent is rarely a dramatic crash. It is the quiet one: the job
that stopped, the number nobody double-checked, the code nobody reads anymore.

## License

MIT — see [LICENSE](LICENSE).
