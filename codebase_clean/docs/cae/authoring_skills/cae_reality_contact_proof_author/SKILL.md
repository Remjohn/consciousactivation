# CAE Reality-Contact Proof Author Skill

**Skill ID:** `cae_reality_contact_proof_author`  
**Maturity:** `development_uncertified`  
**Authority:** Procedural control only; operates under Bundle v3 Reality-Contact & Proof Protocol (`21_CAE_STATE_CONTROL_TEST_AND_PROOF_PROTOCOL.md`).  

---

## 1. Purpose & Reality-Contact Laws

The `cae_reality_contact_proof_author` specifies evidence-bearing evaluation suites, reality-contact countertests, receipt validation, and explicit claim/non-claim boundaries for CAE implementation packages.

### Core Reality-Contact Laws
1. **Four-Tier Fidelity Hierarchy:** Test evidence MUST be strictly classified by execution tier:
   - `E1_STATIC`: Schema, lint, and static contract analysis.
   - `E2_REPOSITORY_FIXTURE`: In-memory and local SQLite/filesystem repository tests.
   - `E3_STAGING_PERSISTENCE`: Live staging PostgreSQL/Storage execution with forced transaction rollback and complete bucket cleanup.
   - `E4_PRODUCTION_RUNTIME`: Live production tenant traffic under full operational governance.
2. **Anti-False-Proof Law:** Passing an E1, E2, or E3 test suite NEVER constitutes proof of E4 real-world effectiveness, human truth, semantic taste, or production safety.
3. **Mandatory Explicit Non-Claims:** Every evaluation suite MUST state explicit non-claims regarding human semantic discernment, taste, anti-centroid integrity, or unproven world outcomes.
4. **Mandatory Adversarial Countertests:** Every positive evaluation claim MUST be paired with an adversarial countertest (e.g. testing for self-attestation, fake token passing, cached payload bypass).

---

## 2. Inputs & Preconditions

- Input MUST conform to `input_schema.yaml`.
- Requires implementation work package ID, tested claims, proposed test fidelity, and countertest definitions.

---

## 3. Procedure

1. **Ingest Evaluation Claims:** Parse claims made by the implementation package.
2. **Assign Strict Fidelity Tier:** Bind each claim to its exact evidence tier (`E1_STATIC`, `E2_REPOSITORY_FIXTURE`, `E3_STAGING_PERSISTENCE`, `E4_PRODUCTION_RUNTIME`).
3. **Formulate Anti-Reward-Hacking Countertests:**
   - Define adversarial failure cases (e.g. corrupt hash, denied RLS actor, unauthenticated span, manipulated receipt).
   - Ensure tests fail deterministically when invariants are violated.
4. **Draft Mandatory Non-Claims Section:**
   - Record explicit boundaries on what the test suite DOES NOT prove.
5. **Enforce Post-Execution Cleanup Contracts:**
   - For E3 tests: specify forced rollback and storage bucket object deletion checks.
6. **Emit Evaluation Suite & Receipt:** Output structured evaluation suite conforming to `output_schema.yaml`.

---

## 4. Prohibitions

- MUST NOT label synthetic or staging test success as real-world / human semantic proof.
- MUST NOT emit an evaluation suite without explicit non-claims.
- MUST NOT emit positive test claims without paired adversarial countertests.
- MUST NOT allow retained test data to pollute staging or production environments.

---

## 5. Escalation & Stop Conditions

- **Stop as `REJECTED_FALSE_REALITY_CLAIM`:** If a test suite attempts to claim human taste or production outcome from synthetic/staging execution.
- **Stop as `REJECTED_MISSING_COUNTERTESTS`:** If positive claims lack deceptive negative test cases.
