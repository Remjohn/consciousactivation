---
name: editorial_candidate_composition
description: Assembles grounded ContentCandidate units by linking authenticated EvidenceSegments with CMF multidimensional scoring and narrative arcs.
version: 1.0.0
lane: COMPOSER
inputs:
  - evidence_links
  - candidate_type
  - title
  - hook_statement
  - cmf_scores
outputs:
  - content_candidate
maturity: PRODUCTION_READY
---

# Editorial Candidate Composition Canonical Skill

## 1. Operational Scope
Governed by CAE Mandate M35 and CAE-M07.
Executed exclusively in the **COMPOSER** lane.
Constructs `ContentCandidate` entities representing potential narrative assets.

## 2. Invariants
- **Grounding Requirement**: Every candidate must have non-empty `evidence_links` mapped to valid `EvidenceSegment` IDs and SHA-256 hashes in the authoritative store.
- **CMF Dimension Scoring**: Scores (emotional resonance, cognitive novelty, authority evidence, narrative velocity) are calculated and stored in integer basis points (`_bps`).
- **Production Status**: Newly composed candidates start in `DRAFT_CANDIDATE` and can only transition to production via Commander operator gates.
