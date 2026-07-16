# Test Plan

Require the then-current complete governed repository regression, initially `427/427 PASS` with no mandatory skips.

Story tests must verify:

- successful validation of the exact active ST-07.02 definition and receipt;
- exact four-obligation mode-specific coverage;
- all 20 required sections and complete target artifact coverage;
- exact definition, authority and upstream lineage;
- target-specific gate coverage and deterministic gate ordering;
- internal Atomic Content Harness compatibility PASS;
- external target compatibility exactly `NOT_EVALUATED_EXTERNAL_TARGET_BRANCH`;
- target separation and universal-profile flattening rejection;
- false production, certification and inherited certification rejection;
- missing, altered, stale, invalidated, wrong-target, externally broadened and unauthorized input rejection;
- deterministic canonical ordering, fresh-context byte equality and changed-input identity;
- payload-safe idempotency and conflicting-command rejection;
- atomic failure with zero partial state and clean retry;
- replay, checkpoint resume, upstream invalidation and historical reproduction;
- deterministic observations and architecture boundaries;
- every predecessor regression.

No Harness execution, external target compilation, Development Capsule generation, network, provider, database, GPU, evaluator, VAE, Delegation runtime, Format 02, conversational or production fixture is permitted.
