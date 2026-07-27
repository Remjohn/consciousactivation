---
tech_spec_id: "TS-CMF-127"
title: "Real-Footage Corpus and Source Media Retrieval Adapter"
story_id: "13.8"
story_title: "Real-Footage Corpus and Source Media Retrieval Adapter"
epic_id: 13
epic_title: "OpenMontage-Inspired Production Orchestration Adapters"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-13.08"
pipeline_stage: "asset research, footage retrieval, and licensing"
entry_object: "RealFootageSearchRequest"
exit_object: "RealFootageCorpusReceipt"
validation_contract: "source media retrieval, license evidence, embedding index, symbolic role, composition role, source/brand compatibility"
required_receipt: "RealFootageCorpusReceipt"
runtime_target: "Python / Pydantic v2 / visual research / source provenance / provider operations / asset package"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-127: Real-Footage Corpus and Source Media Retrieval Adapter

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Pipeline and cinematic meaning mandates. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Verifiable artifact mandate. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` | Product owner for FR-CMF-13.08. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/00_AGENT_START_HERE.md` | CMF-local Python/DSPy/Pi runtime boundary and repository ownership rule. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md` | Canonical object spine and state-machine constraints for pipeline artifacts. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first expression capture, narrative induction, and extraction constraints. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression Moment, archetype routing, route candidate, and package-routing constraints. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, guest workspace, micro-semiotic, and initial asset package requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Creative pipeline, scene program, composition handoff, and render-stage requirements. |
| `THE CMF STUDIO/PROJECT_STRUCTURE.md` | Ensures all adapters write inside the CMF project folder, not the legacy reference repo. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-023-research-fields-and-evidence-capture.md` | Research evidence capture dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-034-guest-asset-pack-spec-generation.md` | Asset package dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Composition role dependency. |
| `THE CMF STUDIO/src/ccp_studio/services/visual_research_service.py` | Existing visual research owner. |
| `THE CMF STUDIO/src/ccp_studio/services/research_service.py` | Existing research owner. |
| `THE CMF STUDIO/src/ccp_studio/services/source_provenance_service.py` | Existing provenance owner. |
| `THE CMF STUDIO/src/ccp_studio/services/asset_package_service.py` | Asset package owner. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_operations_service.py` | Provider capability and retrieval owner. |
| `OpenMontage docs/PROVIDERS.md` | Reference pattern for provider options and retrieval sources. |

## 2. Overview

CMF cannot rely only on generated stills, prompt-based visuals, or decorative motion. Cinematic Story Commentary, Living Commentary Reactions, Challenger assets, and high-trust explainers often need real footage: memory-object inserts, environmental texture, archival proof, metaphor footage, brand-owned B-roll, approved guest clips, or public-domain material.

This spec adds a real-footage retrieval path inspired by OpenMontage's documentary montage orientation while preserving CMF's licensing, provenance, and evidence requirements. The adapter supports internal archives, approved guest footage, brand-owned B-roll, Pexels, Pixabay, Wikimedia, NASA, Archive.org, and future search providers behind capability contracts.

