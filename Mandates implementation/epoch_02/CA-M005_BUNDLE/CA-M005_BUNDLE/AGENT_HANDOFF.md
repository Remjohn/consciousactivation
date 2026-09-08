# CA-M005 Bundle — Agent Handoff

## Mandate identity

- **Mandate ID:** `CA-M005`
- **Repository-authoritative title:** `CAE Mandate 005 — Format and Archetype Matchmaking Gate`
- **Canonical question:** `Q05`
- **Invariant:** `FR-ARCH-001`
- **Requested user title mismatch:** The repository's authoritative `CA-M005` document is the format/archetype gate, not “Multi-Layer Execution Quotas & Throttling.” This bundle implements the repository-authoritative CA-M005 document and does not invent a second mandate under the same ID.

## Summary

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/interview-intelligence/src/cae_interview_intelligence/question_resolver.py` | Extended `CompositionCompatibility` with explicit CA-M005 admission state, aspect-ratio/capability evidence, narrative/hypothesis bindings, profile revision refs, gate version, and deterministic decision digest. `is_compatible()` is fail-closed on gate status and incompatible reasons. | The admission result is typed, inspectable, revision-aware, and cannot report compatibility while carrying a blocked gate or incompatibility reason. |
| `services/interview-intelligence/src/cae_interview_intelligence/composition_compatibility.py` | Added explicit format capability/aspect-ratio metadata and deterministic `evaluate_preproduction_admission()` / `verify_admission_result()` logic. Enforces unknown profiles, unsupported archetype/format coalitions, declared ratio conflicts, and missing capabilities as blocking reasons. | `FR-ARCH-001`: incompatible format/archetype plans are deterministically blocked with inspectable reasons and a reproducible SHA-256 decision record. |
| `services/pipeline/src/cmf_pipeline/candidates/service.py` | Added the pipeline admission seam `enforce_preproduction_gate()` that only admits an explicit `PASS` result with a non-empty decision digest and no incompatible reasons. | The candidate pipeline cannot advance a non-passing CA-M005 result. |
| `packages/ca_runtime/src/ca_runtime/editorial_discovery_program.py` | Runs CA-M005 before any SELECT receipt, storyboard insertion, or production-status mutation; persists the complete gate result in the operator SELECT receipt; exposes the pass rationale in storyboard notes; downstream eligibility rehydrates and cryptographically verifies the stored gate before allowing production compilation. | The production/editorial runtime cannot bypass CA-M005 after selection, and legacy/tampered approvals fail closed. |
| `tests/cae/test_ca_m005_format_archetype_gate.py` | Adds deterministic positive coverage, disallowed coalition coverage, aspect-ratio negative coverage, missing capability coverage, pipeline fail-closed coverage, invalid operator-selection integration coverage, legacy receipt rejection, and tamper detection. | Executable test assertions cover both the unit contract and the actual runtime boundary where the repository currently materializes production admission. |

## Exact paste instructions

Copy the bundled files into the repository root using these exact replacements:

1. Replace `services/interview-intelligence/src/cae_interview_intelligence/question_resolver.py` with the bundled file at the same path.
2. Replace `services/interview-intelligence/src/cae_interview_intelligence/composition_compatibility.py` with the bundled file at the same path.
3. Replace `services/pipeline/src/cmf_pipeline/candidates/service.py` with the bundled file at the same path.
4. Replace `packages/ca_runtime/src/ca_runtime/editorial_discovery_program.py` with the bundled file at the same path.
5. Add `tests/cae/test_ca_m005_format_archetype_gate.py` at the bundled path.

No other repository paths are authorized by this bundle.

## Boundary mapping / implementation note

The mandate names `cae_collision_intelligence/composer.py` and `services/pipeline/src/cmf_pipeline/candidates/service.py` as precheck surfaces. In this repository archive, the collision/composition surface is represented by the existing interview-intelligence compatibility registry, while the actual production admission flow is:

`operator_select_candidate()` → `verify_downstream_production_eligibility()` → `compile_editorial_storyboard()`

There is no `PreProductionPlan` / sealed PreProduction manifest type in the inspected runtime tree. CA-M005 is therefore enforced at the smallest existing authoritative runtime boundary that precedes downstream production compilation, without introducing a parallel state machine.

## Manual post-apply commands

No database migration is required.

The requested validation command is intentionally **not executed in this bundle build**, per instruction:

```bash
python -m pytest tests/cae/test_ca_m005_format_archetype_gate.py
```

Recommended adjacent regression validation after apply:

```bash
python -m pytest \
  tests/cae/test_ca_m005_format_archetype_gate.py \
  tests/interview_intelligence/test_composition_compatibility.py \
  tests/phase3/test_editorial_discovery_activation.py
```

To capture the exact implementation commit SHA after applying and committing the bundle:

```bash
git add \
  services/interview-intelligence/src/cae_interview_intelligence/question_resolver.py \
  services/interview-intelligence/src/cae_interview_intelligence/composition_compatibility.py \
  services/pipeline/src/cmf_pipeline/candidates/service.py \
  packages/ca_runtime/src/ca_runtime/editorial_discovery_program.py \
  tests/cae/test_ca_m005_format_archetype_gate.py

git commit -m "Implement CA-M005 format and archetype admission gate"
git rev-parse HEAD
```

## Automated tests included

- `test_ca_m005_feasible_binding_is_deterministic_and_verified`
- `test_ca_m005_blocks_disallowed_archetype_format_pair`
- `test_ca_m005_blocks_declared_aspect_ratio_mismatch`
- `test_ca_m005_blocks_missing_required_format_capability`
- `test_ca_m005_pipeline_admission_is_fail_closed`
- `test_ca_m005_invalid_selection_creates_no_storyboard_or_select_receipt`
- `test_ca_m005_downstream_rejects_selection_without_gate_receipt`
- `test_ca_m005_tampered_gate_receipt_is_rejected_downstream`

## Verification status

- **Tests run during bundle construction:** none, by explicit instruction.
- **Syntax check:** complete source files were syntax-compiled with `py_compile`; this is not a substitute for the requested test suite.
- **Commit SHA:** unavailable in the uploaded archive because it does not contain Git repository metadata. The apply/commit command above captures the exact post-apply SHA.
- **Residual limitation:** the repository does not currently contain a concrete sealed `PreProductionPlan` object. The integration boundary proven here is the existing authoritative selection/downstream-production gate that precedes storyboard compilation.
- **Aspect-ratio authority:** the bundle only hard-codes an aspect-ratio coalition where the current repository contains explicit format-contract evidence (`FMT-02-REACTION` declares `9:16`). Other formats remain ratio-unconstrained unless the repository supplies a declared ratio.
- **Narrative/hypothesis binding:** the gate supports exact `SemanticRef` bindings and persists them in the receipt when supplied. The current `ContentCandidateRecord` schema does not itself retain an upstream hypothesis revision, so the runtime does not invent one.

## Operator decision required

**Approve or reject CA-M005 based on the evidence above.** The implementation is bounded to the repository-authoritative mandate, is fail-closed, and includes integration coverage; test execution and the final implementation commit SHA remain operator/apply-stage actions.
