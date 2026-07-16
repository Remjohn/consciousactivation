# Test Plan

Implementation begins only after the capsule authorization phrase is supplied. Run the complete preimplementation suite and require 356/356 PASS with no mandatory skips.

Story tests:

- compile the exact empty registry against the active ST-04.05 context;
- assert exact five-of-five capability coverage and zero skill/adaptation/experiment/recipe/capsule entries;
- assert authority-lane, maturity, and plasticity vocabularies remain explicit and distinct;
- verify exact fixture, policy, schema, validation-receipt, version, and hash pins;
- reject registry bytes, pins, version, authority, lineage, run, and context drift;
- reject any nonempty skill set, undeclared use, dynamic discovery, hidden orchestration, or same-version mutation;
- reject duplicate/conflicting capabilities, relation cycles, unsupported dependencies, maturity without evidence, stale evaluator pins, and active sediment;
- reject unauthorized issuance and every prohibited operation;
- prove canonical ordering, fresh-context byte equality, snapshot and receipt hash reproducibility;
- prove identical-command payload-safe idempotency and conflicting-command rejection;
- prove replay and resume reconstruct the same active state;
- prove upstream invalidation deactivates the descendant snapshot without erasing history;
- inject atomic failure and prove zero partial state, then retry successfully;
- verify required observations and receipt linkage;
- verify exact architecture source sets and prohibited-import boundaries.

Completion runs:

1. ST-05.01 suite, first run.
2. ST-05.01 suite, independent repeat.
3. Complete repository regression including all predecessor Stories.
4. Hash and file-allowlist validation.
5. Completion-receipt payload and artifact validation.

No external service, network, provider, database, GPU, VAE, Delegation runtime, evaluator, or Format 02 fixture is permitted.
