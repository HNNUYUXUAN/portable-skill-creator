# Acceptance run — 2026-10-29 — Windows Server 2022 / WorkBuddy 5.9.3

This directory holds one complete, reproducible acceptance run of portable-skill-creator
(v0.1.0-dev, commit `4174224ba419dffab66d4e7e3d49cc28175734a2`) plus the bilingual skill that was
authored during the run.

Start with `acceptance-report.md` (narrative) and `acceptance-results.json` (machine-readable).
`HANDOFF.md` lists the items that still need a human operator.

## What is here

| Path | Content |
|---|---|
| `acceptance-report.md` | Full report: environment, install, checks, defect, evidence labels, open items |
| `acceptance-results.json` | Same run in machine-readable form (checks, exit codes, hashes, scenarios) |
| `HANDOFF.md` | Operator steps: host skill discovery, new-session acceptance prompt, browser setup, upstream fix proposal |
| `evidence/` | 27 raw artifacts: command output, exit codes, patch diffs, file manifests, browser probe |
| `runs/` | Recipient inputs and the two recipient outputs (`zh`, `en`) |
| `tasks/` | Creator task record: `session.json`, `events.jsonl` (16 events), `checkpoint.json`, `checker.py`, `inspect-skill.json`, raw event inputs |
| `skill/` | Author-side source of the new skill `acceptance-note-triage` (entry, both language modules, sample input, delivery manifest) |
| `recipient-export/` | The exported, distributable copy of the same skill (adds `installed.json` with file hashes) |
| `patched/` | Local one-line patch of `scripts/bootstrap.ps1` used only to isolate the OS gate; **not** a proposed upstream change |
| `samples/样例 目录 空格测试/` | `examples/json-to-csv` copied into a directory containing Chinese characters and spaces, with the converted CSV |

`tasks/checker.py` is the acceptor-side checker: it re-derives the expected grouping from the input
lines and compares heading order, verbatim item text, within-group order, declared counts and the
total against the recipient output. Both language runs report `ok: true`.

## Scenario labels (do not over-claim)

| Label | Status |
|---|---|
| Real execution | yes — everything below was run on the machine and captured |
| Static check | yes — `verify` is structure-only; `inspect` is a heuristic dependency scan |
| Simulated scenario | yes — the skill was accepted on a fixed 6-line sample |
| Same-machine relocation | yes — exported to a new directory on the same machine and reused |
| New session, independent | **no** — independent agents with fresh context were used; a real WorkBuddy new-session prompt is in `HANDOFF.md` |
| Clean system / separate device | **no** — one Windows Server 2022 VM, one host, one model |

## Known defect found by this run

`scripts/bootstrap.ps1` line 3 hard-fails on the Windows build number:

```powershell
if ([Environment]::OSVersion.Version.Build -lt 22000) { throw 'Windows 11 or newer build required; other systems untested' }
```

The gate runs before any argument handling, so `-Prepare` and `-Python` cannot bypass it. On this
machine (Windows Server 2022, build 20348) bootstrap therefore aborts even though Python 3.12.10 is
already installed. Affected: Windows 10 (19041–19045), Windows Server 2019 (17763), Windows Server
2022 (20348).

Reproduce: `evidence/bootstrap-original.txt` and `evidence/bootstrap-original-prepare.txt`.
Isolation: `evidence/bootstrap-patch.diff` relaxes only that line and returns
`C:\Program Files\Python312\python.exe` (`evidence/bootstrap-patched.txt`).

Suggested fix: warn and continue with an `os_support: "untested"` field in the JSON result, or add an
explicit `-AllowUnsupportedOS` switch, instead of throwing. Nothing was pushed upstream from the run.

## Deliberately not committed

| Excluded | Why |
|---|---|
| `source/` clone and its `.git` | It is this repository at the same commit; a nested repository inside the branch would be noise |
| `.codebuddy/skills/portable-skill-creator` | An export of this same repository; `evidence/verify-exported.txt` and `installed.json` already record the install result |

Both are reproducible from the commit recorded above.

## Promoting the new skill

`skill/` and `recipient-export/` stay inside the acceptance directory so this branch does not change
the repository's own distribution contract. If `acceptance-note-triage` should become a first-class
example under `examples/`, its files also have to be added to the root `delivery.json` allowlist —
that decision is left to the maintainer.

## Files are stored verbatim

This directory's own `.gitattributes` sets `* -text` so CRLF files (for example the generated CSV) and hashes
in `evidence/` stay byte-identical to what the run produced, instead of being normalised by the
repository-wide `* text=auto eol=lf` rule.
