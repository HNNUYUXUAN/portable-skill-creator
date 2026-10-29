# capture

CAP-1

Read at task start; historical tasks can only use available evidence. Run session start, then append an event after each important tool result, external submission and phase. Allowed fields: step/status/summary/evidence/next/request_id; status is planned, executed, failed or unknown. Use sanitized event files, never raw sensitive output.

Write executed only after execution. Point evidence to necessary artifacts or checks; include hashes, tools and actual versions, never secrets. Remove credential arguments and signed URLs before passing data to the recorder; its filter is a second safeguard.

After interruption run session resume. Inspect unresolved and existing artifacts. Query uncertain external requests before retrying. Historical uncertainty remains; record investigation results in subsequent events. session finish preserves finished_with_gaps; explain resolved items in the acceptance report. A Skill cannot intercept unrelated chats or all processes. Complete when dependencies, artifacts, failures and evidence gaps are recorded.
