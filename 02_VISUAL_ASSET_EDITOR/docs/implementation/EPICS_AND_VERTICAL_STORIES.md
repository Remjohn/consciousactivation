# CMF Visual Asset Editor Epics and Vertical Stories

**Stage:** 4 - Readiness  
**Planning scope:** Release 1, Format 02 Minimal Coach Theatre  
**Implementation authorization:** blocked pending a PASS readiness receipt  
**Requirement baseline:** 176 FRs, 70 NFRs, 28 locked decisions

## Planning rules

These Epics organize work around caller, operator, and downstream-consumer value. They consume the Stage 2 architecture and Stage 3 Delegation boundary; they do not redesign Builder Workflow Runtime, Harness IR, JIT Skills, Control Tower, category constitutions, or Content Harness authority.

Each Story owns one eight-FR feature block so every FR has one primary delivery owner. Cross-cutting NFRs have one primary Story and apply as acceptance gates wherever referenced by the requirement registry. A Story can depend only on a lower-numbered Story. Infrastructure and registries are introduced only when the first vertical Story requires them.

## Epic sequence

| Epic | Value delivered | Primary stories | Depends on |
|---|---|---|---|
| E01 Governed Demand to Feasible Plan | A caller submits one immutable demand and receives a reproducible provider-neutral production plan or an owner-routed conflict | VS-01..VS-05 | none |
| E02 Observable Asynchronous Production | A caller and operator can submit, observe, resume, cancel, and diagnose a plan through existing runtime/Control Tower owners | VS-06..VS-08 | E01 |
| E03 Certified Candidate Portfolio | The service resolves a certified route/workcell/capability bundle, controls budget, and executes equivalent local/cloud jobs | VS-09..VS-13 | E01, E02 |
| E04 Independent Acceptance and Repair | Independent evaluation selects only hard-gate-passing candidates and performs one causal bounded repair | VS-14..VS-15 | E03 |
| E05 Immutable Result and Reuse | Accepted assets, geometry, lineage, usage, recurrence, and steering knowledge remain immutable and authority-aware | VS-16..VS-19 | E04 |
| E06 Governed Capability Improvement | Recurrent gaps can produce evidence-backed capability development without contaminating production authority | VS-20 | E05 |
| E07 Format 02 Certification and Handoff | The complete reference path, rollback, compatibility, scope claims, and Development Capsule earn an evidence-backed release state | VS-21..VS-22 | E06 |

## Vertical Stories

