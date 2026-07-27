# TS-AHP-004 - Workflow Node Kernel, Deterministic Scheduler, Bounded Roles, and Handoffs

```yaml
spec_id: TS-AHP-004
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product: Atomic Harness Pipeline
primary_owner: Atomic Harness Pipeline
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: INDEPENDENT_AUDIT_REQUIRED
writing_wave: 13
controlling_stories: [AIR-ST-19.02, ST-03.04]
controlling_frs: [AIR-FR-112, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-137]
```

This is a specification-only candidate. It does not make V2.1 candidate authority current, authorize implementation, issue a Development Capsule, activate Format 02, begin VAE Stage 5, create shared contract release bytes, or permit an `ACCEPTED_FOR_BUILD`, production, publication, or certification claim.

## 1. Files and authorities read

### 1.1 Admitted Wave 13 draft interfaces

Both upstream drafts are exact, readable, and admitted only under `DRAFT_DEPENDENCY_NOT_ACCEPTED`:

| Edge | Upstream draft | State / SHA-256 | Interface used | Downstream revision impact |
|---|---|---|---|---|
| `SDE-064` | `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-002.md` | `WRITTEN_PENDING_AUDIT`; `3e76ee7e4ec8f3b288a58bb8b8eb886195d9ad17097c67ded613c22fbb3dccd4` | Exact `HarnessRequirementGraphProjection`, `HarnessExecutionBindingManifest`, node/edge, capability, ownership, handoff, evaluation, repair-law, category/profile, authority, lineage, and semantic-parity references. | A hash or accepted-interface change reopens sections 3, 5, 6, 8, 9, and 10. |
| `SDE-065` | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-019.md` | `WRITTEN_PENDING_AUDIT`; `515e42a7e015c212f9f972b4e78e1e7aa0558816448f10ff18db9b9a7f7ecd5e` | Exact AIR failure-attribution, Semantic Repair Program, Repair Referral, Role Semantic Context Requirement, semantic-preservation, JIT conformance, failure-state, and Pipeline handoff interfaces. | A hash or accepted-interface change reopens sections 3, 5, 6, 8, 9, and 10. |

Neither draft is ratified authority. This document consumes their frozen public interfaces for dependency-safe writing and does not represent their details as settled law.

### 1.2 Authority, requirements, source, and brownfield evidence

| Source | State / SHA-256 | Class | Specific fact used |
|---|---|---|---|
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3; `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | required method | One writer writes one spec and cannot audit, revise, accept, build, or issue a capsule. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | recovery packet; `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | required packet | Packet `CA-P03-WRITE-TS-AHP-004-RECOVERY` fixes eight FRs, two Stories, exact path, Wave 13, ownership, dependencies, and claim ceiling. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_13_DISPATCH_LOCK.yaml` | Wave 13; `cbf921af042212cd2fe2f43de067c7145bd931314232bb16bb8120b44135f729` | required dispatch lock | Pins both admitted upstream draft identities. |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1; `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | highest current authority | Pipeline executes format harnesses and repairs the first failed layer without inventing source, role, edge, Primitive, narrative, composition, or human meaning. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate pending ratification; `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | candidate ownership | Pipeline owns workflow nodes, runtime bindings, JIT state, receipts, evaluation control, and selective-repair execution; AIR owns semantic lifecycle/program meaning. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate pending ratification; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | candidate object ownership | Pipeline owns runtime execution state and selective-repair plan; Builder owns `AtomicHarnessDefinition`; AIR owns semantic programs; independent evaluation owns its receipts. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | frozen Prompt 02; `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | required queue | TS-AHP-004 is the canonical queued workflow-kernel specification. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | frozen Prompt 02; `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | required traceability | Fixes the eight controlling FRs, owners, Stories, gate, and claim ceiling. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | frozen Prompt 02; `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | required traceability | Requires graph/scheduler/handoff/role/receipt evidence and assigns AIR-FR-112 implementation ownership to Pipeline. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | current; `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | required source policy | All current implementation and unique evidence used below is byte-available and hash-locked. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPEC_DEPENDENCY_EDGE_CLASSIFICATION.yaml` | Prompt 02C; `4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8` | required dependency policy | Both edges are WRITE-interface dependencies; build acceptance is not a WRITE gate. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | specification only; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | write authorization | Candidate-authority writing and technical convergence are allowed; implementation/build/production remain forbidden. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/spec_assignments/TS-AHP-004.md` | assignment brief; `290407f26cd0f2ab6b5d6aa22d683562df3589a580d8ffac41b3bd8ca1c56d3b` | required assignment | Requires explicit nodes, deterministic scheduling, bounded roles, handoffs, current Builder sources, predecessor adaptation, and exact implementation/test paths. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/EPICS_AND_VERTICAL_STORIES.md` | candidate; `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | required Story | ST-03.04 requires explicit actor/owner/role/product nodes, contract-valid handoffs, replay evidence, denial before side effects, and descendant-only recovery. |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/planning/EPICS_AND_VERTICAL_STORIES.md` | candidate; `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | required Story | AIR-ST-19.02 requires bounded repair, exact roles and handoffs, descendant-only invalidation, replay, and no fabricated authority. |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/AHP_F03_BOUNDED_ROLE_TAXONOMY.md` | `SRC-AHP-F03-001`; `1d50940d7313b89331e872b63393276267e698cb5908254479e216a234f3ec77` | required unique evidence | Actor, capability owner, workflow role, and product boundary are independent; Pipeline owns scheduling, handoffs, JIT state, and immutable node receipts. |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/AHP_F16_EVALUATION_REPAIR.md` | `SRC-AHP-F16-001`; `0a247a2025ef803df09e8bfc97b9456d73a64cf2f867598135b3c8ba03a668e2` | required unique evidence | Failure is attributed before repair; producer cannot self-approve; repair changes declared units and descendants only. |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/ai_v2_predecessor/contracts/11_FAILURE_ATTRIBUTION_AND_REPAIR_PROGRAM.md` | `SRC-AI2-REPAIR-001`; `b25670847d79678eb0d269656afe38cd45d0a9244b47d5051dea931379ec2ae7` | required unique evidence | Repair evidence must identify failed object/layer, root cause, frozen upstreams, change target, descendants, invalidation, rerun, evaluation, and human escalation. |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` | `SRC-INT-001`; `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | required unique evidence | Complete Expression Sessions and Expression Moments feed multiple downstream assets; backend roles organize/route while guests retain truth authority. |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/brownfield/CMF_STUDIO_PREDECESSOR_MIGRATION_AUDIT_V1.md` | `SRC-MIG-001`; `5912930b2abfb376aef67c140bb745845ede054b07ad6aa0e9bb77f9a06301d7` | required unique evidence | Extract Pipeline recipe/run/step/gate patterns, but replace monolithic Studio authority, hidden personas, fake execution, old formats, and in-memory state. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/category_runtime_rules.py` | `SRC-CUR-007`; `cef3bf6673bde2ec501c01099f0efee12b7ad47cb8379c68a58b074a13c35512` | required current implementation | Declares five category-native runtime/evaluation/repair-unit contracts, selective-rerun laws, explicit `NOT_APPLICABLE`, and false production/certification. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/capability_ownership.py` | `SRC-CUR-008`; `14ba709cf693c117560cb4f326b9a5708391475aabe1c2030ce69b20283ee36e` | required current implementation | Capability ownership has explicit kinds, evidence, boundaries, and ordered handoff participants, but current implementation is synthetic CODE-only. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/workflow/actor_explicit_contracts.py` | `SRC-CUR-010`; `9dc8aaf8aa2085aff66adda56faf891fc260287e04e0ca0c35681934126e4399` | required current implementation | Provides an immutable execution-free DAG seed with bilateral typed edges, actor kinds, authority, deterministic identity, and invalidation receipt. |
| `01_ATOMIC_HARNESS_BUILDER/tests/stories/st_09_01/test_actor_explicit_workflow.py` | current evidence; `1996273d226da7f2f233912b2dafa7626e3acc3d1beaa006e5f20aa05ac9fce9` | behavior evidence | Proves actor-kind separation, contract handoffs, order-stable identity, cycle/hidden execution/human-decision replay denial, and non-production status. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/studio_pipeline_recipe_harness.py` | `SRC-LEG-001`; `fd9a613463c71c9e0f1a0ce3b4ba0cd479b7553ead53a50d6d678d72386e81b8` | required predecessor evidence | Useful step/run/gate/artifact vocabulary is mixed with random/time identity, open dictionaries, mutable state, legacy routes, and incomplete graph law. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/pipeline_run_service.py` | `SRC-LEG-002`; `cede54a5f4bf09f047ffdbacc8f3427cfa197306aebc84c0c1950ff87a185021` | required predecessor evidence | Creates planned/blocked runs and step rows but performs a lone mutable upsert with no command/receipt/edge atomicity. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/pipeline_step_run_service.py` | `SRC-LEG-003`; `90c568b255b0d27fe3430f8b4edd7da01cce202cd46f9ec36a916dae2ed362db` | required predecessor evidence | Checks predecessor success and approval state, then mutates a step in memory and returns an unpersisted receipt. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/repositories/studio_pipeline_recipe_harness.py` | predecessor repository; `6c4d79325853836b5a28e6598fe9256b0b4fe0867d6b5f99f2d90ccf41e98755` | direct implementation evidence | Separate untyped dictionaries and unrestricted `upsert` cannot guarantee state/artifact/receipt/edge parity or concurrency. |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_studio_pipeline_recipe_harness_v1.py` | predecessor tests; `dff010a57d343e039037ac7c2eb73168983829eb01c945d8f3f63536b8b17ff8` | test evidence | Covers missing dependencies/gates and recipes but not global cycles, deterministic ready order, four classifications, atomicity, or descendant invalidation. |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_pipeline_recipe_orchestration_spine_integration_v1.py` | predecessor tests; `f3ac2554c8e02e751fc96bd2b347f3a55cff2c43c91c996894052938062f82bc` | test evidence | Proves a declarative spine and blocked provider/renderer calls, not execution trust. |

The output is a `DIRECT_PRODUCT_SPEC_PATH`. No `AGENTS.md` exists at the workspace root or under `05_ATOMIC_HARNESS_PIPELINE`; the Prompt 02/02C path-authority decision expressly permits this one specification path. The Builder and AIR-bundle `AGENTS.md` files were read for source/product boundaries; neither permits their product files to be modified by this task.

## 2. Problem, user outcome, solution, and scope

### Problem

A list of steps is not an execution kernel. The current Builder can compile an execution-free actor-explicit DAG, while the predecessor Studio can instantiate mutable step rows and mark them succeeded. Neither supplies a durable Pipeline runtime that proves four independent classifications per node, chooses ready work deterministically, validates the exact producer output before a handoff, commits state and receipts atomically, exposes humans/external products as nodes, or invalidates only the descendants of an exact changed dependency.

The failure becomes more dangerous during repair. AIR may correctly attribute a semantic or execution failure and constrain a semantic repair, but if Pipeline treats AIR's suspected descendants as runtime graph truth, rewrites the failure meaning, or expands a permitted field set while planning reruns, the executor becomes a hidden semantic authority. Conversely, AIR must not compute Pipeline's runtime dependency traversal, checkpoint reuse, node IDs, provider choices, or scheduling order.

### User and system outcome

A Pipeline operator can load one exact eligible Harness binding, compile a runtime workflow projection without changing its meaning, and execute explicit nodes whose actor, capability owner, role, and product boundary are independently visible. Ready-node selection is reproducible. Every handoff is contract-validated. Humans and external products are first-class boundary nodes. Every attempt, including denial/cancellation, has an immutable receipt. When a governed failure or supersession occurs, Pipeline computes the exact descendant closure from its own frozen runtime graph, preserves valid checkpoints and history, and reruns only authorized affected work while retaining AIR's failure and repair semantics unchanged.

### Bounded solution

Define:

1. an immutable Pipeline `RuntimeWorkflowGraph` projected from TS-AHP-002 without semantic overrides;
2. a four-axis node classification and bounded role registry;
3. a deterministic, gate-aware scheduler with explicit parallelism and side-effect policy;
4. typed JIT context, command, attempt, handoff, event, artifact, and receipt contracts;
5. a Pipeline-owned runtime dependency graph, invalidation traversal, checkpoint-reuse decision, and selective-repair plan;
6. a strict AIR consumer boundary that validates `FailureAttribution`, `SemanticRepairProgram`, `RepairReferral`, and `RoleSemanticContextRequirement` without reinterpreting them;
7. atomic persistence, idempotency, optimistic concurrency, replay, cancellation, migration, recovery, and observability rules.

### In scope

- AIR-FR-112; FR-013 through FR-018; FR-137.
- AIR-ST-19.02 and ST-03.04, including primary, adversarial, replay, CBAR, and selective-recovery criteria.
- Explicit phase/node compilation, four independent classifications, ready ordering, safe parallelism, gates, typed handoffs, humans/products, node attempts, and receipts.
- Hunter, Analyst, Composer, and Commander as bounded workflow roles, never personas or autonomous owners.
- Pipeline-owned runtime dependency graph, invalidation, repair execution plan, JIT capsule, checkpoint reuse, and rerun scheduling.
- Exact failure/repair handoff from AIR and exact immutable result/receipt observation back to AIR.

### Out of scope and non-goals

- Compiling or changing `AtomicHarnessDefinition`, AIR failure attribution, AIR semantic repair meaning, Primitive/archetype/Edge Product/Final Script meaning, Interview truth, VAE production strategy, Delegation transport semantics, or Studio human decisions.
- Inventing an AIR cause, collapsing `CONTESTED`/`UNRESOLVED`, widening a semantic mutation scope, or treating an AIR referral as execution authorization.
- Implementing evaluation, diagnosis, or repair semantics owned by TS-EVAL-001/002/003; this kernel schedules their explicit nodes and preserves their receipts.
- Treating a workflow role as an actor, model, capability owner, product owner, or authority grant.
- Activating a historical recipe or Format 02 path, making provider/renderer/model calls during writing, or asserting production/certification.
- Creating source, schemas, generated types, tests, migrations, contract release bytes, or runtime artifacts in this prompt.

## 3. Governing decisions and constraints

### 3.1 Current and candidate authority

Constitution V1.1 and current product PRDs remain binding. The V2.1 matrices and both upstream specs are `CANDIDATE_NOT_CURRENT`. Their interfaces are usable only because specification work is explicitly authorized. This spec ends at `WRITTEN_PENDING_AUDIT`; build authority remains false, and the maximum later pre-ratification state is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.

### 3.2 Object ownership

| Object or decision | Owner | Pipeline behavior | Forbidden Pipeline behavior |
|---|---|---|---|
| `AtomicHarnessDefinition` | Atomic Harness Builder | consume exact immutable ref through the TS-AHP-002 binding | modify phases, capability requirements, semantic intent, evaluation, or repair laws |
| Semantic lineage and production-program meaning | AIR / exact human value owner | preserve exact refs, epistemic state, versions, hashes, locks, and limitations | reconstruct missing meaning or upgrade inference to observation |
| `FailureAttribution` and `SemanticRepairProgram` meaning | AIR under exact authority | validate exact bytes and compile runtime execution constraints | choose a different cause, hide alternatives, alter target/permitted/forbidden/preserved sets |
| Runtime workflow, node attempts, JIT state, dependency graph, invalidation and rerun plan | Atomic Harness Pipeline | author immutable execution artifacts and receipts | represent them as AIR-authored semantic facts |
| Live source, Reaction Receipts, Expression Moments | Interview Expression / human source authority | reference and validate required evidence | manufacture or rewrite human truth |
| Independent evaluation receipt | Independent Evaluation | schedule/collect/validate exact receipt | let producer self-approve or reinterpret evaluator meaning |
| Visual production plan/repair/production acceptance | VAE | use explicit external-product nodes and immutable results | choose VAE internals or equate transport/consumption with production acceptance |
| Transport lifecycle | Delegation Protocol | submit/observe typed envelope receipts | treat submission as owner acceptance or semantic success |
| Human resolution | attributable human; Studio captures/projections | block on explicit human node and consume exact scoped decision | replay historical approval as new authority |

`Activative Contract Compiler != Activative Intelligence Runtime`. Builder declares dependencies; AIR owns semantic meaning; Pipeline executes.

### 3.3 Four independent classifications

Every runtime node has all four, stored in separate typed fields:

1. **Execution actor:** the actual code module, Programmed Model, Agent Program, human, or external-product boundary actor.
2. **Capability ownership class:** `CODE`, `AGENT`, `HUMAN`, `EXTERNAL`, or `HYBRID`, copied from an eligible ownership decision.
3. **Workflow role:** a governed role such as `HUNTER`, `ANALYST`, `COMPOSER`, `COMMANDER`, or an evidenced `NOT_APPLICABLE_BY_RULE` for nodes not assigned a bounded production role.
4. **Product boundary:** the product whose local lifecycle owns the node result/failure.

No field defaults from another. `HUNTER` does not imply an AI actor; `HUMAN` does not imply Commander; a Pipeline actor does not imply Pipeline owns the input meaning; and an external product cannot be hidden as a tool call.

### 3.4 Bounded-role law

- **Hunter:** discovers missing/conflicting evidence within admitted source classes; cannot approve source truth, semantic meaning, or repair authority.
- **Analyst:** compares exact evidence, causal candidates, contradictions, and exclusions; cannot mutate the target or resolve human-owned ambiguity.
- **Composer:** proposes/executes only the permitted bounded change from approved inputs; cannot widen scope, weaken locks, invent source meaning, or accept its own output.
- **Commander:** selects a next transition already allowed by authority, receipts, gates, stopping law, and resource envelope; cannot ratify authority, approve production, override a human gate, or reinterpret semantics.

Role names are behavior contracts, not prompt personas. Each node separately pins actor, implementation, capability, product, tools, inputs, outputs, evaluation, failure owner, and handoff.

### 3.5 Semantic repair and invalidation boundary

AIR supplies cause and semantic boundaries. Pipeline supplies runtime graph truth.

- Pipeline accepts only exact, eligible AIR artifacts. `CONTESTED` or `UNRESOLVED` cannot silently become a repair; they route to evidence acquisition or an explicit human-resolution node.
- An AIR `SemanticRepairProgram` constrains semantic change through exact target, permitted/forbidden selectors, preserved assertions, frozen refs, inherited locks, evaluation, stopping law, and escalation. Pipeline cannot edit those values.
- `pipeline_execution_constraints` are constraints, not runtime node IDs or provider selections. Pipeline computes its own immutable `RuntimeInvalidationPlan` and `RuntimeSelectiveRepairPlan` from the frozen runtime dependency graph.
- AIR's predecessor-style descendant or rerun suggestions are non-authoritative observations. Pipeline must neither copy them as graph truth nor write its computed graph back as AIR-authored data.
- A Pipeline-owned execution defect may arrive as an AIR `RepairReferral`; Pipeline must validate local authority and compile a local operational correction. Referral acknowledgement is not repair success.
- Invalidating a descendant does not grant permission to mutate it. It marks its current eligibility stale and schedules an authorized successor attempt.

### 3.6 Handoff and side-effect law

A target node becomes ready only when every required inbound edge names a current producer attempt, exact output artifact version/hash, output validation receipt, handoff contract version/hash, authority status, and gate outcome. Parsing a payload while ignoring ownership, provenance, lifecycle, validation, or failure semantics is incompatible.

Before any side effect, Pipeline atomically records the command, run/attempt state, JIT capsule ref, dispatch intent, exact idempotency identity, and outbox item. Human and external-product nodes require distinct request, transport, acknowledgement, owner acceptance/result, and consumption states. A transport receipt never satisfies an output contract by itself.

### 3.7 Determinism and portability

- Logical identities use canonical bytes, never random UUIDs, current time, dictionary insertion order, filesystem traversal order, absolute paths, environment variables, locale, or process-global state.
- Ready order is `(phase_ordinal, node_ordinal, node_id)` using exact Harness ordinals. No scheduler priority is guessed.
- Parallel eligibility is explicit: all dependencies and gates pass, declared concurrency policy permits it, side-effect/resource sets do not conflict, and no human/external ordering constraint is bypassed.
- Observed timestamps, durations, costs, external result bytes, and provider nondeterminism are explicit evidence inputs excluded from deterministic plan identity where specified.
- Replaying history uses original versions and evidence. It does not promise a remote provider will regenerate identical bytes.

### 3.8 `NOT_APPLICABLE`, source, lineage, and locks

`NOT_APPLICABLE` is never null, omission, or an unavailable dependency. It requires a governed rule ID/version/hash, evaluated facts, owner, and receipt. Actor, capability ownership class, product boundary, source lineage, authority, and required handoffs can never be N/A. A required bounded role may be N/A only where the Harness/profile explicitly says the node is not a Hunter/Analyst/Composer/Commander task.

Content-bearing JIT capsules preserve exact source kind, Reaction Receipt/Expression Moment refs where required, field epistemic state, Matrix/role/tension, Primitive/coalition/Edge Product, archetype, Identity/Voice/Visual DNA, Final Script, transfer, Composition Intent, Feature Contracts, T/V routes, and wrong-reading locks. Pipeline does not flatten them into generic context text. Descendants inherit locks; relaxing one requires a new authorized upstream version.

## 4. Current brownfield architecture

| Exact artifact / symbol | Actual behavior | Disposition | Required correction |
|---|---|---|---|
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/workflow/actor_explicit_contracts.py::ActorExplicitWorkflowIR` | Frozen, execution-free DAG; four actor kinds; bilateral edges; sorted identity; cycle and hidden-execution denial; development-only claim. | `ADAPT` | Consume through TS-AHP-002; add runtime actor binding, capability class, role and product boundary as independent fields, durable attempts, gates, scheduler, dependency snapshots, JIT, receipts, and runtime invalidation. Never import Builder code as Pipeline authority. |
| `WorkflowNode` / `WorkflowEdge` | Node owner and actor kind are explicit; edge contract equality and validation flag are enforced. Defaults can derive profile/entry/terminal/source refs; role/capability/product are not separate. | `ADAPT` | Require exact source projection and four classifications; reject inferred current authority and execute only through a Pipeline-owned projection. |
| `WorkflowInvalidationReceipt` | Records an affected scope but does not prove descendant traversal or persistence. | `REPLACE` | Use a frozen Pipeline dependency graph, trigger, traversal proof, preserved checkpoints, invalidated current projections, and historical parity. |
| `capability_ownership.py` | Strong frozen ownership decision shape, but active graph is hard-coded to three synthetic CODE capabilities and non-production status. | `ADAPT` | Bind exact eligible decisions from the Harness/registry; support all governed classes without generalizing synthetic constants. |
| `category_runtime_rules.py` | Declares five categories, category-native runtime requirements, repair units, rerun rules, invalidation triggers, explicit N/A, and no inherited certification. | `REUSE_AS_CONTRACT_EVIDENCE` | Consume exact category/profile rule refs; Pipeline does not copy the Builder registry or activate uncertified formats. |
| `studio_pipeline_recipe_harness.py` | Pydantic step/run/gate/artifact vocabulary, local dependency lists, approval gates, random IDs, wall-clock defaults, mutable lists/open dicts, legacy route IDs, and coarse statuses. | `ADAPT` | Preserve fixtures/vocabulary only; replace identities, typing, graph law, lifecycle, role/authority fields, and semantic assumptions. Historical Format 02 remains historical/reference-only. |
| `pipeline_run_service.py` | Builds mutable step runs and performs one in-memory `upsert`; missing orchestration ID blocks. | `REPLACE` | Commanded aggregate with exact binding/graph, atomic state/artifact/receipt/edge/outbox commit, idempotency, and concurrency. |
| `pipeline_step_run_service.py` | Checks predecessor `SUCCEEDED` flags and approval status, mutates step, then returns a receipt not stored atomically. | `REPLACE` | Validate exact output/handoff evidence; persist attempt/output/validation/handoff/receipt atomically; prevent duplicate/late/conflicting completion. |
| `InMemoryPipelineRecipeHarnessRepository` | Independent untyped dict stores and unrestricted `upsert`; no transaction, revision, dependency parity, or orphan checks. | `ARCHIVE_AS_PRODUCTION_IMPLEMENTATION`; `REUSE_AS_NEGATIVE_FIXTURE` | New repository contract must enforce aggregate revision and artifact/receipt/edge/command parity. |
| predecessor recipe/spine tests | Prove missing dependency/gate blocking and declarative no-provider calls. | `ACTIVATE_AS_MIGRATION_FIXTURES` | Add cycles, deterministic order, four classifications, contracts/hashes, atomics, retries, cancellation, invalidation, replay, and authority boundaries. |
| Builder actor-explicit tests | Strong order/actor/edge/cycle/human replay denials. | `ACTIVATE_AS_CONSUMER_CONFORMANCE` | Reproduce through external contract fixtures, not direct imports; add runtime behavior and AIR repair boundary cases. |

