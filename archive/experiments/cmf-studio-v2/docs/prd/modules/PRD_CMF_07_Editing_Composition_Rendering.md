---
type: prd-module
project: CMF STUDIO
module_id: PRD-CMF-07
status: canonical
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
source_sections:
  - FR-CMF-07
  - FR-CMF-08
last_updated: 2026-06-22
---

# PRD-CMF-07 - Editing, Composition, Rendering, and Provider Operations

## Module Purpose

This module covers the production engine after source expression and route are approved. It defines Complete Editing Sessions, SceneSpecs, scene reproducibility, Ideogram 4 `CompositionJob` JSON, SVRE/Aurore visual research, provider jobs, self-hosted ComfyUI Docker workers, deterministic rendering, audio/caption assembly, and asset lineage.

## Product Requirements

### PR-CMF-07.01 Complete Editing Session

Production starts only after an approved Expression Moment, approved route, source lineage, and locked Brand Context Version exist. A Complete Editing Session preserves source lineage, route, SceneSpec, Creative State, Render Contract, provider jobs, composition state, evaluation receipts, revision history, and approval state.

### PR-CMF-07.02 SceneSpec and Creative State

The system can compile SceneSpecs, Creative State, renderer routes, asset selections, evaluation requirements, platform variants, text plans, caption plans, sonic plans, and revision policies. SceneSpecs must include scene containers, scene components, creative subsystems, and asset-roll intent.

When a `ReactionTemplateRouteReceipt` exists, SceneSpec must preserve the `reaction_template_route_id`, `reaction_template_code`, content format code, live clip slot requirements, motion grammar, renderer route, composition ID, and primitive eval obligations. The template route is lineage, not a UI hint. It determines how live footage, A-roll/B-roll, overlay cards, caption timing, motion rules, and final verdict/poll/ranking states are assembled.

### PR-CMF-07.03 Ideogram 4 CompositionJob

Ideogram 4 `CompositionJob` JSON is a key reproducibility component. The system must preserve prompt hash, composition plate URI, composition analysis, provider metadata, downstream edit jobs, selected brand layers, final text plan, evaluation receipts, and approval state.

Ideogram 4 acts as Composition Director. It is not final identity authority and not final text authority.

### PR-CMF-07.04 Scene Reproducibility

An Operator must be able to reconstruct why a scene looks the way it does from source expression, route, Brand Context Version, composition JSON, provider jobs, layer manifests, render manifests, evaluation receipts, and human approvals.

### PR-CMF-07.05 Provider Job Governance

The system can create provider jobs and receipts for Ideogram 4, GPT Image 2, Flux 2 Klein 9b, Qwen-Image-Layered, SAM3, self-hosted ComfyUI Docker GPU workers, LavaSR, MOSS-TTS, Remotion, and Motion Canvas when applicable.

Provider requests and responses must preserve prompt hashes, model or workflow metadata, seed/config values when available, input assets, output hashes, cost, retries, failure details, and evaluation state.

### PR-CMF-07.06 Self-Hosted ComfyUI Worker

The ComfyUI path is a self-hosted Docker worker on AWS or Google Cloud with 24GB or 32GB VRAM. It is not RunningHub. It must run queued jobs, checkpoint per asset, upload artifacts, write receipts, report cost, and shut down safely.

### PR-CMF-07.07 Rendering and Assembly

Deterministic assets route through Remotion or Motion Canvas using approved brand layers, final text rendering, manifests, timing, motion recipes, captions, and sonic plans. Audio assembly must distinguish source audio, interviewer audio, restored audio, synthetic bridge audio, music, SFX, captions, and final mix.

Reaction editing templates are deterministic renderer contracts for formats such as split-screen versus, tier list, blind ranking, proposal ranking, elimination bracket, mirror quiz, and authority ladder. They may use live filmed guest clips as the source spine, with generated or researched visual layers only as governed supporting assets.

### PR-CMF-07.08 SVRE/Aurore and Asset Research

Asset research must use governed `VisualResearchQuery`, `AssetResearchManifest`, `ImageResolutionMap`, licensing, scoring, candidate selection, and asset-roll intent. Found or generated visual candidates must not become opaque unlicensed media.

## Functional Requirements Covered

- FR-CMF-07.01 through FR-CMF-07.09.
- FR-CMF-08.01 through FR-CMF-08.08.

## Acceptance Gates

- A render cannot start without approved expression, route, Brand Context Version, SceneSpec, and provider policy.
- A reaction-template render cannot start without an accepted `ReactionTemplateRouteReceipt`, compatible content format code, live clip slot mapping, and SceneSpec lineage.
- Ideogram output with final-looking text or identity drift must be rejected or restricted to composition use.
- Provider failures support retry, resume, cancel, compensate, or terminal review without corrupting receipts.
- Timeline, audio, caption, and visual lineage must be preserved.
