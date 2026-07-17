# Test plan

- Acceptance: exact FR coverage and one typed item for each of the three feedback kinds.
- Trace: exact ST-11.02 plan, parent capsule, receipt and evidence hashes.
- Authority: proposal-only state; direct mutation, approval and ratification rejected.
- Negative: absent identity/hash/provenance, unsupported kind and production claim.
- Lifecycle: atomic failure, idempotency, conflicting command, invalidation and history.
- Determinism: fresh-context canonical byte equality for proposal and receipt.
- Observability: attributable start, item, commit, replay and rejection evidence.
- Architecture and full repository regression.

