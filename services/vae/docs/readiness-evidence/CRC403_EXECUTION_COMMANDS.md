# CRC-403 Execution Commands

Current state: `WAITING_FOR_OPERATOR_INFRASTRUCTURE`  
Classification: `non_production_readiness_proof`

## Codex can run now

These commands only revalidate completed repository evidence; they do not close CRC-403:

```powershell
python -B proofs/evaluator/validate_evaluator_foundation.py
python -B validation/tests/test_delegation_rc4_integration.py
python -B reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/proofs/verify_format02_controlled_proof.py
python -B proofs/recovery/verify_recovery_scenario.py
```

Expected existing results are evaluator foundation `PASS` with `insufficient_evidence`, RC4 integration 14/14 `PASS`, Format 02 fixture chain `PASS` with real end-to-end `FAIL`, and recovery simulation `PASS` with runtime recovery `FAIL_not_executed`.

## Why there is no provider shell command yet

No evaluator provider, endpoint contract, model identity, credential reference, or approved invocation method exists. A `curl`, SDK, or provider CLI command would therefore invent an integration surface. The operator must supply the exact invocation method requested in `CRC403_OPERATOR_INPUTS.md`. Secrets must be resolved outside the repository.

## Exact first-proof command

After every operator input is supplied and preflighted, send Codex this exact command:

> Execute CRC-403 proof P1 only: governed evaluator runtime and calibration evidence. Use only the operator-approved provider, endpoint, exact model/version/digest, runtime/API version, invocation method, evaluator and producer identities, credential reference, governed calibration-corpus manifest, protected-set seal and authority receipts supplied for CRC-403. First verify immutable identity, credential separation, endpoint reachability, input/output contract enforcement and fail-closed behavior. Then run the governed calibration corpus and one blinded protected-set execution; produce immutable request/result receipts, false-positive/false-negative/abstention analysis, candidate threshold evidence, non-compensable-gate results and an evaluator rollback baseline. Do not invent or approve final thresholds. Do not mark `certified` without the required signed evaluation and product-authority evidence. Do not run the self-hosted GPU proof, cloud proof, recovery rehearsal, Format 02 end-to-end proof, Stage 5 work, or production actions. Stop after P1 and report exactly `PASS`, `FAIL`, or `WAITING_FOR_OPERATOR_INFRASTRUCTURE`.

This command authorizes only P1. Even after P1 passes, stop for the evaluator authority decision and a separate instruction before P2.

