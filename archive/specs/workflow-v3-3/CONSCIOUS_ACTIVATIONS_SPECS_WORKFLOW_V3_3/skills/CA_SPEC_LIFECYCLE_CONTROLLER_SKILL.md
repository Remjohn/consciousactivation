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

The controller coordinates independent agents. It does not collapse independent roles into one agent and does not allow a specification to skip a state.

## Current authority order

1. Current Program Control authority pointer and ratified Constitution.
2. Activative Intelligence Lifecycle Constitution V2.1.
3. Current product PRD and ratified amendments.
4. Controlling Functional Requirements and Stories.
5. Cross-product ownership and handoff ledger.
6. Accepted upstream Tech Specs and shared contract releases, when they already exist.
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
- `ACCEPTED_FOR_PRODUCT_ADOPTION`
- `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`
- `PRODUCT_ADOPTION_REQUIRED`
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

Each child-agent execution works on exactly one Tech Spec. A controller may coordinate many child executions, but no child writer, auditor, reviser, re-auditor, or builder processes a batch of unrelated specs in one execution.

## Dependency-stage law

A dependency edge must be classified before it can block work. Every edge has exactly one primary class:

- `AUTHORITY_DEPENDENCY` — ratified authority required before WRITE.
- `WRITE_INTERFACE_DEPENDENCY` — the writer needs the upstream object/interface shape. The upstream spec may be `WRITTEN_PENDING_AUDIT`, `REVISED_PENDING_REAUDIT`, `ACCEPTED_FOR_BUILD`, or replaced by an exact frozen `WRITE_TIME_CONTRACT_SEED`.
- `WRITE_CONTEXT_DEPENDENCY` — the upstream draft is useful context but not controlling authority. A hash-pinned draft may be read; absence blocks only when the packet proves unique information is required.
- `ACCEPTANCE_PREREQUISITE` — the upstream spec must be `ACCEPTED_FOR_BUILD` before the dependent spec can receive final `ACCEPTED_FOR_BUILD`; it does not automatically block WRITE.
- `BUILD_PREREQUISITE` — the upstream implementation must be `BUILT` or `INTEGRATION_ACCEPTED` before BUILD; it never blocks WRITE or AUDIT by itself.
- `REFERENCE_ONLY` — non-authoritative context; it cannot block unless separately promoted to required unique evidence.

`QUEUED_FOR_WRITE` is not a readable upstream specification. The controller must write dependency roots first, then release later topological writing waves when required upstream drafts are hash-pinned.

A draft dependency is not accepted authority. Every dependent writer must label it `DRAFT_DEPENDENCY_NOT_ACCEPTED`, pin its hash, and record which sections may require revision if upstream audit changes the interface.

A true requirement for an upstream spec to be accepted before downstream WRITE is exceptional. It must be encoded explicitly as `AUTHORITY_DEPENDENCY` or `REQUIRED_ACCEPTED_SPEC_AT_WRITE` with an attributable Program Control reason. It must never be inferred from a generic `depends_on` field.

## Writing-wave law

Prompt controllers must compute a topological DAG using only WRITE-blocking edges:

- authority edges;
- write-interface edges;
- write-context edges proven to contain unique required information.

Within one wave, disjoint specs may be written in parallel. The next wave may begin after the prior wave emits `WRITTEN_PENDING_AUDIT` receipts and exact draft hashes. Acceptance is not required during the writing factory.

If the WRITE graph contains a cycle:

1. identify the exact strongly connected component;
2. check whether ratified shared contracts already resolve the cycle;
3. otherwise request a bounded Program Control architecture decision or frozen `WRITE_TIME_CONTRACT_SEED`;
4. block only the affected component, not unrelated writing waves.

## Repository write-authority law

Every packet must be checked against the nearest applicable `AGENTS.md` and repository-local write allowlist before dispatch.

Allowed path classes:

- `DIRECT_PRODUCT_SPEC_PATH` — the target product currently permits the exact path.
- `PROGRAM_CONTROL_CROSS_PRODUCT_PROPOSAL` — the product does not permit the target path; write the full proposed amendment under the governed Program Control spec-factory proposal path.
- `DEFERRED_UNTIL_PRODUCT_AUTHORIZATION` — neither direct product writing nor a Program Control proposal is authorized.

A Program Control cross-product proposal must record:

- target product;
- proposed canonical adoption path;
- current repository prohibition;
- adoption status `PRODUCT_ADOPTION_REQUIRED`;
- build state `NOT_BUILD_READY`.

It may complete WRITE, AUDIT, REVISION, and RE-AUDIT. It may receive `ACCEPTED_FOR_PRODUCT_ADOPTION`, but it cannot receive a product-local Development Capsule or `ACCEPTED_FOR_BUILD` until the target product grants write/adoption authority and the adopted bytes are independently re-audited.

## Parallelization law

Parallel work is permitted only when:

- canonical output files are disjoint;
- upstream inputs required for the current lifecycle stage are frozen;
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
- dependency-edge classification ledger;
- write-wave DAG and status registry;
- path-ownership registry;
- product-adoption queue;
- Development Capsule index;
- Build Ledger;
- integration status registry.

## Stop conditions

Stop the affected unit when:

- a source classified as `REQUIRED_AUTHORITY`, `REQUIRED_CURRENT_IMPLEMENTATION`, or `REQUIRED_UNIQUE_EVIDENCE` is missing or unreadable;
- authority is ambiguous;
- ownership is duplicated;
- target file scope overlaps another active lane;
- repository-local write authority is unresolved;
- a required decision is absent;
- a spec hash has drifted;
- an upstream dependency required for the current lifecycle stage is absent;
- the requested state transition is not allowed.

Do not stop the complete writing factory merely because build prerequisites are unbuilt or acceptance prerequisites are not yet accepted.

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

## Authority-stage law

Authority ratification and specification-work authorization are distinct.

Specification work may proceed against a candidate authority package when an attributable Program Control or operator receipt explicitly authorizes:

- reconciliation;
- queue freezing;
- Tech Spec writing;
- independent audit;
- revision;
- re-audit;
- technical convergence.

While ratification is pending:

- candidate authority must remain labeled `CANDIDATE_NOT_CURRENT`;
- writers may not represent it as current product authority;
- no implementation or production authority is created;
- no specification controlled solely by the unratified candidate may receive final `ACCEPTED_FOR_BUILD`;
- the highest technical status is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` or `ACCEPTED_FOR_PRODUCT_ADOPTION`, as applicable;
- Development Capsules and BUILD remain blocked until the required authority transition is complete.

Ratification is therefore a gate for authority promotion and build authorization, not automatically a gate for WRITE, AUDIT, REVISION, or RE-AUDIT.

## Persistent-state law

Canonical workflow gates must rely on committed or otherwise hash-locked durable records.

Ephemeral agent-run logs, console summaries, temporary worktree files, and uncommitted local directories are not mandatory historical inputs unless:

1. they were explicitly declared canonical before the run;
2. their exact bytes and hashes were recorded in a durable manifest;
3. their governed location is available to the next agent.

A correction prompt must never require restoration of an ephemeral failed-run directory merely to rederive a deterministic decision from still-valid canonical inputs.

When failed-run artifacts are absent:

- record `EPHEMERAL_EXECUTION_LOG_NOT_PERSISTED`;
- preserve any committed missing-input or failure report;
- rederive the correction from the canonical queue, dependency DAG, packets, authority receipts, and repository instructions;
- do not fabricate the absent bytes;
- do not block unrelated recovery work.

The next agent must not depend on conversation-only paths such as `D:/...` unless those files are committed, hash-locked, or explicitly supplied as current inputs.
