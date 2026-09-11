# CAE-BMAD Multi-Level Engineering Investigation Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Operator Mandate M03  
**Scope:** Traversal algorithms, descent stop conditions, ascent proof criteria, doc-to-code drift detection, and multi-level investigation trace schemas.

---

## 1. Principles of Multi-Level Engineering Investigation

In long-lived brownfield software systems, documentation, plans, and architectural diagrams frequently drift from the concrete runtime reality.

CAE-BMAD enforces the **Principle of Bidirectional Empirical Verification**:
- **Never trust documentation alone:** Documentation (`Level 02`) is a hypothesis until confirmed by code (`Level 11–13`) or running tests.
- **Never trust code in isolation:** Code without architectural context (`Level 01–03`) risks optimizing for historical accidents rather than intended product outcomes.
- **Explicit Traversal:** All movements between abstraction layers must be recorded as discrete investigation steps with citations to exact files, AST symbols, or test executions.

---

## 2. Descent and Ascent Mechanics

```text
Level 01: PRODUCT / INTENT        [cae-method-orchestrator / cae-product-reconstructor]
         ↕
Level 02: DOCUMENTATION           [cae-documentation-analyst / cae-prd-agent]
         ↕
Level 03: PLAN                    [cae-plan-analyst / cae-delivery-agent]
         ↕
Level 04: AGENT                   [cae-agent-systems-analyst]
         ↕
Level 05: AI WORKFLOW / FACTORY   [cae-workflow-factory-analyst]
         ↕
Level 06: REPOSITORY              [cae-repository-analyst]
         ↕
Level 07: APPLICATION             [cae-application-analyst]
         ↕
Level 08: SCRIPT / CLI            [cae-cli-script-analyst]
         ↕
Level 09: DATABASE / TABLE        [cae-data-analyst]
         ↕
Level 10: MODULE / DIRECTORY      [cae-module-analyst]
         ↕
Level 11: FILE / TYPE / CLASS     [cae-code-forensics-analyst]
         ↕
Level 12: FUNCTION                [cae-code-forensics-analyst]
         ↕
Level 13: LINE / BLOCK            [cae-code-forensics-analyst / cae-brownfield-auditor]
```

### 2.1 Descent Protocol & Stop Conditions
Descent is initiated whenever:
1. A specification requirement lacks concrete codebase evidence.
2. A contradiction is detected between two documentation artifacts.
3. An automated test fails, requiring root-cause debugging.

**Descent Stopping Heuristics:**
- *Primary Stop:* Reached the exact function (`Level 12`) or line/block (`Level 13`) that definitively confirms, refutes, or identifies the missing capability.
- *Terminal Stop:* Reached the lowest accessible layer and discovered that the claimed implementation does not exist (`MISSING_IMPLEMENTATION`).
- *Error Stop:* Reached circular or broken delegation; abort with `WORKFLOW_UNDER_SPECIFIED`.

### 2.2 Ascent Protocol & Proof Requirements
Ascent is permitted only when backed by empirical evidence gathered during descent:
1. **Fact Aggregation:** The lower-level findings (line numbers, test results, schema definitions) are compiled into an investigation report.
2. **Drift Classification:** Discrepancies are categorized as `CONFIRMED`, `DRIFT_DETECTED`, `CONTRADICTED`, or `MISSING_IMPLEMENTATION`.
3. **Abstraction Update:** Higher-level artifacts (PRD, Architecture, Epics) are updated to reflect verified truth rather than speculation.

---

## 3. Drift Classification Taxonomy

| Drift Class | Semantic Definition | Required Remediation Action |
|---|---|---|
| `CONFIRMED` | Codebase and runtime match documented intent perfectly. | Record `VERIFIED` status in Operating Level Assessment. |
| `DRIFT_DETECTED` | Codebase implements the feature, but signatures, endpoints, or field names have evolved. | Update documentation to align with code reality or schedule alignment refactor. |
| `CONTRADICTED` | Codebase explicitly implements logic that directly contradicts the specification. | Log in `CAE_EDITORIAL_CONTRADICTION_REGISTER.md` and escalate to CAE Grill. |
| `MISSING_IMPLEMENTATION` | Stated feature is completely absent from codebase. | Log in Missing Implementation register and create delivery story. |
