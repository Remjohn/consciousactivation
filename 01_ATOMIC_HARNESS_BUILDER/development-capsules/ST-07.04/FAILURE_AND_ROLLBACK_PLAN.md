# Failure and Rollback Plan

Fail closed before commit for absent or altered policy/definition evidence, stale or invalidated lineage, missing sections/artifacts, cross-artifact disagreement, authority conflict, target/profile mismatch, universal-profile flattening, external target field leakage, false external compatibility PASS, production/certification claim, command conflict or portability failure.

One injected in-memory commit failure must leave zero reports, receipts, events, observations, command records, run references or active validation state. The same command must succeed cleanly after fault removal.

Upstream invalidation creates a new validation invalidation and preserves historical bytes. Source rollback removes only the two new ST-07.04 source modules, bounded integrations, five exact-source entries, six Story tests and six completion outputs. It does not mutate ST-07.02 evidence, planning, authority, schemas, governance or external repositories.

If implementation requires any unlisted file, dependency, schema, authority or external product behavior, stop and request a narrow human amendment.
