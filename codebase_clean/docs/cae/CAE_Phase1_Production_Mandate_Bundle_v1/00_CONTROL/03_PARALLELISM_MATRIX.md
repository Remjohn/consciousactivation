# Parallelism Matrix — Phase 1

After M1:
- M2 Program Inventory
- M3 Harness Inventory

After M1/M2/M3:
- M4 State Coverage
- M5 Agent/Skill/Operation Ownership
- M6 Hook Guarantee Matrix

After M4–M6:
- M7 Runtime Gap DAG
- M8 Programs/Artifacts/Chat Contract
- M9 Agent Team Reference Topology
- M10 Builder→Harness→Pipeline Binding Contract

M11 depends on M7–M10.
M12 depends on M1–M11 and owns consolidated Phase 1 PRD/control-state synchronization.

Parallel work is allowed only with disjoint write ownership and a shared baseline commit.
Do not parallelize shared schema/registry migrations, same-file PRD edits, constitution changes,
or competing canonical authority changes.
