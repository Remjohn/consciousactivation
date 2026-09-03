# CAE-BMAD Research Intake and Lineage Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Operator Mandate M02  
**Scope:** Ingestion, scoring, lineage tracking, truth classification, and falsification rules for the 216-source research corpus.

---

## 1. Objective and Anti-Flattening Principle

The primary objective of the **216-Source Research Intake and Lineage System** is to provide an uncompromised, governed knowledge base for the entire CAE-BMAD product reconstruction and planning lifecycle.

### The Anti-Flattening Principle
Historical documents must **never** be flattened into generic, modern summaries that erase original context, terminology, or design rationale.
- **CCP Lineage:** Preserves conscious platform concepts, conscious reactions, mini-apps, and modular PRD structures.
- **CMF Lineage:** Preserves conscious media framework concepts, mood states, subliminal functions, and experience primitive registries.
- **CCF Lineage:** Preserves conscious content factory workflows, trigger-first engines, and automated editorial pipelines.
- **Atomic Harnesses & Visual Syntax:** Preserves visual grammar tokens, storyboard models, and execution harnesses.
- **Runtime Truth:** Maps abstract intents directly against active Python (`ca_runtime`, `services/`) and TypeScript codebases.

---

## 2. The 216-Source Corpus Structure

The 216 sources are partitioned into 8 governed research categories:

| Category ID | Category Name | Source Count | Relevance Range | Primary Lineage |
|---|---|---|---|---|
| `CAT-01` | Product Truth & Canonical Specifications | 36 sources | 90–100 | `CAE_CANON` |
| `CAT-02` | Programs & Operator Product Models | 26 sources | 88–99 | `CAE_CANON` |
| `CAT-03` | Runtime, Agent & Workflow Primitives | 28 sources | 88–96 | `CAE_CANON` |
| `CAT-04` | Constitutions & Canonical Domain Models | 32 sources | 91–100 | `CAE_CANON` |
| `CAT-05` | Brownfield Formation & Evolution Waves | 22 sources | 90–99 | `CAE_CANON` / `HISTORICAL` |
| `CAT-06` | CMF & Subliminal Intelligence Ancestry | 20 sources | 95–98 | `CMF_LINEAGE` / `CCP_LINEAGE` |
| `CAT-07` | CCP Product, PRD & Architecture Lineage | 26 sources | 95–100 | `CCP_LINEAGE` |
| `CAT-08` | Historical Transcripts & External Methods | 26 sources | 85–95 | `TRANSCRIPT` / `BMAD_UPSTREAM` |
| **Total** | **Governed Corpus Target** | **216 sources** | **0–100** | **Comprehensive Lineage** |

---

## 3. Ingestion and Verification Protocol

When intake is performed on any research source:
1. **Source Discovery & Path Verification:** Verify that the declared relative file path exists on disk or in the mounted archive snapshot.
2. **Provenance & Attribution Extraction:** Extract the historical contributor, creation date, and architectural context.
3. **Relevance Scoring:** Assign a relevance score between 0 and 100 based strictly on product/architecture impact:
   - `100`: Indispensable foundational canon.
   - `90–99`: Major architectural and product lineage.
   - `80–89`: Major supporting technical/evaluation source.
   - `70–79`: Important contextual and operational source.
   - `<70`: Specialist or historical reference.
4. **Authority Classification:** Assign one of the 5 authority ranks (`OPERATOR_DECISION`, `CURRENT`, `HISTORICAL`, `TRANSCRIPT`, `REFERENCE`).
5. **Truth Status Tagging:** Assign the appropriate status tag (`KNOWN`, `INHERITED`, `VERIFIED`, `PROPOSED`, `INFERRED`, `MISSING`, `CONTRADICTED`, `DEPRECATED`).
6. **Lineage Crosswalk Binding:** Explicitly record what modern CAE capability this source informs or influences.

---

## 4. Falsification and Contradiction Rules

1. **Source Falsification:** A claim extracted from a source is falsified if an active, passing runtime test proves the codebase behaves differently. In such cases, the source claim is tagged `CONTRADICTED` or `DEPRECATED` and logged in `CAE_EDITORIAL_CONTRADICTION_REGISTER.md`.
2. **Lineage Loss Rejection:** If an agent attempts to author a PRD or architecture artifact that silently ignores a 90+ relevance historical source without citing it or documenting an intentional deprecation, the deliverable must be rejected at the phase gate with error code `TRACEABILITY_BROKEN`.
