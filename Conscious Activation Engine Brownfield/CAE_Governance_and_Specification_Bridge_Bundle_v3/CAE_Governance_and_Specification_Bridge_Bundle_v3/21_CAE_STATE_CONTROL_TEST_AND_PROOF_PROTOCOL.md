# CAE State-Control Test & Proof Protocol v1.0

## 1. Purpose

State control is only valuable if the system can demonstrate that transitions reflect reality rather than merely producing green checks.

## 2. Transition test classes

Every material transition should be tested across:

1. valid transition;
2. illegal transition;
3. missing evidence;
4. stale state;
5. conflicting state;
6. validator failure;
7. retry after transient failure;
8. deterministic failure not blindly retried;
9. duplicate transition request;
10. process restart / recovery;
11. receipt persistence;
12. current-state projection correctness.

## 3. Environment fidelity

State-transition tests must declare fidelity:

- `E0_SYNTHETIC`
- `E1_REALISTIC_FIXTURE`
- `E2_REPOSITORY_INTEGRATED`
- `E3_PRODUCTION_SHAPED`
- `E4_REAL_WORLD_OBSERVED`

A synthetic transition test cannot prove a production-shaped side-effect claim.

## 4. Reward-hacking tests

For each state validator, ask:

> Can an implementation make the state appear complete without satisfying the underlying condition?

Examples:

- setting `authenticated=true` without evidence;
- setting `verified=true` after a self-attestation only;
- writing a receipt before the transition actually commits;
- incrementing `activation_count` without a fresh observed signal;
- marking `CURRENT=true` on multiple overlapping state records;
- copying a previous receipt to satisfy a presence check;
- forcing a proxy score over threshold while the semantic/taste property deteriorates.

## 5. Taste and anti-centroid requirements

For semantic transitions, structural state validity is insufficient.

Example:

`EDGE_VALIDATED`

must not mean merely:

```text
edge_score >= threshold
```

It must include the applicable:

- Matrix of Edging criteria;
- SDA directional checks;
- SFL/perceptual checks;
- anti-centroid evaluation;
- evidence lineage.

## 6. State transition receipt

A material transition receipt should record:

```yaml
receipt_id:
run_id:
transition_id:
source_state:
target_state:
preconditions:
required_evidence:
validator_results:
proxy_metrics:
anti_proxy_tests:
environment_fidelity:
operator_or_agent:
commit_timestamp:
postcondition_snapshot:
```

## 7. Promotion criterion

A green test suite is not enough.

Promotion requires:

```text
state semantics verified
+
transition behavior verified
+
proof mechanism independently adequate
+
reward-hack resistance demonstrated
+
required environment fidelity demonstrated
+
receipt lineage present
```
