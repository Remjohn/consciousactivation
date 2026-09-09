# CAE Operational Product Campaign M0058–M0068 — Copy-Paste Prompt Blocks & Model Allocation Guide

> **Campaign Status:**
> - ✅ **Foundational Epochs 01–09 (Mandates CA-M001 to CA-M057)**: 100% Ingested, Verified & Committed (`commit 934f0fbb`)
> - 🎯 **Current Active Campaign**: **CAE Operational Product Campaign M0058–M0068 (v1)** (11 Mandates)
> - **Objective**: Transition CAE from verified foundational plumbing into an **active, operable video product factory** with real cinematic asset retrieval, native OpenChatCut timeline editing, operator control persistence, and full vertical-slice proof.

---

## Model Allocation Strategy (To Save Tokens on Claude)

Claude has tighter rate/token limits than ChatGPT or Grok. To maximize throughput and eliminate token exhaustion:
- **Assign to 🌟 Claude (Top 4 Lowest Token Footprint):** Mandates that are self-contained, contract/schema-focused, typed metadata bindings, or structured certification reports.
  1. **`CAE-M059`** (Campaign Execution Control Surface)
  2. **`CAE-M061`** (Production Asset Demand / Resolution Contract)
  3. **`CAE-M064`** (Asset Selection, Production Binding and Lineage Handoff)
  4. **`CAE-M068`** (Production Readiness and Residual-Gap Certification)
- **Assign to 🤖 ChatGPT / Grok (Heavy / Sprawling Tasks):** Mandates that require multi-file tracing, heavy media processing, vector/embedding integrations, native timeline runtime bridging, or multi-stage E2E test execution.
  - `CAE-M058`, `CAE-M060`, `CAE-M062`, `CAE-M063`, `CAE-M065`, `CAE-M066`, `CAE-M067`

---

## Parallel Execution Windows & Dependencies

```mermaid
graph TD
    M0058[M0058: Baseline Ledger (Serial)] --> M0059[M0059: Control Surface]
    M0058 --> M0060[M0060: E2E Fixture Harness]
    M0059 --> M0061[M0061: Asset Demand Contract]
    M0060 --> M0061
    M0061 --> M0062[M0062: Corpus Ingestion]
    M0061 --> M0063[M0063: Semantic Retrieval]
    M0062 --> M0064[M0064: Asset Binding & Lineage]
    M0063 --> M0064
    M0064 --> M0065[M0065: OpenChatCut Runtime]
    M0065 --> M0066[M0066: Operator Native Editing]
    M0066 --> M0067[M0067: Real Product Proof (Serial)]
    M0067 --> M0068[M0068: Production Certification (Serial)]
```

- **Window 1 (Parallel):** `M0059` || `M0060` (can execute concurrently once `M0058` is committed)
- **Window 2 (Parallel):** `M0062` || `M0063` (can execute concurrently once `M0061` is committed)
- **Serial Gates:** `M0058` (Entry), `M0061`, `M0064`, `M0065`, `M0066`, `M0067`, `M0068` (Final)

---

## Track A — Operational Reality

### Mandate 1/11: CAE-M0058
Mandate ID: CAE-M0058  
Mandate Title: Operational Brownfield Reconciliation & Product Run Baseline  
Requirement / Invariant: FR-OPS-BASELINE  
Model Recommendation: ChatGPT / Grok (Broad call-path tracing across runtime, programs, and test suites)  
Target Subsystem / Files: `programs/`, `packages/ca_runtime/`, current pipeline/runtime tests  
Core Acceptance Criteria & Invariant Rule: Establish a verified post-M057 product-operability baseline and prove which existing Program, Harness, runtime, state, operator and test paths are actually reachable today. Build an executable brownfield ledger identifying working, partial, mocked, unreachable and conflicting call paths with zero speculative architecture redesign.

---

### Mandate 2/11: CAE-M059
Mandate ID: CAE-M059  
Mandate Title: Campaign Execution Control Surface  
Requirement / Invariant: FR-OPS-CONTROL  
Model Recommendation: 🌟 Claude (Top 1 Lowest Token Demand — self-contained typed control operations and endpoints)  
Target Subsystem / Files: `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`, `api/routers/campaigns.py`, `api/routers/programs.py`  
Core Acceptance Criteria & Invariant Rule: Make the existing campaign/program runtime operable from an explicit product control surface: launch, inspect state, pause/resume where supported, surface failures, and retrieve receipts without bypassing authority lanes or state machine semantics.

---

### Mandate 3/11: CAE-M060
Mandate ID: CAE-M060  
Mandate Title: Product E2E Fixture & Runtime Test Harness  
Requirement / Invariant: INV-PROOF-REAL-001  
Model Recommendation: ChatGPT / Grok (Heavy fixture setup, workspace teardown, and clean test harness runs)  
Target Subsystem / Files: `tests/e2e/test_product_e2e_fixture.py`, fixture utilities, existing proof harness  
Core Acceptance Criteria & Invariant Rule: Create a real, repeatable fixture workspace and test harness that can execute the declared product path against actual CAE services/runtimes with clean deterministic setup, seed data, checkpoints, and evidence capture. Reject mock-only testing.

---

