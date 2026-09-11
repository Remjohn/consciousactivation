# Mandate Delivery Report: CAE M18 — JIT Context Capsule + Package Compilation

**Mandate ID:** CAE-M18  
**Phase:** 2 — Runtime Foundation  
**Status:** COMPLETE (Operator Ratification Requested)  
**Authority Reference:** `00_CONTROL/22_PHASE2_AGENT_PACKAGE_COMPILATION_CONTRACT.md`, `00_CONTROL/27_PHASE2_CONTEXT_BUDGET_CONTRACT.md`, `00_CONTROL/21_PHASE2_CAPABILITY_SECURITY_MATRIX.md`, `docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md`  
**Repository Commit:** `e5cd35ed6448f8454aa3a4a1d20e75563723ecb8`  

---

## 1. Baseline Authority & Mandate References Read

The following authoritative documents and code paths were read in full prior to execution:
1. `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
2. `docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md`
3. `00_CONTROL/22_PHASE2_AGENT_PACKAGE_COMPILATION_CONTRACT.md`
4. `00_CONTROL/27_PHASE2_CONTEXT_BUDGET_CONTRACT.md`
5. `00_CONTROL/21_PHASE2_CAPABILITY_SECURITY_MATRIX.md`
6. `00_CONTROL/20_PHASE2_CAE_PI_STATE_MAPPING.md`
7. `00_CONTROL/28_PHASE2_PILOT_RUNTIME_REQUIREMENTS.md`
8. `02_PHASE_2_RUNTIME_FOUNDATION/M18_GEMINI_ACTIVATION.md`
9. `02_PHASE_2_RUNTIME_FOUNDATION/M18_jit_context_capsule_package_compilation.md`
10. `00_CONTROL/05_PROGRAM_PACKAGE_AND_AGENT_CONVENTION.md`
11. `00_CONTROL/14_PHASE1_BUILDER_RUNTIME_BINDING_CONTRACT.md`
12. `services/builder/src/cmf_builder/skills/jit_capsule.py` & `jit_capsule_commands.py`
13. `packages/ca_runtime/src/ca_runtime/pi_adapter.py`
14. `packages/ca_runtime/src/ca_runtime/program_registry.py`
15. `tests/cae/test_pi_runtime_boundary.py`
16. `tests/cae/test_tenant_slice_operations.py`

---

## 2. Implemented Architecture & Deliverables

### 2.1 Core JIT Context Capsule Engine (`packages/ca_runtime/src/ca_runtime/context_capsule.py`)
1. **Precedence Hierarchy Enforcement:**
   $$\text{CAE Constitutions} (1) > \text{Operator Authorization} (2) > \text{Program/Harness Policy} (3) > \text{Local CAE.md/AGENTS.md} (4) > \text{Agent Instructions} (5) > \text{Skill Procedures} (6) > \text{Artifact Evidence} (7)$$
   - Governed by `ContextPrecedenceLayer` IntEnum with stable intra-layer ordering.
   - Reconciles local `CAE.md` and `AGENTS.md` without duplicating or conflicting with global constitutions.

2. **Skill Maturity Gating:**
   - Skills categorized as `DRAFT`, `TESTED`, `STABLE`, or `QUARANTINED`.
   - `DRAFT` skills are rejected fail-closed with `SkillMaturityViolationError` during production capsule assembly. Only `TESTED` and `STABLE` skills are permitted.

3. **Passive & Flat Skill Verification:**
   - Enforces the Canonical Skill Constitution: skills are pure procedure documents (`SKILL.md`).
   - Any nested sub-agents or nested skills inside a skill directory raise `ContextNestingViolationError`.

4. **Explicit Capability Projections:**
   - Capabilities are explicitly declared via `CapabilityProjection` matching the Phase 2 Capability Security Matrix.
   - Binds `owner_product`, `scope`, `mode` (`READ_ONLY`, `READ_WRITE`, `MUTATION_OPERATION`), `workspace_bound`, `approval_required`, `sandbox_required`, `audit_mode`, `bound_tools`, and `mcp_servers`.
   - Zero ambient or unverified capability access.

5. **Token Budget Accounting & Observable Context Traces:**
   - Every model invocation records a `ContextBudgetReport` tracking consumed tokens per section and remaining token budget.
   - Overflows on mandatory sections fail closed with `ContextBudgetOverflowError`.
   - Optional omitted items are captured in an `exclusion_trace` containing `ContextExclusionRecord` objects with explicit reason codes (`BUDGET_EXCEEDED`, `FORBIDDEN_BY_POLICY`, `LANE_MISMATCH`, `UNCERTIFIED_SKILL`, `INAPPLICABLE_PHASE`).
   - Fully assembled capsules emit a deterministic `capsule_id` and canonical `capsule_sha256` digest.

6. **Eve-Style Agent Package Compiler (`AgentPackageCompiler`):**
   - Compiles agent package directories containing `CAE.md`, `AGENTS.md`, `instructions.md`, `skills/`, `subagents/`, `tools/`, `connections/`, `hooks/`, `extensions/`, and `evals/`.
   - Emits an immutable `CompiledAgentPackage` manifest with a composite SHA-256 package hash.

---

## 3. Verification & Evidence

### 3.1 Focused Test Suite (`tests/cae/test_jit_context_capsule.py`)
10 tests executed and passing:
- `test_token_estimator`: Validates character/word heuristic token estimation.
- `test_context_precedence_hierarchy_assembly`: Verifies strict 6-layer descending precedence ordering in prompt construction.
- `test_reconcile_local_cae_and_agents_md`: Verifies local `CAE.md` outranking `AGENTS.md` in Layer 4.
- `test_skill_maturity_gating`: Verifies `DRAFT` rejection in production vs `STABLE` acceptance.
- `test_agent_package_compiler_with_temp_dir`: Verifies package scanning, anti-nesting violation detection, and manifest compilation.
- `test_context_budget_overflow_and_exclusion`: Verifies budget overflow fail-closed behavior and observable exclusion traces.
- `test_forbidden_and_missing_context`: Verifies forbidden context exclusion and mandatory missing context checks.
- `test_deterministic_capsule_sha256`: Verifies exact matching SHA-256 hashes for identical inputs.
- `test_explicit_capability_projections`: Verifies capability security matrix projections and tool/MCP bindings.
- `test_agent_package_with_subagents`: Verifies subagent package directory discovery and binding.

### 3.2 Aggregate CAE Test Suite (`pytest tests/cae`)
- **Total Tests Passed:** 137 / 137 (100% pass rate).
- **Execution Time:** ~55.51s.
- **Regressions:** 0.

---

## 4. Invariants & Limitations

1. **Non-Negotiables Preserved:**
   - Four Authority Lanes (`HUNTER`, `ANALYST`, `COMPOSER`, `COMMANDER`) strictly separated.
   - Skills remain flat and passive; no skill-to-skill invocation.
   - Pi is runtime substrate; Eve informs package structure only; CAE is sole state and receipt authority.
   - Filesystem directories are composition metadata, not canonical CAE state.
2. **Limitations:**
   - Production execution requires pre-validated `TESTED` or `STABLE` skill manifests.
   - Dynamic tool injection at runtime without declared capability projection remains strictly prohibited.

---

## 5. Next Gate

- Operator review and ratification of Mandate M18 delivery.
- Execution halts as instructed. No next mandate is implicitly started.
