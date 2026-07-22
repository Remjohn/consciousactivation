# CCP Studio V2 — Python-First Implementation Sequence, Migration Plan, and Production Release Gates

**Companion to:** Master Specification and Domain Contracts  
**Operating rule:** build internally in coherent waves, but do not publicly release an incomplete chain.

---

# 1. Delivery Philosophy

“No MVP” does not mean “write the whole codebase in one pass.”

It means:

- do not ship a misleading partial product;
- do not let temporary architecture become permanent;
- implement foundations in dependency order;
- keep every internal increment executable and testable;
- release only when the complete brand-to-publication journey works.

The development unit is an **internally complete vertical slice**. The release unit is the **whole production loop**.

---

# 2. Wave 0 — Repository Archaeology and Decision Freeze

## Objective

Understand existing value before implementing the greenfield runtime.

## Tasks

1. Freeze the legacy repository.
2. Record current branches, deployments, databases, provider integrations, and secrets.
3. Inventory:
   - registry files;
   - prompt families;
   - primitive taxonomies;
   - schemas;
   - evaluation rubrics;
   - render templates;
   - provider code;
   - test fixtures;
   - dead/duplicated code.
4. Create the migration ledger.
5. Identify canonical registry sources when duplicates exist.
6. Hash source artifacts.
7. Approve the Python / Pydantic / DSPy / Pi runtime ADR before any framework scaffolding.
8. Define data-classification and consent requirements.

## Required Outputs

```text
docs/migration/legacy-inventory.md
docs/migration/registry-source-map.md
docs/migration/migration-ledger.csv
docs/migration/dependency-risk-map.md
docs/adr/ADR-001-python-pydantic-dspy-pi-runtime.md
docs/adr/ADR-002-greenfield-runtime.md
docs/adr/ADR-003-registry-kernel.md
docs/adr/ADR-004-brand-context-versioning.md
docs/adr/ADR-005-agent-command-bus.md
docs/adr/ADR-006-durable-workflows.md
docs/adr/ADR-007-provider-adapters.md
docs/adr/ADR-008-tenant-isolation.md
docs/adr/ADR-009-publishing-safety.md
```

## Exit Gate

- every high-value legacy registry has an owner and migration status;
- no unknown production dependency remains;
- greenfield stack ADRs are approved;
- legacy runtime is read-only.

---

# 3. Wave 1 — Contract and Registry Kernel

## Objective

Create the language the entire application will speak.

## Tasks

1. Scaffold monorepo.
2. Implement common IDs, envelopes, versioning, review fields, and source references.
3. Implement canonical Pydantic v2 contracts and JSON Schema/OpenAPI generation.
4. Generate TypeScript interfaces and optional Zod validators from Pydantic.
5. Establish contract-drift checks in CI.
6. Implement registry entry schemas as Pydantic models.
7. Migrate the five core registries.
8. Migrate supporting registries.
9. Build Registry Bundle validation.
10. Add legacy golden fixtures.
11. Add registry admin inspection UI only after the kernel works.
12. Create compatibility and cross-reference tests.
13. Create the DSPy program registry contract and representative typed signatures.

## Exit Gate

- active registry bundle validates at boot;
- no missing cross-reference;
- no active schema lacks an evaluation rubric;
- old prompt examples are represented as fixtures;
- a compiler can retrieve and combine registry contracts without using a monolithic prompt.

---

# 4. Wave 2 — Control Plane and Data Spine

## Objective

Build the durable, secure stateful application core.

## Tasks

1. Authentication and organizations.
2. Brand workspaces and roles.
3. PostgreSQL schema and RLS.
4. Object storage abstraction.
5. Audit log.
6. Domain event and outbox.
7. Temporal cluster/namespace and Python workflow-worker skeleton.
8. Python Command Bus with Pydantic command validation.
9. Agent threads and messages.
10. OpenTelemetry.
11. secret management.
12. backup/restore rehearsal.

## Exit Gate

