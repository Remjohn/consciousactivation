---
name: research_signal_detector
description: Computes temporal velocity, acceleration, divergence, novelty, and confidence for emergent world signals grounded in knowledge clusters.
version: 1.0.0
authority_lane: ANALYST
invocable_by:
  - knowledge_cluster_signal_program
passive: true
---

# Research Signal Detector Skill

## 1. Constitutional Role & Authority Lane
The `research_signal_detector` skill operates strictly in the **ANALYST** authority lane. It evaluates temporal observations across research sources, maps them to semantic knowledge clusters, and calculates 14-feature space metrics.

## 2. Invariants & Constraints
1. **Passive Execution:** This skill is strictly passive and flat.
2. **Temporal Signal Separation:** Research signals represent dynamic external cultural/scientific state, NOT canonical knowledge truth. Signals must not be persisted as immutable canonical nodes.
3. **Integer Basis Points Metrics:** Velocity, acceleration, cross-source divergence, novelty, and confidence scores are calculated in integer basis points ($0 \dots 10000$ bps) or micros ($0 \dots 1000000$).
4. **Corroboration Multiplicity:** Multiplicity must track raw mentions vs independent root domains to prevent syndicated mirror score inflation.

## 3. Output Schema
```json
{
  "signal_id": "sig_uuid7",
  "cluster_id": "kcl_uuid7",
  "topic": "Normalized Topic",
  "entities": ["EntityA", "EntityB"],
  "temporal_window": {
    "start_utc": "2026-08-01T00:00:00Z",
    "end_utc": "2026-08-31T00:00:00Z"
  },
  "velocity_micros": 850000,
  "acceleration_micros": 600000,
  "divergence_micros": 250000,
  "novelty_micros": 900000,
  "confidence_micros": 950000,
  "evidence_excerpt": "Verbatim evidence snippet",
  "source_multiplicity": {
    "raw_mention_count": 3,
    "unique_root_domain_count": 3,
    "independent_source_count": 3,
    "syndication_ratio_bps": 0
  }
}
```
