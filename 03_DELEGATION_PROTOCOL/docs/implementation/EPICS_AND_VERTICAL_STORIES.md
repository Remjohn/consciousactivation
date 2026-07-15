---
title: Delegation Implementation Epics and Vertical Stories
product: CMF Content Harness Visual Asset Editor Delegation Protocol
stage: 4
status: planned_blocked
created: 2026-07-14
---

# Delegation Implementation Epics and Vertical Stories

## 1. Planning Boundary

This backlog plans the transport-neutral Delegation Protocol and conformance
runtime. It does not authorize Stage 5. `EPIC-R4` is readiness remediation;
all implementation epics remain blocked until the Stage 4 verdict is `PASS`
and a signed, immutable contract release is available.

The backlog extends the repository-owned contract catalog and validators. It
does not create alternate Content Harness, VAE, or Control Tower owners.

## 2. Epic Portfolio

| Epic | Outcome | Primary owner | Stage 4 status |
|---|---|---|---|
| EPIC-R4 Contract readiness remediation | Stage 3 baseline exactly matches locked Stage 2 authority, lifecycle, compatibility, and Format 02 specifications | Delegation contract owner with product ratification | Required now |
| EPIC-01 Single-asset protocol kernel | One signed Format 02 demand reaches acknowledged completion through pure ports and test persistence | Delegation reference library | Blocked |
| EPIC-02 Reliability and security | Legitimate duplicates are idempotent, hostile replay is rejected, and recovery preserves one effect | Delegation reference library and security owner | Blocked |
| EPIC-03 Governance lifecycle | Cancellation, budget, amendment, supersession, invalidation, revocation, and replacement preserve immutable history | Delegation reference library plus fact owners | Blocked |
| EPIC-04 Delegation Sets | One multi-asset set coordinates independent member correlations without merging lineage or authority | Delegation reference library | Blocked |
| EPIC-05 Audit, projection, and conformance | Append-only receipts, rebuildable projections, fault tests, and Format 02 evidence prove public behavior | Delegation conformance kit plus Control Tower adapter owner | Blocked |

## 3. EPIC-R4 Contract Readiness Remediation

| Story | Vertical outcome | Specification anchors | Dependencies | Required evidence | Status |
|---|---|---|---|---|---|
| R4-01 Exact field authority | Every public schema field and governed array item resolves to one registered value owner without blanket wildcards; unknown paths fail closed | TS-DLG-02 sections 6 and 15; XRI-019 | Stage 3 catalog | Generated owner metadata, owner-coverage test, unauthorized-path vectors | Complete in `1.0.0-rc.2` |
| R4-02 Canonical lifecycle reconciliation | Registry states and transitions exactly implement the TS-DLG-03 table, including amendment, cost approval, capability gap, human review, partial result, superseded, result rejected, and replaced branches | TS-DLG-03 sections 5 and 15; XRI-020 | R4-01 | Transition-table diff is empty; every legal row and every absent pair is tested | Complete in `1.0.0-rc.2` |
| R4-03 Complete compatibility and migration vectors | One direct path, one deterministic adapter path, and one immutable source-to-target migration have positive, repeat, lossy, forged, and downgrade fixtures | TS-DLG-04 sections 8, 9, and 16; XRI-012 | R4-01 | Golden source/output/receipt hashes and negative field-preservation results | Complete in `1.0.0-rc.2` |
| R4-04 Normative Format 02 scenario portfolio | SCN-01 through SCN-10 match TS-DLG-10 names and assertions, with exact messages, principals, states, audit sequence, effect counts, projections, prohibited effects, and negative variants | TS-DLG-10 sections 7 through 17; XRI-021 | R4-02, R4-03 | Ten scenario bundles and a coverage assertion for every mandatory claim | Complete in `1.0.0-rc.2` |
| R4-05 Owner reconciliation and release | Content Harness, VAE, Control Tower, security, and storage owners ratify applicable boundaries; the baseline is signed, tagged, and published immutably | TS-DLG-01; CROSS_REPO_ISSUES XRI-001, XRI-002, XRI-013 through XRI-017 | R4-01 through R4-04 | Pinned repositories, signed manifests, immutable release URI, release tag, verification report | Externally blocked |
| R4-06 Readiness gate rerun | All seven Stage 4 gates pass against the published release and real upstream evidence | Primary PRD Stage 4 | R4-05 | `IMPLEMENTATION_READINESS.md` replaced by an evidence-backed `PASS` decision | Blocked by R4-05 |

## 4. EPIC-01 Single-Asset Protocol Kernel

| Story | User-visible vertical slice | Specification anchors | Dependencies | Acceptance evidence | Status |
|---|---|---|---|---|---|
| VS-01 Signed single-asset happy path | A Content Harness client submits one exact demand; protocol validation and VAE admission are separate; one result is acknowledged and reaches `COMPLETED` | TS-DLG-01, TS-DLG-02, TS-DLG-03, TS-DLG-06; SCN-01 | R4-06 | Schema/envelope/authority validation, pure lifecycle, test persistence, one execution, result acknowledgement, receipts | Blocked by Stage 4 |
| VS-04 Pinned compatibility negotiation | Before admission, product manifests select one exact protocol/profile or fail with a stable incompatibility reason | TS-DLG-04 | R4-06 | Direct and adapter negotiation vectors, immutable selected-profile hash, no silent upgrade | Blocked by Stage 4 |
| VS-05 Append-only audit and reconstruction | Every accepted or rejected action has a chained receipt; state rebuild equals the pre-restart projection | TS-DLG-03, TS-DLG-08 | VS-01 | Receipt-chain verification, deterministic fold, checkpoint verification, no unaudited acceptance | Blocked by Stage 4 |

