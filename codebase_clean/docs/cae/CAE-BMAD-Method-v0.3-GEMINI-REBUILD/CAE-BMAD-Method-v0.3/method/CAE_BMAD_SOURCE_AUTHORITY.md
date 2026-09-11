# CAE-BMAD Source Authority Framework

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL FRAMEWORK  
**Authority:** CAE Rebuild Program / Operator Mandate M01  
**Scope:** Research corpus governance, source scoring, authority classification, and truth precedence.

---

## 1. Research Corpus Target (216 Sources)

The method is grounded in an explicit 216-source research corpus:
- **Baseline Corpus (144 Sources):** Cataloged in `docs/cae/CAE_Research_Library_144.md`, covering historical CCP/CCF/CMF lineages, foundational PRDs, technical specifications, evaluations, runbooks, and programs.
- **Extended Corpus (72 Sources):** Additional high-relevance architectural records, cross-repo contracts, visual syntax specifications, and operator interview transcripts required to achieve full 216-source coverage.

---

## 2. Source Scoring and Authority Matrix

Every source analyzed in the research phase is classified along two orthogonal axes: **Relevance Score (0–100)** and **Authority Class**.

### 2.1 Relevance Scoring Standard
- **100:** Indispensable / Foundation Canon (e.g. Current canonical PRD, Core Constitution).
- **90–99:** Major Architecture & Lineage (e.g. Editorial Authority Matrix, Brownfield Reality Map).
- **80–89:** Major Supporting Source (e.g. Vertical Slice Tech Specs, Evaluation Suites).
- **70–79:** Important Supporting Context (e.g. Authoring skills, interview transcripts).
- **60–69:** Specialist / Historical Reference (e.g. Archive transcripts, background notes).
- **<60:** Incidental / Contextual only.

### 2.2 Authority Classes and Precedence

When sources conflict, precedence is resolved according to the authority hierarchy:

```text
Rank 1: OPERATOR_DECISION
  - Explicit recorded decisions ratified by the human operator in the Decision Ledger.
Rank 2: CURRENT
  - Active, verified repository code, active constitutions, and current canonical specs.
Rank 3: HISTORICAL
  - Legacy specifications, brownfield code, and archived milestone designs (must be crosswalked).
Rank 4: TRANSCRIPT
  - Historical interview transcripts and conversational records (require confirmation).
Rank 5: REFERENCE
  - External methodology documents, upstream BMAD templates, and theoretical frameworks.
```

---

## 3. Truth Invariants

1. **No Implicit Authority:** A high relevance score does not grant constitutional authority. An 80-score `CURRENT` runtime contract supersedes a 95-score `HISTORICAL` concept unless explicitly overridden by an `OPERATOR_DECISION`.
2. **Provenance Trace:** Every claim in a Product Brief, PRD, or Architecture document must cite the exact `source_id`, path, and authority class of its foundation source.
