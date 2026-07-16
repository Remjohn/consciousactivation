# Acceptance Criteria

1. Given the active Source Lock, complete Evidence Index, governed contract and
   code authority, when saturation is evaluated, then `PASS` is issued with exact
   coverage, lineage and a downstream `PROCEED` consequence.
2. Given a missing required role, when evaluated, then
   `BLOCKED_MISSING_EVIDENCE` is issued and downstream work is blocked.
3. Given present but insufficient target diversity or specimen coverage, when
   evaluated, then `INSUFFICIENT_TARGET_EVIDENCE` is issued.
4. Given contradictory authority evidence, when evaluated, then
   `BLOCKED_CONTRADICTORY_AUTHORITY` is issued and cannot be downgraded by code.
5. Given an explicit authorized human waiver for only non-critical limitations,
   `PASS_WITH_LIMITATIONS` is representable; code authority alone cannot issue it.
6. Given a critical claim without traceable active evidence, evaluation fails closed
   under `HG-002`; `NOT_APPLICABLE` cannot replace required evidence.
7. Missing, altered, stale, superseded or invalidated inputs are rejected before
   commit with zero partial state.
8. Identical governed inputs produce byte-identical evaluations and receipts in a
   fresh context; changed inputs produce a new immutable identity.
9. Identical command replay returns the original receipt; a conflicting payload is
   rejected; observation delivery retry never converts committed state to failure.
10. Upstream invalidation invalidates the active descendant while preserving its
    historical bytes and receipt.
11. Both success and rejection observations carry run, Story, artifact, authority,
    version, provenance, outcome and failure context.
12. Existing Source Lock, Evidence Index, authority, replay, checkpoint and rollback
    behavior remains unchanged and no external-product behavior is introduced.
