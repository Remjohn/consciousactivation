# Evaluator Calibration Runbook

Classification: `non_production_readiness_proof`

This runbook executes the already specified evaluator proof. It does not select a model, approve thresholds or authorize production.

## Preconditions

1. Operator-approved evaluator identity fields and credential reference are available.
2. Producer and evaluator identities are demonstrably separate.
3. `character-scene-evaluator@1.1.0-proof`, its prompt digest and the evaluation profile digest are verified.
4. At least 30 governed calibration cases have approved provenance and adjudicated labels.
5. The protected set has been independently created and sealed before tuning.
6. Non-compensable gate and affinity terminology decisions have authorized receipts.

## Calibration execution

1. Materialize a candidate evaluator pin using the exact provider/model/runtime/credential references; never copy secret values into the repository.
2. Contract-test valid, malformed, missing-evidence, uncertainty, timeout, prompt-injection and self-approval cases.
3. Freeze the corpus version, case-list digest, rubric version and evaluator/program settings.
4. Execute every calibration case once under the frozen identity. Retain raw response, normalized result, input hashes, latency, cost and evaluator receipt.
5. Compare predictions with adjudicated labels overall and for accepted, borderline, wrong-action, identity, composition, technical, recurrence, wrong-reading, Feature Contract, no-text and repairability slices.
6. Produce false-positive, false-negative, abstention and not-applicable analysis. Review every critical false negative individually.
7. Generate candidate operating points from observed distributions. Do not use the protected set and do not promote a threshold without evaluation and product authority approval.
8. Apply approved non-compensable gates independently of ranking thresholds.
9. Set `calibration_ready` only when the corresponding requirements in `EVALUATOR_INPUT_REQUIREMENTS.yaml` all have immutable evidence.

## Protected-set execution

1. An independent custodian verifies the seal, access log and non-overlap proof.
2. Run the sealed set once with the frozen evaluator/program/profile combination.
3. Retain results without feeding protected labels, prompts or failures back into tuning.
4. Any critical gate failure blocks `shadow_ready`; changing model, prompt, program, rubric, corpus policy or applicability invalidates affected evidence.

## Shadow and certification

Run the candidate without acceptance authority alongside the current decision process. Record drift, disagreements, abstentions, arbitration, latency, cost and incidents. Advance to `shadow_ready` and then `certified` only against the exact evidence lists in the requirements file and an authorized signed receipt.

## Existing validation commands

From the repository root:

```powershell
python -B proofs/evaluator/validate_evaluator_foundation.py
```

This validates foundation structure only. A `PASS` does not certify the evaluator.
