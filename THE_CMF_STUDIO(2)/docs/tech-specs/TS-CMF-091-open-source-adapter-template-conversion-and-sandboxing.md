---
tech_spec_id: "TS-CMF-091"
title: "Open-Source Adapter Template Conversion and Sandboxing"
story_id: "platform-2"
story_title: "Open-Source Template Conversion"
epic_id: "platform"
epic_title: "Runtime Integrations, Research, Video Editing, and Adapter Governance"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-080 functional decomposition"
pipeline_stage: "cross-stage integration governance / 10 / 11"
entry_object: "IntegrationAdapterDecisionReceipt and source project reference"
exit_object: "SandboxedTemplateAdapter or ReferenceFixture"
validation_contract: "license, sandbox, generated contract boundary, no domain truth replacement"
required_receipt: "OpenSourceTemplateConversionReceipt"
runtime_target: "Python adapter registry / TypeScript leaf adapters / test fixtures"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-091: Open-Source Adapter Template Conversion and Sandboxing

## 1. Purpose

Turn useful open-source components into governed CMF adapters, fixtures, or references. This spec is the functional follow-through to TS-CMF-076 for composition templates.

## 2. Conversion Categories

| Category | Examples | Output |
|---|---|---|
| Reaction mechanics | `react-debate`, `react-tierlist`, `react-ranking-quiz`, `react-blind-rank`, `react-elimination`, `react-authority-quiz`, `react-mirror-quiz` | JSON-defined Remotion/Motion Canvas mechanics. |
| Timeline UI | `react-video-editor`, `openvideo` | Operator UI reference or sandboxed leaf UI. |
| Clip automation lab | `OmniShotCut`, `video-use`, `yt-short-clipper`, `AI-Youtube-Shorts-Generator` | Lab fixtures only until approved. |
| Visual/layer systems | `Manim`, `hyperframes`, `stretchystudio`, `see-through`, `SCAIL-2` | Renderer/layer/rig reference or adapter. |
| Search/research | `searxng`, `Gen-Searcher`, `last30days-skill`, `Open-Generative-AI` | Research adapter with evidence receipts. |

## 3. Primary Contract

```python
class OpenSourceTemplateConversion(BaseModel):
    schema_version: Literal["cmf.open_source_template_conversion.v1"]
    conversion_id: UUID
    candidate_id: str
    decision_receipt_id: UUID
    source_project_ref: str
    conversion_mode: Literal["adapter", "fixture", "reference", "blocked"]
    allowed_runtime_use: str
    prohibited_runtime_use: str
    generated_contract_refs: list[str]
    sandbox_requirements: list[str]
    security_notes: list[str]
    blocker_codes: list[str]
```

## 4. Conversion Rules

- No production import without adapter decision receipt.
- No project may own CMF source, route, eval, or approval truth.
- UI components consume CMF contracts.
- Lab tools do not process guest data.
- License and security metadata must be stored.
- Any copied pattern must be renamed and reshaped into CMF domain language.

## 5. Commands and Receipts

| Type | Names |
|---|---|
| Commands | `ConvertOpenSourceTemplateCommand`, `SandboxOpenSourceAdapterCommand`, `RegisterReferenceFixtureCommand`, `BlockOpenSourceRuntimeUseCommand` |
| Events | `OpenSourceTemplateConverted`, `OpenSourceAdapterSandboxed`, `ReferenceFixtureRegistered`, `OpenSourceRuntimeUseBlocked` |
| Receipt | `OpenSourceTemplateConversionReceipt` |

## 6. Blockers

| Blocker | Trigger |
|---|---|
| `ADAPTER_DECISION_RECEIPT_MISSING` | No TS-CMF-076 decision. |
| `LICENSE_REVIEW_MISSING` | License not recorded. |
| `GUEST_DATA_SANDBOX_VIOLATION` | Lab/reference tool touches guest data. |
| `DOMAIN_TRUTH_REPLACEMENT` | External component replaces CMF contracts. |
| `UNSCOPED_STATE_IMPORT` | Tool state cannot be reconstructed or scoped. |

## 7. Acceptance Criteria

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Each open-source use has conversion receipt. | Component copied into renderer folder. |
| AC2 | Reaction mechanics become CMF JSON/renderer components. | React app state becomes composition truth. |
| AC3 | Lab-only tools cannot run on guest data. | YouTube clipper processes client footage. |
| AC4 | Timeline UI consumes CMF manifests. | UI stores its own canonical edit state. |

## 8. Testing

- Decision receipt requirement tests.
- License metadata tests.
- Sandbox violation tests.
- Contract boundary tests.
- Converted reaction component fixture tests.

