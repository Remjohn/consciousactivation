---
name: knowledge_clusterer
description: Clusters canonical knowledge nodes into typed, cohesive semantic clusters based on graph edges, tags, and category taxonomies.
version: 1.0.0
authority_lane: HUNTER
invocable_by:
  - knowledge_cluster_signal_program
passive: true
---

# Knowledge Clusterer Skill

## 1. Constitutional Role & Authority Lane
The `knowledge_clusterer` skill operates strictly in the **HUNTER** authority lane. It is a passive, flat skill that forms `KnowledgeCluster` structures by evaluating semantic relationships, common tags, and typed graph edges among canonical knowledge nodes.

## 2. Invariants & Constraints
1. **Passive Execution:** This skill is strictly passive. It cannot invoke subagents, skills, or dynamic external processes.
2. **Deterministic Grouping:** Grouping must be deterministic. Two identical sets of canonical knowledge nodes with identical graph topology must produce the exact same cluster IDs and membership sets.
3. **Integer Coherence Scoring:** Semantic coherence scores must be expressed as integer basis points ($0 \dots 10000$ bps) or micros ($0 \dots 1000000$). Floats are prohibited in canonical payloads.
4. **Lineage Preservation:** Every cluster must record the cryptographic lineage hashes of its member canonical knowledge nodes.

## 3. Output Schema
```json
{
  "cluster_id": "kcl_uuid7",
  "cluster_label": "Title",
  "theme": "Theme description",
  "cluster_type": "thematic | domain | emergent | structural",
  "coherence_score_micros": 850000,
  "member_node_ids": ["kn_001", "kn_002"],
  "lineage_hashes": ["sha256_001", "sha256_002"]
}
```
