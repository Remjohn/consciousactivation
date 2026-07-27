# Acceptance criteria

## AC-01 — Governed declared input

Given an authorized synthetic Builder Core run is `SOURCE_LOCKED` with the exact `ST-01.02` Source Lock,
When the declared-boundary service loads its input,
Then it verifies the capsule input hash, source-profile identity, target candidate identity, synthetic/non-production classification, and category-neutral binding before any decision is accepted.

## AC-02 — Human approval and deterministic compilation

Given the declared candidate has no unresolved critical contradiction and a registered human has an exact active approval grant,
When that human approves with selected candidate, rejected alternatives, evidence refs, rationale, accepted risks, and decision time,
Then Builder code atomically records `AtomicityRatification`, freezes boundary version `1.0.0`, compiles one deterministic Draft Harness Model, evaluates `HG-003=PASS`, transitions the run to `ATOMICITY_RATIFICATION`, and returns a deterministic receipt.

## AC-03 — Transparent field status

Given the model is compiled from the approved synthetic boundary,
When any constitutional field is inspected,
Then it exposes value, authority status, knowledge status, provenance, and confidence/disposition; visual/category/Activative fields are explicit `NOT_APPLICABLE`, hypothesis fields remain `HYPOTHESIS`, and the model status is `UNRATIFIED_CONSTITUTIONAL_FIELDS`.

## AC-04 — Downstream consumption guard

Given a consumer requests a field requiring ratified authority,
When the field is unratified, hypothesized, not-applicable, or invalidated,
Then consumption fails closed with a typed reason and no authoritative state changes.

## AC-05 — Revise and reject

Given an authorized human chooses `REVISE` or `REJECT`,
When the decision is submitted with rationale and evidence,
Then the attributable decision is recorded, no boundary/model is frozen, `HG-003=FAIL`, and downstream use remains blocked.

## AC-06 — Authority boundary

Given an agent, code actor, evaluator, external actor, unknown human, expired grant, wrong resource, or wrong action attempts a decision,
When authorization is evaluated,
Then the operation fails closed and creates no model, ratification, event-stream mutation, command record, or success receipt.

## AC-07 — Immutable freeze and invalidation

Given a boundary is frozen,
When any caller attempts same-version broadening, merge, split, replacement, or silent field rewrite,
Then the change fails; only an authorized human reopen can emit a complete invalidation chain, mark the model unusable, and require a new immutable version.

## AC-08 — Replay, concurrency, and atomic failure

Given a successful command,
When the same command and payload is replayed,
Then the identical receipt is returned with no duplicate authoritative event; changed payload reuse, stale stream version, or injected atomic commit failure fails without partial state.

## AC-09 — Observability and receipt

Given any success or governed rejection,
When observations are inspected,
Then Story/run/artifact/authority/version/provenance/outcome/failure context plus boundary, model, Source Lock, correlation, causation, command, and stream identities are present and receipt-linked.

## AC-10 — Boundary preservation

Given the implementation and full regression suite,
When architecture checks run,
Then existing Format 02 and source-lock behavior remains unchanged, external imports remain absent, no schema or dependency is added, prohibited paths are untouched, and all prior `57` tests still pass.

## AC-11 — Rollback

Given the Story is removed or an atomic commit is deliberately failed,
When rollback evidence is produced,
Then no migration, external compensation, persistent data cleanup, or earlier receipt rewrite is required and the prior `57`-test state is reproducible.
