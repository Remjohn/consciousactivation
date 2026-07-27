# ADR-012: Sandbox And Least Privilege

Status: `ACCEPTED`

Owners: Security and workflow architecture. Trace: D002, D012, D025, D027, D033; TS-02, TS-03, TS-14. Blocker: BD-012.

## Context

Builder nodes process sensitive evidence, invoke models/tools, compile artifacts, and may later support implementation tasks. Shared unrestricted processes allow source mutation, secret leakage, benchmark contamination, and cross-node failure.

## Decision

Use deny-by-default capability grants and three policy classes: deterministic process sandbox, provider-call sandbox, and isolated implementation-task sandbox. Policies specify immutable environment/image, read-only mounts, writable staging, tools, network allowlist, ephemeral secret references, CPU/memory/time limits, output contract, logs, and disposal.

The ratified profiles require deny-by-default grants, read-only evidence mounts, ephemeral credentials, explicit network allowlists, and per-node worktree or container isolation. The exact conforming platform mechanism remains an implementation choice and may not weaken those policy semantics.

## Alternatives

- One trusted host process: rejected for blast radius and reproducibility.
- Container every trivial operation: rejected as a universal rule because measured risk should choose profile.
- Prompt-only restrictions: rejected because they are not security boundaries.

## Interfaces, Data, And Errors

`SandboxManager.create/execute/collect/dispose`; `CapabilityGrant`; `SandboxPolicy`; `SandboxReceipt`. Errors include denied capability, mount escape, network denial, resource limit, output violation, disposal failure, and policy mismatch.

## Authority, Security, And Determinism

Only deterministic policy code issues runtime grants from approved node definitions. Agents cannot widen grants. Evidence mounts are read-only; generators cannot access labels; secrets are short-lived; external repositories use read-only snapshots.

## Consequences

Positive: bounded blast radius, reproducibility, and auditable permissions. Cost: startup overhead, image/policy maintenance, and platform-specific adapters.

## Observability, Performance, Migration

Record policy/version, grants, image hash, startup/run/disposal latency, resource use, denied attempts, and retained output hashes. Policy changes invalidate workflow promotion. No legacy sandbox migration applies.

## Verification

Escape, traversal, secret, network, tool, label, resource exhaustion, crash, cleanup, and cross-platform conformance tests are required.
