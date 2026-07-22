# SKILL — Conscious Activations Specification Lifecycle Controller

## Purpose

Control the complete specification lifecycle:

```text
WRITE
→ AUDIT
→ REVISE
→ RE-AUDIT
→ ACCEPTED_FOR_BUILD
→ DEVELOPMENT CAPSULE
→ BUILD
→ INTEGRATION ACCEPTANCE
```

The controller coordinates agents. It does not collapse independent roles into one agent and does not allow a spec to skip a state.

## Current authority order

1. Current Program Control authority pointer and ratified Constitution.
2. Activative Intelligence Lifecycle Constitution V2.1.
3. Current product PRD and ratified amendments.
4. Controlling Functional Requirements and Stories.
5. Cross-product ownership and handoff ledger.
6. Accepted upstream Tech Specs and shared contract releases.
7. Current repository implementation and current-status receipts.
8. CMF Studio predecessor evidence and exact migration dispositions.
9. External implementation references explicitly admitted by the target spec.

Higher authority wins. Conflicts are recorded; lower authority is not silently blended into current law.

## Status state machine

A specification has exactly one current quality state:

- `QUEUED_FOR_WRITE`
- `WRITING`
- `WRITTEN_PENDING_AUDIT`
- `AUDIT_IN_PROGRESS`
- `REVISION_REQUIRED`
- `ARCHITECT_DECISION_REQUIRED`
- `REVISION_IN_PROGRESS`
- `REVISED_PENDING_REAUDIT`
- `REAUDIT_IN_PROGRESS`
- `ACCEPTED_FOR_BUILD`
- `SUPERSEDED`
- `DEFERRED`

Build states are separate:

- `NOT_BUILD_READY`
- `CAPSULE_REQUIRED`
- `READY_TO_BUILD`
- `BUILD_IN_PROGRESS`
- `BUILD_AMBIGUITY`
- `BUILD_BLOCKED`
- `BUILT`
- `INTEGRATION_ACCEPTED`
- `INTEGRATION_REJECTED`

No transition may be inferred from prose. Every transition requires a typed receipt.

## Independence law

- A writer cannot audit its own spec.
- A reviser cannot perform the controlling re-audit.
- A builder cannot revise its controlling spec.
- A producing product cannot approve its own cross-product authority claim.
- The final accepted hash is issued only by the independent re-audit/integration controller.

## One-spec law

Each child agent execution works on exactly one Tech Spec. A controller may coordinate many child executions, but no child writer, auditor, reviser, re-auditor, or builder processes a batch of unrelated specs in one execution.

## Parallelization law

Parallel work is permitted only when:

- canonical output files are disjoint;
- upstream dependencies are frozen;
- shared schemas are not being edited by more than one lane;
- one controller owns integration;
- every agent has an exact allowlist and denylist;
- every agent emits a receipt and file manifest.

## Drift blacklist

Stop and escalate when work would permit:

- Pipeline recompiling AIR-owned meaning;
- Builder manufacturing Activative or human truth;
- Studio becoming canonical semantic storage;
- VAE production logic placed inside Pipeline;
- Delegation acquiring semantic authority;
- planned evidence represented as observed;
- historical archetypes represented as current authority;
- fuzzy or invented Primitive identities;
- composition before approved Final Script;
- missing psychological role inside a tension;
- missing Primitive Coalition Contract;
- missing Activation Transfer Contract;
- silent runtime substitution;
- active Format 02 implementation without new authority;
- fake artifacts represented as real;
- offline implementation represented as full evidence closure;
- production or certification claims without separate authority.

## Controller artifacts

Maintain:

- canonical specification ledger;
- specification quality status registry;
- accepted spec registry;
- accepted spec hash lock;
- audit findings registry;
- architecture decision ledger;
- dependency DAG;
- path-ownership registry;
- Development Capsule index;
- Build Ledger;
- integration status registry.

## Stop conditions

Stop the affected unit when:

- a source classified by the current `SOURCE_DISPOSITION_LEDGER` as `REQUIRED_AUTHORITY`, `REQUIRED_CURRENT_IMPLEMENTATION`, or `REQUIRED_UNIQUE_EVIDENCE` is missing or unreadable;
- authority is ambiguous;
- ownership is duplicated;
- target file scope overlaps another active lane;
- a required decision is absent;
- a spec hash has drifted;
- an upstream accepted/build receipt is absent;
- the requested state transition is not allowed.

## Source-disposition law

A named source is not automatically a blocking source.

Before WRITE or AUDIT, the controller must maintain a current `SOURCE_DISPOSITION_LEDGER` that classifies every source as one of:

- `REQUIRED_AUTHORITY`
- `REQUIRED_CURRENT_IMPLEMENTATION`
- `REQUIRED_UNIQUE_EVIDENCE`
- `OPTIONAL_REFERENCE`
- `DEFERRED_REFERENCE`
- `SUPERSEDED`

Only the first three classes may block a lifecycle transition when unavailable.

Historical assignment wording does not override the current source-reuse crosswalk, current authority, or an attributable source-disposition decision.

An unavailable optional source must produce a `SOURCE_GAP_NOTICE`; no claim may be attributed to it, but it does not block unrelated specifications.