| Story | Outcome | FR owner | Depends on | Core Given/When/Then acceptance |
|---|---|---|---|---|
| VS-01 Constitutional production boundary | Product, semantic, human, producer, and architecture authority gates are enforced before work | F01 / FR-001..008 | none | Given a demand or action outside registered authority, when admission evaluates it, then work is blocked with a typed reason and no state mutation. |
| VS-02 Immutable demand admission | One canonical Format 02 demand is authenticated, hash-addressed, idempotently submitted, and receipted | F02 / FR-009..016 | VS-01 | Given the same valid submission twice, when both reach admission, then one demand snapshot/execution is admitted and the existing receipt is returned. |
| VS-03 Composition feasibility | Composition intent is validated before expensive production and produces typed geometry obligations or conflict evidence | F05 / FR-033..040 | VS-02 | Given contradictory protected regions and subject geometry, when feasibility runs, then no GPU work starts and a typed non-mutating conflict is emitted. |
| VS-04 Reproducible production plan | Demand and feasibility evidence compile into an immutable provider-neutral Visual Production Plan | F09 / FR-065..072 | VS-03 | Given an accepted exact demand, when planning runs twice with the same registry snapshots, then canonical plan bytes/hash and stage dependencies match. |
| VS-05 Governed conflict resolution | Internal plan changes remain within authority; demand changes return proposals and require supersession | F20 / FR-153..160 | VS-04 | Given a demand-owned constraint conflict, when VAE proposes a change, then the accepted demand remains unchanged until Content Harness supplies a linked new version. |
| VS-06 Resumable execution | Typed nodes execute through the Builder runtime port with events, checkpoints, retries, cancellation, and terminal states | F10 / FR-073..080 | VS-04 | Given a worker interruption after a committed checkpoint, when execution resumes, then completed nodes are reused and no quality-repair round is consumed. |
| VS-07 Asynchronous Delegation service | Callers receive versioned submission, status, event, cancellation, backpressure, and result behavior | F19 / FR-145..152 | VS-02, VS-06 | Given accepted production output without downstream acknowledgement, when status is read, then public lifecycle remains `RESULT_READY`, never `COMPLETED`. |
| VS-08 Supervisory evidence | Existing Control Tower projections expose demand, plan, candidates, lineage, workers, budget, exceptions, and analytics | F18 / FR-137..144 | VS-06, VS-07 | Given a typed exception, when an operator opens the projection, then evidence, permitted actions, authority owner, and action receipt are available without creating a second authority store. |
| VS-09 Governed route selection | The least-complex reliable reuse/transform/generation/hybrid route is chosen with inputs, fallbacks, and receipts | F06 / FR-041..048 | VS-04 | Given certified reuse and generation routes that both satisfy the demand, when routing compares them, then governed reuse wins unless evidence declares it unsuitable. |
| VS-10 Minimal specialist workcell | Only sufficient registered specialists activate; strategy, materialization, deterministic policy, and evaluation stay separate | F07 / FR-049..056 | VS-09 | Given a standard character demand, when the workcell compiles, then no unneeded capability or authority is activated and producer/evaluator identities differ. |
| VS-11 Pinned capability bundle | Workflow, model, VAE, LoRA/control, compiler, and runtime compatibility are resolved and graph compilation is deterministic | F08 / FR-057..064 | VS-09, VS-10 | Given a bundle with an incompatible node/model relation, when compilation validates it, then no provider artifact executes and the incompatibility is receipted. |
| VS-12 Budgeted candidate portfolio | Standard budget reserves four initial/ten maximum candidates, filters hard failures, and ranks quality first | F16 / FR-121..128 | VS-11 | Given one fast failed candidate and one slower hard-gate pass, when selection runs, then only the passing candidate is eligible and budget pressure cannot lower a gate. |
| VS-13 Equivalent local/cloud execution | The same compiled artifact executes through isolated digest-pinned local and cloud worker adapters with recovery receipts | F12 / FR-089..096 | VS-06, VS-11, VS-12 | Given local worker loss after checkpoint, when cloud failover is authorized, then the same plan/artifact/bindings resume and stale local output cannot commit. |
| VS-14 Independent quality decision | Deterministic checks precede independent asset, composition, recurrence, and applicable temporal evaluation | F14 / FR-105..112 | VS-13 | Given candidates with semantic failure, identity drift, hand artifact, and one compliant output, when evaluation runs, then hard failures cannot be averaged away and only compliant output can pass. |
| VS-15 Causal targeted repair | A typed repair preserves valid properties, changes the responsible layer, reruns invalidated descendants, and stops by round three | F15 / FR-113..120 | VS-14 | Given a gesture-only failure with identity/expression/gaze/geometry passing, when repaired, then only allowed pose/gesture bindings and invalidated descendants rerun. |
| VS-16 Canonical asset ontology | Reference evidence, production assets, eight families, represented/certified scope, and migrations remain explicit | F03 / FR-017..024 | VS-02, VS-14 | Given an uncategorized output, when promotion is requested, then it cannot become a production asset until family/subtype and certified scope are explicit. |
| VS-17 Immutable asset lifecycle | Accepted master, variants, geometry, lineage, receipts, reuse, supersession, revocation, and projections are immutable | F04 / FR-025..032 | VS-15, VS-16 | Given a new accepted replacement, when promoted, then the prior version and receipts remain historical and consumers receive a governed replacement notice. |
| VS-18 Syntax-aware asset memory | Every rendered use records context; retrieval favors valid recurrence without hiding supersession or fatigue | F11 / FR-081..088 | VS-17 | Given a superseded character asset that is visually similar, when retrieval runs, then authority/version filters exclude it before similarity ranking. |
| VS-19 Steering and Minimum Complete Context | Production evidence becomes governed recipes/OKF knowledge and authority-aware hybrid retrieval context | F17 / FR-129..136 | VS-18 | Given supporting and contradictory steering evidence, when context compiles, then both are represented with provenance and the model cannot silently choose owner meaning. |
| VS-20 Evidence-backed capability development | Recurring gaps can create isolated datasets, controls, benchmarks, promotion, deprecation, and rollback evidence | F13 / FR-097..104 | VS-11, VS-15, VS-19 | Given a recurrent identity gap, when a LoRA/workflow experiment improves the target but regresses continuity, then promotion is denied and the prior capability remains active. |
| VS-21 Format 02 benchmark and certification | Layered representative/golden/failure/adversarial/mutation/repair/recovery/evaluator/compatibility cases certify only declared scope | F21 / FR-161..168 | VS-05, VS-08, VS-13, VS-15, VS-17, VS-20 | Given a single successful happy path, when certification is evaluated, then release remains uncertified until every mandatory case family and hard gate passes. |
| VS-22 Versioned release and Development Capsule | Product/contracts/capabilities/migrations/rollback are independently versioned and implementation/release authorization is evidence-backed | F22 / FR-169..176 | VS-21 | Given any missing hard-gate evidence or unresolved blocking conflict, when the readiness receipt is generated, then implementation authorization remains false. |

