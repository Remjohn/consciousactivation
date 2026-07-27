# TS-VAE-02 Dynamic Workcell and Capability Routing

Status: draft for architecture validation  
Implementation authorization: no

## 1. Specification identity

- Features: F06, F07
- Owned FRs: FR-041 through FR-056
- Owned NFRs: NFR-WORKFLOW-001 through NFR-WORKFLOW-005
- Decisions: D002, D005, D010
- Components: `WorkcellCompiler`, `RoutePlanner`, `CapabilityResolver`, `SourcePolicyService`, `AssetCommanderPolicy`, specialist actor adapters

## 2. Evidence read

VAE F06/F07 shards, Workcell Authority Registry, Budget Program Registry, plan schema/fixture, preservation/prohibition contracts, capability requirements in Format 02, Delegation authority matrix/failure taxonomy, and Stage 1 coverage/ADR registers.

## 3. Problem, solution, and scope

The VAE needs the smallest sufficient governed team and production route for each accepted demand. A fixed chain wastes cost and a general creative agent blurs authority. The solution is a deterministic `WorkcellCompiler` that activates registered authorities from plan requirements and a `RoutePlanner` that ranks eligible reuse, transform, generate, composite, and hybrid routes using certified evidence.

In scope: authority registry, specialist activation, route eligibility/ranking, hybrid/fallback routes, source/control preparation, route receipts, and effectiveness evidence. Out of scope: redefining demand meaning, provider graph compilation, direct GPU execution, production evaluation, and self-modifying routing policy.

## 4. Brownfield alignment

Retain explicit human/agent/code/evaluator ownership, the Builder Workflow Runtime actor model, deterministic policy services, and exception-only human intervention. The existing `WORKCELL_AUTHORITY_REGISTRY.yaml` is the seed. It is not executable until each authority maps to a typed actor interface and runtime node.

## 5. Components and canonical models

| Component | Responsibility |
|---|---|
| `WorkcellCompiler` | Convert plan requirements into the minimal authority-safe actor set and node permissions. |
| `RoutePlanner` | Produce and compare eligible production routes with evidence, fallback, cost, latency, and risk. |
| `CapabilityResolver` | Query TS-VAE-03 for compatible certified capability bundles. |
| `SourcePolicyService` | Deterministically classify source/reference eligibility and provenance requirements. |
| `AssetCommanderPolicy` | Enforce state, budget, evaluator invocation, repair limits, promotion, and typed exceptions; never create assets. |
| Specialist adapters | Execute bounded analysis/materialization/evaluation contracts under the authority registry. |

`WorkcellPlan` fields: ID/version/hash, demand/plan refs, activated actors, omitted actors/reason, node-to-actor map, per-actor input/output schemas, read/write authority paths, tool/capability grants, context refs, time/budget limits, evaluator separation, human-exception conditions, and registry snapshot.

`RouteOption` fields: strategy, stages, capability requirements, eligibility predicates, expected quality evidence, risk, estimated cost/time, fallback triggers, provenance obligations, and certification scope.

`RoutingDecision` fields: eligible options, rejected options/reasons, selected route, comparison profile, evidence refs, budget fit, uncertainty, policy/compiler versions, and immutable receipt hash.

## 6. Workflow and state machine

Routing states are `REQUIREMENTS_RECEIVED`, `WORKCELL_COMPILED`, `ROUTES_ENUMERATED`, `ELIGIBILITY_RESOLVED`, `ROUTE_SELECTED`, `BLOCKED_CAPABILITY`, `BLOCKED_AUTHORITY`, and `SUPERSEDED`. Only the selected route is bound into a new plan version; alternatives remain evidence.

Successful flow: read plan -> resolve required authorities -> compile minimal workcell -> enumerate routes -> apply authority/certification/compatibility filters -> estimate -> select least-complex reliable route -> persist receipt -> return route binding.

Fallback flow does not mutate the selected route in place. A typed trigger creates a new routing decision and plan version. Capability gap or unresolved authority emits Delegation failure/conflict and checkpoints the run.

## 7. Interfaces, API, queues, events, and integration contract

