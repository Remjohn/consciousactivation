---
document_class: PROPOSED_CROSS_PRODUCT_TECH_SPEC_AMENDMENT
spec_id: TS-VAE-BOUND-001
title: VAE Provider Ownership for SAM3, Lucida, Layered Generation, ComfyUI, and Google GNM
target_product: 02_VISUAL_ASSET_EDITOR
proposal_owner: Program Control
product_owner: Visual Asset Editor
proposal_version: 2.1.0-candidate
issued_on: '2026-07-22'
quality_state: WRITTEN_PENDING_AUDIT
adoption_state: PRODUCT_ADOPTION_REQUIRED
build_state: NOT_BUILD_READY
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: INDEPENDENT_AUDIT_THEN_PRODUCT_ADOPTION_REQUIRED
writing_wave: 13
output_path_class: PROGRAM_CONTROL_CROSS_PRODUCT_PROPOSAL
proposal_path: CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/cross-product-proposals/TS-VAE-BOUND-001.md
proposed_adoption_path: 02_VISUAL_ASSET_EDITOR/docs/tech-specs/TS-VAE-BOUND-001.md
current_product_write_prohibition: 02_VISUAL_ASSET_EDITOR/AGENTS.md permits writes only under docs/constitutional-alignment/ and PROGRAM_STATUS_EXPORT.yaml
controlling_frs: [FR-087, FR-088, FR-089]
controlling_stories: [ST-08.02]
upstream_draft_dependencies:
  - {edge_id: SDE-068, spec_id: TS-DEL-001, quality_state: WRITTEN_PENDING_AUDIT, sha256: aba43b66766795436b2073b528a486e7dbdb4cc48638ca21a1642c0e36e6d751, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
---

# TS-VAE-BOUND-001 - VAE Provider Ownership for SAM3, Lucida, Layered Generation, ComfyUI, and Google GNM

This is a complete implementation-grade **proposal**, not an adopted Visual Asset Editor specification. It remains under Program Control because the current VAE `AGENTS.md` prohibits this product-local write. It authorizes no VAE edit, implementation, Stage 5 activity, provider call, model download, schema or contract release, Development Capsule, build, production use, certification, or `ACCEPTED_FOR_BUILD` claim.

## 1. Files and authorities read

### 1.1 Proposal, packet, path and authority controls

| Source | State / bytes / SHA-256 | Class | Fact used |
|---|---|---|---|
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/.../CA_TECH_SPEC_WRITE_SKILL.md` | V3.3; 9,624; `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | governing method | One writer writes one spec/proposal, reads path authority, emits receipts, and does not audit, accept, build or issue a capsule. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012; `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | exact recovery packet | Packet `CA-P03-WRITE-TS-VAE-BOUND-001-RECOVERY` fixes FRs, Story, proposal path, adoption path, state and sole upstream. |
| `.../PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_13_DISPATCH_LOCK.yaml` | `DISPATCHED`; 2,665; `cbf921af042212cd2fe2f43de067c7145bd931314232bb16bb8120b44135f729` | Wave 13 lock | Freezes TS-DEL-001 at the exact admitted hash. |
| `02_VISUAL_ASSET_EDITOR/AGENTS.md` | current; 909; `aab5f8134b51c7f0dfb6022755ab5b7cd365a10d4c14188caed1614ebb7604e8` | target-product write authority | VAE writes are currently limited to `docs/constitutional-alignment/` and `PROGRAM_STATUS_EXPORT.yaml`; the proposed adoption path is prohibited now. |
| `02_VISUAL_ASSET_EDITOR/00_ALIGNMENT_START_HERE.md` | current; 468; `16b7692101640be4859b79b730fba02bc788d6ea0e0d18422cd7aeef72b05c02` | repository instruction | The existing VAE work is preserved and authority/status pointers govern. |
| `02_VISUAL_ASSET_EDITOR/docs/product-authority/CURRENT_AUTHORITY.md` | current; 428; `15c0c80e39f1bac160021423802c1687c8968e34187c550d071bc1c48725474c` | product-authority pointer | Current authority is the Program Control VAE PRD V1.1 package; adoption is patch-based, not a restart. |
| `02_VISUAL_ASSET_EDITOR/CURRENT_PROJECT_STATUS.md` | current; 3,660; `383b31d94b3623cf7884d5b4d6297d860444b865cc92d3fc3ad2226dc461f95a` | status truth | RC4 integration is bounded local PASS; evaluator is specified-not-certified; Stage 5 and production remain unauthorized. |
| `02_VISUAL_ASSET_EDITOR/PROGRAM_STATUS_EXPORT.yaml` | current; 10,861; `8d994e66be44930c522370c217b9999b84e7ac606063246c42bdcbe74c89665b` | machine status truth | No implementation, production trust, compute/recovery proof or product certification is authorized. |
| `SPEC_PACKET_WRITE_AUTHORITY_MATRIX.csv` | current; `3fa4793ea2baca46dcfbf8e123d039a59ab2467e5814471d49b3daf65e588a73` | path decision | Classifies this output as `PROGRAM_CONTROL_CROSS_PRODUCT_PROPOSAL`, with VAE unmodified. |
| `PRODUCT_ADOPTION_QUEUE.yaml` | current; `4c8753a08634518cb8e54572539c6bbffc8e2d1918cfd168866baa1b31c5cb41` | adoption gate | Requires explicit VAE write authority, governed adoption bytes, product-local re-audit, ratification and later build gate. |
| `SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | specification-only; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | write gate | Candidate writing and technical review are permitted; build/production/certification are false. |

No `AGENTS.md` applies to the Program Control proposal directory. The target product's `AGENTS.md` still governs future adoption and is not bypassed by Program Control proposal authority.

### 1.2 Current and candidate authorities

| Source | State / SHA-256 | Fact used |
|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | highest current authority; `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Visual production realizes already-authorized meaning and human/source lineage; tools and providers do not become semantic authority. |
| Program Control `CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | `CANDIDATE_NOT_CURRENT`; `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | AIR owns semantic lifecycle; VAE owns visual production; Pipeline executes; Delegation transports; Studio projects/corrects. |
| Program Control `SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | `CANDIDATE_NOT_CURRENT`; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | VAE may realize Visual Asset Demands but may not reconstruct missing source/AIR meaning. |
| AHP `PRD_COMBINED.md` | candidate; `387568731acfe57f022a2fadcd2acfc73baf1287b8a5a1e1d3ed78675ccb067d` | The cross-product requirement is an ownership boundary, not permission for Pipeline to implement providers. |
| AHP F15 `Visual Asset Editor, Delegation, and GNM Boundary Integration` | candidate; `eb65e84b126369a3067464a0dc9bd7c0dec72ebd168111cdb7f1fdef69333f44` | FR-087/088/089 keep SAM3, matting, layered generation, ComfyUI and GNM routing inside VAE. |
| AHP `EPICS_AND_VERTICAL_STORIES.md` | candidate; `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | ST-08.02 protects the law that Pipeline does not implement VAE providers and requires route/evidence/replay. |
| `planning/spec_assignments/TS-VAE-BOUND-001.md` | assignment only; `710a4f72ee19ed1359c6af6ca38705982c8d64fb57f4f9498b2c239698e6057c` | Names the provider-boundary topic and evidence sources; its product-local path is superseded until adoption authority exists. |

### 1.3 Sole admitted upstream draft

| Edge | Exact path | State / bytes / SHA-256 | Interface admitted | Revision impact |
|---|---|---|---|---|
| SDE-068 | `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-DEL-001.md` | `WRITTEN_PENDING_AUDIT`; 67,906; `aba43b66766795436b2073b528a486e7dbdb4cc48638ca21a1642c0e36e6d751`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Externally owned RC4 demand/result/geometry/acknowledgement boundary, exact product ownership, semantic compatibility, provider-neutral demand law, lifecycle and production-acceptance/consumption separation. | If the hash changes, reopen sections 3, 5, 6, 8, 9 and 10; rebind every external message/result projection and rerun adoption impact. |

TS-DEL-001 is a draft interface, not ratified or accepted authority. This proposal does not copy, amend or release its shared schemas.

### 1.4 VAE product sources and current design baseline

| Source ID / path | Bytes / SHA-256 | Current disposition | Fact used |
|---|---|---|---|
| `SRC-CUR-013` - `02_VISUAL_ASSET_EDITOR/prd/index.md` | 5,185; `1ac3032b87adbe4f46bedca8dcdea6ccef364855ef316e14a9c0663d2bd103f8` | `REQUIRED_AUTHORITY` | The VAE has separate capability registry, production-plan, compute, evaluation, repair, service and certification feature ownership. |
| `SRC-CUR-015` - VAE F08 | 6,963; `142b5406e3af2318da5986ac4b4429975010a1464534d6048c13c55c4d99780f` | `REQUIRED_AUTHORITY` | Provider workflows, models, controls and runtimes require versioned registry records, compatibility, evidence, maturity and rollback. |
| `SRC-CUR-016` - VAE F09 | 7,019; `db7ece2ec153f144dc55bf00fdcd96c7941f527839db90f9a4ced23536dba47a` | `REQUIRED_AUTHORITY` | VAE owns one provider-neutral `VisualProductionPlan`; provider graphs/payloads are compiled artifacts. |
| `VAE_CODEBASE_INVENTORY.md` | 14,324; `3bb96d50f07d2dac69f27b7c2aa920d1c909f5684b2a0798eb2e9caa1d515c24` | current inventory evidence | The VAE contains specifications, schemas, registries and fixtures but no product source tree, provider adapter, worker or product test suite. |
| `TS-VAE-01-DEMAND-INTAKE-AND-PRODUCTION-PLAN-IR.md` | 21,426; `8d1ecaa67f0b0a4362850963cb1371ac1179155342d5e39a51e10a320ccfcf4e` | preserved draft architecture | Demand is immutable/external; VAE owns a provider-neutral plan and cannot mutate Composition Intent or semantic authority. |
| `TS-VAE-02-DYNAMIC-WORKCELL-AND-CAPABILITY-ROUTING.md` | 13,650; `c5e3171c649ed626b2accc6756c32aee7dc94c08b9d399ba2063d01014b94470` | preserved draft architecture | Route choice binds exact capability snapshots and keeps materializer/evaluator roles independent. |
| `TS-VAE-03-COMFYUI-WORKFLOW-COMPILER-AND-REGISTRIES.md` | 13,718; `c4374a2753530ab03f82343fdce2363c463838b82dcf1e144abaa087ecbb0c01` | preserved draft architecture | Provider-private ComfyUI JSON is compiled deterministically from a plan and registry; it is not canonical product state. |
| `TS-VAE-06-INDEPENDENT-VLM-EVALUATION.md` | 14,370; `7f7619391d11c7206b0a2e7a1c796ece719e5b54acfd0a1558be44807baf9856` | preserved draft architecture | Deterministic checks precede independent evaluation; hard gates cannot be averaged away or self-approved. |
| `VISUAL_PRODUCTION_PLAN.schema.yaml` | 1,783; `be217bccfeeed117ae0bc6f60838b8fc1f822ad6705721bfc9c20992ebd8238b` | PRD-level seed only | Demonstrates plan fields but leaves internal objects open/under-typed; it cannot be treated as implementation contract. |
| `WORKCELL_AUTHORITY_REGISTRY.yaml` | 2,643; `e8f459ac69d553209a0675b9a0b18615b44cf3d0b6f5f82d2362864d506664bc` | binding design | The Editor/Materializer owns masks/compositing/rendering but not plan redesign or self-approval; evaluator is separate. |
| `VISUAL_EVALUATION_PROFILE_REGISTRY.yaml` | 5,737; `7d3d8c75fbd02dc93567cd7261f28bd79af82ca8e9ecad0856a29fee72f46131` | `specified_not_certified` | Required dimensions exist, while thresholds, labeled/protected cases, evaluator pin and rollback evidence remain absent. |
| `SRC-MIG-001` - predecessor migration audit | 10,966; `5912930b2abfb376aef67c140bb745845ede054b07ad6aa0e9bb77f9a06301d7` | `REQUIRED_UNIQUE_EVIDENCE` | Predecessor provider-generation code may be extracted only after ownership/authority review; fake/dry-run results and obsolete pins are not production evidence. |

`SRC-EXT-026` (`github://google/GNM`) is `DEFERRED_REFERENCE`: exact bytes are unavailable and the recorded locator is not a byte lock. `SRC-AM-002` is also `DEFERRED_REFERENCE`. No license, model architecture, performance, demographic, fairness, runtime, API or technical-capability fact in this proposal is attributed to either source. FR-089 supplies only the current candidate ownership/behavior requirement. Exact external bytes and attributable adoption evidence are required before any corresponding capability can advance.

## 2. Problem, user outcome, solution, and scope

### 2.1 Concrete failure without this boundary

A Pipeline node can bypass VAE planning and call a segmentation or matting tool directly; a provider filename can be treated as capability proof; a ComfyUI graph can quietly become the real production plan; a layered-image provider can discard semantic or wrong-reading constraints; or a face-geometry model can be treated as the source of a real person's identity or emotion. Each shortcut may produce an attractive artifact while transferring authority away from the VAE, hiding provider state from evaluation, and breaking demand/result lineage.

The current VAE repository prevents implementation mistakes only in prose and seed contracts. It has no product runtime, provider adapters, registry enforcement, durable event store or executable production tests. A complete adoption-ready boundary specification is required before later implementation can begin.

### 2.2 User and system outcome

Given an exact admitted Visual Asset Demand, VAE compiles one immutable provider-neutral `VisualProductionPlan`, resolves only eligible capability records, and executes provider-specific stages through VAE-owned adapters and workers. Pipeline receives only the external contract-defined Asset Result, measured artifacts/geometry, evaluation and health/receipt evidence. It cannot call, configure, select or claim SAM3, a matting provider, layered generation, ComfyUI or GNM capability.

Operators can inspect which exact capability/version/runtime produced each artifact, why it was eligible, what it was permitted to change, how it was independently evaluated, and how revocation or supersession affects descendants without losing history.

### 2.3 Bounded solution

This proposal adds a provider-sovereignty layer to the existing VAE architecture:

- `ProviderCapabilityRegistry` owns closed versioned capability profiles, compatibility, maturity, provenance/evidence, revocation and rollback;
- `ProviderRouteResolver` binds provider-neutral plan requirements to an exact eligible capability bundle;
- `ProviderBindingCompiler` compiles immutable VAE-private stage bindings and provider artifacts without changing demand/plan meaning;
- VAE-owned SAM3, matting, layered-generation, ComfyUI and GNM adapters execute only typed commands under pinned runtimes;
- deterministic validators verify bytes, masks/mattes/layers/geometry, locks and lineage before independent evaluation;
- the independent evaluator and authorized VAE acceptance service remain separate from the producer;
- a result projector maps only externally governed result/evidence fields into TS-DEL-001/RC4 without leaking provider control into shared demand authority;
- atomic repositories, events, receipts, invalidation and replay preserve exact current and historical truth.

### 2.4 In scope

- FR-087, FR-088, FR-089 and ST-08.02 only.
- Product ownership, routing, registry, plan binding and execution boundaries for SAM3-class segmentation/tracking, Lucida-or-replacement matting, layered-image generation, ComfyUI workflow embodiment and GNM-class geometry references.
- Provider-neutral requirements versus provider-specific immutable bindings.
- Provider/capability identity, provenance evidence, license-policy status, compatibility, maturity, benchmark/evaluation refs, runtime locks and fallback eligibility.
- Typed input/output evidence for masks, tracks, mattes, layers and geometric references.
- Source-backed identity/continuity binding and explicit geometry-only restrictions for GNM-class routes.
- Independent evaluation, production acceptance, result projection, health receipts, repair ownership, cancellation, invalidation, revocation, rollback and historical replay.
- Exact future product paths, tests, adoption evidence and claim ceiling.

### 2.5 Out of scope and non-goals

- Editing the VAE repository during this proposal.
- Implementing or downloading any provider, model, worker, graph, schema, test or source tree.
- Amending Delegation RC4 bytes or creating VAE-local shared contract forks.
- Pipeline-owned provider SDKs, model files, ComfyUI nodes, provider selection, prompt/parameter control or worker scheduling.
- Changing upstream Visual Asset Demand, Composition Intent, source classification/provenance, Activative meaning, Feature Contract intent, wrong-reading locks, identity authority or budget ceilings.
- Treating GNM or any geometry model as identity, emotional truth, demographic authority, source permission or evaluation authority.
- Treating SAM3-class masks as semantic meaning or layered-generation decomposition as canonical composition meaning.
- Certifying Lucida, SAM3, GNM, ComfyUI, a layered provider, evaluator, Format 02 or VAE production from specification or synthetic fixtures.
- Generic creative-safety/content-rights approval authority. Source authority, provenance, permitted use, product sovereignty and operational security remain explicit under their actual owners.

## 3. Governing decisions and constraints

### 3.1 Current/candidate authority and adoption ceiling

Constitution V1.1 and VAE PRD V1.1 are current. The V2.1 ownership model, AHP PRD, F15, Story and TS-DEL-001 interface remain `CANDIDATE_NOT_CURRENT`. Prompt 02C permits writing and later independent technical review. It does not grant VAE adoption, Stage 5, build or production authority.

This proposal may later reach `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`, but cannot reach product-local `ACCEPTED_FOR_BUILD` until:

1. required candidate authority is ratified or an attributable adoption authority expressly governs the boundary;
2. VAE grants product-local spec write/adoption authority;
3. adopted bytes are hash-identical or all differences are governed;
4. adopted product-local bytes receive independent re-audit;
5. a separate build gate and Development Capsule are issued.

### 3.2 Product sovereignty

- Upstream Content Harness/Pipeline owns the immutable Visual Asset Demand: source classification, semantic/Activative purpose, sequence/asset/composition intent, identity/continuity needs, wrong-reading locks, constraints, budget and amendment authority.
- VAE owns the `VisualProductionPlan`, capability requirements, route, workflow/model/LoRA/control/conditioning selection, provider binding, candidate generation, visual evaluation, bounded production repair, production acceptance, artifact lineage and delivery.
- Pipeline may validate demand/result identity, health, evidence and downstream compatibility. It cannot call provider adapters or reproduce VAE planning.
- Delegation owns shared schema validation, authority enforcement, compatibility negotiation, lifecycle routing, replay protection and audit receipt semantics. It cannot choose provider or visual strategy.
- AIR and Interview Expression retain semantic and source truth. VAE consumes exact refs and never reconstructs missing meaning.
- Studio is an operator projection/correction surface. It may issue typed commands but does not hold provider or canonical plan state.
- Provider runtimes are embodiments. Their responses are untrusted candidate evidence until VAE validation and independent evaluation pass.

`Activative Contract Compiler != Activative Intelligence Runtime`; neither is a VAE provider router.

### 3.3 Provider-neutral plan, VAE-private binding

The authoritative VAE `VisualProductionPlan` expresses functions such as segmentation, tracking, transparent extraction, matte refinement, layer separation, pose/gaze/geometry reference or provider workflow execution. It MUST NOT require a provider node ID, mutable model filename, local path or raw graph as product meaning.

A separate immutable `ProviderBindingSet` resolves requirements to exact registry records. ComfyUI JSON, SDK payloads, command lines, provider job IDs, local mounts and worker workspaces are private compiled/execution artifacts. They MUST NOT become the plan, shared demand or upstream amendment.

Provider changes allowed by the demand create a new VAE plan/binding version. A semantic or demand change requires the upstream owner to issue a new immutable demand version.

### 3.4 Capability evidence is not capability certification

A registry entry proves only the state its evidence supports. Mounted weights, import success, an API response, one attractive output, a passing schema, a declared `EVALUATE` capability or a provider's own benchmark cannot establish VAE production certification.

Capability maturity uses the VAE-owned controlled states `experimental`, `benchmarked`, `shadow`, `limited-production`, `production`, `deprecated`, `retired`, plus typed emergency `revoked`. Eligibility requires the demand/profile policy's minimum state. Current proposal examples MUST remain non-production until evidence exists.

The current evaluator state is `specified_not_certified`; this proposal invents no thresholds. Therefore no provider path may claim production certification from current evidence.

### 3.5 SAM3-class boundary

SAM3-class capability means a VAE-owned concept-conditioned segmentation/tracking operation required by a plan. VAE owns provider/version/runtime selection, input preparation, prompting/control within plan constraints, execution, masks/tracks, geometry evidence, validation, independent evaluation, repair and production acceptance.

Pipeline may request provider-neutral segmentation/tracking and consume result evidence. It MUST NOT import the provider SDK, submit jobs, inspect private provider prompts/graphs as authority, or claim the capability. A mask identifies pixels/regions under a declared operation; it does not define human identity, semantic role, emotion or Composition Intent.

### 3.6 Lucida-or-replacement matting boundary

Matting is a provider-neutral VAE capability. A named provider is eligible only through an exact registry profile with version/digest, supported inputs/outputs, runtime, compatibility, provenance and license-policy evidence, benchmarks, known limitations, evaluator requirements, maturity and rollback.

The plan decides that matte/alpha refinement is required; VAE route resolution may choose Lucida or a compatible replacement. Pipeline receives only typed artifact/evidence/blocker fields. An absent exact dependency or license-policy decision blocks the route; it is never inferred from a package name or assignment statement.

### 3.7 Layered generation and ComfyUI boundary

Layered generation remains VAE-owned whether supplied by a model, API, ComfyUI workflow or composite route. Each layer artifact declares source/generation parentage, role, alpha/depth/order/geometry, mutability, locks, limitations and evaluation. Layer order or names cannot silently redefine the Visual Narrative Program or authoritative composition meaning.

ComfyUI is an execution embodiment. VAE owns the workflow registry, graph compiler, node allowlist, model/VAE/LoRA/control locks, runtime image, resource mounts, security policy, execution receipt and rollback. Raw graph edits invalidate compiled identity. Pipeline and Delegation see no provider-private node graph in the shared demand contract.

### 3.8 GNM-class geometry boundary

A GNM-class route may supply only typed geometric reference evidence that the plan requires and the capability profile supports. It MUST bind to approved source-backed identity/continuity evidence when a real person is involved. Geometry output MUST be labeled as a control/reference, never a claim about identity, emotion, intent, personality, demographic truth or source permission.

It is forbidden to create or select a real coach/guest identity from demographic labels, latent samples or a provider default. It is forbidden to use inferred expression labels as authoritative Reaction Receipt, Expression Moment, Voice/Visual DNA or psychological truth. Missing source-backed fitting/reference evidence blocks the route.

Because `SRC-EXT-026` bytes are unavailable, this proposal sets no provider license, API, parameter, topology, performance, runtime, precision or fairness claim. Those facts require a later hash-locked adoption record.

### 3.9 Source, semantic, feature and wrong-reading preservation

Every provider stage binds the exact demand/version, source evidence, applicable Activative/identity/context/Visual Semantic/Visual Narrative/Feature Contract/T-V/Composition Intent refs, and full wrong-reading-lock set. Provider parameters are derived execution choices, not new semantic authority.

Generative, layered, composited, restyled, inpainted/outpainted or otherwise transformative stages carry all applicable locks. Deterministic derivatives inherit every parent lock and may add stricter locks; they may not remove or weaken. Relaxation requires a new authorized upstream demand version. Provider fallback never weakens these rules.

### 3.10 Acceptance and external result boundary

Producer execution success, deterministic artifact validation, independent evaluation, VAE production acceptance and downstream consumption acknowledgement are separate states. A provider cannot evaluate or accept its own output. VAE acceptance does not authorize Pipeline composition consumption; TS-DEL-001's external acknowledgement remains separate.

The external `AssetResult` contains governed demand/result/artifact/provenance/evaluation/geometry/limitation evidence. It MUST NOT expose provider-private prompts, secrets, local paths or make provider strategy part of upstream meaning. Mapping uses the externally owned RC4 release; no VAE-local shared fork is created.

## 4. Current brownfield architecture

### 4.1 Verified current state

The VAE repository is a PRD/governance/specification/contract-seed/reference-fixture package. It contains no product source package, provider adapter, model registry implementation, worker, queue, event store, object store, production API, build manifest or executable product test suite. Recent RC4 integration tests are bounded contract-integration evidence, not provider implementation.

The existing TS-VAE-01/02/03/06 documents already establish the correct conceptual seams: immutable demand intake, provider-neutral plan, VAE-owned routing, capability registry, private deterministic ComfyUI compilation, independent evaluation and no self-approval. This proposal amends those seams with exact cross-product provider-ownership behavior rather than replacing them.

### 4.2 Component disposition

| Current/predecessor component | Disposition after adoption | Reason and constraint |
|---|---|---|
| TS-VAE-01 plan ownership and preservation/mutable bindings | `REUSE` | Correct canonical-plan boundary; add exact provider binding and external result traceability without changing demand authority. |
| TS-VAE-02 workcell/route ownership | `REUSE` | Correct smallest-sufficient workcell and independence; provider route contracts must become closed and exact. |
| TS-VAE-03 capability registry/compiler | `ADAPT` | Correct architecture; extend provider-kind profiles and evidence/receipt requirements for this boundary. |
| TS-VAE-06 independent evaluation | `REUSE` | Correct evaluation separation; current status remains specified-not-certified. |
| `VISUAL_PRODUCTION_PLAN.schema.yaml` | `REPLACE_AFTER_ADOPTION` | Seed has open/under-typed plan objects and strings; replacement must be separately governed, versioned and migrated, not edited by this proposal. |
| Workcell authority registry | `ADAPT` | Preserve materializer/evaluator split and add provider-specific least-privilege grants. |
| Predecessor direct provider assumptions | `ARCHIVE` | Historical design/evidence may inform adapters but cannot supply current product authority or production pins. |
| Predecessor deterministic helpers/fixtures | `ADAPT_AFTER_REVIEW` | Reuse only after namespace, ownership, license, dependency, behavior and current-law review. |
| Fake/dry-run provider results and obsolete pins | `ARCHIVE` | Must never be promoted as implementation or production evidence. |
| Pipeline-side provider code, if discovered | `REPLACE_BOUNDARY_OR_REMOVE` | FR-087/088/089 forbid Pipeline provider ownership. Preserve history and migrate through VAE contracts. |

### 4.3 Migration constraint

No current schema or historical record is edited in place. Adoption must produce new immutable profile/plan/binding versions and explicit equivalence or blocked-migration receipts. Unknown provider fields are not flattened into notes. Missing identity, source, license-policy status, runtime digest, compatibility, evaluation or lock evidence is not guessed.

## 5. Proposed architecture and workflows

### 5.1 Components

| Component | Owns | Must not own |
|---|---|---|
| `ProviderCapabilityRegistry` | Immutable provider/capability profiles, compatibility edges, maturity, evidence, revocation and rollback. | Demand meaning, provider self-certification or upstream source authority. |
| `ProviderRouteResolver` | Eligibility and deterministic resolution from plan requirements to an exact bundle. | Adding/removing plan requirements or weakening hard gates. |
| `ProviderBindingCompiler` | Typed VAE-private stage binding and compiled-artifact identity. | Replacing the plan with graph/payload state. |
| `Sam3CapabilityAdapter` | Segmentation/tracking command, provider translation, masks/tracks and execution receipt. | Meaning, identity or acceptance. |
| `MattingCapabilityAdapter` | Matte/alpha-refinement command, artifacts and execution receipt for an eligible provider. | Provider choice outside registry/plan or license-policy approval. |
| `LayeredGenerationAdapter` | Layered-generation command and layer manifest. | Canonical narrative/composition meaning or self-approval. |
| `ComfyUiWorkflowAdapter` | Compile/execute exact private workflow artifact under runtime/node/resource locks. | Canonical plan or public shared schema. |
| `GnmGeometryAdapter` | Source-bound geometry-reference command and outputs under geometry-only policy. | Real-person identity/emotion/demographic/source authority. |
| `ProviderArtifactValidator` | Hash/media/schema/mask/matte/layer/geometry/lock/provenance checks. | Visual/semantic judgment or threshold invention. |
| `IndependentProviderOutputEvaluator` | Required independent visual/composition/identity/feature/lock evaluation. | Production or provider execution; lowering gates. |
| `VaeProductionAcceptanceService` | Accept/reject provider-stage and candidate results under exact plan/profile/evidence. | Downstream consumption authorization. |
| `DelegationResultProjectionAdapter` | Lossless mapping of accepted VAE evidence to external RC4 result/health/blocker contracts. | Copying shared schemas or exposing private control state. |
| `ProviderExecutionRepository` | Atomic aggregate/artifact/receipt/event/dependency/idempotency history. | Mutable current-only state or orphan records. |
| `ProviderInvalidationProjector` | Exact descendant impact from capability/source/plan/evaluation changes. | Deleting history or invalidating unrelated work. |

### 5.2 Capability lifecycle

Registry lifecycle:

`experimental -> benchmarked -> shadow -> limited-production -> production -> deprecated -> retired`

`revoked` may be entered from any active state by authorized governance evidence. Promotion is a governed command over exact benchmarks, compatibility, evaluation, security/runtime, recovery and rollback evidence. Provider code/model cannot promote itself. An active run remains pinned to the capability snapshot accepted for that run.

This proposal assigns no current provider a production state.

### 5.3 Provider execution state machine

`REQUESTED -> PLAN_BOUND -> CAPABILITY_RESOLVED -> COMPILED -> QUEUED -> RUNNING -> OUTPUT_RECEIVED -> DETERMINISTICALLY_VALIDATED -> INDEPENDENTLY_EVALUATED -> PRODUCTION_ACCEPTED -> PROJECTED_FOR_DELIVERY`

Side/terminal states are `BLOCKED`, `FAILED`, `CANCEL_REQUESTED`, `CANCELLED`, `REJECTED`, `SUPERSEDED`, `INVALIDATED` and `REVOKED`. A provider success cannot skip validation/evaluation. A production-accepted result can still remain unacknowledged and non-consumable downstream.

### 5.4 Happy-path workflow

1. Delegation validates/routes an exact immutable demand; VAE intake creates an internal projection without copying shared schema ownership.
2. VAE compiles a `VisualProductionPlan` with provider-neutral capability requirements, preserved/mutable bindings, evaluation, repair and delivery obligations.
3. `ProviderRouteResolver` reads an exact registry snapshot and produces one bounded candidate set. Unsupported or uncertified requirements block rather than downgrade.
4. An authorized VAE decision selects an eligible bundle. Provider names are now VAE-private bindings, not upstream meaning.
5. `ProviderBindingCompiler` emits typed stage bindings and immutable compiled artifacts. For ComfyUI, graph/node/model/runtime/resource identities are locked.
6. A VAE worker executes one typed command with exact input refs/hashes, idempotency key, deadline, cancellation token and expected output contract.
7. The adapter records raw response as untrusted evidence, hashes artifacts, and emits a provider execution receipt. No result is accepted yet.
8. Deterministic validation verifies artifact integrity, dimensions, alpha/masks/layers/geometry, source/demand/plan/lock lineage and runtime identity.
9. The independent evaluator assesses all applicable profiles. It is separate from producer identity and currently cannot claim certified production status.
10. VAE accepts or rejects production output with typed reasons. Repairs create a new bounded plan/binding/run version and preserve successful properties.
11. The result projector emits only externally governed result/health/evidence fields through Delegation. Pipeline remains unaware of private execution controls except evidence needed by the external contract.
12. Pipeline separately decides downstream acknowledgement. VAE acceptance alone does not authorize use.

### 5.5 Provider-specific flows

**SAM3-class segmentation/tracking:** exact source artifact + concept/control requirement + allowed region/time + identity/lock refs -> provider command -> mask/track set -> deterministic topology/time/coverage checks -> independent source/identity/composition evaluation -> accepted mask/track evidence.

**Matting:** exact source/mask + alpha requirement + edge/subject preservation + output profile -> eligible matting binding -> matte/foreground outputs -> alpha/contamination/geometry/identity checks -> independent composition evaluation -> accepted matte evidence.

**Layered generation:** exact plan + semantic/feature/lock refs + provider-neutral layer contract -> provider binding -> generated layer set -> manifest completeness/order/alpha/depth/source checks -> independent semantic/composition/feature/lock evaluation -> accepted layer package.

**ComfyUI:** exact plan stage + capability bundle + inputs + seed policy -> deterministic private graph -> allowlist/lock/resource validation -> worker execution -> output/artifact receipt. Graph is never the plan.

**GNM-class geometry reference:** exact approved identity/source reference + geometry-only requirement + permitted control domains -> geometry binding -> geometry reference outputs -> source-binding/range/label/identity-non-authority checks -> independent use-context evaluation -> accepted geometry-control evidence. Without source binding or externally verified capability evidence, route blocks.

### 5.6 Cancellation, late results and compensation

Cancellation is a command with expected aggregate version. If the provider has not started, VAE cancels without execution. If running, VAE requests provider cancellation and marks any late response `LATE_RESULT_NON_PROMOTABLE`. A late artifact is retained for audit/cost but cannot bypass cancellation or be projected as accepted.

If acceptance committed before cancellation won optimistic concurrency, cancellation creates a new revoked/non-consumable state and invalidation event; it does not erase cost or history. Compensation never mutates external demand or invents a replacement route. A fallback requires a new route/binding decision under the same exact constraints.

### 5.7 Repair, invalidation and replay

Deterministic failure may retry only after a new eligible input/capability/runtime version. Infrastructure failure may retry the identical command identity without consuming a quality round. Visual/semantic failure enters VAE-owned repair only when the failure maps to a mutable plan binding. Upstream-owned failures request amendment and remain blocked.

Typed dependency edges connect demand -> plan -> capability snapshot -> binding -> compiled artifact -> execution -> artifact -> validation -> evaluation -> acceptance -> external result. A changed source, demand, plan, provider digest, license-policy status, runtime, evaluator or lock invalidates only reachable descendants. Historical records remain exactly replayable from stored bytes and pinned reducers.

## 6. Data models, contracts, schemas, and APIs

All proposed internal contracts are closed, immutable, versioned and canonicalized. Unknown fields/enums fail unless an adopted compatibility profile explicitly allows an owner-namespaced extension. There are no `Any` fields, open maps, placeholder objects, machine paths or implied defaults.

### 6.1 `ProviderCapabilityProfile`

```text
ProviderCapabilityProfile {
  profile_id: ProviderCapabilityProfileId
  version: SemanticVersion
  provider_kind: SAM3_SEGMENTATION_TRACKING | MATTING | LAYERED_GENERATION | COMFYUI_WORKFLOW | GNM_GEOMETRY_REFERENCE
  provider_product_ref: VersionedExternalProductRef
  implementation_digest: Sha256
  artifact_or_model_digest?: Sha256
  runtime_profile_ref: VersionedArtifactRef
  supported_operations: NonEmptyOrderedSet<ProviderNeutralOperation>
  supported_asset_families: NonEmptyOrderedSet<AssetFamilyId>
  supported_category_profiles: NonEmptyOrderedSet<CategoryProfileRef>
  required_input_contract_refs: NonEmptyOrderedSet<SchemaRef>
  output_contract_refs: NonEmptyOrderedSet<SchemaRef>
  parameter_envelope: ClosedParameterEnvelope
  compatibility_edges: OrderedSet<CapabilityCompatibilityEdge>
  source_provenance_ref: VersionedArtifactRef
  dependency_review_ref: VersionedArtifactRef
  license_policy_status: UNVERIFIED | REVIEW_REQUIRED | APPROVED_FOR_DECLARED_SCOPE | REJECTED | REVOKED
  benchmark_refs: OrderedSet<VersionedArtifactRef>
  evaluation_profile_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  known_limitation_refs: OrderedSet<TypedLimitation>
  prohibited_use_codes: NonEmptyOrderedSet<ProhibitedUseCode>
  maturity: EXPERIMENTAL | BENCHMARKED | SHADOW | LIMITED_PRODUCTION | PRODUCTION | DEPRECATED | RETIRED | REVOKED
  rollback_profile_ref?: VersionedArtifactRef
  governance_receipt_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  semantic_hash: Sha256
}
```

`UNVERIFIED` or `REVIEW_REQUIRED` license-policy status cannot enter a route requiring execution. This is dependency/provenance policy, not generic content-rights approval authority.

### 6.2 Requirements, resolution and bundle

```text
ProviderCapabilityRequirement {
  requirement_id: ContentDerivedId
  visual_production_plan_ref: VersionedArtifactRef
  plan_stage_ref: VersionedArtifactRef
  operation: ProviderNeutralOperation
  required_input_features: NonEmptyOrderedSet<FeatureRequirement>
  required_output_features: NonEmptyOrderedSet<FeatureRequirement>
  preserved_binding_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  mutable_binding_refs: OrderedSet<VersionedArtifactRef>
  required_evaluation_profile_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  minimum_maturity: CapabilityMaturity
  runtime/resource_constraints: ClosedResourceConstraint
  fallback_policy_ref?: VersionedArtifactRef
  semantic_hash: Sha256
}

CapabilityResolutionDecision {
  decision_id: ContentDerivedId
  requirements: NonEmptyOrderedSet<ProviderCapabilityRequirementRef>
  registry_snapshot_ref: VersionedArtifactRef
  eligible_profiles: OrderedSet<VersionedArtifactRef>
  ineligible_profiles: OrderedSet<CapabilityDenial>
  selected_bundle_ref?: VersionedArtifactRef
  disposition: RESOLVED | CAPABILITY_GAP | HUMAN_RESOLUTION_REQUIRED
  decision_actor_ref: ActorRef
  authority_ref: AuthorityRef
  deterministic_rule_profile_ref: VersionedArtifactRef
  evidence_manifest_hash: Sha256
  semantic_hash: Sha256
}

ProviderCapabilityBundle {
  bundle_id: ContentDerivedId
  registry_snapshot_ref: VersionedArtifactRef
  selected_profile_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  compatibility_edge_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  runtime_profile_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  evaluation_profile_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  rollback_profile_refs: OrderedSet<VersionedArtifactRef>
  lock_manifest_hash: Sha256
  semantic_hash: Sha256
}
```

Resolution cannot add a provider simply because it is installed. Empty eligible set produces `CAPABILITY_GAP`.

### 6.3 Provider binding set and stage bindings

```text
ProviderBindingSet {
  binding_set_id: ContentDerivedId
  visual_production_plan_ref: VersionedArtifactRef
  demand_ref: VersionedExternalArtifactRef
  capability_resolution_ref: VersionedArtifactRef
  capability_bundle_ref: VersionedArtifactRef
  stage_bindings: NonEmptyOrderedSet<ProviderStageBinding>
  preserved_binding_manifest_ref: VersionedArtifactRef
  wrong_reading_lock_manifest_ref: VersionedArtifactRef
  evaluation_obligation_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  compiler_identity: CompilerIdentity
  semantic_hash: Sha256
}

ProviderStageBinding =
  Sam3SegmentationTrackingBinding |
  MattingStageBinding |
  LayeredGenerationStageBinding |
  ComfyUiWorkflowBinding |
  GnmGeometryReferenceBinding
```

Common stage fields are `stage_id`, exact plan/demand/source refs, capability profile/version/hash, runtime ref/hash, typed inputs/outputs, parameter values validated against the envelope, preservation/mutability refs, Feature Contract refs, Composition Intent ref, wrong-reading locks, evaluation refs, budget/deadline, retry/cancellation policy, and semantic hash.

### 6.4 Provider-specific closed bindings

```text
Sam3SegmentationTrackingBinding {
  common: ProviderStageCommon
  source_artifact_ref: VersionedArtifactRef
  source_frame_or_interval_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  concept_or_region_control_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  operation: SEGMENT | TRACK
  expected_mask_contract_ref: SchemaRef
  expected_track_contract_ref?: SchemaRef
  geometry_coordinate_profile_ref: VersionedArtifactRef
}

MattingStageBinding {
  common: ProviderStageCommon
  source_artifact_ref: VersionedArtifactRef
  source_mask_ref?: VersionedArtifactRef
  output_kind: ALPHA_MATTE_AND_FOREGROUND | ALPHA_MATTE_ONLY
  subject_preservation_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  alpha_contract_ref: SchemaRef
}

LayeredGenerationStageBinding {
  common: ProviderStageCommon
  layer_contract_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  required_layer_roles: NonEmptyOrderedSet<LayerRole>
  ordering_constraint_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  alpha_depth_geometry_requirement_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  source_or_generation_parent_refs: NonEmptyOrderedSet<VersionedArtifactRef>
}

ComfyUiWorkflowBinding {
  common: ProviderStageCommon
  workflow_profile_ref: VersionedArtifactRef
  template_digest: Sha256
  compiled_graph_digest: Sha256
  node_lock_manifest_ref: VersionedArtifactRef
  model_resource_lock_manifest_ref: VersionedArtifactRef
  seed_policy_ref: VersionedArtifactRef
  output_slot_contract_refs: NonEmptyOrderedSet<SchemaRef>
}

GnmGeometryReferenceBinding {
  common: ProviderStageCommon
  geometry_only_policy: REQUIRED_TRUE
  approved_source_identity_ref: VersionedArtifactRef
  source_fitting_evidence_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  permitted_geometry_domains: NonEmptyOrderedSet<GeometryDomain>
  prohibited_inference_codes: NonEmptyOrderedSet<ProhibitedUseCode>
  geometry_output_contract_ref: SchemaRef
  control_reference_label: GEOMETRY_CONTROL_NOT_IDENTITY_OR_EMOTIONAL_TRUTH
}
```

GNM binding is invalid without an approved source identity ref and fitting evidence. `GeometryDomain` values require later adopted provider evidence; this proposal does not invent provider parameters.

### 6.5 Execution command, artifacts and receipts

```text
ProviderExecutionCommand {
  command_id: CommandId
  idempotency_key: IdempotencyKey
  execution_id: ProviderExecutionId
  expected_execution_version: NonNegativeInteger
  provider_stage_binding_ref: VersionedArtifactRef
  exact_input_manifest_ref: VersionedArtifactRef
  capability_profile_ref: VersionedArtifactRef
  runtime_profile_ref: VersionedArtifactRef
  actor_ref: ActorRef
  authority_ref: AuthorityRef
  deadline: EvidenceTime
  cancellation_token_ref: VersionedArtifactRef
  canonical_payload_hash: Sha256
}

ProviderArtifactEvidence {
  artifact_ref: ContentAddressedArtifactRef
  artifact_sha256: Sha256
  media_type: RegisteredMediaType
  dimensions_or_duration: TypedMediaFacts
  parent_artifact_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  operation_ref: VersionedArtifactRef
  mask_track_matte_layer_or_geometry_manifest_ref: VersionedArtifactRef
  source_lineage_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  lock_realization_refs: NonEmptyOrderedSet<VersionedArtifactRef>
  limitation_refs: OrderedSet<TypedLimitation>
  semantic_hash: Sha256
}

ProviderExecutionReceipt {
  receipt_id: ContentDerivedId
  command_ref: VersionedArtifactRef
  execution_ref: VersionedArtifactRef
  binding_ref: VersionedArtifactRef
  provider_profile_ref: VersionedArtifactRef
  runtime_profile_ref: VersionedArtifactRef
  exact_input_manifest_hash: Sha256
  raw_response_evidence_ref?: VersionedArtifactRef
  output_artifact_refs: OrderedSet<ProviderArtifactEvidenceRef>
  result: SUCCEEDED_UNVALIDATED | FAILED | CANCELLED | LATE_RESULT_NON_PROMOTABLE
  provider_failure?: TypedProviderFailure
  cost_resource_receipt_ref?: VersionedArtifactRef
  semantic_hash: Sha256
}
```

Provider success is deliberately `SUCCEEDED_UNVALIDATED`. It cannot be mapped to production acceptance.

### 6.6 Validation, evaluation and acceptance

```text
ProviderOutputValidationReceipt {
  receipt_id: ContentDerivedId
  execution_receipt_ref: VersionedArtifactRef
  artifact_integrity: PASS | FAIL
  contract_conformance: PASS | FAIL
  source_and_demand_lineage: PASS | FAIL
  preservation_and_mutability: PASS | FAIL
  wrong_reading_lock_realization: PASS | FAIL
  provider_kind_checks: NonEmptyOrderedSet<TypedCheckResult>
  profile_ref: VersionedArtifactRef
  findings: OrderedSet<TypedFinding>
  pass_status: PASS | FAIL
  evaluated_manifest_hash: Sha256
  semantic_hash: Sha256
}

ProviderOutputEvaluationReceipt {
  receipt_id: ContentDerivedId
  validation_receipt_ref: VersionedArtifactRef
  evaluator_identity: EvaluatorIdentity
  producer_identity: ProducerIdentity
  independence_result: PASS | FAIL
  evaluation_profile_ref: VersionedArtifactRef
  evaluator_certification_state: SPECIFIED_NOT_CERTIFIED | CERTIFIED_FOR_EXACT_SCOPE | REVOKED
  dimension_results: NonEmptyOrderedSet<TypedEvaluationDimensionResult>
  hard_gate_results: NonEmptyOrderedSet<TypedCheckResult>
  responsible_layer_findings: OrderedSet<TypedFinding>
  verdict: PASS | REPAIR_REQUIRED | REJECTED | EVALUATOR_EXCEPTION
  semantic_hash: Sha256
}

VaeProviderProductionDecision {
  decision_id: ContentDerivedId
  visual_production_plan_ref: VersionedArtifactRef
  execution_receipt_ref: VersionedArtifactRef
  validation_receipt_ref: VersionedArtifactRef
  evaluation_receipt_ref: VersionedArtifactRef
  decision: PRODUCTION_ACCEPTED | REPAIR_REQUIRED | REJECTED
  actor_ref: ActorRef
  authority_ref: AuthorityRef
  limitation_refs: OrderedSet<TypedLimitation>
  external_result_projection_ref?: VersionedArtifactRef
  downstream_consumption_authorized: REQUIRED_FALSE
  semantic_hash: Sha256
}
```

Current evaluator state prevents production-certification claims. A later adopted implementation may still perform specified/shadow evaluation, but cannot represent it as certified.

### 6.7 External result projection

`DelegationResultProjectionAdapter` consumes TS-DEL-001's exact external release types by dependency, never copied schemas. It maps:

- exact demand/result/execution identity;
- artifact hashes/media facts and VAE-owned production provenance;
- completion status and limitations;
- measured masks/tracks/mattes/layers/geometry through governed external evidence fields;
- independent evaluation findings/profile/status;
- Feature Contract and wrong-reading-lock realization evidence;
- cost/attempt/runtime health evidence when externally permitted.

It excludes private prompts, graph JSON, secrets, credentials, local paths, model mounts and mutable worker state. Provider-specific evidence is included only when the external contract owns an appropriate evidence field; otherwise it remains a referenced VAE artifact. The adapter cannot extend RC4 with a VAE-local field.

### 6.8 Commands, events and repository

Commands are closed unions: `RegisterProviderCapability`, `ValidateProviderCapability`, `PromoteProviderCapability`, `DeprecateProviderCapability`, `RevokeProviderCapability`, `ResolveProviderRoute`, `CompileProviderBinding`, `SubmitProviderExecution`, `RequestProviderCancellation`, `RecordProviderOutput`, `ValidateProviderOutput`, `EvaluateProviderOutput`, `DecideProviderProductionAcceptance`, `ProjectDelegationAssetResult`, `RequestProviderRepair`, `InvalidateProviderDescendants`, and `RollbackProviderCapability`.

Events mirror successful transitions and bind command, aggregate/version, before/after hash, inputs/outputs, actor/authority and dependencies. A denied command emits a durable denial receipt without success state.

`ProviderExecutionRepository.commit_transition(...)` atomically stores aggregate, capability/binding/artifact records, command/idempotency record, events, receipts, dependency edges and outbox projection. All are visible together or none. State without receipts/artifacts or receipts without state is corruption.

### 6.9 Internal APIs

Future internal endpoints/ports are versioned and VAE-private:

- `POST /internal/v2.1/provider-capabilities:resolve`
- `POST /internal/v2.1/provider-bindings:compile`
- `POST /internal/v2.1/provider-executions`
- `POST /internal/v2.1/provider-executions/{id}:cancel`
- `POST /internal/v2.1/provider-executions/{id}:validate`
- `POST /internal/v2.1/provider-executions/{id}:evaluate`
- `POST /internal/v2.1/provider-executions/{id}:decide`
- `POST /internal/v2.1/provider-executions/{id}:project-result`
- `GET /internal/v2.1/provider-executions/{id}/versions/{version}`
- `GET /internal/v2.1/provider-capabilities/{id}/versions/{version}`

Every write requires exact input hashes, idempotency key and expected version. No API accepts a provider name, `latest`, local file path or raw graph as authority-bearing input.

### 6.10 Canonical serialization, compatibility and supersession

Canonical identity excludes timestamps, host paths, environment, locale, map insertion order, filesystem traversal, worker scheduling and provider response order. Maps are key-sorted; sets use specified semantic ordering; byte/string normalization is versioned. Caller-provided evidence times are recorded but excluded from semantic hashes unless the domain field itself is authoritative.

Compatibility is semantic: the provider must execute, preserve and evaluate every required feature, not merely parse a payload. Adapters cannot drop locks, source lineage, identity, Feature Contract or evaluation obligations. Active executions remain pinned. Supersession/revocation creates new immutable records and blocks new use without deleting history.

## 7. Implementation stages and exact target paths

All paths in this section are **future proposed product-adoption paths**. They MUST NOT be created or modified until VAE grants write/adoption authority, adopts the specification, required authority is ratified, and a separate Development Capsule authorizes a bounded build.

### 7.1 Proposal and adoption locations

- Current proposal: `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/cross-product-proposals/TS-VAE-BOUND-001.md`
- Proposed adopted spec: `02_VISUAL_ASSET_EDITOR/docs/tech-specs/TS-VAE-BOUND-001.md`
- Current adopted-spec write authority: **prohibited** by `02_VISUAL_ASSET_EDITOR/AGENTS.md`

The proposal may be independently audited/revised/re-audited under Program Control. Product adoption requires an explicit VAE-authorized copy/amendment and product-local re-audit. Program Control technical acceptance cannot substitute for product adoption.

### 7.2 Future domain and registry stage

- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/domain/provider_capability.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/domain/provider_binding.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/domain/provider_execution.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/domain/provider_evidence.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/domain/provider_failures.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/domain/provider_events.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/registries/provider_capability_registry.py`

Maps to FR-087/088/089 and acceptance criteria AC-01 through AC-08. Exit evidence: closed schemas, ownership/presence rules, canonical hashes, compatibility and maturity/revocation tests.

### 7.3 Future planning and routing stage

- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/services/provider_route_resolver.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/services/provider_binding_compiler.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/services/provider_requirement_validator.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/services/provider_plan_preservation_validator.py`

Maps to all controlling FRs and AC-02/03/04/06/09/10. Exit evidence: provider-neutral plan, exact registry snapshot, no requirement weakening, no semantic mutation and deterministic resolution.

### 7.4 Future provider adapter stage

- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/adapters/providers/sam3_provider.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/adapters/providers/matting_provider.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/adapters/providers/layered_generation_provider.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/adapters/providers/comfyui_workflow_provider.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/adapters/providers/gnm_geometry_provider.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/adapters/delegation/asset_result_projection.py`

Maps provider-specific positive/negative behavior to AC-03 through AC-08/11/12/13. Exact SDK/library imports, versions and method bindings are deferred until hash-locked provider evidence and an adopted build capsule exist; this proposal does not invent them.

### 7.5 Future execution, evaluation and persistence stage

- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/services/provider_execution_service.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/services/provider_artifact_validator.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/evaluation/provider_output_evaluator.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/services/provider_production_acceptance_service.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/services/provider_invalidation_projector.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/services/provider_replay_service.py`
- `02_VISUAL_ASSET_EDITOR/src/cmf_vae/repositories/provider_execution_repository.py`

Maps to AC-08 through AC-19. Exit evidence: independent evaluation, acceptance separation, atomic failure matrix, idempotency, concurrency, cancellation, invalidation and historical replay.

### 7.6 Future internal contract paths

- `02_VISUAL_ASSET_EDITOR/contracts/internal/provider-capability-profile.schema.json`
- `02_VISUAL_ASSET_EDITOR/contracts/internal/provider-capability-bundle.schema.json`
- `02_VISUAL_ASSET_EDITOR/contracts/internal/provider-binding-set.schema.json`
- `02_VISUAL_ASSET_EDITOR/contracts/internal/provider-execution-receipt.schema.json`
- `02_VISUAL_ASSET_EDITOR/contracts/internal/provider-output-validation.schema.json`
- `02_VISUAL_ASSET_EDITOR/contracts/internal/gnm-geometry-reference-binding.schema.json`

These are VAE-internal only. Shared Delegation schemas remain external immutable dependencies.

### 7.7 Future exact test paths

- `02_VISUAL_ASSET_EDITOR/tests/unit/domain/test_provider_capability_contracts.py`
- `02_VISUAL_ASSET_EDITOR/tests/unit/services/test_provider_route_resolver.py`
- `02_VISUAL_ASSET_EDITOR/tests/unit/services/test_provider_binding_compiler.py`
- `02_VISUAL_ASSET_EDITOR/tests/unit/services/test_provider_plan_preservation.py`
- `02_VISUAL_ASSET_EDITOR/tests/unit/adapters/test_sam3_provider_boundary.py`
- `02_VISUAL_ASSET_EDITOR/tests/unit/adapters/test_matting_provider_boundary.py`
- `02_VISUAL_ASSET_EDITOR/tests/unit/adapters/test_layered_generation_boundary.py`
- `02_VISUAL_ASSET_EDITOR/tests/unit/adapters/test_comfyui_provider_boundary.py`
- `02_VISUAL_ASSET_EDITOR/tests/unit/adapters/test_gnm_geometry_boundary.py`
- `02_VISUAL_ASSET_EDITOR/tests/contract/test_delegation_provider_result_projection.py`
- `02_VISUAL_ASSET_EDITOR/tests/integration/test_provider_execution_atomicity.py`
- `02_VISUAL_ASSET_EDITOR/tests/integration/test_provider_evaluation_and_acceptance.py`
- `02_VISUAL_ASSET_EDITOR/tests/lifecycle/test_provider_cancellation_invalidation_replay.py`
- `02_VISUAL_ASSET_EDITOR/tests/migration/test_provider_boundary_lossless_or_blocked.py`
- `02_VISUAL_ASSET_EDITOR/tests/architecture/test_provider_product_ownership.py`
- `02_VISUAL_ASSET_EDITOR/tests/clean_environment/test_provider_determinism_and_portability.py`
- `02_VISUAL_ASSET_EDITOR/tests/reference_slices/test_st08_02_provider_sovereignty.py`

### 7.8 Adoption/build sequencing

Sequence after separate authorization: adopt/re-audit spec -> approve internal schemas/registries -> implement domain/registry -> plan/routing -> provider adapters one at a time -> validation/evaluation -> persistence/recovery -> external projection -> bounded reference slice. No provider route advances merely because another is ready. GNM-class route remains blocked until exact external evidence exists.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

| Failure code | Meaning | Owner / response |
|---|---|---|
| `VAE_PROVIDER_PRODUCT_BOUNDARY_VIOLATION` | Pipeline/Delegation/Studio attempts provider selection/execution or VAE provider code is located outside VAE. | Stop; Program Control/product-owner reconciliation. |
| `VAE_PROVIDER_PLAN_AUTHORITY_MUTATION` | Provider binding changes demand/plan semantic or preserved fields. | Reject binding; upstream amendment if meaning must change. |
| `VAE_PROVIDER_CAPABILITY_UNREGISTERED` | Provider/model/workflow/runtime lacks exact registry identity. | VAE blocks before compile. |
| `VAE_PROVIDER_CAPABILITY_INELIGIBLE` | Maturity/profile/category/operation/evaluation policy is unsupported. | VAE returns capability gap; no downgrade. |
| `VAE_PROVIDER_DEPENDENCY_EVIDENCE_MISSING` | Exact provenance/dependency/license-policy evidence absent. | Block adoption/execution of that capability. |
| `VAE_PROVIDER_COMPATIBILITY_FAILED` | Required relationship or behavior unsupported. | Select only an already-declared eligible fallback or block. |
| `VAE_PROVIDER_RUNTIME_UNPINNED` | Runtime/container/nodes/models/resources are mutable or unresolved. | Reject compile/execution. |
| `VAE_PROVIDER_GRAPH_BECAME_PLAN` | Raw graph/payload is submitted as canonical plan state. | Reject as provider artifact. |
| `VAE_PROVIDER_EXECUTION_INTEGRITY_FAILED` | Inputs/runtime/output digest differs from binding. | Quarantine outputs; no quality retry. |
| `VAE_SAM3_OUTPUT_CONTRACT_FAILED` | Required mask/track/geometry/source binding missing or invalid. | Reject output; repair only within mutable binding. |
| `VAE_MATTING_OUTPUT_CONTRACT_FAILED` | Alpha/foreground/source/geometry evidence invalid. | Reject output. |
| `VAE_LAYER_PACKAGE_CONTRACT_FAILED` | Layer roles/order/alpha/depth/parents incomplete or inconsistent. | Reject output. |
| `VAE_GNM_GEOMETRY_SOURCE_BINDING_MISSING` | Real-person geometry has no approved source/fitting evidence. | Prohibit route. |
| `VAE_GNM_IDENTITY_OR_EMOTION_AUTHORITY_VIOLATION` | Geometry output is treated as identity/emotional/demographic truth. | Reject and raise authority incident. |
| `VAE_PROVIDER_WRONG_READING_LOCK_LOSS` | Provider binding/output removes or weakens a lock. | Reject; new upstream demand required for relaxation. |
| `VAE_PROVIDER_SELF_EVALUATION` | Producer and evaluator are not independent. | Reject evaluation/acceptance. |
| `VAE_PROVIDER_EVALUATOR_NOT_CERTIFIED` | A production claim relies on current specified-only evaluator. | Block production/certification claim; retain technical evidence. |
| `VAE_PROVIDER_LATE_RESULT` | Output arrives after cancellation/supersession/revocation. | Store as non-promotable evidence. |
| `VAE_PROVIDER_IDEMPOTENCY_CONFLICT` | Same key carries byte-different command. | Conflict; retain original record. |
| `VAE_PROVIDER_STALE_EXPECTED_VERSION` | Aggregate/plan/capability changed. | No commit; caller reloads exact state. |
| `VAE_PROVIDER_ATOMIC_COMMIT_FAILED` | Any state/artifact/receipt/event/edge/outbox write fails. | Roll back visibility of all staged members. |
| `VAE_PROVIDER_REPLAY_DIVERGENCE` | Historical reconstruction hash differs. | Quarantine and stop at first divergence. |
| `VAE_PROVIDER_EXTERNAL_PROJECTION_LOSSY` | Required result evidence cannot map to external contract. | Do not emit result; negotiate governed compatibility. |

Infrastructure/transient failures may retry the exact idempotent command. Capability, authority, source, license-policy, compatibility, semantic, evaluation and quality failures do not blind-retry.

### 8.2 `NOT_APPLICABLE` handling

`NOT_APPLICABLE` is a typed decision with requirement/field, reason code, evidence, authority/profile and evaluator identity. It is forbidden for exact capability/runtime identity, demand/plan/source lineage, preserved bindings, required output contract, locks, mandatory evaluator or provider execution receipt.

It may be valid for track output on segmentation-only operation, source mask on provider-native matting when the adopted capability contract permits it, GNM stage on a non-geometry route, or temporal evaluation on a static artifact. An empty field or provider omission is not N/A.

### 8.3 Migration and compatibility

Migration produces new immutable profiles/bindings/artifacts plus a receipt. It never edits current/historical VAE specs, releases or provider output.

- Direct provider calls found in Pipeline are inventoried and blocked from new use; historical traces remain preserved.
- Mutable filenames/tags resolve to exact digest only with verified source evidence; otherwise migration blocks.
- Raw ComfyUI graphs become historical provider artifacts only when exact plan/binding/runtime/input/output lineage can be established.
- Historical masks/mattes/layers/geometry without exact source, plan, provider/runtime, locks and evaluation cannot be promoted.
- GNM-like geometry without source-backed fitting evidence remains historical/non-consumable; identity is never inferred.
- Unknown license-policy, capability or evaluation status remains unknown and blocks any route requiring it.
- Active work remains pinned to its accepted versions; deprecated versions do not erase historical reproducibility.

Compatibility is behavior-based. An adapter that parses but cannot enforce provenance, preserved bindings, locks, output contracts or evaluation is incompatible.

### 8.4 Rollback and revocation

Deployment rollback affects future commands and uses a pinned prior registry/compiler/adapter/runtime bundle. It never rewrites historical plan/binding/execution/result bytes. Capability rollback requires a prior eligible profile and impact receipt; absence blocks new execution.

Revocation blocks new use and invalidates exact dependent current artifacts/results/bindings while preserving historical replay. A provider outage may select only a predeclared compatible fallback under the same constraints. No fallback route is invented at runtime.

### 8.5 Atomicity, idempotency and concurrency recovery

Repository transitions write aggregate, artifacts, validation/evaluation, command record, event, dependency edges, outbox and receipt together. Fault injection at each member must show all-or-none visibility. Identical retry after restart returns exact previous hashes. Concurrent plan/binding/acceptance/cancellation commands serialize by expected version; exactly one succeeds.

A provider timeout after request submission does not prove failure or success. Reconciliation queries the exact provider job under the same execution identity. A response with mismatched input/runtime/binding hashes is quarantined.

### 8.6 Observability and security

Structured telemetry records provider kind/profile/version hashes, plan/binding/execution IDs, runtime, operation, input/output counts and hashes, stage/state, validation/evaluation status, maturity, cancellation/late-result, cost/resource receipt, failure code/owner and invalidation fan-out.

Logs exclude raw private source, secrets, credentials, access URLs, prompt bodies not required as evidence, absolute machine paths, local mounts and unrelated identity data. Provider inputs are untrusted data; they cannot grant tools or authority. Worker permissions are stage-local: content-addressed inputs, output namespace, declared provider endpoint/resource and no dynamic install or unrestricted egress.

Technical security, provenance and runtime integrity are operational requirements. This proposal creates no generic content or creative approval authority.

## 9. Behavior-specific acceptance criteria

Every criterion is governed by FR-087/088/089 and ST-08.02 unless narrowed below. Each includes a concrete failure and required test/evidence layer.

### AC-01 - product ownership boundary

**Given** a Pipeline node requests segmentation, matting, layered generation or geometry control, **when** ownership validation runs, **then** it can emit only a provider-neutral Visual Asset Demand and cannot import/call/configure a VAE provider. A direct Pipeline SAM3 SDK call fails `VAE_PROVIDER_PRODUCT_BOUNDARY_VIOLATION`. **Evidence:** dependency/import graph and command spy. **Layer:** architecture/cross-product.

### AC-02 - one provider-neutral plan

**Given** an admitted demand, **when** VAE plans production, **then** one immutable `VisualProductionPlan` expresses functions/constraints while provider names/node IDs appear only in VAE-private bindings. Raw ComfyUI JSON submitted as the plan is rejected. **Evidence:** plan/binding diff and schema tests. **Layer:** domain/contract.

### AC-03 - FR-087 SAM3 inside VAE

**Given** a plan selects an eligible SAM3-class segmentation/tracking capability, **when** execution succeeds, **then** VAE owns exact provider/runtime identity, masks/tracks/geometry, validation, independent evaluation and receipt; Pipeline receives only externally governed result/evidence. A Pipeline-created provider job or mask with no source binding fails. **Evidence:** VAE adapter receipt, external projection and boundary spy. **Layer:** integration.

### AC-04 - SAM3 is not semantic authority

**Given** a mask/track, **when** it is used, **then** it remains pixel/region evidence under exact source/demand/plan refs and cannot assign person identity, viewer role or Composition Intent. A provider label treated as identity fails. **Evidence:** ownership mutation tests. **Layer:** domain/adversarial.

### AC-05 - FR-088 governed matting selection

**Given** a plan requires alpha refinement, **when** VAE resolves a matting capability, **then** the selected profile has exact version/digest/runtime, supported operation, compatibility, provenance/license-policy status, benchmark/evaluation, maturity and rollback. A provider filename alone or unreviewed license-policy status blocks before execution. **Evidence:** registry decision/denial receipt. **Layer:** registry/contract.

### AC-06 - matting result integrity

**Given** an eligible matting execution, **when** outputs return, **then** matte/foreground hashes, alpha contract, source/geometry/preservation/limitation evidence pass before independent evaluation. An attractive cutout with contaminated alpha or missing source identity is rejected. **Evidence:** fixture outputs and validation receipt. **Layer:** adapter/integration.

### AC-07 - FR-089 layered-generation sovereignty

**Given** a layer-separated route, **when** VAE executes, **then** every layer declares role, parent, alpha/depth/order/geometry, mutability, locks and evaluation; provider output cannot change Visual Narrative or composition meaning. A renamed/reordered layer package that changes semantic role fails. **Evidence:** layer manifest and mutation tests. **Layer:** contract/evaluation.

### AC-08 - ComfyUI embodiment only

**Given** the same plan, capability bundle, inputs and compiler, **when** ComfyUI graph compilation repeats in fresh processes, **then** graph and lock hashes match. Mutable tags, startup installs, unknown nodes, manual graph edits or environment-specific paths fail. **Evidence:** golden graph/hash/path-security tests. **Layer:** compiler/clean environment.

### AC-09 - GNM geometry-only boundary

**Given** a real-person geometry-reference route, **when** binding validates, **then** exact approved source identity and fitting evidence exist, outputs are labeled geometry controls, and prohibited identity/emotion/demographic inference codes are active. A request to generate a coach identity from demographic/provider defaults is denied. **Evidence:** binding/denial receipts. **Layer:** authority/adversarial.

### AC-10 - unavailable GNM evidence blocks promotion

**Given** `SRC-EXT-026` exact bytes/license/runtime evidence remain unavailable, **when** a GNM capability is proposed for executable or certified use, **then** dependency evidence remains unverified and the capability cannot advance. A locator/assignment title treated as license or capability proof fails. **Evidence:** source-disposition and promotion-gate test. **Layer:** governance/registry.

### AC-11 - demand/semantic preservation

**Given** source, AIR, Feature Contract, Composition Intent and wrong-reading constraints, **when** any provider binding/output is compared, **then** all authoritative refs/hashes and preserved values match. A provider prompt/output that adds meaning or weakens a lock fails. **Evidence:** before/after pointer/hash crosswalk. **Layer:** contract/property.

### AC-12 - compatibility cannot be parse-only

**Given** a provider adapter parses the command, **when** it cannot enforce a required output, lock, provenance, runtime or evaluation feature, **then** resolution returns incompatible. Silent feature omission fails. **Evidence:** capability negotiation matrix and negative adapter. **Layer:** compatibility.

### AC-13 - independent evaluation and certification truth

**Given** provider output, **when** producer and evaluator identity/program are the same or the required evaluator is absent, **then** production acceptance is blocked. Capability declaration does not change evaluator `specified_not_certified` or production false. **Evidence:** independence/status tests. **Layer:** evaluation/governance.

### AC-14 - production acceptance is not consumption

**Given** a VAE production-accepted result, **when** Pipeline acknowledgement is absent, **then** downstream composition use remains unauthorized. VAE decision always records `downstream_consumption_authorized: false`. **Evidence:** three-stage lifecycle fixture. **Layer:** cross-product lifecycle.

### AC-15 - cancellation and late results

**Given** cancellation wins expected-version concurrency while a provider runs, **when** a late success arrives, **then** it is retained as `LATE_RESULT_NON_PROMOTABLE` and cannot be accepted/projected. Deleting cost/history or promoting the late artifact fails. **Evidence:** race/fault-injection test. **Layer:** lifecycle/recovery.

### AC-16 - atomicity and idempotency

**Given** failure at any persistence member, **when** commit executes, **then** state, artifacts, receipts, events, edges and outbox are all visible or all absent. Identical retries return exact hashes; key reuse with different bytes conflicts. **Evidence:** crash matrix and restart tests. **Layer:** persistence.

### AC-17 - selective invalidation and history

**Given** one capability/runtime/source/plan/evaluator is revoked or superseded, **when** impact projects, **then** only exact descendants become ineligible, stale outputs cannot be used, and every historical version replays. Global deletion or unrelated invalidation fails. **Evidence:** dependency graph and historical replay. **Layer:** recovery/property.

### AC-18 - migration lossless or blocked

**Given** predecessor/direct-provider evidence, **when** migration runs, **then** exact provider/runtime/input/output/plan/source/lock/evaluation fields map to new immutable records or migration blocks. Guessed provider digest, license status, identity, source or evaluation fails. **Evidence:** paired migration fixtures. **Layer:** migration.

### AC-19 - portability and deterministic identity

**Given** identical logical inputs across roots, clocks, locales, environment variables, insertion/traversal/provider response orders, **when** resolution/binding/receipt compilation runs, **then** canonical bytes/hashes match and contain no absolute path. **Evidence:** two-process/two-root hash matrix. **Layer:** clean environment.

### AC-20 - proposal/adoption/claim ceiling

**Given** this Program Control proposal and even complete synthetic tests, **when** status is reported, **then** quality is `WRITTEN_PENDING_AUDIT`, adoption `PRODUCT_ADOPTION_REQUIRED`, build `NOT_BUILD_READY`, authority `CANDIDATE_NOT_CURRENT`, Stage 5 unauthorized, evaluator specified-not-certified and production/certification false. Any product-local acceptance or capsule claim fails. **Evidence:** metadata, path and status assertions. **Layer:** governance.

## 10. Testing and completion evidence

### 10.1 Proposed future test suites

The exact future test paths are listed in section 7. They must cover:

- closed domain schemas, presence/`NOT_APPLICABLE`, canonical serialization and hashing;
- registry compatibility, maturity, provenance/license-policy evidence, promotion/revocation and rollback;
- provider-neutral plan versus private bindings and graphs;
- SAM3 mask/track/source/geometry evidence plus direct-Pipeline-call denial;
- matting alpha/foreground/source/preservation evidence and unverified-provider denial;
- layer role/order/alpha/depth/parent/locks and semantic-mutation denial;
- deterministic ComfyUI graph/lock/resource security and manual-edit denial;
- GNM source-backed geometry-only binding and identity/emotion/demographic misuse denial;
- TS-DEL-001/RC4 result projection without shared-schema fork or lossy fields;
- deterministic validation, evaluator independence, hard gates and specified-not-certified status;
- acceptance versus consumption acknowledgement;
- atomicity, restart idempotency, concurrency/cancellation races, late results, invalidation and replay;
- lossless-or-blocked predecessor migration;
- clean extracted environment portability and claim-ceiling enforcement.

### 10.2 Required fixture matrix

At minimum:

- provider-neutral segmentation demand with eligible and ineligible SAM3-class profiles;
- Pipeline direct-provider call attempt;
- mask/track tied to wrong source/version;
- matting provider missing exact dependency/license-policy evidence;
- valid matte and alpha contamination case;
- valid layered package and missing/reordered semantic layer;
- ComfyUI graph with exact locks, unknown node, mutable tag, network fetch, manual edit and absolute path;
- source-backed geometry-reference case, missing fitting evidence and demographic/identity misuse request;
- provider output attempting to weaken inherited wrong-reading locks;
- parse-only adapter missing evaluation behavior;
- same producer/evaluator identity;
- VAE-accepted but unacknowledged result;
- cancellation/result and acceptance/revocation races;
- capability/runtime/evaluator revocation with selective descendants;
- predecessor record complete enough for migration and one with ambiguous provider/source identity;
- identical inputs under distinct roots, process environments and ordering.

### 10.3 Determinism and replay proof

Run canonical fixtures in at least two fresh processes and two workspace roots with explicit command IDs/evidence times/seeds. Compare byte-for-byte registry snapshot, resolution, bundle, binding, compiled graph, command, execution receipt, validation, evaluation, production decision, external projection, events, edges and commit receipt.

Replay every success/denial/cancellation/supersession/revocation from immutable events/artifacts without `latest` lookups. Search generated artifacts for drive/UNC paths, environment expansion, hostnames, current-time/random identity and unstable map/provider ordering. Any semantic hash difference fails.

### 10.4 Product-adoption evidence required before build readiness

Before the proposal can become an adopted VAE spec, require:

1. independent audit/revision/re-audit evidence for the Program Control proposal;
2. attributable VAE write/adoption authority that supersedes the current path prohibition for this exact adoption action;
3. ratification or explicit governed status for the controlling candidate authority;
4. adopted bytes hash-identical to the technically accepted proposal, or a field-level adoption delta with authority and new audit;
5. product-local re-audit of the adopted bytes under then-current VAE authority/status;
6. reconciliation with TS-VAE-01/02/03/06 and any adopted internal schema plan;
7. exact TS-DEL-001 accepted/adopted interface hash and shared release compatibility evidence;
8. exact provider/dependency/source/provenance/license-policy bytes for each capability intended for implementation;
9. GNM-class external evidence hash lock before that route leaves blocked/experimental status;
10. evaluator certification evidence appropriate to any production claim;
11. compute, storage, recovery, rollback and security proof;
12. a separately authorized, exact-path Development Capsule.

Program Control acceptance alone cannot issue a VAE Development Capsule. VAE Stage 5 remains unauthorized until its own readiness gates close.

### 10.5 Later Build Receipt requirements

If separately authorized after adoption, a Build Receipt must distinguish:

- code/schema/test implementation coverage;
- provider adapter existence versus capability contract compatibility;
- registry maturity per exact capability;
- deterministic/synthetic fixture proof;
- real provider/runtime/compute proof;
- evaluator specification versus certification;
- recovery/rollback proof;
- external Delegation/Pipeline conformance;
- production eligibility and certification;
- unresolved limitations and blocked routes.

The receipt must include exact source/test hashes, FR/Story/symbol/test traceability, atomic fault matrix, two-process determinism results, migration/replay evidence, no-local-shared-schema-fork scan, ownership boundary scan and claim ceiling. This proposal issues no Build Receipt.

### 10.6 Current completion state

This Program Control proposal completes only as:

```yaml
quality_state: WRITTEN_PENDING_AUDIT
adoption_state: PRODUCT_ADOPTION_REQUIRED
build_state: NOT_BUILD_READY
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
target_product_modified: false
```

The next permitted action is independent audit by a different agent. After technical acceptance, VAE product adoption remains a separate governed gate. No writer self-audit, revision, acceptance, implementation, provider execution, schema/release creation, Development Capsule, Stage 5 or production authorization occurred.
