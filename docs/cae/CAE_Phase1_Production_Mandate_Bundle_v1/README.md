# CAE 48-Mandate Production Bundle v1

Status: PROPOSED — OPERATOR RATIFICATION REQUIRED
Purpose: finite, evidence-driven implementation program to make the current CAE
intelligence and control plane executable on a Pi-backed runtime, while preserving
existing CAE constitutions, Programmed Model/workflow machinery, Atomic Harness Builder,
state contracts, Skills, four Authority Lanes, receipts, operator supervision and
brownfield boundaries.

This is NOT a replacement ontology and NOT a mandate to convert every service into an agent.

Target operator surface:
    PROGRAMS + ARTIFACTS + CHAT

Target execution surface:
    Program
      -> Pipeline
      -> Harness / Atomic Harness
      -> Agent Team
      -> Sub-agents
      -> Skills
      -> Typed Operations / Tools / MCP
      -> Hooks / Extensions
      -> CAE state + artifacts + receipts

Runtime substrate:
    Pi is the primary execution substrate candidate.
    Eve is used as a filesystem/package composition reference, not as a new CAE authority.
    OKF is used as a curated knowledge representation/exchange format.
    Supabase/PostgreSQL remains authoritative for structured CAE state and operational data.
    Redis/Iris remains an optional future hot-context/memory layer, not canonical truth.

Execution discipline:
- 48 mandates total, numbered 1–48.
- Four phases, exactly 12 mandates per phase.
- Phase-close mandates: 12, 24, 36, 48.
- Every phase close synchronizes docs/PRD/CURRENT.md from verified evidence.
- Every execution mandate requires reading the full baseline authority pack plus all
  mandate-specific references before action.
- Parallel execution is permitted only where the parallelism matrix marks work as safe
  and PRD/authority write ownership is disjoint.
- Every Gemini prompt is an execution key, not an architecture essay.
- Every mandate ends with evidence, exact commit SHA, explicit limitations and STOP.

Finite target:
Phase 1 = establish one verified production-gap inventory and executable architecture.
Phase 2 = make Program/Harness/Agent/Skill/Hook/State execution real on Pi.
Phase 3 = make the semantic/intelligence Programs executable on real CAE material.
Phase 4 = produce one real supervised activation through production artifacts and harden the runtime.

A phase is not complete because its code compiles. It is complete only when its
acceptance evidence exists and CURRENT.md has been synchronized.

The bundle deliberately refuses to claim "production ready" until Phase 4's final
acceptance gate proves a real supervised run under the defined environment.