Retrieved clips are indexed by visual embedding, transcript/caption, license, source URL, duration, resolution, emotional role, symbolic role, composition role, route fit, brand compatibility, expiration/takedown status, and source evidence. The system distinguishes `direct_use`, `reference_only`, `metaphor_footage`, `archival_evidence`, and `prohibited_material`. Every selection writes a corpus receipt.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-127-001 | `RealFootageSearchRequest` | Typed request for footage by topic, symbolic role, emotional role, composition role, license, and format. |
| DEP-CMF-127-002 | `RealFootageCandidate` | Candidate media record with metadata, license, embedding refs, and permitted use. |
| DEP-CMF-127-003 | `FootageLicenseEvidence` | License proof, source URL, retrieved timestamp, terms, and takedown policy. |
| DEP-CMF-127-004 | `FootageSelectionDecision` | Chosen clip and rejected alternatives with ranking rationale. |
| DEP-CMF-127-005 | `RealFootageCorpusReceipt` | Receipt proving query, candidates, selected assets, license evidence, hashes, and roles. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/visual_research.py` | Add footage search request, candidate, license evidence, selection decision, and receipt models. |
| `src/ccp_studio/services/visual_research_service.py` | Own footage search, candidate ranking, and visual role tagging. |
| `src/ccp_studio/services/research_service.py` | Support evidence-backed query construction and source citation. |
| `src/ccp_studio/services/source_provenance_service.py` | Store source URLs, license evidence, media hashes, and expiry/takedown status. |
| `src/ccp_studio/services/asset_package_service.py` | Admit approved footage into asset package items with use role and license state. |
| `src/ccp_studio/services/provider_operations_service.py` | Route external source retrieval through capability registry. |
| `src/ccp_studio/api/v1/visual_research.py` | Add footage search, candidate inspect, select, and receipt endpoints. |
| `POST /api/v1/visual-research/footage/search`, `POST /api/v1/visual-research/footage/{candidate_id}/inspect`, `POST /api/v1/visual-research/footage/{candidate_id}/select`, `GET /api/v1/visual-research/footage/{candidate_id}` | Exact API routes for footage retrieval and selection. |
| `src/ccp_studio/repositories/visual_research.py` | Persist candidates, license evidence, and corpus receipts. |
| Postgres tables: `real_footage_corpus_items`, `footage_license_evidence`, `footage_selection_receipts`, `footage_embedding_refs`, `asset_package_items` | Durable storage for searchable footage, licensing, selection evidence, and package admission. |

### ADR-05 Primitives

| Primitive ID | Source Mandate | Constraint Enforced |
|---|---|---|
| `EXP-TRS-004` | Cinematic Meaning | Footage must serve story, proof, memory, symbol, or environment, not decoration. |
| `EXP-SOC-001` | Verifiable Artifact | License evidence, source hashes, and selection rationale are receipt-backed. |
| `EXP-FBK-001` | Actionable Rejection | License, quality, source, or brand-fit failures return exact repair action. |
| `EXP-PRG-001` | Inline Routing SLA | Selected footage is routed to asset package and composition role inline. |
| `EXP-FRC-006` | Frictionless Block | Prohibited or expired media is quarantined with safe alternatives. |

### CBAR Mandate Enforcement

| Mandate | Story Origin | Governing Primitive | Enforcement Mechanism |
|---|---|---|---|
| Phase4-M02: Cinematic Meaning Rule | Phase 4 Story 2.1 | `EXP-TRS-004` | Footage candidate must declare emotional, symbolic, or composition role. |
| Phase4-M03: Inline Routing SLA | Phase 4 Story 3.1 | `EXP-PRG-001` | Selected footage routes to asset package and SceneSpec role immediately. |
| Phase4-M05: Actionable Rejection Rule | Phase 4 Story 5.1 | `EXP-FBK-001` | Rejected candidates name license, quality, relevance, or brand-fit reason. |
| Phase5-M01: Verifiable Artifact Rule | Phase 5 Story 1.1 | `EXP-SOC-001` | Corpus receipt stores query, candidates, license, hashes, and selected role. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Separate source footage from retrieved real footage. | Guest/source truth and external B-roll have different consent and license rules. |
| Store license evidence at retrieval time. | External source terms and assets may change. |
| Require composition role before asset package admission. | Prevents decorative footage dumping. |
| Track expiry and takedown status. | Supports removal, replacement, and audit safety. |

## 4. Implementation Plan

1. Add real-footage contracts to `visual_research.py`.
2. Add provider capability records for supported footage sources under TS-CMF-123.
3. Implement search adapter interface with internal archive first, then configured external providers.
4. Extract and store metadata: duration, resolution, captions, license, URL, source timestamp, visual embedding refs, emotional/symbolic/composition role.
5. Rank candidates by route fit, brand fit, license safety, visual quality, source evidence, and primitive fit.
6. Add selection decision and corpus receipt.
7. Admit approved footage to asset package with allowed use role.
8. Add expiration/takedown recheck hook.
9. Add tests for license evidence, prohibited material, role mapping, package admission, and replay.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl


class FootageLicenseEvidence(BaseModel):
    schema_version: Literal["cmf.footage_license_evidence.v1"]
    license_id: str
    source_url: HttpUrl
    license_label: str
    commercial_use_allowed: bool
    attribution_required: bool
    retrieved_at: str
    evidence_sha256: str


class RealFootageCandidate(BaseModel):
    schema_version: Literal["cmf.real_footage_candidate.v1"]
    candidate_id: str
    source_provider: str
    media_uri: str
    preview_uri: str | None = None
    duration_seconds: float
    resolution: str
    permitted_use: Literal["direct_use", "reference_only", "metaphor_footage", "archival_evidence", "prohibited_material"]
    emotional_role: str | None = None
    symbolic_role: str | None = None
    composition_role: str | None = None
    license_evidence: FootageLicenseEvidence
    score: float = Field(ge=0, le=1)


class RealFootageCorpusReceipt(BaseModel):
    schema_version: Literal["cmf.real_footage_corpus_receipt.v1"]
    receipt_id: str
    search_request_id: str
    candidate_ids: list[str]
    selected_candidate_ids: list[str]
    rejected_reasons: dict[str, str]
    selected_asset_package_item_ids: list[str] = Field(default_factory=list)
    receipt_sha256: str
```

