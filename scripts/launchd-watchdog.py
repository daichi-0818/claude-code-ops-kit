#!/usr/bin/env python3
"""macOS launchd health watchdog (read-only).

Scans ~/Library/LaunchAgents/<prefix>*.plist and checks each job for:
  1. Loaded into launchctl (not loaded = NG)
  2. LastExitStatus == 0 (nonzero = NG)
  3. KeepAlive=true but no PID (a daemon that should be resident has died = NG)
  4. The script in ProgramArguments actually exists on disk (missing = NG)
  5. Label matches the filename stem (mismatch = launchctl operations silently
     fail to target the job = NG)
  6. WorkingDirectory / StandardOut(Err)Path under a TCC-protected location such
     as ~/Desktop or ~/Documents (known to make launchd kill the job before it
     starts, exit code 78 = WARN)

On any anomaly it posts a macOS notification and appends to a log. It NEVER
modifies anything — it only detects and tells you. This is the "monitor for
silent death" component: a long-running automated job that quietly stops firing
is the exact failure this catches.

Config: set the label prefix via --prefix or the LAUNCHD_WATCHDOG_PREFIX env
var (default "com.example."). Install this itself as a launchd job that runs
each morning; see com.example.watchdog.plist.template.

Manual run:  python3 launchd-watchdog.py --prefix com.example.
Read-only.   Nothing is ever modified.
"""
import argparse
import glob
import os
import plistlib
import re
import subprocess
from datetime import datetime

HOME = os.path.expanduser("~")
AGENT_DIR = f"{HOME}/Library/LaunchAgents"
LOG = f"{HOME}/Library/Logs/launchd-watchdog.log"
REPORT = f"{HOME}/Library/Logs/launchd-watchdog-last.md"
# Locations that TCC protects; launchd jobs pointing here often die pre-launch.
PROTECTED_DIRS = (f"{HOME}/Desktop", f"{HOME}/Documents", f"{HOME}/Downloads")


def launchctl_table():
    out = subprocess.run(["launchctl", "list"], capture_output=True, text=True).stdout
    table = {}
    for line in out.splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) >= 3:
            pid, status, label = parts[0], parts[1], parts[2]
            table[label] = (pid.strip(), status.strip())
    return table


def check(prefix, self_label):
    table = launchctl_table()
    ng, warn, ok = [], [], []
    for path in sorted(glob.glob(f"{AGENT_DIR}/{prefix}*.plist")):
        if path.endswith((".bak", ".disabled")) or ".bak_" in path:
            continue
        stem = os.path.basename(path)[: -len(".plist")]
        try:
            with open(path, "rb") as f:
                d = plistlib.load(f)
        except Exception as e:
            ng.append(f"{stem}: plist unreadable ({e})")
            continue

        label = d.get("Label", "")
        if label != stem:
            ng.append(f"{stem}: Label mismatch (plist says {label!r}) — launchctl ops won't target it")

        # Script existence check (we don't inspect the body of `bash -c`).
        args = d.get("ProgramArguments", [])
        for a in args[1:]:
            if a.startswith("/") and not a.startswith("-") and re.search(r"\.(sh|py|mjs|js)$", a):
                if not os.path.exists(a):
                    ng.append(f"{stem}: referenced script missing {a}")

        # Protected-dir pattern (known cause of pre-launch death).
        for key in ("WorkingDirectory", "StandardOutPath", "StandardErrorPath"):
            v = d.get(key, "")
            if isinstance(v, str) and any(v.startswith(p) for p in PROTECTED_DIRS):
                warn.append(f"{stem}: {key} under a TCC-protected dir ({v}) — known exit-78 pattern")

        # Runtime state.
        if label == self_label:
            continue  # don't judge our own state; we're mid-run
        if label not in table and stem not in table:
            ng.append(f"{stem}: not loaded in launchctl (disabled)")
            continue
        pid, status = table.get(label) or table.get(stem)
        if status not in ("0", "-"):
            ng.append(f"{stem}: LastExitStatus={status}")
        keepalive = d.get("KeepAlive", False)
        if keepalive is True and pid == "-":
            ng.append(f"{stem}: KeepAlive resident job but no process (daemon dead)")
        if stem not in [x.split(":")[0] for x in ng]:
            ok.append(stem)

    return ng, warn, ok


def main():
    ap = argparse.ArgumentParser(description="macOS launchd health watchdog (read-only)")
    ap.add_argument("--prefix", default=os.environ.get("LAUNCHD_WATCHDOG_PREFIX", "com.example."),
                    help="Label/filename prefix of the jobs to watch (default: com.example.)")
    args = ap.parse_args()
    self_label = f"{args.prefix}watchdog"

    ng, warn, ok = check(args.prefix, self_label)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"# launchd health — {now}", ""]
    lines.append(f"NG {len(ng)} / WARN {len(warn)} / OK {len(ok)}")
    if ng:
        lines.append("\n## NG (action required)")
        lines += [f"- {x}" for x in ng]
    if warn:
        lines.append("\n## WARN")
        lines += [f"- {x}" for x in warn]
    lines.append("\n## OK")
    lines.append(", ".join(ok))
    report = "\n".join(lines)
    with open(REPORT, "w") as f:
        f.write(report + "\n")
    with open(LOG, "a") as f:
        f.write(f"{now} NG={len(ng)} WARN={len(warn)} OK={len(ok)}"
                + (" | " + " / ".join(ng) if ng else "") + "\n")
    if ng:
        msg = f"{len(ng)} automated job(s) anomalous. See launchd-watchdog-last.md"
        subprocess.run(["osascript", "-e",
                        f'display notification "{msg}" with title "launchd health" sound name "Basso"'],
                       capture_output=True)
    print(report)


if __name__ == "__main__":
    main()
