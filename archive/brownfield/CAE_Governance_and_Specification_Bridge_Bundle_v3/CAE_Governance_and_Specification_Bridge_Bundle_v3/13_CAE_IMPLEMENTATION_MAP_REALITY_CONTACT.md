# CAE Implementation Map — Reality Contact, Reward Hacking, and Taste Governance v1.0

## Purpose

This note identifies the classes of runtime code that must participate in the new evaluation doctrine. The goal is not to prescribe filenames without repository inspection; it defines the required implementation responsibilities that the brownfield reconciliation must map onto existing code.

## 1. Validator layer

Every material validator should expose or record:

- claim identifier;
- proxy metric(s);
- intended property;
- evaluator version;
- known gaming modes;
- environment fidelity requirement;
- evidence status.

Validators should return typed results rather than bare booleans where the surrounding architecture can support it.

## 2. Test harness

The test infrastructure should support metadata for:

- test class;
- claim ID;
- environment fidelity;
- fixture provenance;
- reward-hack scenario;
- expected negative result;
- taste/anti-centroid classification.

This does not require every unit test to become heavyweight. Material claims receive the full governance contract; ordinary implementation tests may remain lightweight.

## 3. Receipt layer

Meaningful runtime receipts should preserve enough information to reconstruct what was evaluated:

```yaml
receipt_id:
claim_id:
component_id:
input_snapshot_hash:
registry_snapshot_hash:
output_snapshot_hash:
environment_fidelity:
evaluator_versions: []
validator_results: []
reward_hack_result:
taste_integrity_result:
anti_centroid_result:
evidence_refs: []
timestamp:
```

## 4. Runtime state / event layer

Where evaluation results alter system state, emit immutable events rather than overwriting historical evidence.

Recommended event classes include:

- `EvaluationExecuted`
- `RewardHackDetected`
- `TasteRegressionDetected`
- `AntiCentroidDriftDetected`
- `EnvironmentFidelityInsufficient`
- `VerificationPromoted`
- `VerificationQuarantined`

Exact names remain subject to canonical object reconciliation.

## 5. Registry / migration layer

Inherited SDA/SFL/Primitive records must be tested against crosswalks and failure-corpus references before being treated as executable dependencies.

A registry test that only checks YAML parsing is insufficient. It should also detect:

- broken references;
- family/reference mismatches;
- orphan failure cases;
- version regression;
- missing provenance;
- silent ID substitution.

## 6. Agent / program layer

Agents should receive evaluation results as typed structured evidence and typed errors, not as generic prose such as “quality failed.”

Preferred repair input:

```text
CLAIM_ID
FAILED_GATE
EVIDENCE_STATUS
ENVIRONMENT_FIDELITY
REWARD_HACK_CLASS
TASTE_FAILURE_CLASS
RELEVANT_OBJECTS
AUTHORIZED_REPAIR
```

## 7. Operator / governance surface

Operators should be able to inspect at least:

- claim;
- test;
- environment;
- evaluator version;
- pass/fail history;
- reward-hack findings;
- taste regressions;
- receipts;
- promotion status;
- quarantine reason.

This can be surfaced through existing operator tooling once the brownfield repository is reconciled; the architecture does not require a new UI before the underlying data contract exists.

## 8. Brownfield rule

The coding agent MUST inspect the current repository before choosing implementation locations. This map is a responsibility map, not an assertion that any named service already exists.

Where an existing service already performs one of these functions, extend it rather than creating a competing parallel subsystem unless a formal replacement decision exists.


## 9. State-control implementation responsibilities

The brownfield reconciliation must map these responsibilities onto existing infrastructure before creating new services:

| Responsibility | Required implementation capability | Default authority |
|---|---|---|
| Current state | queryable current-state projection | PostgreSQL/Supabase |
| State history | immutable temporal records | PostgreSQL/Supabase |
| Transition legality | typed transition contract service | CAE application layer |
| Semantic operations | typed authorized functions | CAE application layer |
| Transition evidence | validator + evidence records | CAE validation layer |
| Receipt | immutable transition receipt | existing receipt infrastructure if compatible |
| Recovery | explicit repair / blocked routing | harness/runtime layer |
| Procedural memory | versioned Skills.md / runbook | repository-controlled artifacts |

StateM patterns should be mapped as implementation precedent only.