- cross-brand RLS tests pass;
- commands are idempotent;
- events publish through outbox;
- workflows survive process restart;
- assets upload with correct brand scope and signed access;
- audit records cover all mutations;
- backup restoration succeeds in staging.

---

# 5. Wave 3 — Agent Gateway and Shared Surfaces Foundation

## Objective

Create one intelligent operator across PWA and Telegram.

## Tasks

1. Python Agent Gateway context assembly.
2. Pi Coding Agent orchestration boundary.
3. DSPy program registry and typed signature execution.
4. mode-specific tool registry.
5. model/provider routing.
6. Pydantic command proposals.
7. permission and confirmation policies.
8. PWA chat shell consuming generated TypeScript contracts.
9. Python Telegram bot webhook.
10. Telegram Mini App authentication and shell.
11. cross-surface thread continuity.
12. prompt-injection and untrusted-content guards.
13. tests proving Pi/DSPy cannot bypass the Command Bus or durable workflows.

## Exit Gate

- the same thread works in PWA and Telegram;
- the agent never crosses brands;
- expensive/public commands require confirmation;
- the agent cannot directly write production tables;
- all tool activity is audited;
- Telegram tampering tests pass.

---

# 6. Wave 4 — Full Brand Genesis

## Objective

Onboard a brand into a locked creative universe.

## Tasks

### Intake and Consent

- client and business intake;
- likeness/voice/derivative consent;
- source photo/video upload;
- source QC.

### Strategic Identity

- Business Intelligence;
- Tribe Soul;
- Character Lexicon;
- initial Voice DNA;
- linguistic Negative Space;
- visual constitution and visual Negative Space;
- identity summary approval.

### Acting Library

- provider adapter for GPT Image 2/current approved asset provider;
- batch generation of 64 cells;
- auto-QC;
- approval/fix/reject grid;
- immutable library lock.

### Paper-Cut Actor

- avatar asset generation;
- Qwen-Image-Layered adapter;
- SAM3 adapter;
- See-Through adapter/fallback;
- edit/repair provider;
- canonical Rig Manifest;
- preview tests;
- approval.

### Creative Libraries

- props;
- Micro-Semiotic Anchors;
- motions;
- SFX;
- composition preferences;
- publishing profile.

### Lock

- adversarial validation;
- Genesis Clearance Certificate;
- Brand Context Version lock.

## Exit Gate

A real brand can:

1. upload source media;
2. approve identity;
3. approve all 64 acting cells;
4. approve a functioning paper-cut rig;
5. approve props/anchors/motion/SFX;
6. lock Brand Context v1;
7. reproduce the exact locked context from hashes.

No production session may begin without this gate unless explicitly using a legacy/manual context with a waiver.

---

# 7. Wave 5 — Research and Interview Intelligence

## Objective

Make the application improve interviewing before any editing begins.

## Tasks

1. Research Field and Evidence objects.
2. source provenance and citation support.
3. Guest Dossier compiler.
4. Audience Reality Brief compiler.
5. Context Premise workflow.
6. Evidence Critic/adversarial review.
7. Interviewer Pre-Induction chat.
8. Interviewer Resonance Context.
9. Matrix of Edging.
10. Narrative State Map.
11. Interview Asset Contracts.
12. Deck compiler and review.
13. Live Interview mode UI and cue contract.
14. Interviewer Profile and learning events.

## Exit Gate

For a real guest/topic, the system can:

- show the evidence behind its assumptions;
- distinguish facts and inferences;
- interview the operator;
- create approved Context Premises;
- generate a stateful interview deck;
- produce repair follow-ups;
- explain why every question exists;
- preserve human freedom to deviate.

A human reviewer must judge the final deck as meaningfully better than a generic researched interview.

---

# 8. Wave 6 — Complete Expression Sessions

## Objective

Capture, synchronize, extract, and evaluate authentic expression.

## Tasks

1. recording configuration;
2. calibration/quality gate;
3. session start/stop and markers;
4. recording upload;
5. transcript provider and revisions;
6. timestamp alignment;
7. anchor hit detection;
8. expression moment extraction;
9. source playback review;
10. sensitivity and allowed-use controls;
11. archetype routes;
12. Asset Package Spec;
13. session and interviewer evaluation.