```text
compile_workcell(plan_ref, authority_registry_version) -> WorkcellPlanRef
enumerate_routes(plan_ref, memory_evidence_refs) -> RouteOption[]
select_route(options, capability_snapshot, budget_ref, policy_version) -> RoutingDecisionRef
replan(trigger, prior_decision_ref, preserved_outputs) -> RoutingDecisionRef
```

Events: `WorkcellCompiled`, `RouteOptionRejected`, `RouteSelected`, `FallbackRequested`, `CapabilityGapDetected`, `AuthorityViolationBlocked`. Commands and events use exact immutable refs and run through `WorkflowRuntimePort`.

The internal API accepts only immutable plan/registry/budget references. Queue payloads carry the selected actor authority, required input hashes, deadline, idempotency key, and expected output schema; they never carry free-form authority changes.

| Concern | Required behavior |
|---|---|
| Visual Production Plan IR | Workcell and route are versioned bindings to TS-VAE-01; they never replace the plan. |
| Provider adapters/ComfyUI | Routes name provider-neutral capabilities. TS-VAE-03 performs graph compilation after selection. |
| Docker/model/VAE/LoRA registries | Eligibility requires compatible, pinned, mature registry entries; no raw filenames or mutable tags. |
| GPU/storage | Estimated resource classes come from runtime profiles; actual scheduling belongs to TS-VAE-04. |
| Deterministic/VLM | Authority, eligibility, compatibility, budget, provenance, and route policy are deterministic. Bounded model analysis may estimate visual uncertainty but cannot grant eligibility. |
| Budget/candidates | Route estimates and portfolio classes are checked by TS-VAE-05 before binding. |
| Evaluation | Independent evaluator actor is mandatory when profile requires it and cannot be the materializer. |
| Repair | Route defines typed fallback triggers; blind retry is prohibited. TS-VAE-07 owns repair. |
| Idempotency/checkpoints | Identical plan + registry + policy hashes produce one decision. Workcell and route receipts are checkpoints. |
| Observability/cost | Persist activation reasons, rejected routes, estimate, selected route, fallback, and realized effectiveness. |
| Security | Actor grants are least-privilege and scoped to exact run/objects/tools; model actors receive Minimum Complete Context only. |
| Migration/rollback | Registry/policy version changes affect new decisions only. Active runs retain pinned snapshots; rollback reuses the recorded compiler. |

## 8. Detailed behavioral rules

1. Activate only actors required by plan stages, uncertainty, source needs, and evaluation policy.
2. `AssetCommanderPolicy` may route and enforce but cannot reinterpret meaning, create assets, or approve quality.
3. Semantic interpretation is bounded to translating demand-owned fields into visible requirements and failure indicators.
4. Feasibility analysis returns measurable geometry/control evidence and cannot change composition intent.
5. Strategy and materialization are separate actor authorities.
6. Source classification, registry checks, hashes, license/provenance policy, and compatibility are deterministic services.
7. A route is eligible only if all mandatory capabilities are available, compatible, mature for the category/profile, and affordable within authorization.
8. Prefer valid reuse, then deterministic transform, then the least-complex certified production path capable of passing gates; preference never overrides quality evidence.
9. Hybrid routes identify each stage owner and preserve derivation lineage.
10. Fallbacks require causal triggers such as identity drift, control failure, provider outage, or repair evidence. Unchanged random retries are invalid.
11. Routing effectiveness updates evidence stores but never changes production policy without versioned review/promotion.
12. Human participation occurs only for a registered authority exception, not routine route approval.

## 9. Failure, recovery, performance, and security

Missing certified capability yields `CAPABILITY_GAP`; authority collision yields an authority failure; insufficient source evidence yields a feasibility conflict. Registry outages retry as infrastructure failures with identical inputs. A worker/provider failure may select a predeclared compatible fallback without consuming a quality round. Quality failure routes to TS-VAE-07.

Routing must complete within the planning budget and expose per-stage latency. It may cache immutable registry/memory snapshots by hash. Cache hits must reproduce the same decision. No route can exceed candidate, parallelism, GPU, cost, wall-clock, evaluator, or experimental ceilings.

