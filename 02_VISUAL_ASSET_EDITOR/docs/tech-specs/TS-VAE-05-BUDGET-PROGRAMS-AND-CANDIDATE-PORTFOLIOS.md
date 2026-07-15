# TS-VAE-05 Budget Programs and Candidate Portfolios

Status: draft for architecture validation  
Implementation authorization: no

## 1. Specification identity

- Feature: F16
- Owned FRs: FR-121 through FR-128
- Owned NFRs: NFR-PERF-001 through NFR-PERF-005; NFR-COST-001 through NFR-COST-005
- Decision: D019
- Components: `BudgetProgramRegistry`, `BudgetController`, `PortfolioCompiler`, `CandidateSelector`, `CostLedger`

## 2. Evidence read

VAE F16, Budget Program schema/registry, plan/result/evaluation fixtures, success metrics, readiness gates, Format 02 benchmark; Delegation budget authorization/escalation schemas, lifecycle, authority and resilience rules.

## 3. Problem, solution, and scope

Candidate quality requires bounded exploration, but cost/latency pressure must never weaken hard gates. The solution compiles one authorized Budget Program into immutable ceilings, a purpose-labeled candidate portfolio, reservations, metering, and quality-first selection.

In scope: six programs, authorization, estimates, reservations, candidate classes, controlled variation, hard-gate filtering, ranking, adaptive expansion, early stop, escalation, and receipts. Out of scope: changing demand/evaluator gates, arbitrary random sweeps, provider billing reconciliation beyond receipted usage, or training-budget execution.

## 4. Models and program semantics

`BudgetAuthorization`: Delegation-owned authorization ref, program/version, owner, ceilings for candidates/parallelism/GPU seconds/cost/wall clock/storage/evaluator calls/quality rounds, allowed experimental scope, escalation policy, validity, and signature/audit refs.

`PortfolioPlan`: plan/route refs, fixed properties, variation dimensions and domains, hypotheses, candidate classes, initial/max counts, parallelism, evaluation depth, selection profile, expansion/stop rules, and budget allocations.

`BudgetLedger`: immutable reservations/debits/releases by execution/node/candidate/evaluator/repair, estimated/actual units/cost, source receipt, sequence, and remaining balances.

`PortfolioReceipt`: candidates created/evaluated/eligible/rejected, repairs, parallelism, selected/alternatives, expansion/stop decisions, estimate/actual cost/time/GPU, learning outputs, and complete ledger hash.

Program registry behavior:

- Lean: known certified routes, 1 initial/3 max, one worker, up to two repairs.
- Standard: default production, 4 initial/10 max, two workers, up to three repairs.
- Premium: certified difficult/hero work, 8 initial/20 max, four workers, secondary evaluator.
- Exploration: sandboxed controlled experiments, 8 initial/32 max, six workers, declared variation required.
- Capability Learning: isolated evidence production, 6 initial/40 max, six workers, ensemble/arbitration and capability-development outputs.
- Custom: explicit ceilings validated against constitutional and caller policy; never bypasses the three-round/hard-gate limits.

Physical time/cost ceilings are mandatory in an authorization even where the draft registry says `configured`.

## 5. State machine and interfaces

Budget states: `PROPOSED`, `AUTHORIZED`, `RESERVED`, `ACTIVE`, `PAUSED_APPROVAL`, `EXHAUSTED`, `CLOSED`, `CANCELLED`, `EXPIRED`. Portfolio states: `COMPILED`, `INITIAL_RUNNING`, `EVALUATING`, `EXPANDING`, `EARLY_STOPPED`, `SELECTED`, `NO_ELIGIBLE_CANDIDATE`, `CANCELLED`.

```text
estimate(plan_ref, route_ref, program_ref) -> BudgetEstimate
authorize(delegation_authorization_ref) -> InternalBudgetRef
compile_portfolio(plan_ref, route_ref, budget_ref) -> PortfolioPlanRef
reserve(budget_ref, work_spec) -> ReservationRef
debit(reservation_ref, compute_or_eval_receipt) -> LedgerEntry
decide_next(portfolio_ref, evaluation_set, remaining_budget) -> expand | stop | repair | escalate
select(portfolio_ref, eligible_evaluations, ranking_profile) -> SelectionReceipt
close(budget_ref) -> BudgetReceipt
```

Events: `BudgetAuthorized`, `BudgetReserved`, `BudgetDebited`, `BudgetThresholdReached`, `PortfolioExpanded`, `PortfolioEarlyStopped`, `CandidateSelected`, `BudgetEscalationRequested`, `BudgetClosed`.

## 6. Cross-cutting production contract

| Concern | Required behavior |
|---|---|
| Visual Production Plan IR | Plan pins authorization and portfolio policy; budget changes create a new authorization/plan binding. |
| APIs/queues | Scheduler requires reservation before work; ledger debits use signed compute/evaluation receipts. |
| Provider adapters/ComfyUI/Docker locks | Cost comes from pinned route/runtime/OCI image/bundle; budget cannot choose an incompatible cheaper artifact. |
| GPU/storage | Meter GPU seconds, wall time, storage, transfer, and provider cost per candidate/node. |
| Deterministic/VLM | Authorization, ceilings, filtering, ledger, and stop guards are deterministic. VLM supplies quality/uncertainty evidence only. |
| Candidate selection | Hard-gate failures are ineligible before ranking; ranking profile is versioned and quality-first. |
| Evaluation | Required depth cannot be reduced. Uncertainty may trigger an authorized secondary evaluator. |
| Repair | Quality rounds debit separate repair allocations and never exceed three; infrastructure retry is separate. |
| Idempotency/checkpoints | Reservation/debit keys prevent double charge; portfolio decision sequence is append-only and resumable. |
| Observability/cost | Estimate versus actual and marginal quality gain per cost are visible by program/route/candidate/repair. |
| Security | Only authorized principals select high-cost/experimental programs or approve extensions. |
| Migration/rollback | Program versions are immutable; active runs keep pinned semantics. Rollback restores prior limits/ranking behavior. |

