---
name: supabase_projection_compiler
description: Passive flat skill for compiling canonical knowledge entities into structured relational tables (cae.knowledge_node, cae.knowledge_edge, cae.knowledge_projection, cae.knowledge_provenance_link).
version: 1.0.0
lane: COMPOSER
---

# Supabase Projection Compiler Skill

## Role & Invariants
- Operates strictly under the **COMPOSER** lane.
- Compiles `CanonicalKnowledgeNode` entities into strongly-typed PostgreSQL / Supabase table records (`cae.knowledge_node`, `cae.knowledge_edge`, `cae.knowledge_projection`, `cae.knowledge_provenance_link`).
- Generates standard JSON projection payloads conforming to `knowledge_projection.schema.json`.
- Preserves node IDs, versioning, provenance back-pointers, and multi-tenant workspace isolation.
- Passive and flat: invokes no sub-skills or downstream services.
