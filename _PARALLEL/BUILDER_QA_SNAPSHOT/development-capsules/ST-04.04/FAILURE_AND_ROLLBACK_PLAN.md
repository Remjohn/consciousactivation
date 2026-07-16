# Failure and rollback plan

Validation is complete before commit. Contradiction, missing phase/field/dependency/authority/provenance, ownership conflict, forbidden rewrite, compatibility failure, stale or invalidated parent, altered input, payload conflict or injected persistence failure leaves zero partial context contracts, handoff graph, receipt, domain event or command record.

Rollback is non-destructive:

1. invalidate the active internal handoff graph and only its affected active descendants;
2. preserve immutable historical graph, contexts, handoffs, receipt and upstream lineage for replay;
3. restore predecessor code and exact-source architecture expectations using the preimplementation hashes recorded in completion evidence;
4. rerun predecessor regressions and prove the active ST-04.03 Phase Graph remains consumable.

Rollback never rewrites a Phase Graph, authoritative field or historical receipt. External systems require no cleanup because none are invoked.