## Complete Functional Requirement Ownership

| Feature | Requirement inventory | Epic / Story | Primary technical specification |
|---|---|---|---|
| F01 | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008 | E01 / VS-01 | TS-VAE-10 |
| F02 | FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016 | E01 / VS-02 | TS-VAE-01 |
| F03 | FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-024 | E05 / VS-16 | TS-VAE-08 |
| F04 | FR-025, FR-026, FR-027, FR-028, FR-029, FR-030, FR-031, FR-032 | E05 / VS-17 | TS-VAE-08 |
| F05 | FR-033, FR-034, FR-035, FR-036, FR-037, FR-038, FR-039, FR-040 | E01 / VS-03 | TS-VAE-01 |
| F06 | FR-041, FR-042, FR-043, FR-044, FR-045, FR-046, FR-047, FR-048 | E03 / VS-09 | TS-VAE-02 |
| F07 | FR-049, FR-050, FR-051, FR-052, FR-053, FR-054, FR-055, FR-056 | E03 / VS-10 | TS-VAE-02 |
| F08 | FR-057, FR-058, FR-059, FR-060, FR-061, FR-062, FR-063, FR-064 | E03 / VS-11 | TS-VAE-03 |
| F09 | FR-065, FR-066, FR-067, FR-068, FR-069, FR-070, FR-071, FR-072 | E01 / VS-04 | TS-VAE-01 |
| F10 | FR-073, FR-074, FR-075, FR-076, FR-077, FR-078, FR-079, FR-080 | E02 / VS-06 | TS-VAE-09 |
| F11 | FR-081, FR-082, FR-083, FR-084, FR-085, FR-086, FR-087, FR-088 | E05 / VS-18 | TS-VAE-08 |
| F12 | FR-089, FR-090, FR-091, FR-092, FR-093, FR-094, FR-095, FR-096 | E03 / VS-13 | TS-VAE-04 |
| F13 | FR-097, FR-098, FR-099, FR-100, FR-101, FR-102, FR-103, FR-104 | E06 / VS-20 | TS-VAE-11 |
| F14 | FR-105, FR-106, FR-107, FR-108, FR-109, FR-110, FR-111, FR-112 | E04 / VS-14 | TS-VAE-06 |
| F15 | FR-113, FR-114, FR-115, FR-116, FR-117, FR-118, FR-119, FR-120 | E04 / VS-15 | TS-VAE-07 |
| F16 | FR-121, FR-122, FR-123, FR-124, FR-125, FR-126, FR-127, FR-128 | E03 / VS-12 | TS-VAE-05 |
| F17 | FR-129, FR-130, FR-131, FR-132, FR-133, FR-134, FR-135, FR-136 | E05 / VS-19 | TS-VAE-08 |
| F18 | FR-137, FR-138, FR-139, FR-140, FR-141, FR-142, FR-143, FR-144 | E02 / VS-08 | TS-VAE-09 |
| F19 | FR-145, FR-146, FR-147, FR-148, FR-149, FR-150, FR-151, FR-152 | E02 / VS-07 | TS-VAE-09 |
| F20 | FR-153, FR-154, FR-155, FR-156, FR-157, FR-158, FR-159, FR-160 | E01 / VS-05 | TS-VAE-01 |
| F21 | FR-161, FR-162, FR-163, FR-164, FR-165, FR-166, FR-167, FR-168 | E07 / VS-21 | TS-VAE-10 |
| F22 | FR-169, FR-170, FR-171, FR-172, FR-173, FR-174, FR-175, FR-176 | E07 / VS-22 | TS-VAE-10 |

Coverage result: **176 of 176 FRs have exactly one Epic/Story owner.**

## Complete NFR Ownership

