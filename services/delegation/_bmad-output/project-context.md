---
project: CMF Content Harness Visual Asset Editor Delegation Protocol
context_version: 1
current_stage: 4
readiness_verdict: FAIL
stage5_authorized: false
updated: 2026-07-14
---

# Project Context

## Mission

Provide a transport-neutral shared delegation protocol between the CMF Content
Harness and the Visual Asset Editor while preserving owner sovereignty. The
protocol validates, records, coordinates, audits, and projects public facts. It
does not create meaning, make visual-production choices, or replace either
product's internal workflow.

Release 1 conformance is the Format 02 Minimal Coach Theatre profile.

## Current Stage State

- Stage 1 repository and contract audit: complete with concerns.
- Stage 2 technical specifications: complete with concerns.
- Stage 3 contract candidate `1.0.0-rc.2`: all seven repository-local Stage 4
  gates pass; the package remains unsigned and unpublished.
- Stage 4 readiness: `FAIL` because external ratification, release, security,
  operations, and upstream integration evidence are unavailable.
- Stage 5 implementation: not authorized.

The authoritative readiness decision is
`docs/implementation/IMPLEMENTATION_READINESS.md`.

## Source Of Truth Order

1. Locked primary PRD decisions and Stage 4 gate language.
2. Stage 2 specifications under `docs/tech-specs/TS-DLG-01` through
   `TS-DLG-10`.
3. Contract ownership and cross-repository issue registers.
4. Corrected and published canonical contract package.
5. Generated bindings, fixtures, validators, adapters, and projections.

Generated Stage 3 artifacts do not override Stage 2 normative behavior merely
because their local tests pass.

## Repository Ownership

| Owner | Owns | Must not own here |
|---|---|---|
| Content Harness | semantic and Activative intent, composition intent, wrongness locks, sequence role, budget/cancellation/supersession decisions, result acknowledgement and consumption authorization | VAE plans, execution, evaluation, repair, visual ranking |
| Visual Asset Editor | admission, production plan/execution, production acceptance, evidence, result artifacts, safe cancellation disposition | demand meaning, owner composition changes, downstream consumption authorization |
| Delegation Protocol | shared schemas/versions, validation, compatibility verdicts, public lifecycle, idempotency/replay decisions, routing, audit receipts, source-linked projection facts | creativity, visual-production strategy, a second product authority store |
| Harness Control Tower | additive operational read model over accepted source facts | canonical lifecycle or product authority |
| Security/Platform owners | trust roots, key lifecycle, storage, transaction, retention, backup, recovery, transport adapters | domain meaning or field ownership changes |

Product repositories consume a pinned contract release. They do not copy,
fork, or privately reinterpret shared schemas.

## Locked Contract Decisions

- Wire payloads are JSON; YAML is authoring-only.
- Protocol/message versions use `MAJOR.MINOR`; package releases use SemVer.
- Canonical schema IDs use
  `https://contracts.cmf.dev/delegation/<message_type>/<major>.<minor>/schema.json`.
- Canonical JSON follows RFC 8785 under the safe-integer profile; hashes use
  SHA-256 and Release 1 signatures use Ed25519.
- Demand identity is exactly `request_id`, `version`, `payload_hash`, and
  `canonical_ref`.
- Protocol submission validation and VAE admission are separate receipts.
- VAE results cannot authorize downstream consumption; acknowledgement does.
- Public objects are closed and unknown fields fail validation.
- Lifecycle effects serialize per correlation and accepted audit sequence.
- Idempotency handles legitimate duplicate delivery; replay protection blocks
  hostile or policy-invalid reuse. The controls never collapse into one key.
- Historical facts are immutable through cancellation, supersession,
  invalidation, revocation, and replacement.
- Control Tower is a rebuildable additive projection only.

## Remediation And Remaining Blockers

Local remediation is complete in `1.0.0-rc.2`:

1. Every registered field and governed collection item has an exact owner;
   blanket wildcards are gone and unknown paths fail closed.
2. `lifecycle.json` implements 19 locked states and 44 normalized transitions;
   every absent state/trigger/principal triple is executable as a rejection.
3. Direct, adapter, and immutable migration golden vectors include canonical
   hashes, repeat determinism, owner evidence, and negative-loss cases.
4. The ten Format 02 bundles match the normative TS-DLG-10 portfolio and pin
   exact identities, hashes, lifecycle, audit, outbox, effects, projections,
   prohibited effects, negative variants, and races.

Remaining blockers are external: upstream repositories and product adapters,
owner ratification, trust infrastructure, operational persistence ownership,
the existing Control Tower contract, pinned product releases, and a valid Git
release repository with immutable tag and owner signatures.

R4-01 through R4-04 are locally complete. R4-05 and R4-06 remain blocked by
`DLG-ISSUE-001`, `DLG-ISSUE-002`, canonical `XRI-013` through `XRI-017`, and
canonical `XRI-019` through `XRI-021`. Program issue identity and status are
read only from `../CMF_PROGRAM_CONTROL/04_CROSS_REPO_ISSUES/XRI_REGISTRY.yaml`.
The former Delegation uses of `XRI-001`, `XRI-002`, and `XRI-018` as local
identifiers are preserved only as historical aliases of `DLG-ISSUE-001`,
`DLG-ISSUE-002`, and closed `DLG-ISSUE-018` respectively.

## Planned Reference Architecture

After a Stage 4 `PASS`, the Stage 5 reference library may implement only:

- strict schema/envelope and authority validation;
- pure compatibility negotiation and lifecycle decision functions;
- separate idempotency and replay repositories;
- transport-neutral ports with in-memory/test adapters first;
- per-correlation compare-and-append acceptance;
- atomic message, state, idempotency, audit, and outbox behavior;
- append-only chained receipts and deterministic reconstruction;
- one single-asset flow, one Delegation Set, cancellation, supersession,
  amendment, invalidation, revocation, replacement, and conformance tests.

Storage and transport technologies remain adapter decisions owned by approved
platform interfaces.

## Prohibited Scope

- Content Harness creativity, sequencing internals, or meaning generation
- Visual Production Plans, ComfyUI, VLM evaluation, production workflows,
  candidate ranking, repair strategy, or asset generation
- A new Control Tower or authoritative projection database
- Production adapters or deployment before owner interfaces are supplied
- Stage 5 code while the readiness verdict is not `PASS`

## Verification Commands

From the repository root:

```powershell
python packages/contracts/tools/build_baseline.py
$env:PYTHONPATH='packages/validators'
python -m unittest discover -s packages/validators/tests -v
python scripts/rebuild_manifest.py
python scripts/validate_package.py
```

Passing these commands proves local package consistency only. Readiness also
requires the semantic diff, migration, Format 02, upstream, signature, and
publication evidence listed in `IMPLEMENTATION_READINESS.md`.

## Agent Working Rules

1. Read the primary PRD, all Stage 2 specifications, this context, the current
   readiness verdict, and `CROSS_REPO_ISSUES.md` before changing contracts.
2. Map work to existing repository and product owners before proposing a new
   service, schema, or authority.
3. Treat generated artifacts as outputs. Change canonical source definitions,
   regenerate, and prove no unreviewed drift.
4. Never infer implementation coverage from filenames or prose. Inspect code,
   schemas, fixtures, and executable tests.
5. Record every boundary contradiction in `CROSS_REPO_ISSUES.md`.
6. Do not weaken a gate to obtain `PASS`; provide the missing evidence.
7. Do not begin Stage 5 until `R4-06` records an explicit `PASS`.
