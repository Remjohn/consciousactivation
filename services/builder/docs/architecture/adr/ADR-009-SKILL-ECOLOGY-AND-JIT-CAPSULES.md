# ADR-009: Skill Ecology And JIT Capsules

Status: `ACCEPTED`

Owners: Skill architecture. Trace: D012, D016, D017, D018, D019, D020, D021; TS-08, TS-09. External blocker: BD-010.

## Context

Reusable capabilities need stable identity and maturity, while runtime instructions need harness/phase bindings and minimal context. Treating every variation as a skill creates sprawl; one giant prompt hides dependencies and evaluation identity.

## Decision

Use four layers: Canonical Skill, Harness-local Adaptation, Composition Recipe, and ephemeral JIT Execution Capsule. A versioned capability registry and necessity test govern new skills. Deterministic code resolves versions, authority, precedence, dependencies, references, context, degradation, tools, evaluators, and capsule identity.

## Alternatives

- One skill per harness variation: rejected due duplication and weak reuse.
- One permanent monolithic prompt: rejected due context sediment and hidden orchestration.
- Model-selected dependencies at runtime: rejected because resolution and precedence are code-owned.

## Interfaces, Data, And Errors

Registry, package, recipe, binding, resolver, compiler, and evaluation ports. Errors include missing capability, unnecessary new skill, immature identity, dependency cycle, binding/precedence conflict, context overflow, forbidden degradation, and expired/revoked capsule.

## Authority, Security, And Determinism

Humans approve new canonical capabilities and stable promotion. Independent evaluators issue maturity evidence. Capsules declare least-privilege grants and never embed persistent secrets/protected labels.

## Consequences

Positive: portable skills, exact runtime context, deterministic assembly, and layered evaluation. Cost: registries, versioning, maturity workflows, and compiler complexity.

## Observability, Performance, Migration

Measure reuse/adaptation/new ratio, redundancy, no-op rate, package/context size, compile latency, cache hits, degradation, execution cost, and downstream outcomes. Version changes do not rebind consumers silently. Legacy brief migration is excluded until sources exist.

## Verification

Tests enforce necessity decisions, exact evaluated identity, deterministic capsule bytes, context blocking, precedence conflicts, revocation impact, hidden orchestration rejection, and least privilege.

