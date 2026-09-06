# CAE Mandate Bundle — Wave 04

**Bundle ID:** `CAE_MANDATE_BUNDLE_WAVE_04`  
**Scope:** Canonical Questions **Q24–Q31**  
**Status:** `EXECUTION READY — bounded mandate bundle`  
**Prepared:** `2026-09-06`

## 1. Authority chain

1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
2. `docs/cae/cae_master_57_question_convergence_canon.md`
3. CAE Product Brief / PRDs / Functional Requirements
4. `docs/cae/UI.md`
5. `docs/cae/Architecture.md`
6. `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`
7. `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md`
8. Wave 01 and Wave 02 mandate bundles supplied in the working context
9. Individual Wave 04 mandates and executable repository evidence

The authoring protocol is normative for the 13-section mandate grammar, evidence classes, state grammar, anti-centroid controls, activation prompts, parallelism, and stop behavior. Runtime authority remains the canonical runtime; mandate prose never becomes runtime authority.

## 2. Wave 04 objective

Wave 04 establishes the **authorization → composition → release → distribution → outcome attribution** tranche. It converts already-grounded upstream artifacts into governed downstream production surfaces while preserving the causal boundary: authorization must be durable, policy must be explicit and revision-bound, composition cannot invent semantic meaning, release must be immutable and digest-backed, distribution may only perform permitted technical delivery transformations, and outcome telemetry must remain attributable to the exact released artifact.

Canonical sequence:

```text
Q24 configurable authorization policy
        ↓
Q25 durable authorization receipts
        ↓
Q26 declarative policy packages
        ↓
Q27 prospective policy revision binding
        ↓
Q28 grounded composition / no semantic invention
        ↓
Q29 immutable release manifest
        ↓
Q30 execution-only external distribution
        ↓
Q31 causal outcome attribution
```

Q24–Q27 form the authorization governance cluster. Q28 establishes the composition integrity floor before release. Q29 is the release boundary. Q30 consumes the sealed release and must not alter semantic content. Q31 closes the wave by linking observations to exact releases and causal identifiers without promoting raw telemetry into canonical memory.

## 3. Mandate map

| File | Mandate ID | Canon | Mandate | Primary surface | Dependency |
|---|---|---:|---|---|---|
| `02_CA_MANDATE_025.md` | `CA-M025` | Q24 | Configurable Campaign Authorization Policy | `program_operator_runtime.py; apps/web/src/api/types.ts; docs/cae/CAE_Product_Brief/12_Human_Authorization.md` | `Q08, Q11, Q16, Q23` |
| `03_CA_MANDATE_026.md` | `CA-M026` | Q25 | Durable Authorization Decision Receipts | `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` | `Q24, Q11, runtime state/receipt infrastructure` |
| `04_CA_MANDATE_027.md` | `CA-M027` | Q26 | Declarative Policy Rule Packages | `programs/script_program/CAE.md; programs/editorial_storyboard_program/program_manifest.yaml; relevant policy package schemas/loaders` | `Q24–Q25` |
| `05_CA_MANDATE_028.md` | `CA-M028` | Q27 | Prospective Policy Revisions and Execution Binding | `packages/ca_runtime/src/ca_runtime/program_registry.py; policy/state binding path; relevant execution record schema` | `Q24–Q26, Q11` |
| `06_CA_MANDATE_029.md` | `CA-M029` | Q28 | No-Unanchored-Semantic-Invention Invariant | `cae_collision_intelligence/composer.py; programs/script_program/CAE.md; evidence reference validators` | `Q15–Q16, Q17–Q23, Q11` |
| `07_CA_MANDATE_030.md` | `CA-M030` | Q29 | Immutable Digest-Backed Release Manifest Contract | `services/pipeline/src/cmf_pipeline/application.py; release manifest schema/builder; release verification path` | `Q24–Q28, Q11` |
| `08_CA_MANDATE_031.md` | `CA-M031` | Q30 | External Distribution as Execution-Only Delivery | `docs/cae/CAE_Product_Brief/14_External_Distribution.md; distribution adapter boundary; pipeline delivery execution path` | `Q29, Q24–Q27` |
| `09_CA_MANDATE_032.md` | `CA-M032` | Q31 | Causal Outcome Measurement Attribution | `docs/cae/CAE_Product_Brief/15_Outcome_Measurement.md; outcome telemetry schema/ingestion path; release/campaign attribution boundary` | `Q28–Q30, Q01–Q02, Q07–Q08` |

## 4. Dependency and parallelism

Q24–Q26 touch shared policy semantics and must have one integration owner if they share registries or state. Q27 depends on the resulting policy identity and binds it prospectively to executions. Q28 may inspect Q27 outputs but must not alter policy semantics. Q29 owns the immutable release boundary. Q30 consumes Q29 and is downstream-only. Q31 consumes Q29/Q30 identifiers and owns attribution, not memory promotion.

Read-only inspection may be parallelized. Conflicting writes to policy registries, state schemas, receipt formats, release manifests, or shared migrations are not parallel-safe. The executor must stop where a shared change has no clear integration owner.

## 5. Inherited upstream evidence

Wave 04 executors must verify, not assume, the relevant upstream artifacts from earlier waves: audience layers/convergence, Subject Constitution, causal ordering, format/archetype feasibility, Activative/Elicitation linkage, content portfolio, structured research, sealed pre-production state, sovereign source media, temporal/continuity evidence, verbatim evidence, grounded Collision, evidence-admission predicates, context lineage, expression/reaction/anchor primitives, adaptive elicitation, and yield gating. A planning document stating “complete” remains `DOCUMENT` evidence until runtime or executable tests prove the property.

## 6. Wave-level false-proof suite

The eight mandates collectively must reject:

1. browser-only authorization that does not become durable runtime state;
2. a human approval with no actor/revision integrity binding;
3. permissive policy packages that silently weaken constitutional controls;
4. an in-flight execution that changes policy mid-run;
5. a polished composition containing one unsupported factual claim;
6. a sealed release whose referenced bytes were mutated after sealing;
7. distribution that rewrites semantic content to satisfy a destination;
8. outcome dashboards that attribute events to a campaign name or latest release instead of the exact released artifact.

## 7. Execution/control rule

Each mandate follows:

`LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE WITHIN FILE BOUNDARY → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → REQUEST OPERATOR DECISION → STOP`

Every mandate contains a 200–300 word activation prompt. The activation prompt is a compact execution key and never expands the mandate's authority.

## 8. Completion

Wave 04 is complete only when all eight mandates independently satisfy their proof standards, limitations are recorded, control state is updated, exact commit SHAs are captured by their executors, and the Operator explicitly closes the wave. Completion of Q24–Q31 does not authorize Q32 onward.

## 9. Naming

Wave 04 continues the bundle sequence established by Wave 01 and Wave 02: Q24–Q31 are authored as `CA-M025` through `CA-M032`, with filenames `CA_MANDATE_025` through `CA_MANDATE_032`. This separates bundle-level execution IDs from the canonical question numbers and avoids reusing older legacy/editorial mandate identifiers.