## 5. EPIC-02 Reliability and Security

| Story | User-visible vertical slice | Specification anchors | Dependencies | Acceptance evidence | Status |
|---|---|---|---|---|---|
| VS-02 Idempotent command delivery | Repeating identical signed command bytes returns the original receipt and creates one domain effect; changed bytes under the key return `IDEMPOTENCY_CONFLICT` | TS-DLG-03 section 7; SCN-10 | VS-01, VS-05 | Concurrent duplicate, conflict, pending reservation, restart, and outbox-redelivery tests | Blocked by Stage 4 |
| VS-03 Replay rejection | Reused nonce/message identity with changed bytes, expired validity, wrong recipient, or forged key causes no state effect and emits a security receipt when attributable | TS-DLG-02, TS-DLG-03, TS-DLG-09; SCN-10 | VS-02 | Replay-index tests, signature vectors, expiry/skew tests, zero duplicate production | Blocked by Stage 4 |
| VS-12 Atomic acceptance and recovery | Message, lifecycle, idempotency, audit, and outbox records commit atomically per correlation and recover under every named failpoint | TS-DLG-03, TS-DLG-09 | VS-03, VS-05 | Compare-and-append races, transaction failpoints, restart reconstruction, outbox retry | Blocked by Stage 4 |

## 6. EPIC-03 Governance Lifecycle

| Story | User-visible vertical slice | Specification anchors | Dependencies | Acceptance evidence | Status |
|---|---|---|---|---|---|
| VS-06 Safe cancellation | Owner cancellation prevents new work, records VAE checkpoint/disposition, and prevents late artifacts from current use | TS-DLG-05; SCN-06 | VS-12 | Both commit orders for cancellation/result, retained history, exact budget reconciliation | Blocked by Stage 4 |
| VS-07 Supersession and selective invalidation | A new owner demand terminates the old branch, preserves reusable evidence only through explicit proof, and rejects stale results | TS-DLG-05; SCN-03 | VS-12 | Exact old/new identity, changed-path receipt, late-result rejection, no history deletion | Blocked by Stage 4 |
| VS-08 Constraint amendment | VAE reports a conflict and non-binding options; only the demand owner creates the accepted changed demand | TS-DLG-05; SCN-05 | VS-07 | Authority denial for VAE demand mutation, owner decision, lifecycle continuation or explicit terminal result | Blocked by Stage 4 |
| VS-09 Post-completion governance | Invalidation or revocation changes current-use state without deleting facts; replacement requires a separate current acknowledgement | TS-DLG-06; SCN-07 | VS-12 | Impact receipt, current-use guard, replacement identity, separate acknowledgement, immutable old result | Blocked by Stage 4 |
| VS-13 Budget escalation | VAE stops at the commitment boundary; owner approval supplies a new immutable authorization or resolves to capability gap | TS-DLG-05; SCN-04 | VS-12 | Hard ceiling test, approval/denial transitions, cost reconciliation, cancellation race | Blocked by Stage 4 |

## 7. EPIC-04 Delegation Sets

| Story | User-visible vertical slice | Specification anchors | Dependencies | Acceptance evidence | Status |
|---|---|---|---|---|---|
| VS-10 One atomic Delegation Set | Character, environment, and prop demands retain independent correlations while one declared set policy governs release | TS-DLG-07; SCN-02 | VS-06 through VS-09, VS-13 | Dependency graph validation, member isolation, atomic release, member cancellation/supersession fanout | Blocked by Stage 4 |

## 8. EPIC-05 Audit, Projection, and Conformance

| Story | User-visible vertical slice | Specification anchors | Dependencies | Acceptance evidence | Status |
|---|---|---|---|---|---|
| VS-11 Format 02 conformance runtime | The complete ten-scenario portfolio runs through a standard SUT adapter with deterministic time, faults, security vectors, and exact effect assertions | TS-DLG-09, TS-DLG-10 | VS-01 through VS-10, VS-12, VS-13 | Signed evidence bundle with release digests, scenario results, audit roots, SLI report, traces, limitations, and expiry | Blocked by Stage 4 |
| VS-14 Additive Control Tower projection | Existing Control Tower consumes source-linked delegation facts and rebuilds one non-authoritative operational view | TS-DLG-08 | VS-05, upstream Control Tower contract | Projection parity, lag SLI, denied-action visibility, rebuild test, no second authority store | Externally blocked |

## 9. Planned Delivery Waves

| Wave | Included stories | Entry condition | Exit condition |
|---|---|---|---|
| 0 Readiness | R4-01 through R4-06 | Current Stage 4 `FAIL` | Published signed baseline and Stage 4 `PASS` |
| 1 Kernel | VS-01, VS-04, VS-05 | R4-06 | Single-asset flow and audit reconstruction pass |
| 2 Reliability | VS-02, VS-03, VS-12 | Wave 1 | Duplicate, replay, atomicity, and restart gates pass |
| 3 Governance | VS-06 through VS-09, VS-13 | Wave 2 | Every governance branch and race schedule passes |
| 4 Sets and certification | VS-10, VS-11, VS-14 | Wave 3 plus upstream Control Tower evidence | Format 02 evidence bundle passes all mandatory assertions |

## 10. Explicit Exclusions

- Content Harness creativity, composition meaning, or sequencing internals
- Visual Production Plans, VAE workflow nodes, ComfyUI, VLM evaluation,
  candidate ranking, repair strategy, or asset generation
- A replacement Control Tower or second authority store
- Production transport, storage, or deployment choices before owning teams
  provide and approve their adapter contracts
- Implementation work while the Stage 4 verdict is not `PASS`
