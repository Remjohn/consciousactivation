# Failure and Rollback Plan

Validate hashes, mappings, authority, invariants, and immutable command identity before
commit. Injected failure must leave zero profile registries, receipts, events in governed
state, or command records. Reverting the two additive modules and exact-source-set
registrations restores the prior source tree. Existing registries and ST-06.01 artifacts
must never be mutated.

