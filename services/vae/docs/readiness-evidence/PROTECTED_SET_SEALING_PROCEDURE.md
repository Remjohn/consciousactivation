# Protected Regression Set Sealing Procedure

Status: `awaiting_operator_custodian`  
Classification: `non_production_readiness_proof`

The protected set is a blind, immutable regression asset. It may not be used for prompt tuning, model selection, threshold fitting, rubric training or repeated exploratory runs.

## 1. Appoint custody

Record the human data owner, protected-set custodian, access approvers and incident contact. The evaluator developer, model selector and threshold calibrator must not have direct case access unless explicitly approved for a witnessed run.

## 2. Select cases

After deduplication and near-duplicate grouping, select cases that are disjoint from training and calibration sets. Cover every required positive, negative, adversarial, recurrence, repair, technical, wrong-reading, identity, composition, Feature Contract and no-text family, plus every proposed non-compensable gate. The owner approves the final size; this package does not invent it.

## 3. Build the seal manifest

For every case record case/version ID, asset hash, fixture hashes, authoritative label hash, rights/consent reference and case-family tags. Add the rubric, schema, evaluator input-contract and sealing-tool versions. Do not include secret values or raw restricted locations in the repository copy.

## 4. Seal and store

Encrypt the case payload and authoritative labels in operator-controlled storage. Enable object versioning, retention and audit logs. Compute the manifest SHA-256, have the custodian sign or attest it, and commit only the sanitized seal receipt and credential/storage references.

## 5. Grant run-scoped access

Issue a short-lived, read-only workload identity to the witnessed regression runner. The evaluator receives cases without authoritative labels. No interactive browsing, export or tuning access is permitted. Record access start, expiry and used object versions.

## 6. Execute once per approved candidate

Pin evaluator identity, evaluation-program identity, runtime, input contract and output schema. Run the entire sealed set without threshold or prompt changes. Write outputs to a new immutable result prefix. Failed jobs may resume only under the approved infrastructure-retry rule; they may not reveal labels.

## 7. Score outside the evaluator boundary

After output commitment, a separate scoring identity joins results to authoritative labels. Produce false-positive/false-negative analysis and non-compensable-gate results by family. Any post-run configuration change creates a new candidate and requires a new authorized run.

## 8. Verify and rotate

Recompute the seal hash before and after the run, review access logs, revoke credentials, and confirm no case entered calibration artifacts. Rotate the set if exposure, label leakage, rights changes, excessive reuse or material distribution drift occurs. Preserve the old seal receipt as historical evidence.

The evaluator cannot become `shadow_ready` or `certified` on evidence from an unsealed, exposed or tune-contaminated regression set.
