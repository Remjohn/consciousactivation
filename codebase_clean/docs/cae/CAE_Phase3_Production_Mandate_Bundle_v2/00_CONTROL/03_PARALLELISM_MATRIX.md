# Parallelism Matrix — Updated Phase 3

## Safe parallel groups after Phase 2 acceptance

### Group P3-A — setup and source substrate
- M25 Workspace + Guest Operating Context
- M26 Audience Context
- M27 Guest Genesis
- M28 Research Source Ingestion

These may proceed in parallel if schema/write ownership is disjoint.

### Group P3-B — knowledge
- M29 Knowledge Extraction + Canonicalization
- M30 Knowledge Projection (depends on M29 output contract)
- M31 Clusters/Signals (depends on M29/M30)

M29 may parallelize within its research-analysis agents, but canonical node writes require a single
conflict-resolution authority.

### Group P3-C — activation/interview
- M32 depends on M25–31 and is not parallel with those upstream phase dependencies.
- M33 depends on M32.
- M34 depends on M33.
- M35 depends on M34.

### Phase close
- M36 depends on M25–35.

## Parallelism constraints
- Use a shared Phase 2 commit baseline.
- No concurrent writers to the same canonical knowledge registry without an explicit merge owner.
- No concurrent edits to the same PRD section.
- No concurrent modifications to the same state authority/migration.
- Canonicalization conflicts must serialize at the adjudication point.
- Operator approval is never parallelized.
