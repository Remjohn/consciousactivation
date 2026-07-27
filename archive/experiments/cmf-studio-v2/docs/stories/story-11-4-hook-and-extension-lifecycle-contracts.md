---
story_id: "11.4"
story_title: "Hook and Extension Lifecycle Contracts"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-22"
fr_ids: []
module_requirement_ids:
  - "PRD-CMF-10.03"
  - "PRD-CMF-10.04"
pipeline_stage: "all gated stages"
entry_object: "lifecycle boundary and integration request"
exit_object: "`HookSpec`, `ExtensionSpec`"
validation_contract: "no canonical-state bypass and lifecycle contract"
required_receipt: "hook/extension receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 11.4: Hook and Extension Lifecycle Contracts

**Epic:** 11 - Agent Factory Persona Runtime
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Story Definition

As an Architect, I want hooks and extensions to be explicitly registered, so that lifecycle checks and integrations enforce the pipeline without becoming hidden authority.

**Acceptance Criteria:**

- Given a Hook is registered, when activated, then it must declare lifecycle boundary, trigger condition, allowed checks, blocked mutations, emitted receipt, and failure behavior.
- Given an Extension is registered, when mounted, then it must declare tools, credentials boundary, provider or integration scope, canonical-state restrictions, and receipts.
- Given a Hook attempts creative reasoning instead of deterministic enforcement, when review runs, then activation is blocked.
- Given Publer is used, when `PUB-PUBLERX-EX` runs, then it schedules or reports status without owning approval, caption truth, or asset lineage.
- Given `REV-APPGATE-HK` fires, when an approval blocker exists, then publication cannot continue.

**Technical Notes:** Add `HookSpec`, `ExtensionSpec`, lifecycle enums, gateway mounting rules, and no-canonical-authority checks.

**Legacy and Primitive Mapping:** Preserves callback-like ideas from agent frameworks while enforcing CMF consent, review, provider, and memory gates. Active families: SAF, FRC, FBK.

**Prerequisites:** Stories 1.1, 2.3, 8.1, 9.4.

## Tech Spec Handoff Requirements

- Define hook and extension contracts, lifecycle triggers, mounting rules, and receipts.
- Include tests proving extensions cannot own canonical state and hooks cannot mutate outside command authorization.
