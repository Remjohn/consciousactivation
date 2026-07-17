# Test Plan

## Golden cases

- Short-form edited video compiles time-state ordering, edited transitions, reading
  hierarchy, payoff, intended reaction, and commitment from rich evidence references.
- Format 02 compiles character-performance, staging, expression/state, continuity, and
  beat grammar and demonstrably differs from edited-video grammar.
- Carousel compiles slide roles and swipe progression without frame-time motion.
- Supervisual compiles one-frame attention hierarchy and explicitly marks temporal and
  conversational grammar `NOT_APPLICABLE` with governed justification.
- Each of `public_comment`, `reply_dm`, `reelcast_expression`, and
  `interview_expression` compiles a turn-relationship structure, not a timeline or
  document, and remains structural and uncertified.
- Generic non-Activative input returns explicit `NOT_APPLICABLE` without touching
  Activative contracts.
- The admitted empirical case set reproduces the category-native result and rejected
  flattened comparator recorded by BD-007.

## Negative cases

- Reject edited-video grammar under Format 02 and animation grammar under short-form.
- Reject timeline fields for conversational profiles and frame-time motion for
  carousels/supervisuals.
- Reject unsupported category/profile pairing, multiple category ownership, missing
  applicable syntax evidence, and a corpus identity not admitted by BD-004.
- Reject sparse tokens missing rich source refs, wrong-reading locks, or frozen source
  versions; reject semantic lineage or authority drift.
- Reject invented Reaction Receipt, Expression Moment, desired reaction, human truth,
  landing, or Identity DNA approval.
- Reject Activation First violations, development parsing that invents runtime
  semantics, false benchmark/certification state, provider/runtime calls, and external
  product behavior.
- Reject stale, superseded, invalidated, altered-hash, and conflicting-command inputs.

## Determinism, lifecycle, and boundary tests

- Canonical map/list ordering, byte equality in fresh contexts, stable artifact/receipt
  hashes, payload-safe idempotency, replay and resume.
- Changed governed input creates a new immutable artifact identity; predecessor
  invalidation invalidates active descendants while preserving historical reproduction.
- Injected failure leaves zero syntax artifacts, sequence programs, receipts, events,
  or command records; rollback is non-destructive.
- Authority denial, exact-source architecture checks, no-network/no-provider/no-VAE/
  no-Delegation-runtime boundaries, predecessor suites, and complete regression.

Planned test modules, created only after the blocker cut closes:
`test_category_native_compilation.py`, `test_sequence_and_lineage.py`,
`test_failure_and_authority.py`, and `test_architecture_boundary.py`.

