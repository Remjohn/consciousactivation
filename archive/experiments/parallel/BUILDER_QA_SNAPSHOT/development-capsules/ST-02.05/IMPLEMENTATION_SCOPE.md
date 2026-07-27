# Implementation scope

Implement one vertical declared-boundary outcome at the existing application command seam.

The implementation may add typed domain contracts for a declared atomic boundary, approve/revise/reject decision, human ratification, field-level authority and knowledge status, Draft Harness Model, invalidation, HG-003 evaluation, and decision receipt. It may add an application service that verifies the active synthetic run and its exact Source Lock, loads the hash-pinned declared-boundary capsule input, obtains exact authority, validates the decision, compiles the model deterministically, and atomically commits model, decision, events, command record, and receipt.

Approval must freeze an immutable boundary version and compile a Draft Harness Model. The boundary is human-ratified; downstream constitutional fields remain explicitly unratified, not-applicable, or hypotheses as their field status requires. Revise and reject must record attributable decisions without freezing a model. Reopen must be human-only, explicitly invalidate the frozen boundary and Draft Harness Model, and require a new immutable version before replacement.

The implementation may extend the existing run event stream, authority actions, repository ports, in-memory development/test adapter, and synthetic target-profile lifecycle by the single backward edge `SOURCE_LOCKED -> ATOMICITY_RATIFICATION` with prerequisite `atomic_boundary_ratified`. It must preserve replay, idempotency, optimistic concurrency, source-lock immutability, and current behavior.

The public seam remains a Python application service plus typed contracts. No API, CLI, UI, database, network, external runtime, provider, or task executor is in scope.

The governed input is `DECLARED_BOUNDARY_INPUT.json`; semantic data must not be hard-coded differently from it. No external package may be added.
