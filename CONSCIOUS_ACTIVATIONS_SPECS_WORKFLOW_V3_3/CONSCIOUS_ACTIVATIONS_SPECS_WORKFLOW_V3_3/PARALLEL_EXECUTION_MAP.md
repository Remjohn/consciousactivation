# Parallel Execution Map

## Mandatory sequential control path

```text
Prompt 1 — Authority convergence
    ↓
Prompt 2 — Canonical reconciliation
    ↓
Prompt 3 — Spec writing factory
    ↓
Prompt 4 — Independent audit factory
    ↓
Prompt 5 — Revision factory
    ↓
Prompt 6 — Independent re-audit and acceptance
    ↓
Prompt 7 — Development Capsules and build-readiness
    ↓
Prompt 8 — Shared contracts
```

These stages must remain sequential because each freezes authority or shared bytes consumed by the next stage.

## Parallel work inside Prompt 3

After the Extra High controller freezes lane packets, run these High writers simultaneously:

- Lane A — shared authority and contracts
- Lane B — Activative Intelligence Runtime
- Lane C — Atomic Harness Pipeline kernel and retrieval
- Lane D — Interview Expression and source packages
- Lane E — video, static, and animation runtimes
- Lane F — Studio, revisions, and HumanResolution
- Lane G — evaluation, repair, retrieval, and Programmed Models
- Lane H — VAE, Delegation, workers, operations, and release boundaries

Each agent writes **one Tech Spec per execution**. Multiple agents may run at once only on disjoint canonical files.

## Parallel work inside Prompt 4

Every written spec may be audited in parallel by a different High agent. The writer may not audit its own spec. Shared-schema conflicts go to the Extra High controller.

## Parallel work inside Prompt 5

Independent revisions may run in parallel. Any revision touching shared schemas, object ownership, compatibility policy, or two products waits for an Extra High architecture decision.

## Parallel work inside Prompt 6

Independent re-audits may run in parallel. Final cross-spec convergence and accepted hash locking are performed sequentially by one Extra High integrator.

## Parallel work after Prompt 8

```text
AIR build waves ──────────┐
                          ├→ Prompt 10 → Prompt 11
AHP build waves ──────────┘
```

AIR and AHP may build in parallel only after the shared contract release is frozen, their paths are disjoint, and every child build targets one accepted spec.

## Sidecars that may start during Prompts 1–7

These may run concurrently on isolated documentation or fixture paths:

- operator interview/source preparation;
- CMF Studio archive inventory and source-reuse verification;
- local FFmpeg/Node/Remotion/HyperFrames/Skia readiness inventory;
- VAE external-readiness documentation, without Stage 5;
- external dependency/version/license review;
- clean-environment and test-fixture preparation.

They may not change current authority, canonical schemas, product source, or accepted specs.


## V3.2 Prompt 03 wave parallelism

Prompt 03 is not one global parallel dispatch. It is a topological wave factory:

```text
Wave 0 roots: parallel
    ↓ WRITTEN_PENDING_AUDIT receipts + hashes
Wave 1 dependents: parallel
    ↓
Wave 2 dependents: parallel
    ↓
...
```

A downstream writer may consume a hash-pinned upstream draft when the edge is `WRITE_INTERFACE_DEPENDENCY` or `WRITE_CONTEXT_DEPENDENCY`. The draft is never represented as accepted authority. Acceptance and build prerequisites are enforced later.

Program Control cross-product proposals may be written and audited in parallel with direct product specs, but they remain excluded from Development Capsules until target-product adoption.


## V3.3 recovery sequence

For the current repository state:

```text
Prompt 02C recovery — sequential
    ↓
Prompt 03 Wave 0 writers — parallel
    ↓
Prompt 03 Wave 1 writers — parallel
    ↓
remaining topological waves
    ↓
Prompt 04 independent audits — parallel
```

Final ratification is not required for these specification-quality stages. It becomes mandatory before `ACCEPTED_FOR_BUILD` and Development Capsules.
