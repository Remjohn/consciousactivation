---
name: caebmad-product-reconstruction
description: Reconstructs product architecture, lineage, and domain capabilities from the 216-source research corpus without flattening historical sources.
version: 0.3.0-rebuild
agent: cae-product-reconstructor
---

# Skill: caebmad-product-reconstruction

## 1. Purpose & Invocation
The `caebmad-product-reconstruction` skill synthesizes product truth, historical lineage (CCP/CCF/CMF), and current runtime capabilities from the 216-source research corpus. Use this skill at the beginning of product planning or when legacy capabilities must be understood and mapped to modern architectures.

## 2. Invocation Preconditions
1. Research library loaded from `.caebmad/research/CAE_RESEARCH_LIBRARY.yaml` (216 sources validated).
2. Workspace brownfield directories (`governance/`, `services/`, `packages/`, `Conscious Activation Engine Brownfield/`) accessible.
3. Anti-flattening invariants acknowledged.

## 3. Execution Logic
1. **Source Scanning & Scoring:** Evaluate source relevance (0–100) and authority rank across the 8 research categories.
2. **Lineage Tracing:** Map CCP, CMF, CCF, and Atomic Harness concepts to modern CAE constructs without erasing historical names.
3. **Reality Crosswalk:** Compare historical specifications against active Python and TypeScript runtimes to detect implemented vs missing capabilities.
4. **Contradiction Logging:** Record any divergences between historical PRDs and modern runtime implementations in the Contradiction Register.
5. **Reconstruction Record Assembly:** Author `docs/cae-bmad/01_reconstruction/PRODUCT_RECONSTRUCTION.md` using `templates/product_reconstruction.md`.

## 4. Output Contract
- `docs/cae-bmad/01_reconstruction/PRODUCT_RECONSTRUCTION.md`
- Source lineage crosswalk tables
- Lineage gap and contradiction listings
