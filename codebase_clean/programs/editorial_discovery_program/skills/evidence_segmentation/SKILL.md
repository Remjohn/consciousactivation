---
name: evidence_segmentation
description: Ingests raw authenticated dialogue turns and performs lossless segmentation into EvidenceSegment objects with monotonic timecodes and SHA-256 integrity hashes.
version: 1.0.0
lane: HUNTER
inputs:
  - raw_turns
  - session_id
  - workspace_id
outputs:
  - evidence_segments
maturity: PRODUCTION_READY
---

# Evidence Segmentation Canonical Skill

## 1. Operational Scope
Governed by CAE Mandate M35 and CAE-M05.
Executed exclusively in the **HUNTER** lane.
Converts raw timed speech turns from an authenticated interview session into discrete `EvidenceSegment` units.

## 2. Invariants
- **Lossless Ingestion**: No words or timestamps are dropped or modified.
- **Monotonic Timecodes**: Segment boundaries must satisfy $start\_time\_ms \le end\_time\_ms$.
- **Cryptographic Hash**: Each segment must calculate `text_sha256 = SHA256(verbatim_text)`.
- **Thought Completion**: Boundary type classification (`COMPLETE_THOUGHT`, `PARTIAL_THOUGHT`, etc.) is recorded without modifying verbatim text.