| NFR inventory | Primary Story | Mandatory evidence |
|---|---|---|
| NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005 | VS-01 | authority mutation, observation/inference, meaning hard-gate, profile-context, degradation tests |
| NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005 | VS-06 | duplicate, restart, repair-limit, failure-containment, rollback tests |
| NFR-PERF-001, NFR-PERF-002, NFR-PERF-003, NFR-PERF-004, NFR-PERF-005 | VS-12 | budget-class latency, node timing, checkpoint reuse, early stop, degradation metrics |
| NFR-COST-001, NFR-COST-002, NFR-COST-003, NFR-COST-004, NFR-COST-005 | VS-12 | quote, ceiling, accepted-asset cost, value routing, learning-budget isolation |
| NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005 | VS-22 | immutable IDs, lineage, contract-output links, knowledge provenance, historical version preservation |
| NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005 | VS-08 | event completeness, evidence status, drill-down, analytics, action receipt tests |
| NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005 | VS-07 | least privilege, sandboxing, secret scan, hostile input, artifact integrity tests |
| NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005 | VS-22 | version, minor, migration, pinning, compatibility-manifest fixtures |
| NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005 | VS-14 | producer separation, profile hard gates, calibration, protected set, no-average-compensation tests |
| NFR-MEM-001, NFR-MEM-002, NFR-MEM-003, NFR-MEM-004, NFR-MEM-005 | VS-19 | contextual memory, authority filter, hybrid retrieval, contradiction, minimum-context tests |
| NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005 | VS-13 | immutable profile, scheduling, recovery, isolation, local/cloud equivalence tests |
| NFR-UX-001, NFR-UX-002, NFR-UX-003, NFR-UX-004, NFR-UX-005 | VS-08 | policy-first, exception clarity, visual evidence, accessibility, no routine approval tests |
| NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005 | VS-06 | typed nodes, deterministic orchestration, retry/repair split, bounded parallelism, integration tests |
| NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005 | VS-22 (the registry-promotion item is delivered by VS-20) | preservation, demand authority, promotion governance, readiness authorization, certified-scope tests |

Coverage result: **70 of 70 NFRs have a primary Story and evidence owner.**

## Architecture, UX, Compatibility, and Operations Ownership

| Requirement class | Primary Stories | Evidence source |
|---|---|---|
| Authority/system context and canonical models | VS-01, VS-02, VS-04, VS-16, VS-17 | TS-VAE-01, TS-VAE-08, Stage 3 contracts |
| Builder runtime, events, checkpoints, cancellation | VS-06 | TS-VAE-09; Builder attachment remains externally blocked |
| Dynamic workcell, capabilities, ComfyUI compiler | VS-09..VS-11 | TS-VAE-02, TS-VAE-03 |
| Local/cloud compute and object storage | VS-13 | TS-VAE-04 |
| Independent evaluation and repair | VS-14, VS-15 | TS-VAE-06, TS-VAE-07 |
| Memory, OKF, retrieval, steering | VS-18, VS-19 | TS-VAE-08 |
| Service, Delegation, security | VS-07, VS-22 | TS-VAE-09; Stage 3 dependency/matrix/test plan |
| Supervisory UX and accessibility | VS-08 | TS-VAE-09; NFR-UX-001..005 |
| Versioning, migration, rollback, certification | VS-20..VS-22 | TS-VAE-10, TS-VAE-11, benchmark manifest |

## Stage 5 First Slice

After, and only after, readiness becomes PASS, the first implementation slice may select the minimum behavior from VS-02, VS-03, VS-04, VS-06, VS-07, VS-09 through VS-17 needed to realize:

```text
typed demand fixture
-> production plan IR
-> registered fixture ComfyUI adapter
-> one Standard character portfolio
-> deterministic validation
-> independent fixture evaluator
-> one gesture repair
-> immutable accepted result
-> composition geometry receipt
```

The slice uses exact production ports with fixture-only adapters. It cannot claim VS completion, local/cloud proof, contract conformance, evaluator certification, or limited-production status until the corresponding full Story evidence passes.

## Hard-gate and Failure Examples

- Unauthorized semantic mutation blocks VS-01/VS-02 and emits no admitted execution.
- Unpublished or incompatible Delegation contracts block VS-07 result/service claims.
- Missing Builder extension points block VS-06/VS-08 implementation rather than permitting a duplicate runtime or Control Tower.
- Unpinned workflow/model/runtime resources block VS-11/VS-13 execution.
- Producer/evaluator identity collision blocks VS-14 acceptance.
- Any technical, semantic, Activative, composition, identity, continuity, or required recurrence failure blocks candidate selection.
- A fourth autonomous quality repair is prohibited.
- Cancellation or supersession fences stale output from promotion.
- Missing recovery/rollback evidence blocks VS-21/VS-22 and implementation authorization.

## Non-goals

No Story authorizes every asset family, universal provider support, lip sync, final composition/timing ownership, mutable demand editing, manual production ComfyUI, producer self-approval, a new Builder runtime/Control Tower, or production claims beyond certified Format 02 character/scene scope.