Untrusted references are never passed directly to model/tool adapters. Actor contexts contain only authorized fields; secrets and other tenants' evidence are excluded. Tool calls, context manifests, and outputs are receipted.

## 10. Compatibility and migration

Actor interfaces and route strategies are versioned. Minor additions may introduce optional actors/routes but cannot change existing authority. Major authority or route semantics require migration and updated conformance fixtures. Deprecated routes remain readable for historical reproduction; active runs do not adopt a newer policy/registry.

## 11. Implementation plan

1. Close and version authority, actor, route, workcell, and routing-receipt schemas.
2. Implement registry-backed deterministic workcell compilation.
3. Implement route enumeration and eligibility filters for reuse, transform, generation, composite, and hybrid.
4. Implement evidence-based ranking and budget/capability integration.
5. Register actor node types through `WorkflowRuntimePort`.
6. Implement fallback/replan and typed blocker events.
7. Add route effectiveness receipts, policy promotion tests, and rollback fixtures.

## 12. Given/When/Then acceptance criteria

1. Given a reuse candidate satisfying identity, role, geometry, and freshness, when routes are selected, then reuse is eligible and a more complex route requires explicit evidence.
2. Given no source retrieval requirement, when workcell compiles, then `asset_intelligence_hunter` is omitted with a reason.
3. Given a materializer and evaluator with the same model identity, when workcell validates, then execution is blocked.
4. Given an uncertified LoRA required by a route, when eligibility runs under Standard, then the route is rejected.
5. Given a provider timeout, when a compatible fallback is declared, then a new route decision is created without consuming a quality round.
6. Given a quality failure without causal evidence, when replan is requested, then blind retry is rejected.
7. Given identical plan/registry/policy inputs, when routing repeats after restart, then the same workcell and routing hashes are returned.
8. Given a model actor attempts to change semantic intent, when output validation runs, then the mutation is blocked and audited.

## 13. Testing strategy

Unit-test authority path resolution, minimal actor sets, eligibility predicates, route comparison, and deterministic hashes. Integration-test registry/budget/runtime ports, fallback, restart, and cache. Use mutation tests for actor overreach, uncertified capability, budget bypass, same-producer evaluation, and silent policy updates. Benchmark route quality/cost against controls and verify historical decisions under migration/rollback.

## 14. Constitutional alignment V1.1 addendum

Workcell compilation and routing consume the constitution-complete plan bindings produced by TS-VAE-01. They may translate those bindings into capability requirements, but they may not select or repair upstream meaning.

The required routing context includes immutable references and hashes for the Activation Contract, Visual Semantic Pack, Semiotic MCDA receipt, Visual Narrative Program, applicable Feature Contracts, T/V request, Composition Intent, and wrong-reading locks. Route eligibility fails when any applicable binding is absent, open-ended, unsupported by the route, or would be dropped by an actor.

Routing applies the following precedence:

1. the selected recognition carrier and viewer role come from authoritative upstream contracts;
2. narrative and feature obligations constrain eligible route families;
3. T/V codes are applied only after carrier and narrative are known and cannot be used to invent either;
4. Composition Intent constrains geometry and capability selection while exact composition remains VAE-owned;
5. every materializer declares which Feature Contracts and wrong-reading locks it can enforce;
6. a parseable route that cannot enforce a mandatory semantic behavior is ineligible.

The WorkcellPlan grants each actor only the authoritative slices it needs and records an input-to-output preservation map. A strategy or materializer that proposes a different recognition carrier, viewer role, activation direction, narrative program, meaning-bearing feature, or wrong-reading interpretation is an authority violation, not a creative alternative.

Additional tests cover missing constitutional bindings, attempted T/V-led narrative selection, feature-contract loss, empty locks, and a provider route that accepts syntax but cannot enforce required behavior.

## 15. Non-goals

- A general visual-editor agent or fixed mandatory specialist chain.
- A standalone routine rights analyst.
- Model-driven authority, compatibility, budget, or lifecycle decisions.
- Runtime self-modification from one successful or failed demand.
