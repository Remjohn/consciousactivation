# Test plan

Run with `PYTHONPATH=src`, deterministic clocks and ID providers, the completed synthetic ST-03.04 artifact fixture, the in-memory development adapter, and the exact repository-local policy file. Network, external repositories, external runtimes, model calls, task execution, and filesystem artifact publication are prohibited.

Required tests:

1. valid constitutional validation report and receipt from the exact 21-item artifact set;
2. exact policy path/hash, Constitution V1.1, Builder PRD V1.2, authority order, conflict behavior, lineage, and ownership parsing;
3. closed inventory, artifact bytes/hashes, manifest identity, source-node resolution, and HarnessIR agreement;
4. Markdown and JSON semantic round-trip with formatting ignored but governed fields exact;
5. five rich lineage keys remain separate and synthetic `NOT_APPLICABLE` is explicit;
6. generated-view subordinate authority and non-executable status;
7. missing, extra, drifted, syntactically invalid, syntactically valid conflicting, compressed, invented, or authority-escalated view failures;
8. missing/altered/invalidated IR, manifest, artifact set, receipt, policy bytes, authority, or lineage failures;
9. code-only validator authority, arbitrary-path rejection, stale concurrency, payload-safe idempotency, and atomic injected failure;
10. report replay, run event replay/state hash, resume preservation, invalidation, active-consumption block, and immutable history;
11. all required observations and typed findings without payload/secret logging;
12. exact source set, standard-library-only imports, no schema/dependency/external product/Workflow IR/later-Story behavior;
13. all 35 ST-03.04 tests, all earlier Story suites, and the full 147-test predecessor regression.

Run the ST-03.05 suite twice in fresh deterministic contexts. Completion requires all tests PASS, zero mandatory skips, and no prohibited path or dependency change.
