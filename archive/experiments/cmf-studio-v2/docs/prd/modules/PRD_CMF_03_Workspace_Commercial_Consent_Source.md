---
type: prd-module
project: CMF STUDIO
module_id: PRD-CMF-03
status: canonical
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
source_sections:
  - FR-CMF-01
  - FR-CMF-02
last_updated: 2026-06-22
---

# PRD-CMF-03 - Workspace, Commercial, Consent, and Source Governance

## Module Purpose

This module covers the product foundation that protects brand scope, roles, pricing, consent, source truth, likeness, voice, and recording provenance. It combines FR-CMF-01 and FR-CMF-02 from the current PRD.

## Product Requirements

### PR-CMF-03.01 Brand Workspace Governance

CMF STUDIO must operate as a governed multi-brand production environment. Owners and Admins can create, suspend, archive, restore, and inspect organizations and brand workspaces. Operators can switch active brand context explicitly. Every command, query, upload, receipt, provider job, render, memory admission, and publishing action must bind to organization and brand scope.

The product must prevent cross-brand leakage of transcripts, identity assets, provider jobs, approvals, memory, publishing records, source files, and cost records.

Every brand workspace must expose guest/client management as a first-class operational area. Guests must not appear as loose contacts in a global list. Each guest record belongs to a brand workspace and carries its own consent state, source artifacts, sessions, Voice DNA/Emotional DNA references, Interview Asset Contracts, Expression Moments, Asset Package Specs, content assets, approvals, publishing intents, and memory entries.

The operator-facing hierarchy is:

```text
organization -> brand_workspace -> guest -> expression_session -> asset_package -> content_asset -> asset_version
```

The UI and backend must make active brand and active guest context explicit before showing production data or allowing commands.

### PR-CMF-03.02 Role and Command Governance

The system must support role-based permissions for Owners, Admins, Operators, Reviewers, Migration Stewards, Production Stewards, Publishing Approvers, and Commercial Administrators. Every state-changing command must be permission-checked, idempotent, tenant-scoped, and receipt-writing.

Telegram and PWA surfaces must share the same backend command model and object state.

### PR-CMF-03.03 Commercial Policy

The only customer-facing content charges are:

- `$29/week` trial Guest Asset Packs;
- `$99/month` Monthly Asset Engine.

The system may enforce internal quotas, usage controls, cost tracking, worker limits, and entitlement policies. It must not expose extra public content tiers, credit systems, newsletter packages, or unsupported deliverables.

### PR-CMF-03.04 Versioned Consent

Guests and clients can provide, narrow, expire, and revoke consent for recording, source storage, likeness use, derivative generation, provider processing, synthetic voice eligibility, reuse, retention, and publication.

Consent must be evaluated before upload processing, provider jobs, render jobs, memory admission, Voice-DNA Boost, approval, publishing intent, and Publer scheduling.

### PR-CMF-03.05 Source Artifact Integrity

The system must preserve immutable source artifacts, transcript revisions, timestamp references, source hashes, upload provenance, recording setup, master recording status, backup recording status, and file-quality gates.

The product must not silently treat compressed platform recordings as canonical production sources when a master source is required.

### PR-CMF-03.06 Voice and Likeness Safety

Voice-DNA Boost is allowed only as a documented structural repair exception. It cannot carry primary claims, decisive confessions, medical assertions, or unsupported emotional truth. The system must distinguish source voice, repaired source voice, synthetic bridge voice, interviewer voice, music, SFX, and generated audio in manifests and receipts.

## Functional Requirements Covered

- FR-CMF-01.01 through FR-CMF-01.07.
- FR-CMF-02.01 through FR-CMF-02.07.

## Acceptance Gates

- Brand A commands cannot return, mutate, or reference Brand B production objects.
- Guest A commands cannot return, mutate, or reference Guest B sessions, source artifacts, asset packages, content assets, approvals, or memory unless an explicit cross-guest compilation workflow is created and approved.
- Revoked or incompatible consent blocks provider jobs, renders, memory, voice repair, review approval, and publishing.
- Customer-facing pricing surfaces expose only `$29/week` and `$99/month`.
- Telegram approvals produce the same command receipt and policy checks as PWA approvals.

## Explicit Non-Goals

- generic self-serve SaaS onboarding that ignores creative production state;
- one-time consent checkbox;
- synthetic voice as convenience rewriting;
- newsletters as deliverables.
