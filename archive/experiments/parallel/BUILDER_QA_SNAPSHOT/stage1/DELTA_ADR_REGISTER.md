# Delta ADR Register

These are architecture decisions that must be authored before implementation. `Proposed` is the ADR workflow state, not a requirement-coverage verdict.

| ADR | State | Locked decisions | Verified baseline | Required decision delta | Blocking input |
|---|---|---|---|---|---|
| ADR-001 Governed lifecycle and authority | Proposed | D001-D003, D006, D027 | CLI and JSON run state; no transition enforcement | State machine, actor authority, checkpoints, invalidation, waivers, authorization receipt | Operator identity and waiver policy |
| ADR-002 Evidence workspace and identity | Proposed | D005 | File/ZIP hashes, text keywords, image dimensions | Source profiles, stable IDs, roles/status, directory/archive identity, media pipeline, conflict and saturation contracts | SRC-002-SRC-010 and target repos |
| ADR-003 Visual Syntax First pipeline | Proposed | D007 | Image metadata only | Frame/slide extraction, primitive ontology, temporal parser, motif/grammar induction, confidence and provenance | SRC-004 corpus; multimodal provider |
| ADR-004 Atomicity and draft harness model | Proposed | D008 | Direct enum assignment | Evidence-linked classification, rationale, partition/cluster graph, draft model, human ratification | Reference harness and category choice |
| ADR-005 Transactional Genesis | Proposed | D002, D009-D010 | Static decision graph and question files | Typed transaction, dependency invalidation, source-linked recommendation compiler, commit/abort semantics | Human authority and persistence ADR |
| ADR-006 Canonical Harness IR | Proposed | D011 | Fragmented Pydantic models and template compiler | Root aggregate, IDs, integrity, serializer, schema evolution, migrations, compiler interfaces | Storage and artifact identity choices |
| ADR-007 Capability, module, phase, and handoff contracts | Proposed | D012-D015 | Partial models and static graph nodes | Ownership registry, executable DAGs, contract validation, failure ownership, handoff compiler | Three target repo seams |
| ADR-008 Reference, SPR, and context budgets | Proposed | D013, D016, D019-D020 | Context-plan fields | Registry, SPR compiler, loading/precedence engine, manifests, budget enforcement, truncation failure | Provider token accounting |
| ADR-009 Skill ecology and JIT capsules | Proposed | D017-D018, D021 | SkillRef/JIT data models | Registry, maturity lifecycle, dependency solver, behavioral evaluation, recipe/capsule compiler, runtime adapters | Seed skills and runtime providers |
| ADR-010 Behavioral benchmark system | Proposed | D003, D021-D024 | No implementation | Corpus governance, protected split, evaluator independence, repeated runs, scorecards, receipts, leakage controls | Benchmark corpus and threshold owners |
| ADR-011 Event ledger and Control Tower | Proposed | D025 | CLI status only | Event envelope/store, projections, API, UI, interventions, evidence drill-down, exports, accessibility | Backend, UI, auth, and deployment choices |
| ADR-012 Repair and readiness authorization | Proposed | D003, D026-D027 | Structural readiness checker | Failure taxonomy, causal graph, layer-local repair, retest protocol, hard-gate engine, signed authorization | Benchmark and event-ledger ADRs |
| ADR-013 Category constitutions and sequencing | Proposed | D030-D031, D033 | Module configs and legacy Format 01 guard | Four isolated constitutions, atomic ownership, category IR, sequence compiler, fidelity evaluation, migration | Canonical category seed artifacts |
| ADR-014 Development Capsule handoff | Proposed | D029 | OpenSpec output and target pointer scaffold | Manifest compiler, architecture/epic/story/fixture generation, trace closure, checksums/signatures, acceptance validator | Target repo contracts and owners |
| ADR-015 V2.1 migration and release | Proposed | D028, D032 | Re-saturation command and donor heuristic | Inventory, source-to-IR migration, dual compile, equivalence report, deprecation ledger, rollback and release gates | Original archives and target baselines |
| ADR-016 Three compilation targets | Proposed | D004, D032 | Three separate OpenSpec module trees pass structural tests | One canonical IR with target-local IRs, compatibility matrix, target conformance and release policy | All target repos and maintainers |
| ADR-017 Builder Workflow Runtime | Proposed | D001-D002, D006, D025, D027, D033 | Human-operated Markdown steps | Workflow IR, node contracts, router, bounded scheduler, retries, sandbox, telemetry, CI gates, promotion and rollback | Workflow engine and isolation policy |
| ADR-018 Deployment and operations | Proposed | D025, D027, D032 | No deployment assets | Service topology, storage, authn/authz, secrets, queues, artifact store, observability, CI/CD, backup/restore, environments | Hosting, data classification, SLOs, budget |

## Decision Coverage

All locked decisions D001-D033 are referenced by at least one proposed ADR. F18 has no dedicated additional locked decision in the current D001-D033 register; ADR-017 therefore binds its architecture to the applicable lifecycle, authority, observability, authorization, and anti-goal decisions without inventing D034.

No ADR above is accepted by this audit. Acceptance requires the unavailable source/target evidence, explicit owners, alternatives, consequences, and testable decision criteria described in the specification plan.

