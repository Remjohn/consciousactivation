---
name: authenticated_evidence_packager
description: Passive, flat Canonical Skill for assembling authenticated evidence packages with cryptographic 6-link lineage.
version: 1.0.0
authority_lane: COMPOSER
---

# Authenticated Evidence Packager Skill (COMPOSER)

## Purpose
Governs the compilation and synthesis of accepted interview evidence into structured downstream content candidates and sealed evidence packages.

## Invariants & Rules
- **Flat Skill**: Passive instruction set; no direct storage mutation or self-invoking tools.
- **6-Link Lineage Survival**:
  - Every downstream content candidate MUST maintain a verifiable cryptographic link chain:
    `upstream hypothesis refs` -> `question candidate` -> `question attempt` -> `source ref (transcript SHA-256)` -> `observation` -> `accepted evidence ref` -> `downstream candidate ref`.
- **Source Sovereignty**:
  - Guest spoken evidence cannot be rewritten, sanitized, or substituted with synthetic claims.
- **Archetype & Format Verification**:
  - Evaluate narrative role (`ARCH-CRUCIBLE`, `ARCH-INVESTIGATIVE`, etc.) and structural response criteria before candidate packaging.