## 6. Backward Compatibility Fallback

Existing visual research can continue without footage retrieval when no real-footage provider is configured. In that case the system returns a `no_configured_footage_provider` blocker and may route to generated assets only if the target format and pre-compose gate allow it.

If license evidence is missing or expired, selected footage cannot enter asset packages. The fallback is to find a licensed alternative, use brand-owned footage, use generated metaphor assets, or require human approval for reference-only use.

## 7. Tasks

| Task | Owner Area | Output |
|---|---|---|
| T127-01 | Contracts | Add search request, candidate, license evidence, selection decision, receipt. |
| T127-02 | Provider Registry | Add footage provider capabilities. |
| T127-03 | Services | Implement search, metadata extraction, candidate ranking, and selection. |
| T127-04 | Provenance | Store license evidence and source hashes. |
| T127-05 | Asset Package | Admit approved footage with role and rights. |
| T127-06 | Review UI | Surface candidates, license, role, and rejected options. |
| T127-07 | Tests | Add license, ranking, package admission, expiry, and replay tests. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR / Test Evidence |
|---|---|---|---|
| AC127-01 | Retrieved footage includes license evidence and source hash before selection. | Clip is downloaded with no license record. | Phase5-M01; license evidence test. |
| AC127-02 | Candidate must declare permitted use and composition role. | Decorative clip is added to cinematic asset package with no role. | Phase4-M02; role mapping test. |
| AC127-03 | Prohibited or expired material cannot enter asset package. | Expired external clip is still used in final render. | Phase4-M05; expiry/takedown test. |
| AC127-04 | Rejected candidates include ranking rationale. | Operator cannot see why top clip was rejected. | Phase4-M05; selection receipt test. |
| AC127-05 | Selected footage routes to composition or asset package inline. | Approved clip is left in a loose download folder. | Phase4-M03; routing test. |

## 9. Dependencies

| Dependency | Type | Required Status |
|---|---|---|
| `TS-CMF-023` | Research evidence | Query and evidence patterns. |
| `TS-CMF-034` | Asset package | Selected footage becomes package item. |
| `TS-CMF-123` | Provider menu | Footage providers must be configured capabilities. |
| `visual_research_service.py` | Existing service | Extend. |
| `source_provenance_service.py` | Existing service | Store license and hashes. |
| `asset_package_service.py` | Existing service | Admit selected footage. |

## 10. Testing Strategy

| Test Type | Required Coverage |
|---|---|
| Contract tests | Footage candidate and license evidence reject missing fields. |
| Provider tests | Unconfigured providers block retrieval with repair command. |
| License tests | Missing, expired, or prohibited license blocks package admission. |
| Ranking tests | Candidates score by route fit, brand fit, license safety, visual quality, and role. |
| Package tests | Selected clips create asset package items with permitted use and composition role. |
| Receipt tests | Corpus receipt replays query, candidates, selected clips, rejected reasons, and hashes. |
