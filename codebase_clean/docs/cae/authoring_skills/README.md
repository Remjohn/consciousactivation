# CAE Authoring Control Skills Suite

**Status:** `DEVELOPMENT_UNCERTIFIED`  
**Phase ID:** `CA-AUTH-01`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/03_CA_AUTH_01_AUTHORING_CONTROLS_MANDATE.md`  
**Authority Reference:** CAE Governance & Specification Bridge Bundle v3; Phase 0 Object Constitution Protocol; CA-MAP-01 Scope & Authority Matrix  

---

## 1. Purpose & Scope

The CAE Authoring Control Skills suite provides bounded, repeatable, auditable authoring and review procedures for downstream Conscious Activation Engine specifications, object constitutions, traceability matrices, state migration contracts, Tech Specs, and reality-contact proofs.

### Critical Boundary Distinctions
- **Procedure vs Artifact:** An authoring Skill is a procedure for authoring/reviewing an artifact. It is NOT the artifact it produces.
- **Procedure vs Authority:** An authoring Skill owns zero ontology authority, zero database schemas, zero runtime semantic operations, and zero implementation licenses.
- **Constitution vs Skill:** An Object Constitution is the versioned law of a canonical object. A Skill is the controlled protocol for drafting or evaluating that constitution.
- **Maturity:** Every package in this suite is explicitly classified as `development_uncertified`. None of these skills are production-certified compilers or runtime capabilities.

---

## 2. Authoring Skills Inventory

| Skill Package | Role & Bounded Function | Primary Input | Primary Output | Gate Enforcement |
|---|---|---|---|---|
| [`cae_scope_authority_mapper`](cae_scope_authority_mapper/) | Maps & validates plane, scope, 3 authority axes, parent chains, and write boundaries. | Candidate Object Proposal | Scope & Authority Mapping Record | Tenancy & Authority Invariants |
| [`cae_object_constitution_author`](cae_object_constitution_author/) | Routes candidate to 1 primary class grammar; authors 26-dimension constitution. | Ratified Scope Mapping | 26-Dimension Object Constitution | 26-Dimension Completeness |
| [`cae_constitution_collision_reviewer`](cae_constitution_collision_reviewer/) | Independently challenges candidate constitutions across 9 collision vectors. | Candidate Constitution | Collision Review Verdict & Register Entry | Independent Anti-Conflation Gate |
| [`cae_requirement_traceability_author`](cae_requirement_traceability_author/) | Converts ratified constitutions into PRD/FR traceability records with transitions & operations. | Ratified Constitution | PRD/FR Traceability Matrix | Zero-Orphan Requirement Law |
| [`cae_state_migration_contract_author`](cae_state_migration_contract_author/) | Drafts single-aggregate 5-state migration contracts; strictly prohibits backfill execution. | Ratified Entity/State Model | State Migration Contract | Zero-Data-Movement Rule |
| [`cae_tech_spec_gate_reviewer`](cae_tech_spec_gate_reviewer/) | Reviews implementation Tech Specs against Gates A–I and state control invariants. | Draft Tech Spec | Gate A–I Compliance Audit Receipt | Non-Waivable Gate Law |
| [`cae_reality_contact_proof_author`](cae_reality_contact_proof_author/) | Formulates E1–E4 evaluation suites, receipts, countertests, and explicit non-claims. | Implementation / Test Plan | Reality-Contact Evaluation Suite | Anti-Reward-Hacking & Non-Claims |

*(Note: `cae_execution_mandate_compiler` is explicitly deferred as authoring tooling is focused on the core 7 control packages).*

---

## 3. Package Structure Standard

Every authoring skill directory contains the following six mandatory files:
1. `SKILL.md` — Purpose, lane, authority, inputs, procedure, outputs, prohibitions, escalation, and stop conditions.
2. `manifest.yaml` — Stable ID, version `0.1.0`, maturity `development_uncertified`, owner, dependencies, and allowed consumers.
3. `input_schema.yaml` — Bounded typed schema for procedure inputs (no loose prose buckets).
4. `output_schema.yaml` — Bounded typed schema for procedure outputs.
5. `evaluation.yaml` — Structural test fixtures, positive anchors, deceptive negatives, expected verdicts, and fidelity statement.
6. `receipt_schema.yaml` — Typed execution receipt capturing inputs, author/reviewer identities, tool versions, validation status, and unresolved questions.
7. `references.md` — Explicit references to governing Bundle v3 protocols and CA-MAP-01 mappings.

---

## 4. Verification & Testing

All authoring controls are statically validated via `scripts/cae/authoring/verify_authoring_skills.py`, which executes structural assertions and deceptive negative fixture evaluations to ensure false or conflicting proposals are deterministically rejected.
