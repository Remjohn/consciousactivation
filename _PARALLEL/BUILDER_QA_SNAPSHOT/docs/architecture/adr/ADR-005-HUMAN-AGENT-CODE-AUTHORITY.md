# ADR-005: Human-Agent-Code Authority

Status: `ACCEPTED`

Owners: Product authority, security, and architecture. Trace: D002, D010, D012, D027; TS-00, TS-01, TS-05, TS-07, TS-13, TS-14.

## Context

Builder combines mechanical transformations, semantic inference, independent evaluation, and irreversible human decisions. Ambiguous ownership enables unsupported claims, hidden policy, and self-authorization.

## Decision

Every command, capability, and workflow node declares one primary actor: deterministic code, bounded agent, human gate, or governed hybrid. Deterministic code validates and commits. Agents produce proposals under exact capsules. Humans own constitutional decisions, creative policy, risk, waivers, irreversible architecture, and authorization. Evaluators are isolated from generators.

## Alternatives

- Agent-by-default: rejected because mechanical work and authority become nondeterministic.
- Human approval for every operation: rejected because it adds noise without authority value.
- Role labels in documentation only: rejected because enforcement must occur at command and sandbox boundaries.

## Interfaces, Data, And Errors

`AuthorityGrant`, `ActorAssignment`, `ActionDescriptor`, and signed `HumanReceipt` are versioned schemas. The command bus checks actor, action, resource, run, evidence class, policy, expected version, and required receipts. Unauthorized actions return typed denial without events.

## Authority, Security, And Determinism

Identity is authenticated; permissions are deny-by-default and time/scoped. Agents cannot issue grants, sign receipts, inspect protected labels, or directly commit state. Hybrid nodes separate proposal, deterministic validation, and human decision.

## Consequences

Positive: auditable responsibility and safe automation. Cost: explicit actor matrix, identity integration, and more command types.

## Observability, Performance, Migration

Audit every allow/deny, human latency, agent recommendation, and override. Cache policy evaluation only by exact policy/identity/resource hash. No legacy authority migration applies.

## Verification

Authorization matrix tests cover every command. Adversarial tests attempt agent ratification, evaluator leakage, stale grants, forged receipts, and UI bypass.

