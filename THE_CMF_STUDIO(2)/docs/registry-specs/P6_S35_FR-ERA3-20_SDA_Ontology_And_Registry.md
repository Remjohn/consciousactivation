# Spec Prompt: FR-ERA3-20 — SDA Ontology and Registry

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-20
SPEC_TITLE:      SDA Ontology and Registry
PHASE:           6 — SDA Foundation
SOURCE_PRD:      PRD-01, PRD-02, PRD-08
MAPPED_STORIES:  Wave0 SDA Adoption — PRD-01 §3.4 + §1.5, PRD-02 SDA packet/runtime adoption, PRD-08 §3.6 Primitive/SDA separation
CBAR_MANDATES:   Anti-Centroid Law preservation, ADR-05 primitive traceability, SDA No-False-Registry Rule, Role-before-Schema Rule, Canonical-vs-Derived Separation Rule, Scalar Separation Rule
BACKEND_REL:     NEW sibling registry stack — MUST remain separate from FR-ERA3-06 Primitive Registry Query Service, but interoperable with it via future crosswalks
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is the canonical source-of-truth spec for the SDA artifact substrate. It must define what is a canonical registry object, what is a structural grammar object, what is a runtime-derived object, and what is explicitly NOT a registry. The spec must hard-protect the distinction between:
> - `Existential Invariants`
> - `Representation Geometries`
> - `Archetypal Geometries`
> - `Species Composition Grammar`
> - runtime semantic dynamics
> - adversarial evaluation assets
>
> Hard rule: do **not** collapse all SDA artifacts into one flat registry abstraction.

> [!IMPORTANT]
> **MANDATORY SDA SOURCE SET — READ IN EVERY SDA SPEC SESSION:**
> - `lab/semantic_discernment_architecture_content_engine_v_1.md`
> - `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`

> [!WARNING]
> **TRACEABILITY NOTE:**
> There is no dedicated Phase 6 epic file yet. For this spec, Step 3 of the normal prompt flow is replaced by the Wave 0 PRD additions listed in `MAPPED_STORIES` plus the mandatory SDA source set above. In Section 3.4, use `SDA Governance Constraints` if no formal `PhaseX-M#` mandate exists.

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` — §2 backend, §3 Pre-Flight, §4 Format
2. Source PRDs: `PRD-01`, `PRD-02`, `PRD-08` — especially the new SDA sections added in Wave 0. **PROOF:** Quote the exact Wave 0 SDA adoption lines.
3. SDA source set: all 4 mandatory SDA docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing registry/backend references: read `src/ccp/services/` and `src/ccp/models/` files relevant to existing registry patterns, especially anything used by FR-ERA3-06. **PROOF:** Quote real method signatures.
5. Primitive YAMLs: read at least 2 experience YAMLs and 2 meaning YAMLs to preserve ADR-05 traceability expectations. **PROOF:** Quote `id:` + `name:`. **BANNED:** `EXP-TRB-*`.
6. Existing test patterns: read 2 `tests/integration/` files that cover registry or service query patterns.
7. Existing April SDA-aware PRDs: confirm how PRD-01/02/08 distinguish ontology, runtime packets, and operator layers.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (≥8) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (≥3 files) | §3.3 Primitives / SDA artifacts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (≥4 phases, ≥12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `ExistentialInvariant`
  - `RepresentationGeometry`
  - `ArchetypalGeometry`
  - `SpeciesCompositionGrammar`
- Explicitly define which SDA artifacts are **derived**, **runtime**, **policy**, or **adversarial assets**
- Include `Invariant Gravity`, `Invariant Activation Intensity`, and `Invariant Resonance Multiplier`
- Ban false flattening of:
  - `HardNegative`
  - `RecursivePattern`
  - `EmergentContextualInvariant`
  - `FeedbackLoop`
  into canonical registry rows if they are not supposed to live there
- Define versioning, provenance, and queryability expectations
- Preserve clean separation from the Primitive Registry while allowing future crosswalks

**REJECTION:** Treating all SDA artifacts as one registry | No scalar separation | No role-before-schema logic | No failure examples | Invented method signatures | EXP-TRB-* | Missing provenance/versioning | Generic testing

**Write the pre-work log. Then write the spec. No permission needed.**
