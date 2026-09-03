---
name: caebmad-product-brief
description: Synthesizes research lineage and operator intent into authoritative Product Briefs with explicit non-goals and success metrics.
version: 0.3.0-rebuild
agent: cae-product-brief-agent
---

# Skill: caebmad-product-brief

## 1. Purpose & Invocation
The `caebmad-product-brief` skill enables the `cae-product-brief-agent` to author, validate, and maintain canonical Product Briefs at `Level 01: PRODUCT / INTENT`.

## 2. Invocation Preconditions
1. Product Reconstruction record available.
2. Decision Ledger accessible.
3. Schema `schemas/product_brief.schema.json` loaded.

## 3. Execution Logic
1. **Intent Formulation:** Extract product vision, market problem, and core value proposition.
2. **Pillar Alignment:** Map against the 5 Core Capability Pillars.
3. **Non-Goals Articulation:** Define hard negative boundaries to prevent scope creep.
4. **Deliverable Emission:** Assemble `docs/cae-bmad/03_product/PRODUCT_BRIEF.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/03_product/PRODUCT_BRIEF.json`
- `docs/cae-bmad/03_product/PRODUCT_BRIEF.md`
