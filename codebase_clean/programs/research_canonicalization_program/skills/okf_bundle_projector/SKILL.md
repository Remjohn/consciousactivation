---
name: okf_bundle_projector
description: Passive flat skill for compiling canonical knowledge nodes into Open Knowledge Format (OKF) Markdown bundles and catalog indexes.
version: 1.0.0
lane: COMPOSER
---

# OKF Bundle Projector Skill

## Role & Invariants
- Operates strictly under the **COMPOSER** lane.
- Compiles `CanonicalKnowledgeNode` entities into Open Knowledge Format (OKF) Markdown files with standardized YAML frontmatter.
- Formats frontmatter with `cmf-okf-research-knowledge-1.0` profile metadata and typed relationship edges.
- Generates catalog `index.md` and deterministic composite bundle SHA-256 digest.
- Passive and flat: invokes no sub-skills or downstream services.
