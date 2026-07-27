# ST-04.05 rollback evidence

Verdict: `PASS`

## Atomic failure rollback

`MinimumCompleteContextFailureTests.test_injected_atomic_failure_leaves_zero_partial_state` injects the repository commit failure after all domain validation and before commit. The command raises `AtomicCommitFailed`, while the event count remains at the ST-04.04 predecessor value and graph, manifest-bearing graph, compilation receipt, and command-record counts remain zero. No cleanup mutation is needed.

## Required-overflow rollback

`ReferenceAndBudgetIntegrityTests.test_required_overflow_names_causes_and_does_not_truncate` reduces the hard budget below the governed required contribution. Compilation raises `ContextBudgetOverflow` with the exact required reference identities, three governed remediation choices, and `silent_truncation: false`. No required item is removed, summarized, compressed, retrieved, or committed.

## Non-destructive upstream invalidation

`MinimumContextReplayInvalidationTests.test_upstream_reopen_invalidates_exact_context_descendants_and_preserves_history` reopens the authoritative atomic boundary after a completed context compilation. The run records exactly ten ordered events:

1. `AtomicBoundaryReopened`
2. `DraftHarnessModelInvalidated`
3. `HarnessIRInvalidated`
4. `ArtifactSetInvalidated`
5. `ConstitutionalValidationInvalidated`
6. `CapabilityOwnershipInvalidated`
7. `ResponsibilityModulesInvalidated`
8. `PhaseGraphInvalidated`
9. `PhaseHandoffsInvalidated`
10. `MinimumContextInvalidated`

The invalidation records exactly the two affected manifest identities. Active consumption fails closed; the historical graph and byte-identical manifests remain retrievable and reproducible. Upstream artifacts are not mutated.

## Source rollback procedure

If this bounded implementation must be removed before a later Story consumes it:

- restore the four modified predecessor source files and five exact-source architecture tests to their pre-ST-04.05 content using the predecessor ST-04.04 completion hashes;
- remove only the two ST-04.05 source modules and six ST-04.05 test files;
- leave all predecessor completion evidence and immutable governed inputs unchanged;
- rerun the preimplementation repository baseline and require `328/328 PASS`.

This procedure has no network, provider, model, skill, database, transport, VAE, Delegation, GPU, workflow, production, or external cleanup step because none was invoked or created.
