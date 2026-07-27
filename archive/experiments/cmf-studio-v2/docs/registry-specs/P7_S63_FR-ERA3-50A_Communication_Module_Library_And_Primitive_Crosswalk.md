# Spec Prompt: FR-ERA3-50A â€” Communication Module Library And Primitive Crosswalk

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-50A
SPEC_TITLE:      Communication Module Library And Primitive Crosswalk
PHASE:           7 â€” Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-08 (Conscious Primitives), PRD-02 (CCF)
MAPPED_STORIES:  Canonical communication module registry, primitive crosswalk mappings, fixed skill contracts with input/output/anti-pattern definitions, module-to-archetype routing, evaluator hook registration
CBAR_MANDATES:   Fixed-Skill-Contract Rule, Crosswalk-Not-Duplication Rule, Registry-Routing-Separation Rule, No-Flat-Persuasion-List Rule
BACKEND_REL:     NEW canonical registry â€” MUST interoperate with Primitive Registry (FR-ERA3-06), SDA Ontology (FR-ERA3-20), SFL (FR-ERA3-25), SFL Query (FR-ERA3-26) without duplicating ontology ownership
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-50A_Communication_Module_Library_And_Primitive_Crosswalk_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the canonical communication module library â€” the fixed skill contracts that the Persuasive Speaking Program and Transformational Webinar Program operate on.
>
> Critical architectural discipline from the Roadmap (Â§4.2â€“4.3):
> - **Fixed skills** = stable named modules with clear jobs and delivery expectations
> - **Registries/crosswalks** = routing substrate (module-to-primitive, module-to-archetype, module-to-format, etc.)
> - **Recipes** = reusable delivery patterns beneath fixed skills (separate spec: FR-ERA3-50C)
> - **Evaluators** = scoring layer (separate spec: FR-ERA3-50D)
> - **Memory banks** = expressive material store (separate spec: FR-ERA3-50E)
>
> Hard rule: do NOT flatten everything into one giant list of persuasion concepts.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (10+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Remotion mandate)
> - `docs/architecture/april_updates/FR-ERA3-06_Primitive_Registry_Query_Service_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-26_Subliminal_Function_Query_And_Profile_Service_Tech_Spec.md`
> - `reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md` (PRD Module)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-08`. **PROOF:** Quote lines on primitive registry boundaries and content intelligence ownership.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote references to primitive activation and subliminal functions mapping in the unified assembling pipeline.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the communication module ontology split (Roadmap Â§4.2â€“4.3) and the primitive-to-module alignment examples (Source of Truth Â§7.2â€“7.3).
5. Existing registries: read FR-ERA3-06, FR-ERA3-20, FR-ERA3-25. **PROOF:** Quote how each separates canonical, runtime, policy, and adversarial assets.
6. Existing primitives YAMLs: read experience YAMLs and meaning YAMLs. **PROOF:** Quote `id:` + `name:`.
7. Existing backend: read real registry service files. **PROOF:** Quote real method signatures.
7. Existing test patterns: read 2 `tests/integration/` files covering registry or query patterns.

**PRE-WORK LOG â€” required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 350 LINES

Â§1 Files Read (>=8) | Â§2 Overview | Â§3.1 DEP-IDs | Â§3.2 Backend (>=4 files) | Â§3.3 Module library contracts | Â§3.4 Governance Constraints | Â§3.5 Technical Decisions | Â§4 Plan (>=4 phases, >=14 tasks) | Â§5 Schema (Pydantic v2, no Any) | Â§6 Fallback | Â§7 Tasks | Â§8 AC (with FAILURE EXAMPLE) | Â§9 Dependencies | Â§10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define the canonical fixed skills as schemas:
  - `CommunicationModule` â€” base model: id, name, job_description, input_conditions, expected_audience_effects, delivery_notes, anti_patterns, scoring_hooks, primitive_coalition
- Define the full module inventory:
  - Authority, Positioning, Identification, Commitment, Micro-Commitment, Proof Stack, Testimonial Deployment, Objection Softening, Objection Smashing, Hope, Intrigue, Transition, Story Arc, Humor Relief, Permission to be Seen, Contextual Explanation, Two-Choice Close
- Each module must have:
  - input conditions (when to use)
  - expected audience effects (what it does psychologically)
  - delivery notes (how to carry it)
  - anti-patterns (what makes it fail)
  - scoring hooks (how evaluators judge it)
- Define crosswalk schemas:
  - `ModuleToPrimitiveCrosswalk` â€” maps each module to its primitive coalition (e.g., Humor â†’ HUM, VOC, SOC)
  - `ModuleToArchetypeCrosswalk` â€” maps modules to archetypes they dominate
  - `ModuleToFormatCrosswalk` â€” maps modules to Living Commentary format families
  - `ModuleToAudienceStateCrosswalk` â€” maps modules to audience readiness states
  - `ModuleToRiskSurfaceCrosswalk` â€” maps modules to their failure/risk surfaces

**REJECTION:** Flat list of persuasion concepts | no crosswalk discipline | no input/output contracts per skill | skills duplicate primitive ownership | no anti-patterns | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**

