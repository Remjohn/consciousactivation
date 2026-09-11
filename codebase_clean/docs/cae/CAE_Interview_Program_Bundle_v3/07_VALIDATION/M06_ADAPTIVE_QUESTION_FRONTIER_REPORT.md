# M06 — Adaptive Question Frontier Validation Report

**Mandate ID:** M06  
**Status:** ACCEPTED / COMPLETED  
**Quality State:** IMPLEMENTED_AND_VERIFIED  
**Controlling Specifications:** `02_TECH_SPEC/01_TS_INTERVIEW_PROGRAM_001.md`, `04_MANDATES/M06_Adaptive_Question_Frontier.md`, `00_GOVERNANCE/03_PRD_DELTA.md` (FR-IP-005)  
**Execution Timestamp:** 2026-08-30T05:06:00+02:00  

---

## 1. Exact Current Implementation Source Path

- **Adaptive Question Frontier Engine & Models:** [`services/interview-intelligence/src/cae_interview_intelligence/adaptive_frontier.py`](file:///d:/Work/consciousactivation/services/interview-intelligence/src/cae_interview_intelligence/adaptive_frontier.py)
- **Question Intelligence Resolver:** [`services/interview-intelligence/src/cae_interview_intelligence/question_resolver.py`](file:///d:/Work/consciousactivation/services/interview-intelligence/src/cae_interview_intelligence/question_resolver.py)
- **Package Exports:** [`services/interview-intelligence/src/cae_interview_intelligence/__init__.py`](file:///d:/Work/consciousactivation/services/interview-intelligence/src/cae_interview_intelligence/__init__.py)
- **Acceptance Test Suite:** [`tests/interview_intelligence/test_adaptive_frontier.py`](file:///d:/Work/consciousactivation/tests/interview_intelligence/test_adaptive_frontier.py)

---

## 2. Adaptive Frontier Architecture & Runtime Rules

1. **Deterministic Selection Stability (AC-01):**
   The runtime ensures that identical input states (`coverage spine + unresolved requirements + latest answer observation + locks`) always produce identical candidate rankings and deterministic `QuestionAttempt` output.
2. **Specificity Escalation on Generic Answers (AC-02):**
   When an answer is vague, generic slop, or abstract (`specificity_score < 0.40` or `resolution == ABSTRACT/GENERAL`), the engine evaluates `AdaptiveAction.DEEPEN`, selecting episodic crucible follow-up probes.
3. **Contradiction Reconciliation (AC-03):**
   When an observed response contains a factual contradiction (`has_contradiction == True` or declared `discrepancy_refs`), the engine evaluates `AdaptiveAction.RECONCILE`, routing to targeted discrepancy probes.
4. **Breadth Expansion on Partial Coverage (AC-04):**
   When an answer provides partial information and active coverage spine milestones contain unresolved requirements, the engine evaluates `AdaptiveAction.BROADEN`, expanding inquiry breadth across unaddressed dimensions.
5. **Advancement and Saturated Closure (AC-05):**
   When response evidence satisfies active milestone requirements (`InformationCompleteness.SUFFICIENT` or `VERIFIED`), the engine evaluates `AdaptiveAction.ADVANCE` to progress along the coverage spine. When all spine milestones are fulfilled, it evaluates `AdaptiveAction.CLOSE` and marks the session terminal.
6. **Scripted/Invalid Candidate Pruning (AC-06):**
   All candidate prompts are vetted against `assert_non_scripted_prompt`. Any leading questions (e.g. "Don't you agree...") or invalid syntax patterns are pruned from the candidate pool before ranking.
7. **Operator Locks Enforced at Runtime (AC-07):**
   Operator-locked candidates (`is_locked == True` or `candidate_id in locked_question_ids`) are strictly prioritized and cannot be overridden by adaptive routing.
8. **Bounded Candidate Pool (AC-08):**
   The evaluated candidate pool is strictly bounded between 3 and 5 typed `QuestionCandidate` objects at every step.
9. **Deterministic 7-Tier Tie-Breaking:**
   Candidates are scored across:
   1. `requirement_coverage` (100.0 max)
   2. `hypothesis_evidence_fit` (50.0 max)
   3. `interactional_fit` (25.0 max)
   4. `composition_compatibility` (15.0 max)
   5. `semantic_novelty` (10.0 max)
   6. `operator_preferences` (5.0 max)
   7. `deterministic_candidate_order` (final deterministic SHA256 tie-breaker)

---

## 3. Acceptance Criteria Verification Matrix

| AC # | Acceptance Test | Result | Summary Evidence |
|---|---|---|---|
| **AC-01** | `test_deterministic_selection_stability` | **PASS** | Identical frontier state and candidate pool yields identical candidate ranking and selection. |
| **AC-02** | `test_generic_answer_triggers_deepen_action` | **PASS** | Generic/abstract answer triggers `DEEPEN` specificity escalation. |
| **AC-03** | `test_contradiction_triggers_reconcile_action` | **PASS** | Contradiction observation triggers `RECONCILE`. |
| **AC-04** | `test_incomplete_coverage_triggers_broaden_action` | **PASS** | Incomplete requirements coverage triggers `BROADEN`. |
| **AC-05** | `test_sufficient_evidence_triggers_advance_and_close` | **PASS** | Sufficient/verified evidence triggers `ADVANCE` and terminal `CLOSE`. |
| **AC-06** | `test_invalid_and_scripted_candidate_pruned` | **PASS** | Scripted/invalid prompts are pruned from candidate pool. |
| **AC-07** | `test_operator_locks_enforced_at_runtime` | **PASS** | Operator locks are preserved and prioritized without override. |
| **AC-08** | `test_bounded_candidate_pool_size_limits` | **PASS** | Evaluated pool size is strictly bounded: `3 <= len(pool) <= 5`. |

---

## 4. Test Suite Execution Logs

```powershell
python -m pytest tests/interview_intelligence/ tests/interview_composer/ -v
```
**Output:**
```
============================= 58 passed in 36.60s =============================
```

**Total Baseline:** **58 / 58 tests passing** (100% pass rate).
