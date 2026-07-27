---
type: prd-module
project: CMF STUDIO
module_id: PRD-CMF-05
status: canonical
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
source_sections:
  - FR-CMF-04
last_updated: 2026-06-22
---

# PRD-CMF-05 - Brand Genesis and Brand Context

## Module Purpose

Brand Genesis manufactures the reusable creative universe for a brand. It is not setup, onboarding decoration, or a one-time prompt profile. A locked `BrandContextVersion` becomes the creative, visual, sonic, narrative, consent, and identity substrate for interviews, SceneSpecs, render contracts, provider jobs, evaluation receipts, revisions, and memory.

## Product Requirements

### PR-CMF-05.01 Brand Genesis Session

Operators can run Brand Genesis from intake, consent, source media, brand notes, audience reality, offer, forbidden tone, visual preferences, Voice DNA, Emotional DNA, visual constitution, and negative-space constraints.

### PR-CMF-05.02 Acting Library

The system can generate, evaluate, repair, reject, approve, and lock a 64-state acting library across emotional and gesture families. Each approved state must have identity fit, gesture clarity, style consistency, review status, and downstream usability metadata.

### PR-CMF-05.03 Paper-Cut Rig

The system can generate and validate a paper-cut avatar rig with layer separation, pivot points, mouth shapes, eye and brow variants, gesture variants, body layers, preview tests, and a rig manifest.

### PR-CMF-05.04 Micro-Semiotic and Creative Libraries

Operators can create and govern prop libraries, micro-semiotic anchors, motion recipes, SFX libraries, composition preferences, platform profiles, and publishing profiles. These libraries must be brand-scoped and versioned.

### PR-CMF-05.05 Review, Repair, and Lock

Generated references must be scored for likeness, gesture clarity, hand quality, paper texture, style adherence, negative space, and production usability. The product must support reject, repair, replace, approve, and lock decisions before production jobs depend on the assets.

### PR-CMF-05.06 Versioning and Forking

The system can fork Brand Context Versions for approved changes while preserving historical outputs against their original locked context. Production jobs cannot use unapproved, unlocked, stale, or cross-brand identity assets.

## Functional Requirements Covered

- FR-CMF-04.01 through FR-CMF-04.07.

## Acceptance Gates

- Complete Editing Sessions can only select assets from a locked Brand Context Version.
- Historical renders remain bound to the Brand Context Version used at render time.
- A failed likeness, hand, identity, or style evaluation blocks lock until repaired, replaced, or explicitly rejected.
- LoRA or identity model training is not default when approved-reference workflows are sufficient.

## Downstream Consumers

- Interview intelligence uses Brand Context, Voice DNA, Emotional DNA, forbidden tone, and audience reality.
- SceneSpecs use acting library, props, micro-semiotic anchors, visual constraints, motion recipes, SFX, and platform profiles.
- Evaluation uses Brand Context Version as identity and style authority.
