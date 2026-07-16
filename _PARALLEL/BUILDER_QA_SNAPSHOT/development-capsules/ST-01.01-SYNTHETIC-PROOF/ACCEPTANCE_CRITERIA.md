# Acceptance criteria

## AC-SP-01 — Preserve the completed foundation

Given the original `ST-01.01` completion receipt with SHA-256 `ec3e425cb562c16a6b31e427046962687b2dbfb781856b677593520635cffd7b`, when the supplemental branch suite starts, then that exact receipt validates, the original capsule is unchanged, and all original 20 acceptance/regression tests pass.

## AC-SP-02 — Admit only the pinned synthetic profile

Given the exact capsule fixture and its manifest hash, when an authorized operator starts an `atomic_content_harness` run for `synthetic_text_normalization_v1`, then the Builder creates one stable run identity, binds the exact profile and empty-registry hashes, and exposes the declared required-work sequence.

## AC-SP-03 — Preserve explicit proof classification

Given an admitted synthetic run, when its state and events are inspected, then they state `synthetic`, `repository_owned`, `non_production`, `non_certified`, and `builder_core_validation_only`, and they do not claim canonical category membership.

## AC-SP-04 — Resume without duplicate decisions

Given a checkpointed synthetic run with one completed transition, when the run resumes and the same command is replayed, then its run identity and prior decision remain stable and no duplicate authoritative event or work completion is emitted.

## AC-SP-05 — Enforce the empty registry

Given the hash-pinned empty registry, when the synthetic profile is loaded, then zero external skills are declared; when any undeclared or dynamically discovered skill is requested, then the operation fails closed without mutating run state.

## AC-SP-06 — Fail closed on fixture drift or wrong identity

Given a fixture with a changed byte, wrong profile ID, wrong compilation target, production-eligible flag, canonical category membership, or wrong registry hash, when the repository loads it, then loading fails before a run is created and emits no success event.

## AC-SP-07 — Preserve authority boundaries

Given an unauthorized actor or invalid lifecycle transition, when a synthetic run command is attempted, then the command fails with the existing typed authority or transition error, state is unchanged, and no authoritative success event is appended.

## AC-SP-08 — Exclude external and future product behavior

Given the supplemental branch, when its dependencies and emitted evidence are inspected, then it has no Format 02 corpus, VAE, Delegation runtime, conversational, GPU, evaluator, provider, visual-baseline, publication, or production-certification invocation.

## AC-SP-09 — Produce complete observability evidence

Given each successful synthetic transition, when audit evidence is read, then run ID, target, profile ID and hash, registry ID and hash, actor, authority decision, prior and new state, command ID, event ID, timestamp, and non-production classification are present and correlated.

## AC-SP-10 — Stop at the branch boundary

Given a valid admitted and resumable synthetic run, when branch completion is assessed, then no synthetic task workspace, Harness IR, AtomicHarnessDefinition, task Development Capsule, or final task output has been created, and `ST-01.02` remains blocked pending this branch's PASS receipt.

All ten criteria are mandatory and executable. No waiver may convert a failure into branch completion.
