# Failure and Rollback Plan

Generation fails closed on missing or altered authority, receipt, definition, validation, section, trace, contract, scaffold reason, fixture, test, immutable hash, authority, or bounded classification.

Repository commit is atomic across run event, capsule, receipt and command record. Injected failure must leave zero partial capsules, receipts, events or command records. Clean retry must succeed.

Upstream reopening creates immutable descendant invalidation evidence and clears only active references. Historical capsule bytes and receipts remain reproducible.

Source rollback is removal of the two new modules plus the bounded additions in the four existing source files and exact-source tests; prior immutable artifacts and receipts are never rewritten.
