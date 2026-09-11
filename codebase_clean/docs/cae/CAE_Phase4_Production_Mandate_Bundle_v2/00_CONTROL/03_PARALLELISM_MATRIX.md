# Parallelism Matrix

Parallel work saves time only when outputs are independently mergeable and authority ownership
does not conflict. This follows the current CAE mandate protocol.

## Phase 1

Safe after M1–M3:
- M4 State Inventory
- M5 Agent/Skill/Operation Inventory
- M6 Hook/Extension Inventory
- M7 Runtime Gap Matrix
- M9 Agent/Team Contract
- M10 Harness/Atomic Harness Package Contract
- M11 Pi/Eve/StateM Architecture Decision

Dependent:
- M8 Program/Artifact/Chat Contract depends on M2 Program Inventory.
- M12 depends on M1–M11.

## Phase 2

Potential parallel groups:
- M13 Pi substrate spike
- M14 Program package/registry
- M16 Builder export extension
- M18 JIT capsule integration
- M22 Skill maturity/loader
- M23 Hooks/extensions

Dependent:
- M15 Harness binding depends on M13 + M14.
- M17 workflow/capability bridge depends on M16 + M15.
- M19 universal Program state runtime depends on M15.
- M20 State context/recovery depends on M19.
- M21 four-lane agent orchestration depends on M15 + M22.
- M24 depends on all.

## Phase 3

Potential parallel groups after M24:
- M25 Workspace/Guest operating context
- M26 Audience context
- M27 Guest setup/genesis
- M28 Research ingestion
- M29 Knowledge canonicalization / OKF
- M30 Knowledge projection
- M31 Research signals/clusters

Dependent:
- M32 Collision depends on M25–M31 as applicable.
- M33 Interview Prep depends on M32.
- M34 Live Interview depends on M33 + runtime.
- M35 Evidence→Editorial depends on M34.
- M36 depends on all.

## Phase 4

Potential parallel groups after M36:
- M37 Editorial candidate formation
- M38 scoring/clustering/operator selection
- M39 Storyboard/SemanticProgram
- M40 Script
- M41 Visual prompt/asset annotation
- M42 Carousel/SuperVisual/Animation
- M43 Video edit/CompositionIR/CMF
- M44 VAE delegation / visual realization
- M45 Release/Outcome
- M46 Operator Programs/Artifacts/Chat UI

M47 pilot depends on all production-path prerequisites.
M48 depends on M47 + adversarial/hardening evidence.

## Prohibited parallelism

Never parallelize:
- shared schema migrations with another migration owner;
- changes to the same registry without an integration owner;
- changes to the same PRD section;
- state authority changes with competing owners;
- Program approval decisions;
- constitution changes;
- canonical Skill changes while an adapter is being authored against it;
- the same Atomic Harness manifest/library slot from multiple agents.

## PRD synchronization

Each mandate identifies its owned PRD section(s). Parallel mandates may update CURRENT.md only
when their PRD ownership is disjoint and mergeable. Phase close owns the consolidated phase summary.
