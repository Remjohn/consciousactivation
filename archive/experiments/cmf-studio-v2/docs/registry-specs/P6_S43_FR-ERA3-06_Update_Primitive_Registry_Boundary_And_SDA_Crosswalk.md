# Spec Prompt: FR-ERA3-06 — UPDATE: Primitive Registry Boundary and SDA Crosswalk

> **READY TO PASTE — SPEC UPDATE.** Copy into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:          FR-ERA3-06
SPEC_TITLE:       UPDATE: Primitive Registry Boundary and SDA Crosswalk
PHASE:            6 — Existing Spec Updates
SOURCE_PRD:       PRD-08, PRD-02
EXISTING_FILE:    docs/architecture/april_updates/FR-ERA3-06_Primitive_Registry_Query_Service_Tech_Spec.md
OUTPUT_FILE:      docs/architecture/april_updates/FR-ERA3-06_Primitive_Registry_Query_Service_Tech_Spec_UPDATED.md
```

## CHANGES REQUIRED

Update the primitive registry spec so it explicitly preserves the Primitive Registry boundary after Wave 0. The revised spec must:

- state clearly that SDA artifacts are sibling infrastructure, not new primitive families
- define the integration seam with FR-ERA3-21 SDA Query and Crosswalk Service
- specify which lookups remain primitive-native versus crosswalk-mediated
- preserve ADR-05 and dual-source validation without turning the primitive registry into a generic semantic warehouse

Do not merge or duplicate SDA ontology into the primitive registry schemas.

> [!IMPORTANT]
> **MANDATORY SDA SOURCE SET — READ IN EVERY SDA SPEC SESSION:**
> - `lab/semantic_discernment_architecture_content_engine_v_1.md`
> - `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. This is an UPDATE to an EXISTING spec, not a new spec. Your output is a revised version of the existing file with targeted changes applied.

---

## MANDATORY PRE-WORK

1. Read the EXISTING SPEC FILE listed in `EXISTING_FILE`.
2. Read the Master Protocol.
3. Read `PRD-08` and `PRD-02`, including the Wave 0 SDA additions.
4. Read the full mandatory SDA source set listed above.
5. **PROOF:** Quote the exact section in the existing spec that needs a boundary clarification now that SDA exists.

---

## UPDATE FORMAT

Output the COMPLETE revised spec file. Do NOT output just the changed sections — output the whole file.
Mark all changed sections with `<!-- UPDATED: [reason] -->` HTML comments so changes are traceable.
Do NOT change anything outside the `CHANGES_REQUIRED` scope listed above.

## REJECTION

Collapsing SDA into the primitive registry | Breaking existing ADR-05 logic | No crosswalk seam | No explicit primitive-native vs crosswalk-mediated boundary

**Write the revised spec. No permission needed.**
