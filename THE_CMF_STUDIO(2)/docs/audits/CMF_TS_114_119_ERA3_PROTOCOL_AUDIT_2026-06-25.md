---
title: "ERA3 Protocol Audit - TS-CMF-114 through TS-CMF-119"
date: "2026-06-25"
status: "audit-complete-revision-required"
auditor_role: "Principal CCP Architecture Reviewer"
scope:
  - "TS-CMF-114-conscious-sequencing-contract-kernel-and-registries.md"
  - "TS-CMF-115-interview-brief-v2-sequence-hypothesis-and-expression-acquisition-plan.md"
  - "TS-CMF-116-live-ingredient-coverage-tracker-and-cue-suppression-policy.md"
  - "TS-CMF-117-expression-ingredient-inventory-and-relation-graph.md"
  - "TS-CMF-118-content-sequence-program-compiler-and-composition-handoff.md"
  - "TS-CMF-119-sequence-eval-gates-learning-and-package-sequencing.md"
verdict: "revision-required-before-implementation"
---

# ERA3 Protocol Audit - TS-CMF-114 through TS-CMF-119

## 1. Audit Sources Loaded

| Source | Use |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory writing protocol and rejection criteria. |
| `THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Audit.md` | Five-lens audit protocol. |
| `THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Revision.md` | Revision instruction protocol, used only to understand next step. |
| `THE CMF STUDIO/docs/architecture/april_updates/TRIGGER_COMMAND_AUDIT.md` | One-spec-at-a-time audit trigger discipline. |
| `docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 CBAR mandates used as reference because the CMF project copy is missing this file. |
| `docs/architecture/april_updates/Phase5_Growth_Epics.md` | Phase 5 CBAR mandates used as reference because the CMF project copy is missing this file. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-114...TS-CMF-119` | Audited target specs. |

Protocol evidence:

- ERA3 protocol requires Section 3 to include Architecture Traceability, Existing Backend Integration, ADR-05 Primitives, and CBAR Mandate Enforcement.
- ERA3 protocol requires Acceptance Criteria to include failure examples and CBAR mandate references.
- ERA3 protocol requires exact Python files, database tables, and API routes in Existing Backend Integration.
- The audit prompt requires five lenses: FR Coverage, DEP-ID and Primitive Integrity, Boundary Precision, Gate and CBAR Completeness, Cross-Spec Consistency.

## 2. Executive Verdict

The six specs are conceptually aligned with the Conscious Sequencing bundle, but they are not ERA3-complete and should not enter implementation yet.

The domain architecture is directionally correct:

```text
Registry kernel
-> Interview Brief V2 procurement
-> Live coverage
-> Expression Ingredient Inventory
-> Content Sequence Program
-> Sequence eval / package learning
```

The protocol failure is structural and compliance-oriented:

- CBAR mandate enforcement is missing as a formal Section 3 subsection.
- Acceptance criteria do not include failure examples or mandate references.
- Most specs do not provide Architecture Traceability DEP-ID tables.
- Primitive references are fuzzy, not exact YAML IDs or registry IDs.
- Database table ownership and Receipt Chain Guard writes are not specified.
- The Phase Epic files required by the protocol are not present inside `THE CMF STUDIO/docs/architecture/april_updates`.

## 3. PASS - Specs With Zero Flags

None.

All six specs require revision before implementation.

## 4. FLAGS

### FLAG 1

**[TS-CMF-114..119] | LENS 1 + LENS 4 | SEVERITY: CRITICAL**

- **Finding:** The CMF project copy does not contain the Phase4/Phase5 Epic files that the ERA3 audit and writing protocols require before CBAR mandate validation.
- **Location:** `THE CMF STUDIO/docs/architecture/april_updates/` contains only protocol/prompt files; the required Phase Epic files were found only in root `docs/architecture/april_updates`, not inside the CMF project folder.
- **Required Action:** Migrate or canonically mirror the Phase Epic files and CBAR audit references into `THE CMF STUDIO/docs/architecture/april_updates`, then update each spec's `Files Read` table with the exact local CMF paths and proof that the relevant mandates were loaded.

### FLAG 2

**[TS-CMF-114..119] | LENS 4 | SEVERITY: CRITICAL**

- **Finding:** The specs do not include the mandatory Section 3 subsection `CBAR Mandate Enforcement`, even though the protocol states specs without this subsection are rejected.
- **Location:** Section 3 in each spec:
  - `TS-CMF-114`, lines 56-137
  - `TS-CMF-115`, lines 49-96
  - `TS-CMF-116`, lines 45-94
  - `TS-CMF-117`, lines 45-97
  - `TS-CMF-118`, lines 47-97
  - `TS-CMF-119`, lines 46-95
- **Required Action:** Add `### CBAR Mandate Enforcement` to Section 3 of every spec with applicable mandate IDs, story origins, governing primitive IDs, and exact enforcement mechanisms. At minimum, evaluate Phase4-M01 through Phase4-M07 and Phase5-M01 where artifact/package/publish trust is involved.

