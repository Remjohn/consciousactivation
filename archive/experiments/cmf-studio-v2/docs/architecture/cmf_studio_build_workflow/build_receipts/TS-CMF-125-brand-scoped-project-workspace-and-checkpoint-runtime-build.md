---
title: "TS-CMF-125 Build Receipt"
status: "implemented"
implemented_at: "2026-06-25"
batch: "Batch 3"
spec: "THE CMF STUDIO/docs/tech-specs/TS-CMF-125-brand-scoped-project-workspace-and-checkpoint-runtime.md"
---

# TS-CMF-125 Build Receipt

Implemented `ProductionWorkspace`, `WorkspaceArtifactSlot`, `WorkspaceCheckpoint`, and `WorkspaceResumeDecision` so each brand/guest workspace owns artifact slots, object-storage prefixes, checkpoints, and resumable runtime state.

Verification: `test_batch3_provider_workspace_footage_and_runtime_locking_are_governed`.
