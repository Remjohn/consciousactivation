# Acceptance criteria

## AC-01 — Exact active HarnessIR

Given a synthetic run at `GENESIS` with the PASS ST-03.03 snapshot,
When artifact compilation begins,
Then the service requires the exact active, hash-valid, non-invalidated `cmf-builder-harness-ir/v1@1.0.0` identity and rejects stale, missing, altered, superseded, or foreign IR.

## AC-02 — Complete bounded artifact inventory

Given valid IR and reproducible build config,
When the compiler runs,
Then it produces exactly 8 human Markdown shards, 3 governed OpenSpec JSON views, and 10 machine JSON views, with no partial, extra, executable, or later-Story artifact.

## AC-03 — Single-source projections

Given any generated semantic value,
When its provenance is inspected,
Then it resolves to declared HarnessIR source-node paths and preserves value, knowledge status, authority, evidence, disposition, and explicit `NOT_APPLICABLE`/hypothesis state without invention or duplicate authority.

## AC-04 — Deterministic manifest identity

Given identical IR, compiler version, and reproducible build config in fresh contexts,
When compilation repeats,
Then all artifact bytes, content hashes, ordered inventory, manifest bytes/hash, artifact-set ID, and receipt hash are byte-identical.

## AC-05 — Required binding metadata

Given any generated artifact or the manifest,
When identity metadata is inspected,
Then source IR ID/hash, exact source-node set, compiler ID/version, config hash, reproducible RFC3339 generation timestamp, media type, authority class, and artifact content hash are present and valid.

## AC-06 — Governed OpenSpec and machine views

Given OpenSpec or machine projection output,
When it is parsed,
Then it is canonical JSON derived from the same IR, explicitly non-executable and subordinate to HarnessIR, and contains no external OpenSpec runtime, Control Tower, provider, workflow, or certification behavior.

## AC-07 — Manual drift fails closed

Given bytes of a generated authoritative view are altered,
When manifest validation runs,
Then a typed drift report identifies the path and expected/observed hashes, quarantines the altered view, preserves the original manifest and HarnessIR, and never promotes the edit.

## AC-08 — Atomicity and completeness

Given an incomplete renderer result, undeclared IR read, cross-artifact conflict, or injected commit failure,
When compilation runs,
Then no artifact, manifest, run reference/event, command record, or receipt is committed.

## AC-09 — Authority and security

Given the compile or drift-validation seam,
When an agent, evaluator, external actor, unauthenticated human, network path, secret, or undeclared external reference is introduced,
Then the operation fails closed; deterministic Builder code alone may create generated views.

## AC-10 — Idempotency, replay, and concurrency

Given one successful command,
When the identical payload repeats,
Then the same receipt returns without duplicate events; changed payload reuse or stale stream version fails without mutation, and event replay reconstructs the exact artifact-set reference and state hash.

## AC-11 — Upstream invalidation

Given the atomic boundary is authoritatively reopened after artifact compilation,
When the invalidation chain commits,
Then HarnessIR and artifact-set descendants are explicitly invalidated and unusable while their immutable history remains available; a new IR and artifact-set version are required.

## AC-12 — Observability, scope, and rollback

Given success, replay, rejection, drift, atomic failure, or invalidation,
When Story observations and completion evidence are inspected,
Then all required identities and typed outcomes are receipt-linked, the full prior 112-test state remains green, exact file scope passes, and no prohibited schema, dependency, external behavior, task execution, or next Story is introduced.
