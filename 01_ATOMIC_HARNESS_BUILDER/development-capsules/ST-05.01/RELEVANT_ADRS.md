# Relevant Accepted ADR

## ADR-009 — Skill Ecology and JIT Capsules

Authoritative file: `docs/architecture/adr/ADR-009-SKILL-ECOLOGY-AND-JIT-CAPSULES.md`

SHA-256: `812e8a7277300235d39c2cb946666d5fc7296ddcd36e2d854fb4784f22466337`

The implementation must preserve the four-layer distinction between canonical skills, Harness-local adaptations, composition recipes, and ephemeral JIT capsules. For this synthetic proof all four behavior-bearing sets are empty; no layer may be collapsed into another or inferred from code-owned capabilities.

Deterministic code owns exact registry, version, hash, authority, precedence, dependency, and receipt validation. Humans remain the authority for new canonical capabilities and stable promotion; independent evaluators remain the authority for maturity evidence. This Story performs neither action.

Model-selected dependencies, hidden orchestration, persistent skill context, production recipe binding, and JIT capsule compilation are prohibited.