### Mandate 4/11: CAE-M061
Mandate ID: CAE-M061  
Mandate Title: Production Asset Demand / Resolution Contract  
Requirement / Invariant: INV-ASSET-DEMAND-001  
Model Recommendation: 🌟 Claude (Top 2 Lowest Token Demand — clean typed contract schemas, duration/rights constraints, and translators)  
Target Subsystem / Files: `services/asset-intelligence/`, `production-program`, `packages/ca_runtime/`  
Core Acceptance Criteria & Invariant Rule: Establish the executable typed contract between existing semantic/production Programs and asset resolution so a Program can express exactly what physical media is required (duration, role, semantic obligation, rights) without teaching the runtime how to decide meaning.

---

## Track B — Cinematic Asset Retrieval and Production Binding

### Mandate 5/11: CAE-M062
Mandate ID: CAE-M062  
Mandate Title: Cinematic Corpus Ingestion and Scene Organization  
Requirement / Invariant: INV-CINEMA-CORPUS-001  
Model Recommendation: ChatGPT / Grok (Scene segmentation, timestamp extraction, contextual captions, and corpus indexing)  
Target Subsystem / Files: `services/asset-intelligence/` and derived retrieval/index storage  
Core Acceptance Criteria & Invariant Rule: Ingest explicitly authorized cinematic/archival/owned media into a governed, timestamped, searchable scene corpus compatible with the existing AssetAnnotation doctrine, generating stable scene boundaries, contextual captions, insert roles, and immutable ingest receipts.

---

### Mandate 6/11: CAE-M063
Mandate ID: CAE-M063  
Mandate Title: Natural-Language Semantic Cinematic Retrieval  
Requirement / Invariant: INV-RETRIEVAL-001  
Model Recommendation: 🌟 Claude / ChatGPT (Vector model binding, hybrid ranking, and fail-closed abstention logic)  
Target Subsystem / Files: `services/asset-intelligence/`, retrieval/index implementation  
Core Acceptance Criteria & Invariant Rule: Implement natural-language retrieval over the governed scene corpus so semantic queries retrieve ranked E/D-roll/B-roll candidates with exact source timestamps, contextual explanations, semantic roles, and rights verification, with fail-closed abstention when queries fall below confidence.

---

### Mandate 7/11: CAE-M064
Mandate ID: CAE-M064  
Mandate Title: Asset Selection, Production Binding and Lineage Handoff  
Requirement / Invariant: INV-ASSET-LINEAGE-001  
Model Recommendation: 🌟 Claude (Top 3 Lowest Token Demand — lineage DAG hashing, typed handoff resolution, and invalidation rules)  
Target Subsystem / Files: `production-program`, `CompositionAssetPack`, `packages/ca_runtime/`  
Core Acceptance Criteria & Invariant Rule: Convert explicitly selected retrieval candidates into existing production semantic structures (`CompositionAssetPack`), preserving exact asset identity, time intervals, rights, and provenance through to executable runtime inputs with tamper-evident lineage receipts.

---

## Track C — Native Operator / Runtime Surfaces

### Mandate 8/11: CAE-M065
Mandate ID: CAE-M065  
Mandate Title: Native OpenChatCut Runtime and Timeline Handoff  
Requirement / Invariant: INV-VIDEO-RUNTIME-001  
Model Recommendation: ChatGPT / Grok (OpenChatCut runtime integration, EDL mapping, and timeline schema translation)  
Target Subsystem / Files: `services/pipeline/` video edit path + OpenChatCut integration surface  
Core Acceptance Criteria & Invariant Rule: Make the existing video Program executable against a real OpenChatCut runtime and timeline so selected CAE assets become actual native multi-track edit structures, transferring media identity, source cut ranges, and semantic roles while keeping CAE as the authoritative system of record.

---

### Mandate 9/11: CAE-M066
Mandate ID: CAE-M066  
Mandate Title: Operator Control, Native Editing and Human Resolution Persistence  
Requirement / Invariant: INV-HUMAN-RESOLUTION-001  
Model Recommendation: ChatGPT / Grok (UI integration, before/after diffing, and human resolution episode persistence)  
Target Subsystem / Files: operator workspace + `HumanResolutionEpisode`/revision state  
Core Acceptance Criteria & Invariant Rule: Make the native editing surface operator-operable, allowing manual asset substitution or timing adjustment within bounded constraints, and persist all operator interventions as immutable `HumanResolutionEpisode` records with CAS safety and before/after evidence diffs.

---

## Track D — End-to-End Product Proof & Certification

### Mandate 10/11: CAE-M067
Mandate ID: CAE-M067  
Mandate Title: Real Campaign Vertical Slice and Product Operability Proof  
Requirement / Invariant: INV-PRODUCT-REAL-001  
Model Recommendation: ChatGPT / Grok (Highest token demand; massive end-to-end multi-stage live execution run)  
Target Subsystem / Files: E2E harness + all integrated product/runtime surfaces  
Core Acceptance Criteria & Invariant Rule: Execute one complete real campaign and one adversarial campaign end-to-end from semantic intent through asset retrieval, production Program execution, native OpenChatCut runtime, operator intervention, and release evidence, capturing every checkpoint and receipt without mocks.

---

### Mandate 11/11: CAE-M068
Mandate ID: CAE-M068  
Mandate Title: Production Readiness and Residual-Gap Certification  
Requirement / Invariant: INV-CERT-REAL-001  
Model Recommendation: 🌟 Claude (Top 4 Lowest Token Demand — structured certification matrix, evaluation report, and gap ledger)  
Target Subsystem / Files: `docs/`, certification/evidence manifests, verification test logs  
Core Acceptance Criteria & Invariant Rule: Formally evaluate the 10 campaign completion criteria against observed execution evidence, compile the final Production Readiness Certification Report and Residual-Gap Ledger, and establish the certified operational status of the product.

