# TS-08: Canonical Skill Ecology

Status: `IMPLEMENTATION_SPEC_COMPLETE_PENDING_BD-010`

## Traceability

- Owned: FR-081 through FR-090; NFR-MAINT-002.
- Decisions: D012, D016, D017, D019, D021, D033.
- Supporting NFRs: NFR-EVAL-001, NFR-EVAL-002, NFR-PORT-001, NFR-TRACE-003.

## Responsibility And Authority

Own the Canonical Skill Capability Registry, authority lanes, maturity/plasticity, necessity test, reuse/adaptation decisions, Skill Design Brief, leading-word anchors, portable packages, evaluation bindings, and redundancy/no-op detection. It does not compile runtime capsules or execute skills.

Deterministic code validates packages, dependencies, identities, maturity gates, and duplication. Agents draft designs and behavioral anchors. Humans approve new canonical capabilities, stable promotion, deprecation, and high-plasticity changes. Independent evaluators own maturity evidence.

## Modules And Components

`skills/registry.py`, `skills/design_brief.py`, `skills/necessity.py`, `skills/package.py`, `skills/maturity.py`, `skills/redundancy.py`, and `application/skill_commands.py`.

## Canonical Data Structures

- `SkillCapability { capability_id, outcome, authority_lane, input_contracts, output_contract, completion, failures, exclusions }`
- `CanonicalSkill { skill_id, version, capability_refs, procedure, leading_words, references, dependencies, evaluator_refs, maturity, plasticity, package_hash }`
- `SkillDesignBrief { problem, gap_evidence, alternatives, selected_design, behavior_cases, cost, context, degradation, portability }`
- `NecessityDecision { capability_gap, reuse_candidates, adapter_candidates, decision, rationale, human_receipt? }`
- Maturity: `DRAFT`, `PROTOTYPE`, `EVALUATED`, `STABLE`, `DEPRECATED`, `REVOKED`.
- Plasticity: `LOCKED`, `CONTROLLED`, `EXPERIMENTAL`.

Only `EVALUATED` or `STABLE` skills may enter production recipes, and exact evaluated package identity is mandatory.

## APIs, Commands, Events, Persistence

- Commands: `RegisterCapability`, `RunNecessityTest`, `CreateSkillDraft`, `SubmitSkillEvaluation`, `PromoteSkill`, `DeprecateSkill`, `DetectRedundancy`.
- Queries: capability search, version/dependency graph, maturity evidence, reuse candidates, affected recipes.
- Events: `CapabilityRegistered`, `SkillDrafted`, `NecessityDecisionRecorded`, `SkillEvaluated`, `SkillPromoted`, `SkillDeprecated`, `SkillRedundancyDetected`.
- Persistence: registry and design records in Harness IR/global registry store; packages and evaluation receipts in CAS.

## Dependency, Invalidation, Idempotency, Resume

Skill versions are immutable. A new version invalidates no existing recipe until explicitly rebound. Revocation invalidates bound recipes/capsules and routes to repair. Registration key is `(skill_id, semantic_version, package_hash)`. Evaluation resumes by case/run identity without mixing generator context.

## Security And Isolation

Skill packages declare tool, source, network, secret, and reference requirements. Registry validation rejects undeclared capabilities, prompt injection that attempts authority escalation, embedded secrets, unrestricted tools, and hidden orchestration.

## Observability, Cost, And Performance

Measure registry size, reuse/adaptation/new ratios, no-op rate, redundancy clusters, evaluation stability, context footprint, per-use cost, and deprecation impact. Search target is p95 under 500 ms for 10,000 skills; semantic retrieval is advisory and deterministic filters remain authoritative.

## Failures And Recovery

Unproven gaps reject new-skill promotion. Evaluation regression moves a skill to `REVOKED` or prior maturity and invalidates consumers. Dependency cycles fail package validation. Recovery uses a new immutable version or rebinding; package history remains.

## Acceptance Tests

1. A new canonical skill requires a stored necessity decision.
2. Reuse/adaptation is selected when capability equivalence is proven.
3. Draft or prototype skills cannot enter production recipes.
4. Package hash must match the evaluated artifact identity.
5. Leading-word changes trigger behavioral re-evaluation.
6. Duplicate capabilities are detected without automatic destructive merge.
7. Hidden orchestration or undeclared tool grants fail validation.
8. Revocation finds every dependent recipe and capsule.

## Implementation Tasks

1. Define capability, skill, design brief, necessity, maturity, and package schemas.
2. Implement registry indexes and dependency graph.
3. Implement deterministic package validator and content hashing.
4. Implement necessity/reuse workflow and human approval.
5. Integrate behavioral evaluation receipts from TS-10.
6. Seed only ratified Format 02 capabilities after BD-010.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Represent conversational parsing and recompilation capabilities without hiding workflows in skills | skill_registry_owner | Skills perform bounded syntax/expression tasks; workflow orchestration and authority stay deterministic | capability declarations for Activative Call parsing, Reaction Receipt validation, Expression Moment extraction, and recompile recommendation | Missing evaluated capability blocks profile promotion; a monolithic interview skill fails HG-011 | capability-gap, maturity, and hidden-workflow tests | Required capabilities have explicit owners, inputs, outputs, evaluations, and no execution authority | Additive capability taxonomy; seed identities remain blocked by BD-010 |

## Non-Goals And Migration

No migration of legacy design briefs or assumed V2.1 skills occurs. Large briefs may inform future designs only when supplied as authoritative evidence.
