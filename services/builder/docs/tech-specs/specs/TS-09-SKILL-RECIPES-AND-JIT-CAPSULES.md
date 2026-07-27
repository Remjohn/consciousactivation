# TS-09: Skill Composition Recipes And JIT Execution Capsules

Status: `IMPLEMENTATION_SPEC_COMPLETE_PENDING_BD-010`

## Traceability

- Owned: FR-091 through FR-102.
- Decisions: D012, D017, D018, D019, D020, D021, D027, D033.
- Supporting NFRs: NFR-PERF-002, NFR-PERF-003, NFR-PORT-002, NFR-REL-001, NFR-TRACE-003.

## Responsibility And Authority

Own harness-local adaptations, recipes, binding schemas, deterministic capsule assembly, dependency/authority/precedence resolution, degradation, Minimum Complete Context, immutable package identity, and ephemeral lifecycle. It does not author canonical skills, select creative policy, or execute provider models.

Deterministic code owns all resolution, loading, budget, assembly, hashing, and receipts. Agents execute only after a capsule is compiled. Humans approve degradation that changes creative policy or risk.

## Modules And Components

`skills/adaptation.py`, `skills/recipe.py`, `skills/bindings.py`, `skills/resolver.py`, `skills/capsule_compiler.py`, `skills/degradation.py`, and `application/capsule_commands.py`.

## Canonical Data Structures

- `SkillAdaptation { adaptation_id, canonical_skill_ref, harness_ref, ontology_bindings, allowed_mutations, local_failures, evaluator_overrides }`
- `CompositionRecipe { recipe_id, phase_ref, skills, adaptations, bindings_schema, conditions, references, context_policy_ref, output_contract_ref, evaluator_refs }`
- `BindingValue { key, value, authority, precedence, evidence_ref?, invalidates, degradation_policy? }`
- `ExecutionCapsule { capsule_id, recipe_ref, resolved_versions, active_instructions, context_manifest, references, tool_grants, model_policy, output_contract, completion, evaluators, expires_at, receipt_ref }`
- `CapsuleReceipt { input_hashes, resolution_trace, omitted_branches, degradation, compiler_version, capsule_hash }`

## APIs, Commands, Events, Persistence

- Commands: `RegisterAdaptation`, `ValidateRecipe`, `ResolveBindings`, `CompileCapsule`, `ExpireCapsule`, `RevokeCapsule`.
- Events: `AdaptationRegistered`, `RecipeValidated`, `BindingsResolved`, `CapsuleCompiled`, `CapsuleDegraded`, `CapsuleExpired`, `CapsuleRevoked`.
- Persistence: recipes/adaptations in Harness IR; capsules and receipts in CAS with metadata index. Capsules are immutable and phase-local.
- Compilation interface: `compile(recipe_ref, binding_set, phase_context, policy_versions) -> ExecutionCapsule`.

## Dependency, Invalidation, Idempotency, Resume

All required bindings and exact skill versions resolve before compilation. Authority and precedence conflicts block. Cache key includes recipe, skills, adaptations, bindings, context manifest, references, model policy, compiler, and degradation approvals. Changed inputs yield a new capsule and revoke stale pending use. Execution resume may reuse a capsule only before expiry and with identical input identities.

## Security And Isolation

Tool, source, secret, and network grants are explicit and least privilege. Capsules cannot embed persistent secrets or protected labels. Compiler runs without model access. Execution environments verify capsule hash and grants before invocation.

## Observability, Cost, And Performance

Record compile latency, context tokens/bytes, omitted references, cache hits, degradation, tool grants, estimated model cost, execution outcome, and evaluator identity. Context overflow blocks unless a pre-approved typed degradation applies.

## Failures And Recovery

Unresolved binding, precedence conflict, immature skill, missing reference, expired capsule, or output-contract mismatch fails closed. Repair returns to the owning binding, recipe, skill, or context node; it never patches compiled text in place.

## Acceptance Tests

1. Same inputs compile a byte-identical capsule and receipt.
2. Draft/revoked skill identities are rejected.
3. Precedence conflict blocks before capsule creation.
4. Required context is never silently truncated.
5. Inactive branches are absent and listed in the receipt.
6. Capsule grants match declared phase needs and no more.
7. Expired/revoked capsules cannot execute.
8. Output-contract failure routes to the responsible recipe/binding node.

## Implementation Tasks

1. Define adaptation, recipe, binding, capsule, and receipt schemas.
2. Implement dependency, authority, precedence, and degradation resolver.
3. Implement deterministic context assembler and capsule serializer.
4. Implement lifecycle, expiry, revocation, and execution verification ports.
5. Add golden, conflict, context-budget, security, and replay tests.
6. Bind exact evaluation identities from TS-10.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Compile minimum conversational/visual context while retaining rich lineage | capsule_compiler_owner | Capsule gets task-minimum tokens; canonical IR retains frozen rich objects | sparse token plus immutable rich-object refs and policy/version pins | Block required-context overflow or missing lineage; never silently truncate | sparse-token resolution, budget overflow, and stale-ref fixtures | Capsule is minimal, reproducible, and resolves all authority-bearing values | Existing capsules require recompilation under the V1.2 schema; canonical source objects remain unchanged |

## Non-Goals And Migration

No provider/model runtime, universal prompt builder, legacy brief migration, or hidden workflow orchestration is included.