No Pipeline source or test tree exists yet under `05_ATOMIC_HARNESS_PIPELINE`; only candidate specifications exist. This document does not create implementation files.

## 5. Proposed architecture and workflows

### 5.1 Components

```text
HarnessExecutionBindingManifest + HarnessRequirementGraphProjection
                              |
                              v
RuntimeWorkflowCompiler -> RuntimeWorkflowGraphRepository
                              |
                   +----------+----------+
                   |                     |
                   v                     v
          DeterministicScheduler    JITContextCompiler
                   |                     |
                   +----------+----------+
                              v
                         NodeDispatcher
                              |
             explicit code/model/human/product nodes
                              |
                              v
             Output + Validation + Handoff Receipts
                              |
                              v
                 RuntimeDependencyGraphProjector
                              |
          AIR failure/repair input -> InvalidationPlanner
                              |
                              v
                 RuntimeSelectiveRepairPlan
```

| Component | Pipeline responsibility | Prohibition |
|---|---|---|
| `RuntimeWorkflowCompiler` | Project exact phases/nodes/edges/bindings into executable runtime contracts and semantic-parity digest. | Add/remove/change semantic requirements, phases, roles, or handoffs. |
| `NodeClassificationValidator` | Enforce actor/capability/role/product independence and owner/authority compatibility. | Infer one classification from another. |
| `DeterministicScheduler` | Compute stable ready sets, safe parallel batches, dispatch ordinals, and blocked reasons. | Guess priorities, skip gates, or perform hidden effects. |
| `JITContextCompiler` | Build minimum complete node context from exact refs, redactions, allowed/forbidden actions, tools, output/evaluation and expiry/cancel rules. | Copy unrestricted case context or invent missing semantics. |
| `NodeDispatcher` | Dispatch only atomically recorded eligible work through typed ports. | Let a model/product/human execute outside an explicit node. |
| `HandoffValidator` | Prove producer output, validation, contract, authority, lifecycle, and consumer compatibility. | Advance on status or transport acknowledgement alone. |
| `RuntimeDependencyGraphProjector` | Record exact runtime artifact/control/authority/evaluation/lock/product-result dependencies. | Treat AIR causal candidates as runtime graph edges without evidence. |
| `RuntimeInvalidationPlanner` | Traverse current descendants, decide checkpoint reuse, and emit immutable plan/receipt. | Rewrite history, globally invalidate unrelated work, or mutate semantic objects. |
| `AIRRepairConsumer` | Validate frozen AIR failure/repair/referral/context requirement and preserve its exact constraints. | Re-attribute, simplify, or broaden AIR meaning. |
| `WorkflowRunRepository` | Atomically store commands, graph/run/node states, JIT refs, artifacts, validation/handoff/invalidation receipts, dependency edges, events, idempotency, and outbox. | Partial success, in-place historical rewrite, or unversioned upsert. |

