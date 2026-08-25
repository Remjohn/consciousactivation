# CAE Requirement Traceability Author Skill

**Skill ID:** `cae_requirement_traceability_author`  
**Maturity:** `development_uncertified`  
**Authority:** Procedural control only; operates under Bundle v3 Object-to-Spec Traceability Protocol (`03_CAE_OBJECT_TO_SPEC_TRACEABILITY_PROTOCOL.md`).  

---

## 1. Purpose & Traceability Laws

The `cae_requirement_traceability_author` converts ratified object constitutions into strict Product Requirement Document (PRD) and Functional Requirement (FR) traceability matrices.

### Core Traceability Laws
1. **Zero-Orphan Requirement Law:** Every functional requirement MUST trace to at least one ratified Object Constitution. Unratified or candidate concepts cannot become requirements.
2. **Transition & Operation Completeness:** Every stateful requirement MUST bind to explicit state transitions (`from_state -> to_state`), typed semantic operations, and error codes.
3. **Evidence & False-Proof Requirement:** Every requirement MUST declare required evidence items, test class/fidelity (E1–E4), and explicit anti-reward-hacking/false-proof countertests.
4. **No Implementation Licensing:** A traceability record authorizes specification completeness only; it does not authorize runtime coding or data cutover.

---

## 2. Inputs & Preconditions

- Input MUST conform to `input_schema.yaml`.
- Requires ratified Object Constitution and collision review approval receipt (`cae_constitution_collision_reviewer`).
- Requires requirement ID, title, narrative description, and target functional slice.

---

## 3. Procedure

1. **Validate Constitutional Provenance:** Confirm the referenced constitution has an approved collision review receipt and is ratified.
2. **Derive Functional Requirement (FR) Blocks:**
   - Map functional scope to specific constitutional dimensions (Attributes, Relations, State Model, Operations).
   - Formulate unambiguous acceptance criteria (`SHALL`/`MUST`).
3. **Bind State Transitions & Operations:**
   - Specify triggering semantic operation.
   - Define exact `(from_state, to_state)` transition and expected version lock.
   - Enforce mandatory error taxonomy mapping.
4. **Formulate Verification & False-Proof Contract:**
   - Define required evidence anchors and receipts.
   - Assign test class and fidelity level (`E1_STATIC`, `E2_REPOSITORY_FIXTURE`, `E3_STAGING_PERSISTENCE`, `E4_PRODUCTION_RUNTIME`).
   - Define at least one deceptive false-proof or reward-hacking risk with a countertest.
5. **Emit Traceability Matrix & Receipt:** Output structured requirement record conforming to `output_schema.yaml`.

---

## 4. Prohibitions

- MUST NOT create requirements for unratified or candidate object models.
- MUST NOT emit a stateful requirement without an explicit state transition contract.
- MUST NOT omit error codes, evidence expectations, or false-proof analysis.
- MUST NOT claim that requirement definition constitutes implementation verification.

---

## 5. Escalation & Stop Conditions

- **Stop as `REJECTED_ORPHAN_REQUIREMENT`:** If referenced object constitution is unratified or absent.
- **Stop as `REJECTED_INCOMPLETE_TRACEABILITY`:** If state transitions, operations, errors, or countertests are missing.
