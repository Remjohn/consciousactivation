# CAE-BMAD Method Certification Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Operator Mandate M12  
**Scope:** Final integration, end-to-end operational proof on a real CAE capability slice, full-spectrum operating-level coverage (Levels 01–13), cross-mandate verification matrix (M01–M12), and master certification package standards.

---

## 1. The Method Certification Standard

A method rebuild is certified **only when**:
1. Every mandate (M01 through M12) is executed, tested, and validated against explicit JSON schemas.
2. An end-to-end integration run is executed on a real, physical slice of the codebase (`World Signal Ingestion & CAS Program State Mutation Pipeline`), touching active classes, functions, and lines on disk.
3. All 13 operating levels (`Level 01: PRODUCT / INTENT` to `Level 13: LINE / BLOCK`) are mapped with assigned agents, loadable skills, and verified deliverables.
4. All residual implementation gaps are explicitly registered in `docs/cae-bmad/07_brownfield/MISSING_IMPLEMENTATION_REGISTER.md` rather than hidden.
5. All 88+ automated regression tests in `tests/` pass with zero failures.

---

## 2. The Real CAE Integration Slice

The end-to-end method run executes across the real vertical capability slice:

```text
Level 01: PRODUCT / INTENT        → Vision & Capability Pillar 5 (Multi-Agent Runtime)
Level 02: DOCUMENTATION           → PRD-005 & Functional Requirement FR-005
Level 03: PLAN                    → Epic 5 & Stories (CAS Program State Mutations)
Level 04: AGENT                   → cae-runtime-agent invocation harness
Level 05: WORKFLOW / FACTORY      → Step scheduler in cmf_pipeline.workflow
Level 06: REPOSITORY              → packages/ca_runtime/ & services/world-intelligence/
Level 07: APPLICATION             → World Signal Ingestion & Verification Service
Level 08: SCRIPT / CLI            → Python test runner & validation entrypoints
Level 09: DATABASE / TABLE        → In-Memory CAS & State Aggregate Constitution
Level 10: MODULE / DIRECTORY      → packages/ca_runtime/src/ca_runtime/
Level 11: FILE / CLASS            → ProgramStateRuntime in program_state_runtime.py
Level 12: FUNCTION                → transition_state_cas() with optimistic locking
Level 13: LINE / BLOCK            → Verbatim AST line checks on state mutation logic
```

---

## 3. Certification Deliverable Standards

1. **Master Certification Package (`docs/cae-bmad/10_certification/CAE_BMAD_METHOD_CERTIFICATION.md` & `.json`):**
   - Summarizes 12 mandate validations, 13 operating level bindings, test metrics, and certification verdict.
2. **End-to-End Integration Run Trace (`docs/cae-bmad/10_certification/END_TO_END_INTEGRATION_RUN.md` & `.json`):**
   - Records chronological execution steps, input/output data contracts, and verbatim line-level code proofs.
