# 08 - Tech Specs Doctrine-Driven Testing Audit

Date: 2026-06-23

## Scope

- Specs reviewed: 77
- Review target: CMF tech specs TS-CMF-001 through TS-CMF-077.
- Audit lens: whether each spec has an explicit doctrine-driven test harness binding or needs one because it touches governed CMF behavior.

## Audit Rule

A spec needs conditional revision when it touches governed CMF behavior and does not already contain a `Doctrine-Driven Test Harness Binding` section. TS-CMF-077 is the source standard.

## Summary

- Specs already carrying explicit binding: 1
- Specs requiring conditional revision: 76
- Specs with baseline/no additional revision need: 1

## Per-Spec Findings

| Spec | Testing Section | Eval/Primitive/Doctrine Language | Existing Binding | Conditional Revision |
|---|---:|---:|---:|---:|
| `TS-CMF-001-contract-kernel-command-spine.md` | yes | yes | no | yes |
| `TS-CMF-002-pipeline-stage-orchestration-records.md` | yes | yes | no | yes |
| `TS-CMF-003-python-dspy-pi-bmad-spec-workflow.md` | yes | yes | no | yes |
| `TS-CMF-004-organization-and-brand-workspace-lifecycle.md` | yes | yes | no | yes |
| `TS-CMF-005-role-based-production-permissions.md` | yes | yes | no | yes |
| `TS-CMF-006-commercial-entitlements-without-offer-drift.md` | yes | yes | no | yes |
| `TS-CMF-007-pwa-and-telegram-state-parity.md` | yes | yes | no | yes |
| `TS-CMF-008-versioned-consent-records.md` | yes | yes | no | yes |
| `TS-CMF-009-recording-setup-and-source-artifact-gate.md` | yes | yes | no | yes |
| `TS-CMF-010-consent-blockers-across-workflows.md` | yes | yes | no | yes |
| `TS-CMF-011-voice-dna-boost-eligibility-and-audio-classification.md` | yes | yes | no | yes |
| `TS-CMF-012-consent-and-source-review-surface.md` | yes | yes | no | yes |
| `TS-CMF-013-migration-ledger-inventory-and-hashing.md` | yes | yes | no | yes |
| `TS-CMF-014-registry-conversion-fixtures-and-evals.md` | yes | yes | no | yes |
| `TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md` | yes | yes | no | yes |
| `TS-CMF-016-legacy-import-hidden-prompt-and-template-gates.md` | yes | yes | no | yes |
| `TS-CMF-017-intentional-orchestration-migration-contracts.md` | yes | yes | no | yes |
| `TS-CMF-018-brand-genesis-intake-and-session-creation.md` | yes | yes | no | yes |
| `TS-CMF-019-64-state-acting-library.md` | yes | yes | no | yes |
| `TS-CMF-020-paper-cut-rig-and-creative-libraries.md` | yes | yes | no | yes |
| `TS-CMF-021-brand-context-version-locking-and-forking.md` | yes | yes | no | yes |
| `TS-CMF-022-production-gate-to-locked-brand-context.md` | yes | yes | no | yes |
| `TS-CMF-023-research-fields-and-evidence-capture.md` | yes | yes | no | yes |
| `TS-CMF-024-guest-dossier-audience-reality-context-premise-and-resonance.md` | yes | yes | no | yes |
| `TS-CMF-025-matrix-of-edging-brief.md` | yes | yes | no | yes |
| `TS-CMF-026-interviewer-pre-induction.md` | yes | yes | no | yes |
| `TS-CMF-027-interview-asset-contract-and-quality-gate.md` | yes | yes | no | yes |
| `TS-CMF-028-cral-context-premise-emotional-dna-and-root-down-induction.md` | yes | yes | no | yes |
| `TS-CMF-029-complete-expression-session-creation.md` | yes | yes | no | yes |
| `TS-CMF-030-source-ingestion-transcript-alignment-and-provenance.md` | yes | yes | no | yes |
| `TS-CMF-031-anchor-hit-and-expression-moment-candidate-detection.md` | yes | yes | no | yes |
| `TS-CMF-032-expression-moment-review-and-boundary-control.md` | yes | yes | no | yes |
| `TS-CMF-033-archetype-and-asset-derivative-routing.md` | yes | yes | no | yes |
| `TS-CMF-034-guest-asset-pack-spec-generation.md` | yes | yes | no | yes |
| `TS-CMF-035-rejected-candidate-and-coalition-fatality-memory.md` | yes | yes | no | yes |
| `TS-CMF-036-complete-editing-session-creation-from-approved-source.md` | yes | yes | no | yes |
| `TS-CMF-037-scenespec-creative-state-and-render-contract-compilation.md` | yes | yes | no | yes |
| `TS-CMF-038-ideogram-4-compositionjob-lineage.md` | yes | yes | no | yes |
| `TS-CMF-039-layer-manifests-animation-plans-edl-captions-and-sonic-plans.md` | yes | yes | no | yes |
| `TS-CMF-040-revision-and-reconstruction-audit.md` | yes | yes | no | yes |
| `TS-CMF-041-scene-containers-creative-subsystems-and-asset-roll-orchestration.md` | yes | yes | no | yes |
| `TS-CMF-042-provider-capability-registry-and-job-receipts.md` | yes | yes | no | yes |
| `TS-CMF-043-deterministic-remotion-and-motion-canvas-rendering.md` | yes | yes | no | yes |
| `TS-CMF-044-generative-provider-adapters.md` | yes | yes | no | yes |
| `TS-CMF-045-self-hosted-comfyui-docker-gpu-worker.md` | yes | yes | no | yes |
| `TS-CMF-046-comfyui-template-migration-to-worker-assets.md` | yes | yes | no | yes |
| `TS-CMF-047-audio-caption-timeline-and-mix-assembly.md` | yes | yes | no | yes |
| `TS-CMF-048-provider-job-retry-resume-cancel-and-compensation.md` | yes | yes | no | yes |
| `TS-CMF-049-svre-aurore-and-asset-research-engine-routing.md` | yes | yes | no | yes |
| `TS-CMF-050-evaluation-receipt-generation.md` | yes | yes | no | yes |
| `TS-CMF-051-evidence-rich-review-surface.md` | yes | yes | no | yes |
| `TS-CMF-052-review-commands-and-voice-dna-boost-requests.md` | yes | yes | no | yes |
| `TS-CMF-053-approval-blockers.md` | yes | yes | no | yes |
| `TS-CMF-054-publishing-intent-and-publer-adapter.md` | yes | yes | no | yes |
| `TS-CMF-055-telegram-quick-review-with-evidence.md` | yes | yes | no | yes |
| `TS-CMF-056-evidence-backed-memory-admission.md` | yes | yes | no | yes |
| `TS-CMF-057-memory-review-correction-expiry-and-quarantine.md` | yes | yes | no | yes |
| `TS-CMF-058-neo4j-relationship-projection.md` | yes | yes | no | yes |
| `TS-CMF-059-operations-board.md` | yes | yes | no | yes |
| `TS-CMF-060-workflow-recovery-actions.md` | yes | yes | no | yes |
| `TS-CMF-061-operational-readiness-checks.md` | yes | yes | no | yes |
| `TS-CMF-062-persona-code-registry-and-validation.md` | yes | yes | no | yes |
| `TS-CMF-063-agentrolespec-and-departmentspec-runtime.md` | yes | yes | no | yes |
| `TS-CMF-064-subagentrolespec-and-delegation-boundaries.md` | yes | yes | no | yes |
| `TS-CMF-065-hookspec-and-extensionspec-lifecycle-contracts.md` | yes | yes | no | yes |
| `TS-CMF-066-skillbinding-and-jit-skill-mode-binding.md` | yes | yes | no | yes |
| `TS-CMF-067-agent-readiness-evals.md` | yes | yes | no | yes |
| `TS-CMF-068-pi-harness-tool-registry.md` | yes | yes | no | yes |
| `TS-CMF-069-adk-agents-cli-adapter-export-and-drift-gate.md` | yes | yes | no | yes |
| `TS-CMF-070-ui-architecture-and-operator-experience.md` | yes | yes | no | yes |
| `TS-CMF-071-reaction-editing-template-routing.md` | yes | yes | no | yes |
| `TS-CMF-072-scene-template-runtime-binding-for-reaction-clips.md` | yes | yes | no | yes |
| `TS-CMF-073-canonical-composition-json-registry-and-preview-approval.md` | yes | yes | no | yes |
| `TS-CMF-074-reaction-clip-renderer-and-background-removal-compositing.md` | yes | yes | no | yes |
| `TS-CMF-075-operator-composition-and-template-approval-workbench.md` | yes | yes | no | yes |
| `TS-CMF-076-open-source-integration-adapter-evaluation-and-import-plan.md` | yes | yes | no | yes |
| `TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md` | yes | yes | yes | no |

## Revision Decision

Apply a standard doctrine-driven test harness binding section to every spec marked `Conditional Revision = yes`. The section must reference TS-CMF-077 and require doctrine invariants, primitive/eval obligations, negative fixtures, receipt-chain tests, and approval blockers where relevant.
