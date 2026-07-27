# Failure and rollback plan

All failures are typed and fail closed. Required classes cover unavailable or invalid ST-03.04 receipt/manifest/artifacts; policy path or hash drift; unsupported policy, IR, or manifest version; missing/extra/drifted artifacts; unresolved or undeclared source nodes; semantic mismatch, compression, invention, authority escalation, missing applicability, lost rich lineage, or hidden executable behavior; unauthorized writer; stale concurrency; payload mismatch; and injected atomic failure.

The persistence boundary atomically commits the immutable report, run event/reference, command record, and receipt. A failing report may be returned as diagnostic evidence but cannot attach an active PASS reference. Injected failure must prove zero report, event, reference, command record, or receipt.

An authorized upstream reopen preserves prior IR, artifacts, reports, and receipts, emits linked invalidations, blocks active consumption, and requires new immutable upstream, artifact-set, and validation versions.

Source rollback is additive: remove the three new modules and seven Story test files, restore the four source files and six architecture tests to their recorded pre-ST-03.05 hashes, and rerun the 147-test predecessor suite. No database, schema, migration, dependency, published artifact, network, or external compensation exists. Never execute a destructive workspace rollback; issue hash-based evidence.
