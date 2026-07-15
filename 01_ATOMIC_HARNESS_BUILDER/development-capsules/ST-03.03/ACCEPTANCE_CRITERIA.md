# Acceptance criteria

## AC-01 — Exact active upstream package

Given the completed synthetic run is at `ATOMICITY_RATIFICATION`,
When canonical IR compilation begins,
Then the service requires the exact active Source Lock, frozen boundary, human ratification, Draft Harness Model, matching hashes/references, `HG-003=PASS`, no upstream invalidation, and the repository-owned non-production synthetic profile.

## AC-02 — One complete typed canonical IR

Given valid upstream inputs,
When deterministic code compiles revision 1,
Then exactly one immutable `cmf-builder-harness-ir/v1@1.0.0` snapshot contains the required identity, evidence, syntax, Activative semantics, phases, contexts, contracts, modules, skills, references, evaluators, repairs, budgets, implementation-units, and authorization sections.

## AC-03 — Governed material values

Given any material leaf is inspected,
When its metadata is read,
Then value, knowledge status, authority, evidence refs, decision ref where applicable, confidence/disposition, creator/version, and dependency impact are explicit; missing required provenance fails closed.

## AC-04 — Activative and category lineage without invention

Given the category-neutral synthetic source has no Activative or category-native semantics,
When its IR is compiled,
Then Identity DNA, Context Premise, Resonance, Matrix of Edging, and Activative Intelligence Pack keys remain separate canonical governed fields marked `NOT_APPLICABLE` with upstream provenance, and no required lineage is flattened into notes, promoted, or fabricated.

## AC-05 — Deterministic canonical identity

Given byte-equivalent governed inputs in fresh contexts,
When they are canonicalized,
Then canonical JSON bytes and IR hash are identical, key order is deterministic, timestamps are excluded from identity hashes, and a same-version semantic rewrite is rejected.

## AC-06 — Compatibility, migration, and deprecation

Given initial schema version `1.0.0`,
When compatibility is evaluated,
Then read/write `1.0.0`, an explicit empty prior-migration registry, and an explicit empty deprecation set validate; unknown versions or a claimed migration without a registered transformation receipt fail without mutation.

## AC-07 — Harness IR and Workflow IR separation

Given a candidate IR or typed patch contains worker, queue, retry, sandbox, deployment, or other Workflow IR ownership,
When validation runs,
Then it fails closed; Workflow IR may later reference the Harness IR identity but cannot own or rewrite product-semantic values.

## AC-08 — Authority boundary

Given code receives the already attributable human ratification,
When IR compilation executes,
Then deterministic Builder code may compile but agents, evaluators, external actors, and unauthenticated humans cannot directly write, promote, or replace IR values; no new human product decision is invented.

## AC-09 — Atomicity, concurrency, and replay

Given a successful compile command,
When it is replayed with the identical payload,
Then the identical snapshot and receipt return with no duplicate authoritative event; payload reuse, stale stream version, or injected atomic failure leaves no partial IR, run reference, command record, or receipt.

## AC-10 — Upstream invalidation and replay state

Given the frozen boundary/model later receives an authorized reopen,
When invalidation is committed,
Then the IR descendant is explicitly invalidated and unusable while prior history remains replayable; run replay reconstructs the exact active/invalidated IR reference and state hash.

## AC-11 — Observability and receipt

Given success or failure,
When Story observations are inspected,
Then run, Story, artifact, authority, schema/revision, provenance, upstream identities, IR hash, compatibility, dependency impact, correlation, causation, command, stream, outcome, and typed failure context are present and receipt-linked.

## AC-12 — Boundary preservation and rollback

Given the Story and full regression suites,
When architecture and rollback checks run,
Then prior Source Lock, run-governance, atomicity, synthetic profile, authority, replay, checkpoint, and idempotency behavior remains green; exact file scope passes; no schema/dependency/external behavior is added; and the prior `84`-test state is hash-reproducible.
