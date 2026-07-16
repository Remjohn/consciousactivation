# ADR-013: Target Compilers And External Boundaries

Status: `ACCEPTED`

Owners: Cross-product architecture. Trace: D004, D005, D011, D014, D029, D030, D031, D032, D033; TS-11. External blocker: BD-014.

## Context

Builder must compile Atomic Content Harness, Visual Asset Editor, and Delegation Contract targets without flattening them into one profile or importing external production behavior. Content semantic authority must survive compilation.

## Decision

Maintain three versioned `CompilationTargetProfile` records with distinct source profiles, IR projections, Genesis graphs, compilers, artifact sets, evaluation gates, and certification scopes. External target compilers consume read-only versioned interface snapshots and emit schemas/specifications/fixtures/packages only.

Visual Asset Editor and Delegation packages remain `UNCERTIFIED` in Release 1. Their owning repositories control runtime and shared contracts. Cross-target compatibility validates content-owned fields as immutable.

## Alternatives

- Universal target profile: rejected by D004 and D033.
- Vendor external schemas into Builder as editable truth: rejected because ownership and version authority would drift.
- Call external runtimes during compilation: rejected due product boundary and reproducibility.

## Interfaces, Data, And Errors

`TargetCompiler.compile(ir, profile, interface_snapshots) -> TargetPackageManifest`. Errors include missing profile/snapshot, incompatible contract, forbidden semantic mutation, unsupported certification, and external-version mismatch.

## Authority, Security, And Determinism

Compilers have no external runtime credentials/network. Snapshots are read-only and hashed. Human cross-product owners ratify breaking contract versions and certification.

## Consequences

Positive: explicit target differences, preserved ownership, safe structural support. Cost: three compiler/test suites and interface-version coordination.

## Observability, Performance, Migration

Record target/profile/compiler/snapshot identities, compatibility, artifact hashes, and certification. External contract changes invalidate only dependent packages. No V2.1 target migration applies.

## V1.2 Constitutional Alignment Amendment

The accepted three-target decision is unchanged. Conversational Activation / Human Expression is the fifth category under the Atomic Content Harness target, not a fourth compilation target.

| Implementation owner | Component boundary | Data / contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- |
| cross_product_architecture | Builder compiles/validates versioned packages; Visual Asset Editor and Delegation owners execute externally | five-category registry, conversational profile registry, Shared Activative Core, Reaction/Expression contracts, visual-semantic/narrative/composition/T/V/Delegation handoff | Reject target/category conflation, semantic mutation, missing snapshot, false certification, or external runtime capability | three-target invariance, five-category coverage, non-mutation, no-network/no-credential fixtures | All four conversational profiles are structural `UNCERTIFIED`; visual handoff preserves the complete activation-first chain | Additive category/profile and snapshot fields; existing three target IDs and accepted decision remain compatible; BD-014 stays open |

## Delegation RC3 Pin Addendum

The accepted external-boundary decision is unchanged. Its active Delegation snapshot is now the exact local unsigned `1.1.0-rc.3` candidate pinned by release and receipt hashes. Builder owns mapping and validation only; the Delegation repository continues to own schemas, generated types, compatibility semantics, and runtime.

| Implementation owner | Component boundary | Data / contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- |
| cross_product_architecture | Builder reads and validates the pinned external package; no external contract is vendored as Builder truth | `DELEGATION_CONTRACT_PIN.yaml`, `BUILDER_TO_DELEGATION_WIRE_MAPPING.yaml`, RC3 compatibility profile | Reject version ranges, RC1/RC2 active references, hash mismatch, unsigned-as-production claims, local schema forks, or ownership inversion | exact hash, no-active-prior-RC, external ownership, generated-type, and no-runtime tests | Every active Builder Delegation dependency resolves to exact RC3 and declares `local_unsigned_release_candidate`, `production_eligibility: false` | Historical RC1/RC2 receipts stay immutable; active references are superseded; a later release requires explicit repinning and compatibility validation |

## Verification

Boundary tests reject external runtime modules, cross-target semantic rewrites, missing snapshots, false certification, and nondeterministic packages.
