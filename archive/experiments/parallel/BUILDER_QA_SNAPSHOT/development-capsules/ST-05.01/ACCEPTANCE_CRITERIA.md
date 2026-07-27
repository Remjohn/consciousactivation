# Acceptance Criteria

## AC-01 — Exact governed registry consumption

Given the exact active ST-04.05 Minimum Complete Context graph and all four pinned empty-registry governance artifacts, when the authorized Builder actor compiles the synthetic skill-registry snapshot, then exactly one active immutable snapshot and one receipt are committed with exact run and upstream lineage.

## AC-02 — Capability coverage with no invented skills

Given the five expected deterministic Builder-owned capabilities, when the snapshot is compiled, then each capability appears exactly once as builder-owned code, declares skill-required false, and the canonical-skill, Harness-local-adaptation, experimental-capability, recipe, and JIT-capsule sets are all empty.

## AC-03 — Classification semantics remain distinct

Given the TS-08 and ADR-009 taxonomies, when the empty snapshot is inspected, then authority lanes, maturity states, and plasticity states are explicit governed vocabularies and no code-owned capability is misrepresented as a skill or maturity claim.

## AC-04 — Exact immutable pin validation

Given the policy, fixture, schema, validation receipt, and registry version, when any byte, hash, identifier, or version differs from the capsule pins, then compilation fails closed before any state is committed.

## AC-05 — No silent mutation or version reuse

Given the governed empty registry, when a command attempts to add a skill, adaptation, experiment, dependency, evaluator receipt, or dynamic-discovery grant under the same registry or Harness version, then it is rejected and a new immutable upstream registry and Harness version is required.

## AC-06 — Maintainability violations fail closed

Given duplicate or conflicting capability identities, a relation cycle, unsupported dependency, maturity without an exact evaluator receipt, stale evaluator pins, or deprecated/revoked sediment represented as active, when validation runs, then a typed rejection is emitted and zero partial state remains.

## AC-07 — Authority and scope boundaries

Given an unauthorized actor or a request for register, promote, deprecate, revoke, discover, execute, compose, or JIT-compile behavior, when the command is submitted, then it fails closed without mutating predecessor or governance artifacts.

## AC-08 — Determinism and idempotency

Given identical governed inputs in fresh repositories, when the snapshot is compiled, then canonical bytes, snapshot identity, receipt identity, observations, and hashes are byte-identical; an identical repeat command returns the original payload, while a conflicting payload fails closed.

## AC-09 — Replay, resume, and invalidation

Given committed snapshot events and receipts, when the run is replayed or resumed, then state is reconstructed exactly; when the active Minimum Complete Context or earlier governing ancestor is invalidated, then the snapshot is marked inactive while historical bytes remain reproducible.

## AC-10 — Atomic failure and rollback

Given injected failure at each authorized commit boundary, when compilation fails, then no snapshot, receipt, event, command record, run reference, or descendant artifact is partially committed and retry succeeds after the fault is removed.

## AC-11 — External and production exclusions

Given the synthetic mode, when architecture and scope tests inspect the implementation, then no Format 02, VAE, Delegation runtime, provider, network, GPU, conversational, workflow-execution, Control Tower, production registry, or certification behavior is present.

## AC-12 — Observable completion

Given all acceptance and regression tests pass, when completion evidence is issued, then success and failure observations include run, Story, snapshot, registry, capability count, authority, version, provenance, outcome, and failure context; rollback and file-scope evidence are hash-pinned in a separate PASS Story Completion Receipt.
