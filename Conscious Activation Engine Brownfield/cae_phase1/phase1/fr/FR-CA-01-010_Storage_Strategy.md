# FR-CA-01-010 — Storage Strategy: SQL + JSONB + Vector + Events

## Requirement
The architecture SHALL use storage mechanisms according to semantic role rather than convenience.

## Policy
- PostgreSQL typed columns: stable semantics, keys, statuses, canonical scalar fields.
- Relational tables: important relationships and joins.
- JSONB: evolving structured attributes, hypotheses, examples, rich configuration, bounded prose where explicitly typed.
- Vector index: fuzzy semantic retrieval; never the ontology authority.
- Event records: append-only temporal observations and transitions.
- Views/functions: constrained semantic retrieval and agent governance boundaries.

## Acceptance Criteria
An object must have a documented reason for its chosen physical representation and a migration path when JSONB/experimental structures are promoted into canonical schemas.
