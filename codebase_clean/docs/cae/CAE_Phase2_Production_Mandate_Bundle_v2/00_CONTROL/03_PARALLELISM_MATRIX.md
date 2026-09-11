# Parallelism Matrix — Phase 2 Updated

## Safe parallel groups
After Phase 1 acceptance:
- M13 Pi substrate
- M14 Program discovery
- M16 Builder export metadata
- M18 JIT context/package compiler
- M22 Skill loader

After M13/M14/M16 as dependencies require:
- M15 Harness binding
- M17 workflow/capability bridge

After M15/M17/M18:
- M19 universal Program state
- M21 four-lane Agent Team

After M19 + M20 prerequisites:
- M20 state/recovery/resume hooks
- M23 Hooks/Extensions/capability enforcement (can parallel with M22 when file/registry ownership is disjoint)

M24 is the only consolidation gate.

## Parallel safety rules
- one writer per shared schema/registry;
- no two agents edit the same PRD section concurrently;
- all parallel mandates pin the same baseline commit;
- no mandate may consume an unstable contract without declaring the dependency;
- operator decisions, constitutional changes and canonical authority changes are never parallelized.
