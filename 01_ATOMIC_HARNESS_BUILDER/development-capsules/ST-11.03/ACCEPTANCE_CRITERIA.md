# Acceptance criteria

1. Given the exact active ST-11.02 plan and receipt, when deterministic Builder code
   ingests the pinned fixture, then one immutable proposal and receipt cover FR-158/FR-159.
2. Given three feedback kinds, then each retains subject identity/hash, source,
   evidence hash, provenance, finding, recommendation and human disposition need.
3. Given proposal compilation, then validated authority remains byte-unchanged and the
   proposal is explicitly unratified, non-production and non-certified.
4. Given missing identity, hash, provenance, unsupported kind or incompatible plan,
   then intake fails closed with zero partial state.
5. Given direct mutation, approval, ratification or certification is requested, then
   the command fails closed.
6. Given identical inputs, then proposal and receipt bytes are identical across fresh
   contexts; identical commands return the original receipt.
7. Given upstream invalidation, then active proposal access fails while historical
   proposal bytes remain reproducible.
8. Given injected commit failure, then no proposal, receipt or command record remains.

