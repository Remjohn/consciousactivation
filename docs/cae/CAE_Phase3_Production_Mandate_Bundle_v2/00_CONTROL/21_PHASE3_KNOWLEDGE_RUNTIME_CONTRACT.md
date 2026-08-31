# Phase 3 Knowledge Runtime Contract

OKF is the curated knowledge representation/exchange layer.
Supabase/PostgreSQL is the authoritative structured operational layer.
Obsidian/Git is the human curation/inspection surface.
Retrieval is a service boundary, not the source of truth.

## Required projection

OKF/curated knowledge
    ↓
canonical IDs + versions + provenance
    ↓
Supabase/Postgres
    ├── structured/SQL retrieval
    ├── lexical retrieval
    ├── vector retrieval (where implemented)
    └── graph-ready relationships

The phase must not introduce Redis as canonical storage. A hot-context/memory layer may be evaluated
later without changing knowledge authority.
