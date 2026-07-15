# Deterministic test plan

Run with `PYTHONPATH=src` and no mandatory skips.

1. Preimplementation: validate this capsule, the ST-04.04 PASS receipt, empty-registry policy/receipt, and full `328/328` regression.
2. Acceptance: compile exact manifests for both phases and assert all 13 owned obligations and 12 acceptance criteria.
3. Registry: reject ghost, duplicate, altered, hashless, unowned, unauthoritative, or unsupported-mode references.
4. Loading/influence: reject wrong-phase loads, forbidden runtime loads, must-not-influence violations, and authority promotion.
5. Progressive disclosure: preserve typed pointers and block missing or altered pointer targets without loading their payloads.
6. SPR: prove explicit `NOT_APPLICABLE` exclusion for the synthetic deterministic proof without weakening production policy.
7. Budget: validate hard/soft token, latency, and cost declarations; required overflow blocks with named causes and zero truncation.
8. Manifest: assert complete included/excluded/summarized/retrieved/compressed sets, hashes, governed token contributions, priorities, and rationales.
9. Authority/lineage: reject non-code writers, conversation-history substitution, stale or invalidated handoffs, altered lineage, and receipt drift.
10. Determinism/replay: fresh repositories yield byte-identical outputs; repeat commands are idempotent and conflicts fail closed.
11. Invalidation/atomicity: exact affected descendants invalidate; injected failures leave zero partial graph, manifest, event, receipt, or command state.
12. Architecture/regression: exact source-set and import boundaries pass, Story suite passes twice, then full repository regression passes with no skips.

There are no network, tokenizer, model, provider, skill, VAE, Delegation runtime, GPU, workflow, or production tests.