## Exit Gate

One real interview produces:

- immutable source artifacts;
- synchronized transcript;
- approved moments with source timestamps;
- approved routes;
- an Asset Package Spec;
- post-session learning;
- no fabricated or ungrounded output.

---

# 9. Wave 7 — Complete CMF Production

## Objective

Compile approved expression into every required production route.

## Tasks

### Common

- Complete Editing Session;
- Creative State;
- SceneSpec;
- asset retrieval;
- provider receipts;
- Evaluation Receipts;
- revision branches.

### Composition and Image

- Ideogram 4 Composition Provider;
- GPT Image asset/edit provider;
- Flux Edit provider;
- approved workflow templates;
- reference selection.

### Layering and Rig

- Qwen-Image-Layered semantic decomposition;
- SAM3 precision masks/tracking;
- See-Through character route;
- repair/edit route;
- layer QC;
- Rig Provider.

### Deterministic Render Routes

- Personal-Brand Commentary;
- Paper-Cut Explainer;
- Animated Avatar Explainer;
- Carousel Static/Motion;
- Quiz/Ranking;
- Data Story;
- Living/Conscious Reactions.

### Generative/Special Routes

- SCAIL-2 motion transfer;
- cinematic video generation;
- HyperFrames route;
- final Remotion packaging.

### Sound

- authentic primary audio;
- subtitle sync;
- motion/SFX plan;
- sound doctrine.

## Exit Gate

Golden test outputs pass for:

1. real-footage commentary;
2. paper-cut explainer;
3. animated avatar;
4. carousel;
5. meme and poll;
6. data story/bar-chart race;
7. quiz/ranking;
8. SCAIL motion-transfer sample;
9. cinematic sample.

Each has full receipts and can be revised without losing lineage.

---

# 10. Wave 8 — Review, Telegram Cockpit, and Publishing

## Objective

Operate the whole system from the PWA and on the move.

## Tasks

1. portfolio and brand dashboards;
2. production board;
3. render comparison;
4. Telegram notifications;
5. Mini App preview/chat;
6. revision commands;
7. approval events;
8. Publishing Intent;
9. platform variants;
10. Publer media upload;
11. draft/schedule/publish adapter;
12. status synchronization;
13. performance ingestion.

## Exit Gate

- a render notification arrives in Telegram;
- the operator previews it in the Mini App;
- chat has the correct brand/object context;
- a revision command branches correctly;
- approval is reflected in PWA;
- publishing requires explicit confirmation;
- Publer status is reconciled;
- duplicate scheduling is prevented.

---

# 11. Wave 9 — Memory, Hardening, and Operational Readiness

## Objective

Make the system safe and sustainable.

## Tasks

1. Brand Memory admissions.
2. Interviewer Memory.
3. Neo4j projection.
4. performance correlations.
5. provider cost/performance reporting.
6. runbooks.
7. penetration/security test.
8. restore drills.
9. provider outage/fallback tests.
10. load and batch tests.
11. user acceptance.
12. documentation completion.
13. release candidate freeze.

## Exit Gate

- memory is evidence-based and reversible;
- Neo4j can rebuild from events;
- system recovers from provider outage;
- backups restore;
- spend alerts work;
- no P0/P1 security defects;
- operator can complete the full workflow without developer intervention.

---

# 12. Production Release Gate

Public launch is prohibited until all conditions pass.

## 12.1 Functional Gate

- Brand Genesis complete;
- Interview Intelligence complete;
- Complete Expression Session complete;
- full CMF routes complete;
- PWA complete;
- Telegram Bot/Mini App complete;
- Publer flow complete;
- memory update complete.

## 12.2 Data Gate

- 100% brand scoping;
- locked context versioning;
- receipt chain;
- audit trail;
- export/delete flow;
- consent enforcement.

## 12.3 Reliability Gate

