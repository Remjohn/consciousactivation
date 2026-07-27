# ST-06.02 Rollback Evidence

All input hashes, mappings, authority, identity, and immutable conflicts are validated
before commit. The injected failure test proves zero profile registries and zero receipts
remain after failure. A repeated command returns its original receipt; conflicting reuse
is rejected. Existing governance registries and ST-06.01 artifacts are never mutated.

The implementation is additive and introduces no database, migration, transport,
external runtime, or persistent real-profile state. Removing its two additive modules
and exact-source registrations restores the prior executable surface.

