# M15 — Harness Package Loader + Runtime Binding

    Status: PROPOSED — OPERATOR-RATIFICATION-REQUIRED
    Phase: 2 — Runtime Foundation

    ## 1. Decision / Objective
    Bind authored Harness packages to the existing Harness Builder/Pipeline binding machinery without creating a parallel Harness authority.

    ## 2. Mandatory reading before action
    Baseline: `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
    Mandate-specific:
    M10 binding contract; Harness authoring guide; Builder/Pipeline binding/compiler; M13 state mapping; Harness library/manifest.

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
    Implement loader/binding adapter and prove a real existing Harness package reaches the current binding compiler with workflow/actor/capability metadata intact.

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
    A real Harness loads/binds; invalid packages fail before runtime; source→binding field provenance is recorded.

    ## 7. Stop conditions
    STOP for authority conflict, undefined owner, new-canonical-object pressure, lane collapse, Skill nesting,
    capability bypass, dual state/receipt authority, unexplained state/receipt disagreement, or unverifiable completion.

    ## 8. Recovery / rollback
    Keep changes reversible/forward-migratable. External effects require idempotency or reconciliation.
    On failed implementation restore the prior known-good path unless operator explicitly accepts the intermediate state.

    ## 9. Operator gate
    Operator accepts the evidence or records a blocker/correction. No next mandate is implicitly authorized.
    Execute only M15 and STOP.
