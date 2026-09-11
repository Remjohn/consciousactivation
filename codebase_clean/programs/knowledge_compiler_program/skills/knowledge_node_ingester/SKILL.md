---
name: knowledge_node_ingester
description: Passive flat skill for ingesting validated canonical knowledge nodes and OKF documents with source SHA-256 provenance preservation.
version: 1.0.0
lane: HUNTER
---

# Knowledge Node Ingester Skill

## Role & Invariants
- Operates strictly under the **HUNTER** lane.
- Ingests verified `CanonicalKnowledgeNode` entities and OKF documents produced by upstream canonicalization.
- Verifies that all incoming nodes retain valid `node_id`, `source_record_refs`, `source_evidence_hashes`, and `lineage_sha256`.
- Ensures zero modification of source records or protected evidence.
- Passive and flat: invokes no sub-skills or downstream services.