### 5.2 Workflow compilation

1. `CompileRuntimeWorkflowCommand` identifies the exact eligible TS-AHP-002 binding, requirement projection, authority/admission snapshot, category/profile rules, and expected aggregate revision.
2. Compiler verifies all referenced hashes and rechecks semantic parity; stale or invalidated bindings fail.
3. Each Builder node maps exactly once to a Pipeline `RuntimeWorkflowNode`. No extra executable node is permitted except a typed Pipeline control/boundary node explicitly authorized by a source node/repair contract; such nodes cannot change semantic order.
4. Four classifications resolve independently with exact evidence. Unknown/mixed owner, hidden actor, missing role N/A receipt, or product-boundary conflict fails.
5. All edges resolve bilaterally to versioned/hash-pinned contracts, conditions, validation policies, authority and failure owners. Graph is acyclic; entry/terminal sets and phase boundaries match the source projection.
6. Pipeline freezes a `RuntimeWorkflowGraph`, `RuntimeDependencyGraphSnapshot`, compilation receipt, command/idempotency record, event, and current-head projection in one transaction.
7. Workflow compilation has no provider, model, renderer, VAE, Delegation, Studio, or human side effect.

### 5.3 Deterministic scheduling and node execution

1. `StartWorkflowRunCommand` pins workflow graph, binding, dependency snapshot, execution authorization/claim ceiling, actor/capability eligibility snapshot, and expected revision.
2. Scheduler derives ready nodes only from current terminal producer attempts whose exact outputs passed validation and handoff gates. Failed/blocked/cancelled/invalidated/missing outputs never count.
3. Ready nodes sort by exact phase ordinal, source node ordinal, and node ID. The scheduler emits a `ReadySetReceipt` even when empty, including each blocked dependency/gate.
4. Nodes can share a dispatch batch only when a pinned parallelism policy allows it, dependency closure is disjoint or read-only, declared resources/side effects do not conflict, product/human ordering is preserved, and idempotency/cancellation policies exist.
5. Before dispatch, repository atomically commits `NodeAttemptPlanned`, JIT capsule ref, dispatch command, attempt identity, event, and outbox. No effect occurs if commit fails.
6. Actor returns an output or typed failure through its port. Pipeline stores raw result evidence, canonical output artifact, deterministic validation, independent evaluation where required, attempt receipt, dependency edges, and terminal transition atomically.
7. `HandoffValidator` emits a separate receipt. Only a PASS handoff can make the target ready.
8. Scheduler repeats until terminal success, typed block/failure, cancellation, or explicit human/external wait. It never retries a semantic/quality failure as a transient error.

