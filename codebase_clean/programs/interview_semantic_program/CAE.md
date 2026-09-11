# Interview Semantic Program Package

Governed by TS-APP-COMPOSER-001 and Phase 1 M02/M08 Contracts.
Authority Lanes: HUNTER, ANALYST.
Typed Operations: ingest_interview_source, record_interview_turn.
Mutation Boundary: CAE PostgreSQL state only via typed operations.
Filesystem contents are composition metadata, not canonical state.
