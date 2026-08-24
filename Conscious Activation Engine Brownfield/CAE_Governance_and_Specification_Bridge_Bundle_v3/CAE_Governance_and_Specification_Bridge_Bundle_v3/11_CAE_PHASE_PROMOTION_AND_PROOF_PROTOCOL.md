# CAE Phase Promotion & Proof Protocol v2.0

## Purpose

This protocol modifies the CAE phase governance chain so that Phase 0–7 documents cannot become implementation authority merely because they are internally coherent or pass documentation checks.

## Canonical chain

```text
Phase 0–7
     ↓
Target Architecture
     ↓
PHASE VALIDATION
     ↓
Brownfield Reconciliation
     ↓
Functional Requirements
     ↓
CAE Tech Specs
     ↓
Implementation
     ↓
Tests / Receipts
     ↓
Reality-Contact Evaluation
     ↓
Verified Runtime
```

## Promotion statuses

Each phase and each major requirement MUST carry one status:

`DOCUMENTED` → `ARCHITECTURALLY_RATIFIED` → `BROWNFIELD_VALIDATED` → `SPEC_READY` → `IMPLEMENTED_PENDING_VERIFICATION` → `VERIFIED`

Optional quarantine states:

`QUARANTINED_EVIDENCE`, `QUARANTINED_REGISTRY`, `QUARANTINED_REWARD_HACK`, `QUARANTINED_CENTROID`

## Proof packet

Every promotion from `IMPLEMENTED_PENDING_VERIFICATION` to `VERIFIED` requires a proof packet containing:

```yaml
proof_id:
requirement_id:
phase_id:
object_ids: []
implementation_refs: []
test_refs: []
receipt_refs: []
environment_fidelity:
reward_hacking_status:
taste_integrity_status:
anti_centroid_status:
evidence_refs: []
known_limitations: []
review_decision:
```

## Phase validation upgrade

Phase validation MUST evaluate not only whether the architecture is represented but whether the planned verification mechanism is capable of detecting false success.

Add to every phase evidence matrix:

| Claim | Minimum Fidelity | Reward-Hack Test | Taste/Reality Test | Receipt | Promotion Status |
|---|---|---|---|---|---|

## Functional Requirement upgrade

Every FR MUST include:

- the proposition being implemented;
- the source evidence;
- environment fidelity requirement;
- primary proxy metrics;
- known proxy-gaming risks;
- false-proof test;
- semantic/taste criteria;
- receipt requirements;
- promotion evidence.

## Tech Spec upgrade

Every Tech Spec MUST contain a validation subsection that identifies:

1. the operational claim;
2. the proxy being measured;
3. the likely reward-hacking strategy;
4. the adversarial counter-test;
5. the required environment fidelity;
6. the taste/reality-contact check;
7. the runtime receipt proving what actually happened.

## Implementation Gate upgrade

`READY_FOR_DEVELOPMENT` authorizes coding.

`IMPLEMENTED_PENDING_VERIFICATION` means the code exists but proof is incomplete.

`VERIFIED` means the claim survived all applicable structural, fidelity, anti-hack, taste, and evidence gates.

## Fatal promotion errors

Do not promote when:

- test results are green only under an inadequate environment;
- evaluator gaming has not been tested;
- a taste-sensitive claim has only structural evidence;
- an immutable evidence claim has only derived evidence;
- a runtime receipt is absent for a material state-changing action;
- a phase requirement is contradicted by brownfield evidence without a migration decision;
- the implementation passes only after weakening the claim to match the implementation.

## Brownfield principle

Implementation evidence may revise the target design. It MUST NOT silently rewrite history.

The system should instead produce:

`new evidence → contradiction → decision → revised FR/spec → implementation → re-verification`

This preserves the auditability of the architecture.