### 5.4 Human and external-product boundary nodes

A human node persists `WAITING_FOR_HUMAN` with required decision schema, exact authority, scope, inputs, options, and expiry/no-expiry semantics. The decision is attributable and versioned. Historical replay observes the old decision but cannot issue it as new authority.

An external-product node persists a typed request/outbox record and distinguishes `SUBMITTED`, `TRANSPORT_ACKNOWLEDGED`, `OWNER_ACCEPTED`, `RESULT_AVAILABLE`, `RESULT_REJECTED`, `CANCELLED`, `SUPERSEDED`, and `INVALIDATED`. Delegation delivery, VAE production acceptance, and Pipeline consumption are separate. Provider/model calls are implementation actors behind owned product nodes, not product boundaries by themselves.

### 5.5 Bounded role and JIT workflow

For ordinary execution, the Harness supplies role requirements or governed N/A. For AIR repair work:

1. Pipeline receives exact `RoleSemanticContextRequirement` and repair/referral refs.
2. `JITContextCompiler` resolves only the required immutable semantic/evidence refs and exact runtime facts necessary for the assigned role.
3. A `JITContextCapsule` separately records role, actual actor, capability owner, product boundary, node, permitted/forbidden actions, tools, output/evaluation/stopping law, redactions, expiry/cancellation, and limitations.
4. Capsule validation proves required/present/missing/extra refs and semantic constraint equality. Extra context is denied unless the requirement explicitly permits the source class and purpose.
5. Hunter, Analyst, Composer, or Commander execution cannot exceed the role law in section 3.4, even if actor/model/tool capability is broader.
6. Pipeline emits a JIT conformance receipt that AIR may observe. AIR can reject semantic incompleteness without owning the Pipeline capsule or scheduler.

### 5.6 Failure, invalidation, and selective-repair workflow

1. **Admit failure input.** Validate AIR `FailureAttribution` owner/version/hash/status, all candidates/alternatives, frozen refs, semantic-preservation refs, repair route, authority, evaluator receipts, lifecycle, and limitations. Unknown or stale inputs fail.
2. **Choose lawful branch without re-attribution.** `ATTRIBUTED` may proceed by declared route. `MULTI_CAUSAL` proceeds only when branches and owners are separately executable without hidden conflict. `CONTESTED` and `UNRESOLVED` create evidence-acquisition or human-resolution nodes, not an automated repair. `NO_REPAIR_REQUIRED` closes observation only.
3. **Validate repair/referral.** For AIR semantic repair, check exact `SemanticRepairProgram` permitted/forbidden/preserved/lock/evaluation/stopping/escalation constraints. For Pipeline-owned failure, require an exact referral plus local Pipeline repair authority; do not pretend AIR mutated runtime state.
4. **Freeze runtime graph snapshot.** Select the exact graph/run version active when the failed object/result was produced. Verify target artifact/node/result binding and all dependency edges.
5. **Compute affected closure.** Start only from exact changed/failed runtime refs supported by the attribution/referral/evidence. Traverse directed current dependency edges to descendants. Record visited edge paths and reasons. AIR-suggested descendants do not replace traversal.
6. **Decide preservation and reuse.** A checkpoint is reusable only if its artifact bytes, complete dependency closure, authority, context, JIT capsule, implementation, profile, locks, validation/evaluation, and lifecycle remain eligible and the repair law permits reuse.
7. **Compile `RuntimeSelectiveRepairPlan`.** Identify current projections made stale, preserved historical attempts, reusable checkpoints, rerun nodes, role assignments, JIT requirements, side-effect compensation/cancellation, evaluation gates, and stopping/escalation. Include a semantic-constraint equality digest; never add semantic fields.
8. **Independent conformance.** Deterministic validation proves graph closure and constraint equality. Required independent evaluation assesses preservation/repair adequacy; producer cannot self-approve.
9. **Commit atomically.** Persist plan, invalidation projection, dependency paths, receipts, command/event/idempotency/outbox in one transaction. Prior attempts/artifacts remain immutable.
10. **Execute successor run.** Rerun only planned nodes under a new run/attempt identity. Late old results are historical/orphaned for current-state purposes. AIR observes exact execution/result/evaluation refs but Pipeline retains runtime-plan ownership.

### 5.7 Idempotency, concurrency, cancellation, and replay

- Command identity is SHA-256 of command type, canonical payload, exact authority/binding/graph revisions, and expected aggregate revision.
- Exact repeat returns the stored result. Same command ID with byte-different payload fails `AHP_WORKFLOW_IDEMPOTENCY_CONFLICT`.
- Every mutation checks `expected_revision`. One concurrent writer wins; losers receive `AHP_WORKFLOW_CONCURRENCY_CONFLICT` without partial state.
- Cancellation before dispatch leaves no side effect. Cancellation during work requests cooperative cancellation and records incurred evidence. Completion racing with cancellation resolves by committed revision; terminal history is never erased.
- Late results bind only to the exact attempt. Byte-identical duplicate delivery is idempotent; conflicting bytes are quarantined.
- Replay rebuilds graph/run/node current projections from immutable commands/events/receipts and checks checkpoint hash. Verification replay uses stored external result bytes and historical authority; it never calls a provider or synthesizes a missing human decision.

## 6. Data models, contracts, schemas, and APIs

All objects are immutable, closed, versioned, and canonically serializable. `additionalProperties: false`; no `Any`, untyped dictionaries, random/time defaults, implied latest refs, wildcard selectors, or behavior-bearing generic notes.

### 6.1 Shared strict types and identities

```text
ArtifactRef = {object_id, schema_id, version, sha256, owner_product_id, lifecycle_state}
ContractRef = {contract_id, version, sha256, owner_product_id, required_feature_refs}
ActorRef = {actor_id, actor_kind, implementation_ref, operator_or_service_identity_ref}
AuthorityRef = {authority_id, version, sha256, owner, scope, permitted_actions, status}
TypedBlocker = {code, responsible_owner, failed_invariant, evidence_refs,
                next_admissible_action, required_authority_ref_or_not_applicable}
```

Canonical JSON uses UTF-8, NFC, lexicographically sorted keys, exact enum strings, no insignificant whitespace, fixed integer units/decimal strings, no NaN/Infinity, and one terminal newline. Set-semantic arrays sort by declared stable keys; order-semantic arrays retain governed order. Logical identity excludes evidence-only observed timestamps while preserving their values in receipts.

### 6.2 `RuntimeWorkflowGraph`

Schema: `ca.pipeline.runtime-workflow-graph/2.1.0-candidate`.

Required fields:

- `workflow_graph_id`, `workflow_graph_version`, `content_sha256`;
- exact `atomic_harness_definition_ref`, `harness_requirement_graph_projection_ref`, `harness_execution_binding_manifest_ref`, and `authority_snapshot_ref`;
- `category_id_or_not_applicable`, `format_profile_id_or_not_applicable`, and exact category-rule ref;
- ordered `phase_refs`, ordered `nodes`, ordered `edges`, `entry_node_ids`, `terminal_node_ids`;
- `source_graph_digest`, `runtime_projection_digest`, `semantic_parity_digest`;
- `claim_ceiling`, `production_eligible: false`, `certified: false`, lifecycle, supersession, and limitations.

`runtime_projection_digest` proves the executable projection. `semantic_parity_digest` proves that goal, purpose, phase meaning, creative degrees, authority, lineage, locks, evaluation, repair, and category/profile values exactly equal the Builder projection. A runtime control node requires `control_node_authorization_ref` and cannot emit semantic content.

### 6.3 `RuntimeWorkflowNode` and edge

```text
RuntimeWorkflowNode
  node_id: NodeId                         # exact source ID or authorized control ID
  source_node_ref: ArtifactRef
  phase_ref: ArtifactRef
  phase_ordinal: NonNegativeInt
  node_ordinal: NonNegativeInt
  capability_requirement_ref: ArtifactRef
  execution_actor: ActorRef
  capability_owner_kind: CODE | AGENT | HUMAN | EXTERNAL | HYBRID
  capability_ownership_decision_ref: ArtifactRef
  workflow_role: WorkflowRoleAssignment
  product_boundary: ProductBoundaryRef
  authority_requirement_ref: AuthorityRef
  input_contract_refs: ordered[ContractRef]
  output_contract_refs: ordered[ContractRef]
  inbound_edge_ids: ordered[EdgeId]
  outbound_edge_ids: ordered[EdgeId]
  execution_precondition_refs: ordered[RuleRef]
  completion_condition_ref: RuleRef
  gate_refs: ordered[GateRef]
  jit_context_requirement_ref: ArtifactRef
  validation_profile_ref: ArtifactRef
  independent_evaluation_profile_ref_or_not_applicable: ArtifactRef | GovernedNotApplicable
  retry_policy_ref: ArtifactRef
  cancellation_policy_ref: ArtifactRef
  checkpoint_policy_ref: ArtifactRef
  parallelism_policy_ref: ArtifactRef
  tool_grant_policy_ref: ArtifactRef
  side_effect_class: NONE | LOCAL_REVERSIBLE | EXTERNAL_REVERSIBLE |
                     EXTERNAL_IRREVERSIBLE | HUMAN_DECISION
  failure_owner_product_id: ProductId
  lineage_refs: ordered[ArtifactRef]
```