- workflow resume;
- idempotency;
- provider retry/fallback;
- batch checkpoint;
- backup/restore;
- queue monitoring.

## 12.4 Quality Gate

- approved golden tests;
- calibrated evaluations;
- identity and source-truth hard failures at zero in release set;
- motion/style review;
- interviewer plan judged high quality.

## 12.5 Security Gate

- RLS test;
- Telegram auth test;
- provider token protection;
- prompt-injection test;
- file-upload security;
- least privilege;
- no public asset exposure.

## 12.6 Operational Gate

- runbooks;
- cost dashboards;
- alerting;
- support/admin tools;
- incident ownership;
- provider terms/data-policy review.

## 12.7 Human Acceptance Gate

The operator must complete at least one real brand cycle:

```text
onboarding
→ interview preparation
→ interview
→ asset package
→ render
→ revision
→ approval
→ publishing
→ memory update
```

without direct database edits or ad hoc developer scripts.

---

# 13. Initial Backlog for the Coding Agent

The first approved implementation backlog is:

1. create the Python-first hybrid monorepo;
2. write and approve runtime, greenfield, registry, workflow, and security ADRs;
3. build the legacy inventory script;
4. build the migration-ledger format;
5. implement common Pydantic contracts;
6. implement JSON Schema and OpenAPI generation;
7. generate TypeScript interfaces and optional Zod validators;
8. establish CI drift checks for generated contracts;
9. implement registry Pydantic schemas;
10. migrate one archetype of each registry type;
11. implement registry validation and bundle signing/hash rules;
12. implement the DSPy Program Registry and representative signatures;
13. implement organization/brand persistence mappings;
14. implement RLS;
15. implement audit log;
16. implement domain event/outbox;
17. implement Temporal Python bootstrap;
18. implement the Python command bus;
19. implement the Python Agent Gateway skeleton;
20. implement Pi orchestration context and approved tool boundaries;
21. implement PWA/Telegram shared thread identity;
22. implement Brand Genesis workflow skeleton;
23. implement source media upload/QC;
24. implement consent enforcement;
25. implement identity summary review;
26. implement 64-cell library schema and review grid;
27. implement provider capability registry;
28. implement image asset provider contract;
29. implement paper-cut rig contracts;
30. implement Brand Context lock;
31. implement research evidence and Context Premises;
32. implement interviewer pre-induction;
33. implement DSPy Interview Asset Contract compiler;
34. implement Complete Expression Session;
35. implement Complete Editing Session;
36. implement render/provider adapters;
37. implement evaluation and approval;
38. implement Publer adapter;
39. implement complete release gates.

The agent should submit architecture, migrations, and tests in small reviewed pull requests while preserving the final no-half-release doctrine.

---

# 14. Pull Request Definition of Done

Every PR must include:

- linked requirement/ADR;
- domain impact;
- Pydantic schemas, generated projections, and affected types;
- tests;
- migration if needed;
- observability;
- security/brand-scope review;
- documentation;
- rollback note.

A PR fails review if it:

- introduces an untyped payload or a hand-authored shadow contract;
- calls a provider from domain code;
- hides state in Pi/DSPy/chat context;
- lacks idempotency for side effects;
- lacks brand scoping;
- bypasses approval;
- imports legacy runtime code;
- creates a duplicate registry truth.

---

# 15. Agent Reporting Cadence

At the end of each internal wave, report:

```text
Completed
Evidence/tests
Architectural deviations
Unresolved risks
Cost impact
Security impact
Migration status
Next-wave prerequisites
```

Do not report “done” based on file count. Report against exit gates.

---

# 16. Final Execution Directive

Build the system in dependency order, with production-quality boundaries from the first commit.

The greenfield codebase should be smaller and more legible than the legacy system even though the product is broader, because intelligence lives in registries, contracts, workflows, and reusable provider capabilities rather than duplicated prompt logic.

The final product must make the operator:

- more informed before the interview;
- more present during the interview;
- more perceptive after the interview;
- faster and more coherent in production;
- safer in approval and publishing;
- smarter with every completed session.

That is the release.
