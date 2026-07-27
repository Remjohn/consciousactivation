# Evaluator Selection Decision

Classification: `non_production_readiness_proof`  
Decision status: **operator decision required**  
Current evaluator status: `specified_not_certified`

No evaluator model, provider or endpoint is selected by this package. The repository contains a pinned evaluation program and prompt, but the evaluator identity remains intentionally unbound until an authorized operator supplies and approves the external inputs in `EVALUATOR_INPUT_REQUIREMENTS.yaml`.

## Operator decision record

Complete this record outside secret-bearing systems, then provide only the approved identifiers and credential reference:

| Field | Required operator decision |
|---|---|
| Deployment mode | Managed API, operator-managed private endpoint, or isolated local self-hosted evaluator |
| Provider and endpoint | Stable service identity; no mutable alias-only endpoint |
| Model/weight identity | Exact model reference and SHA-256 weight or provider release identity |
| Runtime/API | Exact runtime or API version |
| Evaluator principal | Identity used for evaluation receipts |
| Producer principal | Identity used for candidate generation; must be distinct for evaluated claims |
| Credential boundary | Secret-manager, workload-identity, keychain, or environment-variable reference only |
| Data policy | Region, retention, deletion and permitted media classification |
| Deterministic controls | Temperature/seed/schema mode or provider-equivalent settings |
| Limits | Context, image, rate, concurrency, latency and cost limits |

## Selection tests

A candidate is rejected before calibration if it cannot return the required structured findings, cannot preserve immutable input identities, cannot abstain, silently changes model identity, shares the producer identity, requires repository-stored secrets, treats supplied media as instructions, or cannot expose a stable receipt identity.

Selection is not certification. Passing adapter and schema tests makes a candidate eligible for calibration only. Empirical labels, protected evidence, threshold decisions, error analysis, shadow operation and rollback remain separate gates.

## Approval

Record the evaluation authority, product authority, decision ID, date, approved identity fields and evidence references. Until that receipt exists, keep `evaluator-program-pin.candidate.yaml` status `unbound` and do not change the evaluation profile from `specified_not_certified`.
