# author

WRITE-1

Read after dependency analysis. Write actionable rules preserving actual inputs, outputs and recovery. Use a short SKILL.md routing to one language. Creator and outputs include zh-CN/en; explicit language wins, otherwise follow the conversation. Keep step IDs, commands, states and acceptance equivalent.

Entrypoint limit: 4096 bytes; language module: 8192 bytes. Load only current-phase references. Scripts handle deterministic transformations/checks; models interpret and extract knowledge. Run from the skill root or resolve absolute script paths; never assume caller cwd.

Create delivery.json with schema_version=1, name/version/files/requirements; files is an explicit relative allowlist excluding delivery.json itself and installed.json. Requirements have id/kind/handling and optional probe. Consult the three examples without turning their task constraints into universal rules. Run verify, fix structure, then independently execute a task. Verification does not prove semantic equivalence or functionality.
