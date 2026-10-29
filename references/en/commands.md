# CLI

CLI-1

Run from the skill root; replace PYTHON with the executable returned by bootstrap. Task directories belong outside the release.

```text
PYTHON scripts/creator.py session start TASK --goal GOAL --host HOST --model MODEL
PYTHON scripts/creator.py session record TASK --event EVENT.json
PYTHON scripts/creator.py session resume TASK
PYTHON scripts/creator.py session finish TASK
PYTHON scripts/creator.py inspect SKILL --out REPORT.json
PYTHON scripts/creator.py doctor SKILL --out CHECKS.json
PYTHON scripts/creator.py verify SKILL
PYTHON scripts/creator.py export SKILL NEW_DIR
PYTHON scripts/creator.py upgrade SKILL INSTALLED_DIR
PYTHON scripts/creator.py rollback INSTALLED_DIR
```

Example event; sanitize its input file too. Unknown outcomes must not be automatically retried.

```json
{"step":"CAP-1","status":"executed","summary":"Read declared dependencies","evidence":"report.json; sha256 recorded separately","next":"Review dynamic references"}
```

Doctor probes support env_present/name and command/name only; neither proves service validity. Exit codes: 0 operation completed, 1 structural failure or update conflict, 2 input/operation error. Bootstrap returns 3 when setup is needed.