### FLAG 3

**[TS-CMF-114..119] | LENS 4 | SEVERITY: CRITICAL**

- **Finding:** Acceptance Criteria are plain numbered checks and do not include failure examples or CBAR mandate references.
- **Location:** Section 8 in each spec:
  - `TS-CMF-114`, lines 244-252
  - `TS-CMF-115`, lines 200-208
  - `TS-CMF-116`, lines 187-195
  - `TS-CMF-117`, lines 204-212
  - `TS-CMF-118`, lines 214-222
  - `TS-CMF-119`, lines 217-225
- **Required Action:** Rewrite Section 8 into ERA3 AC format: each AC must include requirement, failure example, mandate reference, and test evidence. For example, a source-grounding AC must state that synthetic guest meaning in a sequence is a failure and reference the relevant CBAR/doctrine gate.

### FLAG 4

**[TS-CMF-115..119] | LENS 2 | SEVERITY: CRITICAL**

- **Finding:** These specs name entry objects, exit objects, receipt objects, read models, state objects, and compiler outputs without assigning DEP-IDs in an Architecture Traceability table.
- **Location:** Frontmatter and Primary Output Schema sections:
  - `TS-CMF-115`, lines 12-13 and 112-149
  - `TS-CMF-116`, lines 12-13 and 110-148
  - `TS-CMF-117`, lines 12-13 and 112-145
  - `TS-CMF-118`, lines 12-13 and 113-155
  - `TS-CMF-119`, lines 12-13 and 111-159
- **Required Action:** Add Architecture Traceability tables with registered DEP-IDs for every entry, transformation, output, receipt, read model, state object, and event. Cross-reference DEP producers/consumers across TS-CMF-114 through TS-CMF-119.

### FLAG 5

**[TS-CMF-114] | LENS 2 | SEVERITY: WARNING**

- **Finding:** TS-CMF-114 has an Architecture Traceability table, but the new registry snapshot and normalization receipt schema objects introduced later are not assigned DEP-IDs.
- **Location:** `TS-CMF-114`, Architecture Traceability lines 58-70, Primary Output Schema lines 152-200.
- **Required Action:** Add DEP-IDs for `SequenceRegistryItem`, `SequenceRegistrySnapshot`, and `SequencingRegistryNormalizationReceipt`, then reference them in the API/event contracts.

### FLAG 6

**[TS-CMF-114..119] | LENS 2 | SEVERITY: CRITICAL**

- **Finding:** Primitive references are not expressed as exact YAML IDs or exact registry IDs; terms like "primitive triad", "meaning", "delivery", "format/material", "primitive tags", and "primitive coalition" are fuzzy from an ERA3 audit perspective.
- **Location:** Examples include:
  - `TS-CMF-114`, lines 116-126 and 263-275
  - `TS-CMF-115`, line 105 and lines 221-233
  - `TS-CMF-117`, lines 41, 156, and 232
  - `TS-CMF-118`, lines 12, 85, 96, 104, 108, 139, 221, and 231
  - `TS-CMF-119`, lines 38 and 44
- **Required Action:** Add an `ADR-05 Primitives` subsection to Section 3 of every spec. Use exact primitive IDs from the verified registry or exact composition primitive registry IDs. Do not rely on role labels alone.

### FLAG 7

**[TS-CMF-114..119] | LENS 4 + LENS 5 | SEVERITY: CRITICAL**

- **Finding:** Receipt objects are named, but Receipt Chain Guard writes and database persistence ownership are not specified.
- **Location:** Required receipt frontmatter in all six specs; receipt schemas in:
  - `TS-CMF-114`, lines 184-200
  - `TS-CMF-115`, lines 119-134
  - `TS-CMF-116`, lines 117-134
  - `TS-CMF-117`, lines 119-134
  - `TS-CMF-118`, lines 143-155
  - `TS-CMF-119`, lines 144-159
- **Required Action:** For each receipt, specify the exact persistence table, receipt chain action, immutable hash fields, replay/idempotency key, and event emitted after write. If using a shared receipt service, define the adapter and table columns.

### FLAG 8

**[TS-CMF-115..119] | LENS 3 + LENS 5 | SEVERITY: CRITICAL**

- **Finding:** Most specs do not include the mandatory `Existing Backend Integration` subsection with exact Python files, database tables, and API routes.
- **Location:** Section 3 in `TS-CMF-115` through `TS-CMF-119` has no `Existing Backend Integration` subsection. `TS-CMF-114` includes Python service/file references at lines 104-114 but still lacks database tables.
- **Required Action:** Add `### Existing Backend Integration` to every spec with a four-column table: Python owner, database table(s), API route(s), and migration/backfill behavior. Include whether each item extends, wraps, or replaces an existing owner.

### FLAG 9

**[TS-CMF-114..119] | LENS 4 | SEVERITY: WARNING**

