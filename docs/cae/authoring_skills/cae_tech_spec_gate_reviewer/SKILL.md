# CAE Tech Spec Gate Reviewer Skill

**Skill ID:** `cae_tech_spec_gate_reviewer`  
**Maturity:** `development_uncertified`  
**Authority:** Procedural audit control only; operates under Bundle v3 Implementation Gate Protocol (`08_CAE_IMPLEMENTATION_GATE.md`) and Tech Spec Protocol (`02_CAE_TECH_SPEC_WRITING_PROTOCOL.md`).  

---

## 1. Purpose & Non-Waivable Gate Laws

The `cae_tech_spec_gate_reviewer` provides a rigorous audit procedure to review an implementation-authorizing Tech Spec against Gates A through I before any engineering or coding phase is authorized.

### Non-Waivable Gate Laws
1. **Zero-Waiver Law:** No implementation gate (A through I) may be waived, bypassed, or deferred to runtime.
2. **Mandatory Storage & RLS Isolation:** Any Tech Spec specifying persistence MUST include explicit PostgreSQL Row-Level Security (RLS) tenant isolation policies and private Storage bucket boundaries.
3. **Mandatory Anti-Reward-Hacking:** Any Tech Spec claiming evaluation, assessment, or AI execution MUST specify adversarial countertests and explicit false-proof risk analyses (Gate H).
4. **No Implementation Authority:** The gate reviewer audits specifications; it does NOT write code, execute migrations, or deploy infrastructure.

---

## 2. Gates A through I Checklist

The reviewer audits the following 9 gates:

- **Gate A — Scope & Authority Alignment:** Clean plane separation, single tenant root (`Workspace`), legal parent chain.
- **Gate B — Object Model Alignment:** Every entity/state backed by ratified constitutions.
- **Gate C — Semantic Operation Contracts:** Typed operations, explicit `(from_state, to_state)`, expected version locks.
- **Gate D — Relational & Storage Security:** PostgreSQL schema with RLS `workspace_id = current_setting(...)` and private Storage bucket paths (`storage://cae-media/...`).
- **Gate E — Idempotency & Version Control:** Unique idempotency keys, atomic transaction bounds, optimistic locking.
- **Gate F — Receipt Lineage & Provenance:** Execution receipts referencing immutable source package, engine version, and evaluator identity.
- **Gate G — Error Taxonomy:** Typed error codes covering all operational failure modes.
- **Gate H — Reality-Contact & Anti-Reward-Hacking:** Explicit E1–E4 test tiers, countertests against self-attestation, and taste non-claims.
- **Gate I — Rollback & Recovery:** Deterministic rollback procedure, schema down-migration, and transient state cleanup.

---

## 3. Inputs & Preconditions

- Input MUST conform to `input_schema.yaml`.
- Requires full Tech Spec text, author identity, and target implementation slice.

---

## 4. Procedure

1. **Ingest Tech Spec Document:** Parse structure and verify 14-section Tech Spec standard.
2. **Audit Gates A through I:** Systematically evaluate requirements for each gate.
3. **Verify State Control Additions:** Check RLS policies, Storage paths, idempotency keys, and rollback contracts.
4. **Formulate Gate Verdicts:**
   - Every gate MUST receive `PASS`, `FAIL_DEFECT_DETECTED`, or `INAPPLICABLE_WITH_REASON`.
5. **Determine Overall Spec Status:**
   - `GATES_CLEARED_RECOMMENDED_FOR_OPERATOR_GATE`: All applicable Gates A–I passed.
   - `FAILED_GATE_VIOLATION`: One or more applicable gates failed.
   - `REJECTED_INCOMPLETE_SPEC`: Spec lacks required sections.
6. **Emit Gate Audit Receipt:** Output structured report conforming to `output_schema.yaml`.

---

## 5. Prohibitions

- MUST NOT waive any failed gate.
- MUST NOT allow a Tech Spec lacking RLS or Storage isolation to pass Gate D.
- MUST NOT allow an evaluation Spec lacking countertests to pass Gate H.
- MUST NOT authorize implementation execution.

---

## 6. Escalation & Stop Conditions

- **Stop as `FAILED_GATE_VIOLATION`:** If any applicable Gate A through I fails compliance check.
- **Stop as `REJECTED_INCOMPLETE_SPEC`:** If the specification document lacks required standard sections.
- **Stop as `BLOCKED`:** If prerequisite constitutions or traceability matrices are unratified.