`WorkflowRoleAssignment` is either a registry-pinned `HUNTER`, `ANALYST`, `COMPOSER`, or `COMMANDER` assignment with purpose/allowed/forbidden behavior, or `NOT_APPLICABLE_BY_RULE` with rule/evidence/owner/receipt. The actor, capability owner, role, and product boundary must remain independently addressable and may not be a compound string.

```text
RuntimeWorkflowEdge
  edge_id: EdgeId
  source_node_id: NodeId
  target_node_id: NodeId
  edge_kind: DATA | CONTROL | AUTHORITY | EVALUATION | LOCK_INHERITANCE |
             EXTERNAL_RESULT
  payload_contract_ref_or_not_applicable: ContractRef | GovernedNotApplicable
  source_output_selector: TypedFieldSelector
  target_input_selector: TypedFieldSelector
  condition_ref: RuleRef
  producer_validation_required: bool
  handoff_validation_profile_ref: ArtifactRef
  failure_owner_product_id: ProductId
  cancellation_propagation_ref: ArtifactRef
```

Every edge exists in both endpoint declarations and resolves one producer/consumer contract. A cycle, orphan required node, conflicting ordinal, duplicate edge, or implicit cross-product call fails compilation.

### 6.4 `JITContextCapsule`

Schema: `ca.pipeline.jit-context-capsule/2.1.0-candidate`.

Fields: `capsule_id`, version/hash, workflow/run/node/attempt refs, workflow-role assignment, actual actor, capability owner, product boundary, authority, task purpose, ordered typed context entries, context-manifest ref, required/present/missing/extra semantic-ref sets, epistemic assertions, preserved-property/lock refs, source redaction constraints, allowed/forbidden actions, node-local tool grants, output contract, validation/evaluation profile, repair-program/referral ref or governed N/A, stopping/escalation refs, creation evidence, expiry policy, cancellation state, limitations, and content hash.

A context entry is `{entry_id, object_ref, selector, value_hash, owner, epistemic_state, purpose, redaction_class}`. Rendered free-form context can be an evidence artifact but never replaces the typed manifest.

### 6.5 Run, attempts, scheduler, artifacts, and handoffs

```text
WorkflowRun
  run_id, workflow_graph_ref, binding_ref, dependency_snapshot_ref
  state: CREATED | VALIDATED | READY | RUNNING | WAITING_FOR_HUMAN |
         WAITING_FOR_EXTERNAL | BLOCKED | SUCCEEDED | FAILED | CANCELLING |
         CANCELLED | INVALIDATED
  expected_revision, claim_ceiling, authority_ref, created_by
  current_node_projection_refs, terminal_receipt_ref_or_not_applicable

NodeAttempt
  attempt_id, run_ref, node_ref, attempt_ordinal, dispatch_ordinal
  state: PLANNED | READY | DISPATCH_RECORDED | RUNNING | WAITING |
         SUCCEEDED | FAILED | BLOCKED | CANCELLED | ERROR
  jit_capsule_ref, actor_binding_ref, input_artifact_refs, command_ref
  output_artifact_refs, validation_receipt_refs, evaluation_receipt_refs
  handoff_receipt_refs, failure_or_blocker_ref, predecessor_attempt_ref_or_not_applicable

ReadySetReceipt
  run_ref, graph_revision, scheduler_version_hash, ordered_ready_node_ids
  parallel_batch_groups, blocked_node_reasons, input_state_digest, receipt_hash

HandoffValidationReceipt
  edge_ref, producer_attempt_ref, output_artifact_ref, output_validation_ref
  producer_contract_ref, consumer_contract_ref, authority/lifecycle checks
  compatibility checks, outcome, blocker_or_not_applicable, receipt_hash
```

Terminal attempt state is immutable. Later invalidation changes a separate current-eligibility projection, not the historical `SUCCEEDED` receipt.

`NodeExecutionReceipt` records FR-018 evidence: exact input refs/hashes, JIT capsule, implementation/actor/role/product/authority, command/actions/tool invocations, outputs, deterministic validation, independent evaluation, state transition, observed start/end/duration, cost with unit/currency/source or governed N/A, lineage/dependency refs, idempotency/attempt/cancellation, blockers, and receipt hash. An external result/transport/acceptance receipt remains separately owned and referenced.

### 6.6 Runtime dependency and invalidation contracts

```text
RuntimeDependencyGraphSnapshot
  snapshot_id, run/workflow/binding refs, graph_revision
  vertex_refs: ordered[RuntimeDependencyVertex]
  edge_refs: ordered[RuntimeDependencyEdge]
  current_head_refs, graph_digest, authority_ref, lifecycle, content_sha256

RuntimeDependencyVertex
  vertex_id, object_ref, object_kind: NODE_ATTEMPT | ARTIFACT | CONTEXT_CAPSULE |
      VALIDATION_RECEIPT | EVALUATION_RECEIPT | HUMAN_DECISION |
      EXTERNAL_REQUEST | EXTERNAL_RESULT | CHECKPOINT
  owner_product_id, lifecycle_state, current_eligibility

RuntimeDependencyEdge
  edge_id, upstream_vertex_id, downstream_vertex_id
  dependency_kind: DATA | CONTROL | AUTHORITY | CONTEXT | IMPLEMENTATION |
      EVALUATION | LOCK_INHERITANCE | EXTERNAL_RESULT
  source_rule_ref, required: bool, edge_hash

RuntimeInvalidationTrigger
  trigger_id, trigger_kind: SUPERSESSION | REVOCATION | SOURCE_CORRECTION |
      SEMANTIC_REPAIR | EXECUTION_DEFECT | EVALUATION_REJECTION |
      POST_COMPLETION_INVALIDATION | CANCELLATION
  changed_or_failed_ref, replacement_ref_or_not_applicable
  failure_attribution_or_referral_ref_or_not_applicable
  submitted_by, authority_ref, evidence_refs, content_sha256

RuntimeInvalidationPlan
  plan_id, trigger_ref, graph_snapshot_ref, traversal_algorithm_ref
  root_vertex_refs, ordered_visited_edges, invalidated_current_projection_refs
  preserved_historical_refs, unaffected_current_refs
  checkpoint_reuse_decisions, rerun_candidate_node_refs
  semantic_constraint_digest, deterministic_validation_receipt_ref
  independent_evaluation_receipt_ref_or_not_applicable
  status, blocker_refs, content_sha256
```

The invalidation closure is mechanically derived from Pipeline edges. Root selection must be supported by exact evidence and AIR/referral constraints where applicable, but Pipeline does not alter AIR cause meaning. `RuntimeInvalidationReceipt` contains old/new eligibility projections, traversal proof, affected/unaffected sets, preserved history, authorization, command/commit/event refs, and hash.

### 6.7 `RuntimeSelectiveRepairPlan`

Schema: `ca.pipeline.runtime-selective-repair-plan/2.1.0-candidate`.

Required fields:

- exact `failure_attribution_ref`, `semantic_repair_program_ref_or_not_applicable`, `repair_referral_ref_or_not_applicable`, and local Pipeline repair-authority ref;
- exact workflow/run/binding/dependency-snapshot/invalidation-plan refs;
- `air_semantic_constraint_digest`, with separate hashes for target, permitted selectors, forbidden selectors, preserved assertions, frozen upstreams, inherited locks, evaluation, stopping law, and escalation;
- ordered invalidated current projections, preserved historical artifacts/receipts, reusable checkpoint decisions, rerun nodes, role assignments, JIT requirement refs, implementation bindings, side-effect/cancellation/compensation actions, postconditions, evaluation gates, stopping/escalation, claim ceiling, limitations, and content hash.

The plan has no editable copy of AIR semantic values. It stores exact refs and equality hashes. `CONTESTED` or `UNRESOLVED` failure status, missing authority, broad/wildcard scope, weakened lock, unproven root, stale graph, or non-reusable checkpoint yields a blocker.

### 6.8 Commands, events, ports, and repositories

Commands:

```text
CompileRuntimeWorkflow
StartWorkflowRun
ScheduleReadyNodes
DispatchNodeAttempt
RecordNodeResult
ValidateHandoff
RecordHumanDecision
RecordExternalProductResult
CancelWorkflowRun
ApplyRuntimeInvalidation
CompileRuntimeSelectiveRepairPlan
ExecuteRuntimeSelectiveRepairPlan
VerifyHistoricalReplay
```

Every command contains ID, canonical payload hash, expected aggregate revision, actor, authority, exact input refs, desired transition, and submitted-at evidence.

Events include `RuntimeWorkflowCompiled`, `WorkflowRunStarted`, `ReadySetComputed`, `NodeDispatchRecorded`, `NodeAttemptSucceeded`, `NodeAttemptFailed`, `NodeAttemptBlocked`, `HumanDecisionRequested`, `ExternalProductRequested`, `HandoffValidated`, `RuntimeInvalidationPlanned`, `RuntimeProjectionInvalidated`, `SelectiveRepairPlanned`, `WorkflowRunCancelled`, and `HistoricalReplayVerified`.

Typed ports:

