---
name: caebmad-research
description: Governs the intake, scoring, indexing, and validation of the 216-source research corpus.
version: 0.3.0-rebuild
agent: cae-product-reconstructor
---

# Skill: caebmad-research

## 1. Purpose & Invocation
The `caebmad-research` skill ingests, scores, and maintains the 216-source research library. It validates source provenance, scores relevance (0–100), tags authority classes, and verifies that no source is cited without reality inspection.

## 2. Invocation Preconditions
1. Research corpus catalog present or being initialized.
2. `schemas/research_source.schema.json` and `schemas/research_library.schema.json` active.

## 3. Execution Logic
1. **Catalog Ingestion:** Execute `scripts/intake_research_corpus.py` to index the 216 sources.
2. **Schema & Integrity Validation:** Run `scripts/validate_research_corpus.py` to verify score bounds, authority enums, and path reachability.
3. **Source Lineage Card Generation:** When detailed investigation of a single source is requested, author a source card using `templates/source_lineage_card.md`.
4. **Research Coverage Gate Check:** Verify that downstream product planning has cited at least the 100-relevance foundation sources before PRD compilation.

## 4. Output Contract
- `.caebmad/research/CAE_RESEARCH_LIBRARY.yaml`
- `.caebmad/research/CAE_RESEARCH_LIBRARY_216.md`
- Source audit and validation reports
