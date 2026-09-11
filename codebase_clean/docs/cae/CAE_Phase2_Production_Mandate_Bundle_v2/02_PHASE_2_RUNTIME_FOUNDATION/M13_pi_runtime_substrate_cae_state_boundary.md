# M13 — Pi Runtime Substrate + CAE State Boundary

    Status: PROPOSED — OPERATOR-RATIFICATION-REQUIRED
    Phase: 2 — Runtime Foundation

    ## 1. Decision / Objective
    Prove the minimal CAE-to-Pi boundary and explicitly map canonical CAE run/state/transition/receipt semantics to Pi session/lane/operation state.

    ## 2. Mandatory reading before action
    Baseline: `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
    Mandate-specific:
    Pi `packages/agent/docs/harness-v2-state-machine.md`; Pi `packages/agent/docs/harness-v2.md`; 00_CONTROL/20_PHASE2_CAE_PI_STATE_MAPPING.md; relevant CAE state/runtime adapter code; Phase 1 M11 ADR.

    Before any edit, report the exact files read and current repository commit. Inspect live symbols/callers.
    If a referenced implementation has moved or differs materially, classify the discrepancy and stop rather than silently redesigning.


## Constitutional constraints
- Read the complete baseline authority set and all mandate-specific references in full before action.
- Preserve CAE canonical ontology, object authority, Workspace scope, typed operation mutation boundaries, state contracts and receipt authority.
- Preserve Hunter / Analyst / Composer / Commander as separate authority lanes.
- Preserve passive, versioned, flat Canonical Skills; no Skill may invoke another Skill.
- Pi is an execution substrate; Eve is a package organization reference; neither may redefine CAE authority.
- Program/Harness package files are composition metadata, not canonical state.
- Capability access is explicit and fail-closed; no ambient secrets/network/process access.
- Agent text, UI status or a receipt without matching state/artifact evidence is not completion proof.


    ## 3. Allowed work
    Build the smallest adapter needed for one CAE typed operation to execute in Pi. Carry CAE run identity, preserve CAE state authority, and produce a runtime trace. Add an interruption/resume test.

    ## 4. Prohibited work
    - No broad migration of Programs.
    - No mass service→agent conversion.
    - No new canonical object/authority without explicit Phase 1 evidence and operator authorization.
    - No parallel receipt/state/Skill/Harness authority.
    - No scope expansion into another mandate.

    ## 5. Verification and evidence
    - Record exact environment and commit SHA.
    - Run focused tests before aggregate tests.
    - Capture runtime trace identifiers and artifact/receipt IDs.
    - For recovery work, execute the specified fault injection.
    - Separate pre-existing failures from new failures.
    - Produce a mandate report with files read, changes, tests, runtime proof, limitations and next gate.

    ## 6. Acceptance criteria
    One real CAE operation executes in Pi; canonical CAE state and Pi runtime state are distinguishable; an interruption/resume path is proven without state corruption and with matching evidence.

    ## 7. Stop conditions
    STOP for authority conflict, undefined owner, new-canonical-object pressure, lane collapse, Skill nesting,
    capability bypass, dual state/receipt authority, unexplained state/receipt disagreement, or unverifiable completion.

    ## 8. Recovery / rollback
    Keep changes reversible/forward-migratable. External effects require idempotency or reconciliation.
    On failed implementation restore the prior known-good path unless operator explicitly accepts the intermediate state.

    ## 9. Operator gate
    Operator accepts the evidence or records a blocker/correction. No next mandate is implicitly authorized.
    Execute only M13 and STOP.