```text
RuntimeWorkflowCommandPort.handle(CommandEnvelope) -> CommandReceipt
RuntimeWorkflowReadPort.get(ArtifactRef) -> RuntimeWorkflowGraph | WorkflowRunView
NodeExecutionPort.dispatch(NodeDispatchEnvelope) -> DispatchAcceptance
HumanDecisionPort.request(HumanDecisionRequest) -> HumanDecisionSubmissionReceipt
ExternalProductPort.submit(ExternalProductRequest) -> TransportSubmissionReceipt
AIRFailureRepairPort.load(FailureAttributionRef, RepairProgramOrReferralRef) -> AIRRepairInputBundle
JITContextConformancePort.evaluate(RoleSemanticContextRequirementRef, JITContextCapsuleRef)
    -> JITCapsuleConformanceReceipt
RuntimeInvalidationPort.plan(RuntimeInvalidationTrigger) -> RuntimeInvalidationPlan
WorkflowReplayPort.verify(run_ref, through_revision) -> WorkflowReplayReceipt
```

Repositories are `RuntimeWorkflowGraphRepository`, `WorkflowRunRepository`, `NodeAttemptRepository`, `RuntimeDependencyGraphRepository`, `ArtifactRepository`, `ReceiptRepository`, `CommandRepository`, `IdempotencyRepository`, `EventRepository`, and `OutboxRepository`. One aggregate transaction API commits state, artifacts, dependency edges, receipts, command/idempotency, events, and outbox or none. Integrity validation rejects state without a command/receipt, receipt without artifacts, artifact without lineage/dependencies, and success without validated handoffs.

### 6.9 Compatibility and examples

Compatibility is semantic and feature-pinned. A minor version may add optional evidence fields that do not change behavior. Changes to required fields, meanings, classifications, ownership, gate algebra, hashing, or invalidation behavior require a major version. Active runs remain pinned to accepted graph/binding/contract versions. Adapters cannot drop authority, lineage, epistemic state, role, product boundary, locks, evaluation, repair, or failure limitations.

Positive node excerpt:

```json
{
  "node_id": "repair-analyst-01",
  "execution_actor": {"actor_id": "analyst-program-v3", "actor_kind": "AGENT_PROGRAM"},
  "capability_owner_kind": "AGENT",
  "workflow_role": {"role_id": "ANALYST", "role_version": "2.1.0-candidate"},
  "product_boundary": {"product_id": "AtomicHarnessPipeline"},
  "side_effect_class": "NONE"
}
```

This shape does not claim that the Analyst actor owns AIR attribution. Negative examples rejected before dispatch include `owner: "AIR|Pipeline"`, `role: "autonomous repair expert"`, missing product boundary, an ungoverned null role, `semantic_overrides`, a hidden VAE call inside a tool grant, or an AIR program with wildcard permitted selectors.

## 7. Implementation stages and exact target paths

Every path below is a future target requiring ratification/adoption as applicable, independent audit/revision/re-audit, a bounded Development Capsule, and explicit build authority. This prompt creates none of them.

### Stage 1 - Workflow domain and projection

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/domain/models.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/domain/enums.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/domain/errors.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/domain/canonicalization.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/compiler.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/classification_validator.py`

Maps FR-013, FR-014, FR-017, FR-137 and both Stories. Completion: exact TS-AHP-002 projection, four classifications, bounded roles, acyclic/bilateral graph, semantic parity, closed types, canonical identity, and no side effects.

### Stage 2 - Scheduler, JIT context, and handoffs

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/scheduler.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/jit_context.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/handoff_validator.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/dispatcher.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/ports/node_execution.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/ports/human_decision.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/ports/external_product.py`

Maps AIR-FR-112, FR-015 through FR-017, FR-137. Completion: stable ready order, safe parallelism, complete JIT, exact contracts/gates, explicit human/product nodes, dispatch-before-effect persistence, and denied hidden execution.

### Stage 3 - Attempts, receipts, and atomic repository

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/run_service.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/application/attempt_service.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/domain/receipts.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/infrastructure/repositories.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/infrastructure/sqlite_repositories.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/infrastructure/outbox.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/infrastructure/migrations/0001_workflow_kernel.sql`

Maps FR-018 and ST-03.04 evidence/replay. Completion: command/state/artifact/edge/receipt parity, optimistic concurrency, idempotency, cancellation race, no orphan state, and historical replay.

### Stage 4 - Runtime dependency graph and invalidation

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/dependency/graph.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/dependency/projector.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/dependency/invalidation.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/dependency/checkpoint_reuse.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/dependency/replay.py`

Maps ST-03.04 selective recovery and AIR-ST-19.02 descendant invalidation. Completion: exact traversal proof, unaffected/preserved/reusable sets, stale-not-consumable projections, lock inheritance, and historical reproduction.

### Stage 5 - AIR failure/repair consumer and runtime repair plan

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/repair/air_contracts.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/repair/air_consumer.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/repair/plan_compiler.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/repair/conformance.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/ports/air_failure_repair.py`

Maps AIR-FR-112/AIR-ST-19.02. Completion: exact AIR status/owner/scope/preservation/lock/evaluation equality, Pipeline-owned traversal/JIT/reruns, blocked unresolved/contested cases, and no local AIR schema fork.

### Stage 6 - Migration and adapters

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/adapters/builder_workflow.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/adapters/legacy_studio_recipe.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/adapters/delegation_product_node.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/migrations/legacy_recipe_to_runtime_graph.py`
- `05_ATOMIC_HARNESS_PIPELINE/docs/workflow/LEGACY_PIPELINE_RECIPE_MIGRATION.md`

Maps all FRs' brownfield evidence. Completion: lossless-or-blocked new artifacts, historical aliases, no random/time identity, no old format authority, and current cross-product boundaries.

