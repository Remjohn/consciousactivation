# Failure and Rollback Plan

Validate dependency receipts, evidence admission, hashes, category/profile ownership,
authority, source lineage, grammar applicability, wrong-reading locks, and immutable
command identity before commit. Any failure must leave zero syntax artifacts, sequence
programs, receipts, events in governed state, or command records.

Rollback removes only the two additive ST-06.03 modules, Story tests, exact-source-set
registrations, and active ST-06.03 derived state. Existing category/profile registries,
predecessor artifacts, evidence records, and historical receipts remain immutable.
Invalidated outputs remain historically reproducible but cannot authorize active work.

