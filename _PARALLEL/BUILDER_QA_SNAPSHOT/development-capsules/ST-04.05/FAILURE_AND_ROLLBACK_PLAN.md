# Failure and rollback plan

Validation completes before commit. Missing or ghost references, invalid modes, influence violations, missing pointers, conversation-history substitution, required overflow, silent truncation, stale/invalidated handoffs, altered lineage, unauthorized actors, payload conflict, or injected persistence failure leaves zero partial graph, manifest, receipt, event, or command record.

Rollback is non-destructive:

1. invalidate the active minimum-context graph and only its affected descendants;
2. preserve immutable historical references, policies, manifests, receipts, upstream handoffs, and lineage;
3. restore predecessor source and exact-source tests using completion-evidence preimplementation hashes;
4. rerun the ST-04.04 `328/328` predecessor regression.

No external cleanup is needed because no network, model, skill, VAE, Delegation, workflow, database, or production system is invoked.