- **Finding:** Gate tables include thresholds and consequences, but the specs do not define a shared verdict model (`PASS`, `PROVISIONAL`, `FAIL`, `BLOCKED`) or state how each verdict writes an evaluation receipt.
- **Location:** Gate threshold sections:
  - `TS-CMF-114`, lines 128-137
  - `TS-CMF-115`, lines 84-96
  - `TS-CMF-116`, lines 84-94
  - `TS-CMF-118`, lines 87-97
  - `TS-CMF-119`, lines 84-95
- **Required Action:** Add a gate verdict semantics subsection to each spec or a shared reference to a canonical gate verdict contract. Include receipt writes and downstream state transitions for `PASS`, `PROVISIONAL`, `FAIL`, and `BLOCKED`.

### FLAG 10

**[TS-CMF-117] | LENS 3 + LENS 5 | SEVERITY: WARNING**

- **Finding:** The relation graph read model is introduced without defining graph storage ownership or reconciliation with the immutable inventory snapshot.
- **Location:** `TS-CMF-117`, lines 136-144 and API contract lines 181-191.
- **Required Action:** Specify whether the graph is persisted in Postgres JSONB, Neo4j, or a projected read model only. Define reconciliation ownership when an inventory revision supersedes a graph.

### FLAG 11

**[TS-CMF-118] | LENS 5 | SEVERITY: WARNING**

- **Finding:** `SequenceCompositionHandoff` targets downstream engines but does not map its target enum to exact downstream spec object schemas or ownership boundaries.
- **Location:** `TS-CMF-118`, lines 121-142 and API contract lines 193-204.
- **Required Action:** Add a downstream compatibility matrix mapping each `composition_engine_target` to the canonical spec/object it must produce or call: Video Edit Program, CarouselSpec, SingleImage/SuperVisual spec, TwoDCharacterProgram, or reaction template runtime.

### FLAG 12

**[TS-CMF-119] | LENS 3 + LENS 5 | SEVERITY: WARNING**

- **Finding:** Learning recommendations may affect registries, thresholds, examples, and adapter mappings, but the spec does not define promotion governance strongly enough to prevent drift from operator revisions into active registry behavior.
- **Location:** `TS-CMF-119`, lines 41-44, 111-141, and 219-224.
- **Required Action:** Add a registry-promotion state machine and approval rule: learning signals may only create recommendations; active registry changes require separate registry revision receipt, operator approval, and compatibility tests against TS-CMF-114.

### FLAG 13

**[TS-CMF-114..119] | LENS 1 | SEVERITY: WARNING**

- **Finding:** The specs use invented story IDs `12.1` through `12.6` and `epic_id: 12`, but no local PRD module or epic file is cited as the owning FR/Story authority.
- **Location:** Frontmatter in every spec.
- **Required Action:** Add a local PRD/epic module for Conscious Sequencing or cite an existing PRD module section as the authority. If this is a bundle-derived spec family, create a formal `PRD_CMF_12_Conscious_Sequencing_Expression_Acquisition.md` or equivalent crosswalk before implementation.

### FLAG 14

**[TS-CMF-116] | LENS 4 | SEVERITY: NOTE**

- **Finding:** The live coverage spec correctly states coverage estimates are provisional, but the cue suppression policy does not define rate limits, cooldown windows, or maximum cues per interview state.
- **Location:** `TS-CMF-116`, lines 69-94 and line 106.
- **Required Action:** Add cue-rate limits and cooldown semantics to protect the "not a checklist" rule.

## 5. Summary Statistics

| Metric | Count |
|---|---:|
| Total specs reviewed | 6 |
| Specs with zero flags | 0 |
| Total CRITICAL flags | 8 |
| Total WARNING flags | 5 |
| Total NOTE flags | 1 |
| DEP-ID issues requiring registration | 6 specs affected |
| Primitive registry issues requiring exact IDs | 6 specs affected |
| Cross-spec consistency issues requiring arbitration | 4 |

## 6. Required Revision Order

1. Restore the missing local Phase Epic / CBAR source files into `THE CMF STUDIO`.
2. Add formal PRD/epic ownership for `Epic 12 / Story 12.1-12.6`.
3. Apply a global CBAR Mandate Enforcement section to every spec.
4. Apply a global ADR-05 Primitive ID section to every spec.
5. Add DEP-ID tables to every spec, including receipts/read models/events.
6. Add backend integration tables with Python owner, database table, API route, and migration behavior.
7. Rewrite Acceptance Criteria with failure examples and mandate references.
8. Add receipt-chain persistence and gate verdict semantics.
9. Repair per-spec issues: TS117 graph ownership, TS118 downstream compatibility, TS119 learning promotion governance, TS116 cue cooldowns.

## 7. Implementation Readiness Verdict

```text
NOT READY FOR IMPLEMENTATION
```

The specs are strong enough as domain drafts, but not strong enough as ERA3 implementation specs. The next correct step is not build. The next correct step is `PROMPT_Spec_Revision.md`: produce copy-pasteable revision instructions for every finding, then apply those revisions spec by spec.

