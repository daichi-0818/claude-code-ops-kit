# Install

The kit has three kinds of components. Install only what you need — they are
independent.

## Skills (`skills/`)

Skills are Markdown files with YAML frontmatter that Claude Code auto-invokes
based on their `description`. Copy the ones you want into your Claude Code
skills directory:

```sh
# user-level (all projects)
cp -R skills/* ~/.claude/skills/

# or pick individual ones / project-level (this repo only)
cp -R skills/self-audit .claude/skills/
```

Each skill lives in its own folder as `SKILL.md`. After copying, they fire
automatically when their trigger conditions match; you can also invoke one by
name. The per-recipient table in `self-audit` is a template — fill in your own
audiences and the specific mistakes each one catches.

## Agents (`agents/`)

`adversarial-verifier.md` and `code-reviewer.md` are subagent definitions. Copy
them into your agents directory:

```sh
cp agents/*.md ~/.claude/agents/    # user-level
# or
cp agents/*.md .claude/agents/      # project-level
```

Both are read-only (`Read, Grep, Glob, Bash`): they can re-run tests and
dry-runs but cannot edit, deploy, or push. `code-reviewer` is the quality pass
(CRITICAL findings block the deploy); `adversarial-verifier` is the separate
"assume broken" judge. Invoke them before deploying an important change or
submitting a report.

## Template (`templates/`)

`CLAUDE.global.md` is a starter global CLAUDE.md for a new machine:

```sh
cp -n templates/CLAUDE.global.md ~/.claude/CLAUDE.md
```

Then edit the placeholders (role, data boundaries, locations). If you already
have a global CLAUDE.md, merge the sections you want by hand instead.

## Scripts (`scripts/`)

Both scripts are standard-library-only Python 3 and take all paths as
arguments — no hard-coded locations.

### launchd-watchdog.py (macOS)

Watches your launchd jobs for silent death. Run manually:

```sh
python3 scripts/launchd-watchdog.py --prefix com.example.
```

To run it every morning, edit `scripts/com.example.watchdog.plist.template`
(replace `__HOME__` and `__PREFIX__`), then:

```sh
cp scripts/com.example.watchdog.plist.template \
    ~/Library/LaunchAgents/com.example.watchdog.plist
launchctl load ~/Library/LaunchAgents/com.example.watchdog.plist
```

Keep the plist `Label` equal to its filename stem, and keep its log paths out of
`~/Desktop`, `~/Documents`, and `~/Downloads` (TCC can kill the job otherwise —
the watchdog will warn you if you forget).

### tidy.py (any OS)

Month-archives a running notes file, regenerates INDEX.md files, and rotates
dated logs. Always dry-run first:

```sh
python3 scripts/tidy.py \
    --notes ~/notes/DAILY.md \
    --archive-dir ~/notes/archive \
    --index-dir ~/notes \
    --log-dir ~/notes/logs --log-prefix log_ \
    --dry-run
```

Drop `--dry-run` to apply. It is idempotent and takes a one-time full backup of
the notes file before the first rewrite. Schedule it nightly with launchd (see
the template) or cron.
