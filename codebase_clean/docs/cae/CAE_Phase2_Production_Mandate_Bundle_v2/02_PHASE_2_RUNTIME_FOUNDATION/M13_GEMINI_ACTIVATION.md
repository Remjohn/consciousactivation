# GEMINI EXECUTION — M13 — Pi Runtime Substrate + CAE State Boundary

Execute ONLY M13.

READ FIRST — in full:
1. `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
2. Every mandate-specific reference below.
3. Live code at each referenced path and exact callers/symbols.
Report files actually read and repository commit before editing.

OBJECTIVE
Prove the minimal CAE-to-Pi boundary and explicitly map canonical CAE run/state/transition/receipt semantics to Pi session/lane/operation state.

MANDATE-SPECIFIC REFERENCES
Pi `packages/agent/docs/harness-v2-state-machine.md`; Pi `packages/agent/docs/harness-v2.md`; 00_CONTROL/20_PHASE2_CAE_PI_STATE_MAPPING.md; relevant CAE state/runtime adapter code; Phase 1 M11 ADR.

WORK
Build the smallest adapter needed for one CAE typed operation to execute in Pi. Carry CAE run identity, preserve CAE state authority, and produce a runtime trace. Add an interruption/resume test.

NON-NEGOTIABLE
CAE remains authoritative. Preserve Workspace scope, four Authority Lanes, passive/flat Skills, typed mutation boundaries,
canonical CAE state/receipts and real operator gates. Pi executes; Eve informs package organization only.
Do not create parallel CAE ontology. Do not rely on assistant text or UI status as proof. Capability access is explicit.

PROOF
One real CAE operation executes in Pi; canonical CAE state and Pi runtime state are distinguishable; an interruption/resume path is proven without state corruption and with matching evidence.
Capture commands, environment, test/fixture, runtime trace, artifacts/receipts, failures and limitations.

STOP on authority conflict, lane collapse, Skill nesting, capability bypass, dual-state/receipt behavior, stale source,
or unverifiable completion. Do not begin another mandate.