## 7. Candidate and selection rules

1. Every candidate has a declared class/purpose, fixed variables, varied variables, seed/bindings, parent route, cost, and lineage.
2. Exploration and Capability Learning require a hypothesis and comparable baseline; indiscriminate prompt/seed sweeps are invalid.
3. Technical, semantic, Activative, composition, identity/continuity, temporal, provenance, and repair-precision hard gates apply before ranking.
4. Ineligible candidates remain evidence but cannot win.
5. Eligible ranking may combine fidelity, effectiveness, continuity, distinctiveness, technical quality, editability, repair risk, cost, and latency using a registered profile.
6. Completion speed is never the sole winner criterion.
7. Early stop requires a passing candidate above a calibrated confidence threshold and low expected value from additional work.
8. Expansion requires unresolved uncertainty, a declared intervention, expected value, and sufficient remaining budget.
9. If budget is insufficient, checkpoint and issue Delegation `budget-escalation-request`; do not weaken quality.
10. Learning budgets and production budgets are accounted separately.

## 8. Failure, recovery, performance, and security

Reject invalid/expired/unauthorized programs, negative or inconsistent ceilings, and quality-gate overrides. Duplicate receipts do not double debit. Missing receipt pauses closure. Provider-price drift beyond authorization pauses before new work. Cancellation releases unused reservations and preserves actual cost.

Targets: estimate before execution; no hidden candidate/evaluator cost; node timing and cache reuse visible; at least 95% of completed runs within program ceilings excluding explicit approval. Performance optimization follows accepted-asset quality, not raw throughput.

Ledger is append-only with principal, correlation, source receipt, and hash. Budget data is tenant-scoped; authorization and escalation are verified through Delegation. Custom policies cannot exceed constitutional repair or experimental restrictions.

## 9. Implementation plan

1. Close schemas for authorization mapping, program version, estimates, reservations, ledger, portfolio, decision, selection, and receipts.
2. Make six registry records complete with physical time/cost/evaluator ceilings for the reference environment.
3. Implement deterministic authorization/reservation/debit/close logic.
4. Implement portfolio compilation and controlled-variation validation.
5. Integrate hard-gate filtering and registered ranking with TS-VAE-06.
6. Implement early stop, adaptive expansion, escalation, cancellation, and recovery.
7. Add dashboards, estimate calibration, concurrency/performance tests, and rollback fixtures.

## 10. Given/When/Then acceptance criteria

1. Given Standard authorization, when portfolio compiles, then initial/max candidates, parallelism, repairs, cost/time, and evaluator depth are pinned.
2. Given a candidate failing a semantic hard gate, when ranking runs, then it cannot be selected regardless of aesthetic score or speed.
3. Given a strong passing candidate and low expected value, when early-stop evaluates, then unused budget is released and the reason is receipted.
4. Given unresolved uncertainty and remaining budget, when expansion occurs, then varied/fixed factors and hypothesis are recorded.
5. Given duplicate compute receipt delivery, when debited, then cost is recorded once.
6. Given exhausted budget, when more work is proposed, then execution pauses and a typed escalation is emitted.
7. Given a denied escalation, when policy resolves, then no gate is weakened and the run enters the appropriate capability/exception state.
8. Given program rollback, when a new run selects the prior version, then its ceilings and selection behavior match historical fixtures.

## 11. Testing strategy

Unit-test ceilings, reservations, ledger idempotency, filtering, ranking, stop/expand guards, and receipt totals. Integration-test compute/evaluator receipts, cancellation, escalation, restart, out-of-order messages, and concurrency. Behavioral-test selection against labeled portfolios. Performance-test parallel limits and estimate error. Adversarially test budget bypass, hidden evaluator calls, random sweeps, unauthorized Premium/experimental use, and hard-gate weakening.

## 12. Constitutional alignment V1.1 addendum

Candidate eligibility is extended to every applicable constitutional gate before ranking. The ineligible set includes failure of zero-second hook, pattern-match strength, pattern-interrupt strength, viewer-role clarity, activation-direction fidelity, prediction gap, payoff, affinity, anticipation residue, anti-cliche strength, wrong-reading risk, Feature Contract compliance, and delete-caption/no-text survival where the profile declares applicability.

No Budget Program, early-stop rule, adaptive expansion, cost preference, or ranking weight may omit an applicable dimension or turn a failed hard gate into a score trade-off. A candidate with strong technical or aesthetic quality remains ineligible when any activation, narrative, role, feature, wrong-reading, or no-text gate fails.

SelectionReceipt records the exact evaluation-profile version, applicability set, per-gate outcomes, and the reason each rejected candidate was excluded. Missing required evaluation evidence blocks selection and budget closure rather than being treated as zero, not-applicable, or optional.

## 13. Non-goals

- Spending all available budget by default.
- Optimizing candidate count, speed, or cost ahead of accepted quality.
- Using a high-budget program as uncontrolled generation.
- Folding capability-training cost into ordinary production without explicit authorization.
