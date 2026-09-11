# GEMINI EXECUTION — M20 — State Context + Transition + Repair + Resume Hooks

Execute ONLY M20.

READ FIRST — in full:
1. `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
2. Every mandate-specific reference below.
3. Live code at each referenced path and exact callers/symbols.
Report files actually read and repository commit before editing.

OBJECTIVE
Operationalize state context loading, checkpointing, before-transfer checks, repair, resume and recovery using deterministic runtime hooks/checks.

MANDATE-SPECIFIC REFERENCES
M19; StateM paper; Pi hooks/extensions; 23_PHASE2_EVENT_TRACE_CONTRACT.md; 24_PHASE2_FAULT_INJECTION_MATRIX.md; 26_PHASE2_REPLAY_IDEMPOTENCY_CONTRACT.md.

WORK
Implement lifecycle checks/hooks and recovery routing; execute representative fault injection for stale state, failed hook, duplicate resume and partial external effects.

NON-NEGOTIABLE
CAE remains authoritative. Preserve Workspace scope, four Authority Lanes, passive/flat Skills, typed mutation boundaries,
canonical CAE state/receipts and real operator gates. Pi executes; Eve informs package organization only.
Do not create parallel CAE ontology. Do not rely on assistant text or UI status as proof. Capability access is explicit.

PROOF
All tested failures produce the declared outcome; resumed work avoids unsafe duplicates; state/artifact/receipt agreement survives failure.
Capture commands, environment, test/fixture, runtime trace, artifacts/receipts, failures and limitations.

STOP on authority conflict, lane collapse, Skill nesting, capability bypass, dual-state/receipt behavior, stale source,
or unverifiable completion. Do not begin another mandate.
