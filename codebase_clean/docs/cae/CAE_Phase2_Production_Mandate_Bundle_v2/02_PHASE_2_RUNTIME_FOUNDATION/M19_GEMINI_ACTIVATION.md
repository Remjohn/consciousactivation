# GEMINI EXECUTION — M19 — Universal Program State Runtime

Execute ONLY M19.

READ FIRST — in full:
1. `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
2. Every mandate-specific reference below.
3. Live code at each referenced path and exact callers/symbols.
Report files actually read and repository commit before editing.

OBJECTIVE
Implement one reusable runtime adapter from existing CAE State Aggregate/Transition/Contract to Harness/Pi execution for executable Programs.

MANDATE-SPECIFIC REFERENCES
Phase 1 M4; docs/cae/state; StateM paper; 20_PHASE2_CAE_PI_STATE_MAPPING.md; current state runtime.

WORK
Implement Program state persistence/binding, state-local context, transition validation, repair state and Pi projection.

NON-NEGOTIABLE
CAE remains authoritative. Preserve Workspace scope, four Authority Lanes, passive/flat Skills, typed mutation boundaries,
canonical CAE state/receipts and real operator gates. Pi executes; Eve informs package organization only.
Do not create parallel CAE ontology. Do not rely on assistant text or UI status as proof. Capability access is explicit.

PROOF
At least two distinct Programs use the same state runtime; invalid transitions are blocked; state transitions are auditable.
Capture commands, environment, test/fixture, runtime trace, artifacts/receipts, failures and limitations.

STOP on authority conflict, lane collapse, Skill nesting, capability bypass, dual-state/receipt behavior, stale source,
or unverifiable completion. Do not begin another mandate.
