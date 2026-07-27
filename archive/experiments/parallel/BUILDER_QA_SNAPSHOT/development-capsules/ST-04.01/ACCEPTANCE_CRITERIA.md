# Acceptance criteria

## AC-01 — Exact validated parent

Given the PASS ST-03.05 report and receipt, when compilation begins, then the active run, Harness IR, artifact set, constitutional report, authority hashes, and receipt identities match exactly and none is invalidated.

## AC-02 — Exact capability inventory

Given `skills.capabilities`, when the input decisions are loaded, then every and only the three declared capabilities appear once in canonical order; missing, extra, duplicate, renamed, or stale capabilities fail closed.

## AC-03 — No disappeared capability

Given the compiled graph, when coverage is evaluated, then capability coverage is 3/3 with no unowned node and no implicit default owner.

## AC-04 — Explicit ownership vocabulary

Given each capability, when ownership is validated, then its owner kind is one of `CODE`, `AGENT`, `HUMAN`, `EXTERNAL`, or `HYBRID`, its owner identity and authority boundary are non-empty, and the synthetic fixture uses only explicit `CODE` assignments.

## AC-05 — Reliability evidence

Given an ownership decision, when it is accepted, then attributable non-empty reliability evidence justifies the owner and deterministic code ownership cannot be generalized to real profiles.

## AC-06 — Cost evidence

Given an ownership decision, when it is accepted, then non-empty cost evidence records the bounded local choice without inventing provider, GPU, benchmark, or production economics.

## AC-07 — Hybrid and non-code failure boundary

Given a hybrid, agent, human, or external decision, when required authority, ordered participants, reliability/cost evidence, or explicit handoff responsibility is absent, then compilation fails closed without silently converting it to code ownership.

## AC-08 — Skill-policy separation

Given the governed empty-registry policy, when ownership compiles, then it proves only that the synthetic capabilities are code-owned and require no external skill; it does not perform skill discovery, selection, packaging, or production inference.

## AC-09 — Atomicity and idempotency

Given a valid command, when committed or repeated, then graph, run event/reference, command record, and receipt commit atomically; repeat payloads return the same receipt and stale, changed, or injected-failure commands leave no partial state.

## AC-10 — Invalidation and history

Given an active capability graph, when the authoritative boundary is reopened, then all descendants including the graph become inactive while immutable graph history remains reproducible and a new version is required.

## AC-11 — Observability and authority

Given success or failure, when evidence is emitted, then run, Story, IR, constitutional report, graph, owner/evidence coverage, authority, provenance, command, correlation, outcome, and typed failure context are observable without payload logging.

## AC-12 — Bounded completion

Given completion, when the Story receipt is issued, then all tests, exact file scope, rollback, 186 predecessor regressions, five owned obligations, and prohibited-boundary assertions pass with no later Story or production claim.