### Stage 7 - Delivery and documentation

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/api/contracts.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/api/handlers.py`
- `05_ATOMIC_HARNESS_PIPELINE/docs/workflow/WORKFLOW_NODE_KERNEL.md`
- `05_ATOMIC_HARNESS_PIPELINE/docs/workflow/BOUNDED_ROLE_REGISTRY.md`
- `05_ATOMIC_HARNESS_PIPELINE/docs/workflow/RUNTIME_INVALIDATION_BOUNDARY.md`

Completion: typed command/query APIs, explicit claim ceilings, no secret/absolute-path leakage, and clear AIR/Builder/VAE/Delegation/Studio boundaries.

### Stage 8 - Tests and completion proof

Create the exact test paths named in section 10. All stages remain unauthorized until a later capsule and build receipt.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

| Code | Condition | Owner / next action |
|---|---|---|
| `AHP_WORKFLOW_INPUT_STALE_OR_INVALID` | Harness/binding/authority/category/profile/implementation ref is stale, revoked, superseded, or hash-invalid. | input owner; supply current eligible immutable version |
| `AHP_WORKFLOW_GRAPH_MISMATCH` | Runtime projection differs from source graph/semantic digest. | Pipeline compiler; deny and inspect projection |
| `AHP_WORKFLOW_CYCLE_OR_ORPHAN` | Cycle, duplicate, required orphan, or entry/terminal mismatch. | Builder/source compiler; issue a new Harness version |
| `AHP_WORKFLOW_CLASSIFICATION_INCOMPLETE` | Actor, capability class, role/N/A, or product boundary is missing/mixed. | binding/ownership owner; supply exact evidence |
| `AHP_WORKFLOW_ROLE_AUTHORITY_LEAK` | Role name expands actor/product/semantic authority. | Pipeline; reject node/capsule |
| `AHP_WORKFLOW_HIDDEN_HUMAN_OR_PRODUCT_CALL` | Human/external work appears as an internal tool call. | Pipeline binding owner; compile explicit boundary node |
| `AHP_WORKFLOW_JIT_CONTEXT_INCOMPLETE` | Required ref/epistemic state/lock/action/evaluation is absent or stale. | Pipeline context compiler; rebuild or block |
| `AHP_WORKFLOW_JIT_CONTEXT_OVERBROAD` | Extra unrestricted context, secret, or unowned semantic value is included. | Pipeline context compiler; redact/recompile |
| `AHP_WORKFLOW_READY_ORDER_DRIFT` | Equivalent state yields different ready order/batches. | scheduler owner; stop and repair deterministic inputs |
| `AHP_WORKFLOW_UNSAFE_PARALLELISM` | Dependency/resource/side-effect/human/product constraint conflicts. | scheduler; serialize or obtain governed policy |
| `AHP_WORKFLOW_HANDOFF_INVALID` | Output/validation/contract/authority/lifecycle/compatibility gate fails. | producer/failure owner; no downstream start |
| `AHP_WORKFLOW_OUTPUT_UNVALIDATED` | Status says success without required validation/evaluation evidence. | producer/Pipeline; mark attempt blocked/error |
| `AHP_WORKFLOW_AIR_INPUT_MISMATCH` | AIR artifact version/hash/owner/status/route differs. | AIR/transport consumer; reacquire exact artifact |
| `AHP_WORKFLOW_AIR_FAILURE_NONEXECUTABLE` | Attribution is contested/unresolved or route forbids repair. | AIR/evidence/human owner; no automated repair |
| `AHP_WORKFLOW_SEMANTIC_REINTERPRETATION` | Pipeline changes AIR cause, target, selector, preserved value, lock, evaluation, or stopping law. | Pipeline; reject plan and incident |
| `AHP_WORKFLOW_REPAIR_SCOPE_BROADENED` | Rerun/role/action exceeds semantic/local authority. | Pipeline; recompile bounded plan |
| `AHP_WORKFLOW_INVALIDATION_ROOT_UNPROVEN` | Requested root lacks exact graph/evidence relation. | trigger owner; obtain evidence or block |
| `AHP_WORKFLOW_INVALIDATION_SCOPE_MISMATCH` | Plan misses a dependent descendant or includes unrelated state. | Pipeline graph/invalidation owner; deny commit |
| `AHP_WORKFLOW_CHECKPOINT_REUSE_INVALID` | A dependency/context/implementation/profile/lock/lifecycle changed. | Pipeline; rerun checkpoint node |
| `AHP_WORKFLOW_HISTORICAL_DECISION_REPLAY` | Old human/external acceptance is used as current authority. | Pipeline/authority owner; request new decision if needed |
| `AHP_WORKFLOW_IDEMPOTENCY_CONFLICT` | Same command ID, different canonical payload. | caller; issue reviewed new command |
| `AHP_WORKFLOW_CONCURRENCY_CONFLICT` | Expected revision differs. | caller; reload exact current aggregate |
| `AHP_WORKFLOW_ATOMIC_COMMIT_FAILED` | Any state/artifact/edge/receipt/event/outbox member fails. | repository; rollback all staged members |
| `AHP_WORKFLOW_LATE_RESULT_QUARANTINED` | Result arrives after cancel/supersession/invalidation or conflicts by bytes. | Pipeline; preserve as historical evidence only |
| `AHP_WORKFLOW_REPLAY_DIVERGENCE` | Rebuilt bytes/state differ from immutable history. | Pipeline; stop at first divergence and open incident |
| `AHP_WORKFLOW_MIGRATION_AMBIGUOUS` | Legacy step/owner/role/contract/dependency cannot map exactly. | migration owner; emit blocked receipt, never guess |

Deterministic/semantic/quality failures do not retry as transient errors. Storage, queue, or transport failures may retry only with the same idempotency identity and payload. Provider retry remains with its owning product/node policy; VAE production retry remains VAE-owned; Delegation transport retry remains Delegation-owned.

### 8.2 Legacy migration

Migration reads exact predecessor bytes and creates a new immutable candidate graph plus receipt; it never mutates legacy objects. The receipt records source bytes/hash, adapter version/hash, field mappings, aliases, omissions, blockers, target hash, authority, and claim ceiling.

- Random UUID/time IDs become historical aliases; new logical IDs are content-derived. Times remain evidence only.
- Legacy `PipelineRecipeStep` maps only when an exact current capability, actor, role/N/A, product boundary, contracts, gates, and dependency edges exist.
- Old recipe/format IDs do not become current category/profile authority. Format 02 remains deferred/reference-only until separately governed.
- Open dictionaries, free-text blockers, implicit defaults, local URIs, mutable approvals, and unpinned services cannot enter active contracts.
- Missing source classification, role, owner, authority, handoff, lineage, or semantic context is `UNAVAILABLE_FROM_PREDECESSOR` and blocks active use.
- A legacy success status is historical evidence, not a current validation/handoff PASS.

### 8.3 Rollback and recovery

Deployment rollback changes active reader/scheduler/adapter bindings for future commands and is itself receipted. It does not delete or edit artifacts from the failed version. Database rollback uses forward compensation/migration, never destructive historical reset.

Repository recovery replays immutable commands/events/receipts to rebuild graph/run/node/idempotency/outbox/current-eligibility projections; validates all hashes and parity; and compares checkpoint digest. Orphan state, orphan receipt, missing artifact, missing dependency edge, success without validation/handoff, or event revision gap is a P0 trust failure and prevents current consumption.

If scheduling infrastructure is degraded, new dispatch stops. Already committed external work may finish and be receipted through the exact attempt; uncommitted work cannot be inferred. If an ownership/profile registry is unavailable, cached bytes are usable only when exact version/hash/expiry policy remains valid; otherwise work blocks.

### 8.4 Invalidation, supersession, and historical reproduction

New source, semantic object, Harness, binding, actor implementation, context, evaluator profile, lock, human decision, product result, or contract version creates a new immutable artifact. Current projections that depend on a superseded/revoked/failed version become `STALE_NOT_CONSUMABLE`; historical attempts retain their original terminal outcome and bytes.

The invalidation plan preserves unrelated work. A changed Expression Moment invalidates only dependents that reference its exact version; an unrelated keyframe or evaluation dimension does not invalidate a node with no dependency path. Revocation can block new/current consumption while prior historical playback remains reproducible under the old authority/evidence snapshot.

### 8.5 Upstream draft revision impact

Any TS-AHP-002 hash/interface change reopens graph projection, node/edge/binding fields, semantic parity, compatibility, invalidation roots, acceptance, and tests. Any TS-AIR-019 hash/interface change reopens failure status/route, semantic repair equality, role context/JIT conformance, invalidation boundary, repair-plan fields, acceptance, and tests. Upstream acceptance alone does not accept this spec; material changes require revision and independent re-audit.

### 8.6 Observability and security

Structured logs use refs and codes: command/run/graph/node/attempt, revision, actor/capability/role/product, authority, phase/dispatch ordinal, JIT manifest, contracts/gates, artifact/validation/evaluation/handoff, failure/AIR repair, invalidation/checkpoint/rerun, idempotency, cancellation, commit, and blocker. Logs exclude private source/reaction content, unrestricted JIT text, prompts/responses unless controlled evidence, secrets, credentials, and absolute paths.

Metrics include graph size/cycles/orphans, classification/role denials, ready-set/batch size, blocked reasons, queue/run latency, handoff failures, human/external waits, attempt outcomes/cost evidence, JIT missing/extra refs, semantic-boundary denials, invalidation fan-out, checkpoint reuse/denial, cancellation/late results, concurrency/idempotency conflicts, atomic rollback, replay divergence, and orphan scans. Metrics are operational facts, not semantic truth, human value, certification, or production authorization.

Security tests enforce command authority, least-privilege tools, context redaction, payload/graph/receipt size limits, safe artifact references, transport authenticity/replay protection, and no hidden product/network calls. Technical security remains operational and does not invent generic creative-safety/content-rights authority.

## 9. Behavior-specific acceptance criteria

### AC-01 - FR-013 / ST-03.04: exact phases compile into explicit nodes

**Given** an eligible TS-AHP-002 graph/binding with complete phases, nodes, edges, capabilities, contracts, gates, evaluation and repair refs, **when** runtime compilation executes, **then** each source node appears exactly once with its exact phase/capability/handoff lineage and the semantic-parity digest matches. **Failure example:** compiler adds a generic “creative agent” node that changes phase meaning. **Evidence:** source-to-runtime node matrix and compilation receipt. **Test layer:** contract/integration.

### AC-02 - FR-014 / ST-03.04: four classifications remain independent

**Given** code, model, human, hybrid and external fixtures, **when** nodes validate, **then** actor, capability owner kind, role/N/A and product boundary each resolve independently with exact evidence. **Failure example:** `HUNTER` is used as actor and authority, or `Pipeline|VAE` as product owner. **Evidence:** actor/capability/role/product matrix and denial receipts. **Test layer:** domain/architecture.

### AC-03 - AIR-FR-112, FR-137 / AIR-ST-19.02, ST-03.04: bounded roles are not personas

**Given** Hunter, Analyst, Composer and Commander repair nodes, **when** their JIT capsules compile, **then** each has exact purpose, actual actor, capability, inputs, outputs, allowed/forbidden actions, product, authority, evaluation, failure owner and handoff. **Failure example:** every role receives an unrestricted case dump or Commander grants build/semantic authority. **Evidence:** four role capsules, conformance and authority-denial receipts. **Test layer:** contract/security/integration.

### AC-04 - FR-015 / ST-03.04: deterministic ready order and safe parallelism

**Given** the same eligible graph/state in fresh processes with shuffled map/input order, **when** ready sets compile, **then** ordered node IDs and parallel batches are byte-identical by phase/node ordinals and node ID. **Failure example:** filesystem order changes which paid external job dispatches first, or conflicting side effects run together. **Evidence:** two-process ready-set hash matrix and resource-conflict denials. **Test layer:** property/clean environment.

### AC-05 - FR-016 / ST-03.04: every handoff validates before downstream start

**Given** a producer reports success, **when** output hash, schema/contract, deterministic validation, required independent evaluation, authority/lifecycle and compatibility are checked, **then** target readiness changes only after one PASS handoff receipt. **Failure example:** a `SUCCEEDED` flag or transport acknowledgement advances an invalid output. **Evidence:** handoff receipt and downstream state trace. **Test layer:** integration/contract.

### AC-06 - FR-017 / ST-03.04: humans and products are explicit nodes

**Given** an attributable human decision and a VAE/Delegation external interaction, **when** workflow compiles, **then** each is a boundary node with typed request, wait, response, owner, cancellation and failure states. **Failure example:** a hidden model tool call impersonates VAE or historical approval is reused as current authority. **Evidence:** graph/port matrix and hidden-call/historical-decision denials. **Test layer:** architecture/security.

### AC-07 - FR-018 / ST-03.04: every attempt has a complete immutable receipt

**Given** success, denial, block, failure, error or cancellation, **when** an attempt terminates, **then** the receipt records exact inputs, JIT capsule, implementation, actor/role/product/authority, actions/tools, outputs, validation/evaluation, status, observed timing, cost evidence/N/A, lineage, dependencies and commit refs. **Failure example:** state is stored without a receipt or receipt cites a missing artifact. **Evidence:** repository parity scan. **Test layer:** persistence/integration.

### AC-08 - AIR-ST-19.02: AIR failure meaning is consumed without reinterpretation

**Given** exact `ATTRIBUTED`, `MULTI_CAUSAL`, `CONTESTED` and `UNRESOLVED` AIR fixtures, **when** Pipeline admits them, **then** it preserves statuses, candidates, alternatives, owners, epistemic state, limitations and routes exactly; only lawful branches proceed. **Failure example:** Pipeline selects one convenient cause from a contested set. **Evidence:** AIR/Pipeline byte and field parity plus blocker receipts. **Test layer:** cross-product contract.

### AC-09 - AIR-ST-19.02: semantic repair constraints remain exact

**Given** an AIR `SemanticRepairProgram`, **when** Pipeline compiles a runtime repair plan, **then** target/permitted/forbidden/preserved/frozen/lock/evaluation/stopping/escalation hashes are equal and no semantic override exists. **Failure example:** Pipeline broadens `/script/line/3` to `/script` or removes a wrong-reading lock. **Evidence:** constraint-digest matrix and negative scope diff. **Test layer:** contract/architecture.

### AC-10 - AIR-ST-19.02, ST-03.04 selective recovery: Pipeline computes exact descendants

**Given** a proven changed runtime vertex in a frozen dependency snapshot, **when** invalidation plans, **then** Pipeline traverses exact directed edges, lists every affected path, preserves unrelated current work and all history, and treats AIR descendant suggestions only as non-authoritative evidence. **Failure example:** global run invalidation or omission of a Feature Contract-dependent artifact. **Evidence:** traversal matrix, affected/unaffected sets and invalidation receipt. **Test layer:** graph property/recovery.

### AC-11 - selective recovery: checkpoint reuse is evidence-bound

**Given** a candidate checkpoint, **when** reuse validates, **then** artifact bytes and full dependency/context/implementation/profile/lock/validation/evaluation/lifecycle closure remain unchanged and reuse is allowed by the repair law. **Failure example:** reuse after evaluator profile or source version changed. **Evidence:** checkpoint dependency diff and reuse/denial receipt. **Test layer:** recovery/integration.

### AC-12 - authority ambiguity stops before side effects

**Given** unknown owner, missing source/Reaction Receipt/Expression Moment, human-owned new meaning, unsupported role, stale repair authority or ungoverned N/A, **when** scheduling or repair is requested, **then** a typed blocker names cause, owner and next action before dispatch. **Failure example:** model fabricates missing human authority to make a node ready. **Evidence:** side-effect spies and blocker corpus. **Test layer:** adversarial/security.

### AC-13 - idempotency, concurrency and atomicity

**Given** exact duplicate command, byte-different ID reuse, concurrent expected revisions, and fault injection after each transaction member, **when** commands execute, **then** exact repeat returns one result; conflict fails; one revision wins; and state/artifact/edge/receipt/event/idempotency/outbox all commit or none. **Failure example:** succeeded node row exists without handoff receipt. **Evidence:** transaction/fault matrix and store parity. **Test layer:** persistence integration.

### AC-14 - cancellation, late result and compensation

**Given** cancellation before dispatch, during reversible work, during irreversible external work and racing with completion, **when** processed, **then** no undispatched effect occurs, incurred work remains receipted, owning-product compensation policy applies, committed revision wins deterministically, and late/conflicting results cannot change current state. **Failure example:** cancelled provider result reopens the old run. **Evidence:** race matrix and quarantine receipt. **Test layer:** concurrency/recovery.

### AC-15 - historical replay and portability

**Given** a completed run later superseded/revoked and executed from another workspace root/process, **when** replay verifies, **then** original graph, JIT, attempts, decisions, outputs, receipts, invalidation and outcome hashes reproduce from stored bytes with no current/latest substitution, absolute path, clock, random or environment dependence. **Failure example:** replay asks the human again or uses the latest model/profile. **Evidence:** fresh-context hash matrix and first-divergence report. **Test layer:** replay/clean environment.

### AC-16 - migration is lossless or blocked

**Given** legacy recipe/run/step/gate records, **when** migration runs, **then** only exact current mappings create new immutable candidate artifacts and historical aliases remain; ambiguous role/owner/contract/dependency/format/source fields block. **Failure example:** old `format02_golden_path` becomes active certified current profile. **Evidence:** migration ledger and positive/blocked receipts. **Test layer:** migration/contract.

### AC-17 - lifecycle boundaries remain separate

**Given** an external visual node, **when** Delegation submission, VAE acceptance/result, Pipeline handoff/consumption and independent evaluation occur, **then** each state/receipt remains distinct and no one state implies another. **Failure example:** transport success marks node production-accepted and consumable. **Evidence:** multi-receipt lifecycle fixture. **Test layer:** cross-product integration.

### AC-18 - claim ceiling

**Given** all structural/synthetic tests pass while ratification/build/production authority is absent, **when** status projects, **then** this spec/run evidence remains non-build-ready, production/certification false, and no Format 02/VAE Stage 5 activation is inferred. **Failure example:** deterministic scheduler PASS becomes production authorization. **Evidence:** status and receipt assertions. **Test layer:** governance/architecture.

## 10. Testing and completion evidence

### 10.1 Exact future test paths

- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/unit/test_runtime_workflow_graph.py`: exact projection, phase/node/edge parity, cycles, orphans, ordinals, semantic digest.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/unit/test_node_classifications.py`: actor/capability/role/product independence, all owner classes, governed N/A, role authority leak.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/unit/test_bounded_roles.py`: Hunter/Analyst/Composer/Commander allowed/forbidden behavior and actor variability.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/unit/test_deterministic_scheduler.py`: ready order, gates, parallel batches, resource/side-effect conflicts, empty ready sets.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/unit/test_jit_context_capsule.py`: exact required refs, epistemic state, redaction, missing/extra/stale context, tools, expiry/cancel.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/unit/test_handoff_validator.py`: output/contract/hash/authority/lifecycle/evaluation and external-state separation.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/unit/test_runtime_dependency_graph.py`: vertex/edge integrity, descendant traversal, cycles prohibited in execution control, exact closure.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/unit/test_checkpoint_reuse.py`: full dependency closure, lock/profile/context/implementation changes and reuse denials.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/contracts/test_air_failure_repair_consumer.py`: all AIR statuses/routes, alternatives, owner/epistemic/limitations, hash mismatch, no re-attribution.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/contracts/test_air_semantic_repair_constraint_parity.py`: target/selectors/preservation/locks/evaluation/stopping/escalation equality and scope-broadening denial.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/contracts/test_builder_workflow_consumer.py`: TS-AHP-002 producer/consumer graph and binding conformance without Builder imports.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/integration/test_workflow_primary_journey.py`: compile, stable schedule, node attempts, handoffs and terminal receipt.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/integration/test_explicit_human_and_product_nodes.py`: human decision, Delegation, VAE lifecycle separation, cancellation and rejection.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/integration/test_atomic_workflow_repository.py`: command/state/artifact/edge/receipt/event/idempotency/outbox fault injection and optimistic concurrency.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/integration/test_air_bounded_repair_execution.py`: AIR repair input to Pipeline invalidation/JIT/rerun/result without semantic mutation.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/recovery/test_selective_invalidation.py`: affected/unaffected state, checkpoint reuse, lock inheritance and stale consumption denial.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/recovery/test_cancellation_late_results_and_replay.py`: races, quarantine, historical state rebuild and first divergence.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/migration/test_legacy_pipeline_recipe_migration.py`: random/time aliases, open fields, old format IDs, ambiguous blocks and lossless round trip.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/architecture/test_workflow_product_boundaries.py`: no Builder/AIR/VAE/Delegation/Studio internal imports; no hidden semantic owner or product call.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/clean_environment/test_workflow_determinism_portability.py`: two roots/processes, shuffled maps/order/environment, no absolute paths or undeclared files.
- `05_ATOMIC_HARNESS_PIPELINE/tests/workflow/reference_slices/test_st03_04_and_air_st19_02.py`: both Stories' primary, adversarial, replay, CBAR, selective recovery and claim ceiling.

### 10.2 Required test and evidence layers

| Layer | Mandatory evidence |
|---|---|
| Schema/model | Closed field/enum coverage, unknown/missing/duplicate values, canonical round trip/hash vectors, no mutable defaults/open maps. |
| Domain/property | DAG/entry/terminal/ordinal/classification/role/edge laws, deterministic ready sets, graph traversal, preserved/unaffected sets, N/A law. |
| Cross-product contracts | Builder projection/binding and AIR failure/repair/context interfaces; human/Delegation/VAE/evaluator state separation; no local schema fork. |
| Integration | Primary workflow, all actor/owner/role/product kinds, explicit handoffs/gates, JIT, node receipts, bounded repair and terminal run. |
| Persistence/concurrency | Atomic parity, exact retry, ID conflict, optimistic writers, transaction fault injection, outbox duplication, orphan detection. |
| Recovery/replay | Cancellation races, late results, supersession/revocation, descendant invalidation, checkpoint reuse, rollback, historical reproduction. |
| Migration | Exact mapping or block, original byte retention, aliases, old formats, no guessed role/source/authority/certification. |
| Architecture/security | Import direction, hidden product/tool denial, least privilege, authority checks, redaction, size/path/payload safety, no self-approval. |
| Clean environment | Fresh processes/roots, stable hashes, no clock/random/traversal/environment/absolute-path dependence. |

### 10.3 Completion proof and future Build Receipt

A later implementation-completion claim requires:

1. ratified/adopted authority and accepted upstream interface locks;
2. exact source/changed-file manifest and schema/model parity;
3. full AIR-FR-112, FR-013 through FR-018, FR-137, AIR-ST-19.02 and ST-03.04 traceability;
4. all AC-01 through AC-18 positive, negative, adversarial, boundary, recovery and observability results;
5. two fresh-process full regressions and Python compilation/type/static checks;
6. Builder producer-to-Pipeline consumer and AIR producer-to-Pipeline consumer conformance without local forks;
7. role/actor/capability/product matrix, deterministic schedule/parallelism evidence and complete node-receipt parity;
8. atomicity/idempotency/concurrency/cancellation/late-result/outbox proof;
9. descendant invalidation, checkpoint reuse, rollback and historical-replay matrix;
10. security, context redaction, no-hidden-product-call and portability evidence;
11. separate truth for implementation coverage, Story completion, external proof, production authority and certification;
12. independent audit by a different agent and, after any revision, independent re-audit.

A future Build Receipt must cite the independently accepted spec hash, attributable ratification/adoption, exact bounded Development Capsule, implementation/test hashes, evidence results, remaining blockers, rollback, and maximum claim. It cannot infer production eligibility, Format 02 certification, VAE Stage 5, evaluator certification, provider trust, or product release authority from local tests.

This writing task ends at `WRITTEN_PENDING_AUDIT`. No audit, revision, acceptance, implementation, build, release, Development Capsule, production, or certification action is performed.
