# Builder to Delegation RC3 Integration Correction

Date: 2026-07-14  
Verdict: `PASS`  
Stage boundary: bounded correction complete; Step 4 has not started on the corrected baseline.  
Implementation authorization: `false`.

## Outcome

Builder now has one exact active Delegation dependency: `delegation-contracts@1.1.0-rc.3`, release digest `sha256:e3100f9b3ec5db4077def2861128795451085bb8993f1fe318f5aaf6a6653cdf`, compatibility profile `cmf-delegation-compatibility-profile-1-0`. The candidate is recorded as `local_unsigned_release_candidate` with `production_eligibility: false`.

The correction does not redesign the confirmed 12 Epics or 69 Stories, does not regenerate the 410-obligation inventory, does not implement Delegation or VAE behavior, and does not write production code. No new planning obligation was required.

## RC3 validation

| Validation | Result | Evidence |
| --- | --- | --- |
| Release receipt and exact identity | PASS | Receipt hash `sha256:bb5c5c236fd77b4715bb279f378e72881a05943527e1b88ad4845bb71f0f7c4d` |
| Release manifest | PASS | Manifest hash `sha256:e7501488be54221da3ab437a32d57f80a74cabf3347b6b6b874922b1019ff51f` |
| Released hashes | PASS | 146 receipt entries and 145 manifest entries checked; zero mismatches |
| Release-layout validator | PASS | Package `1.1.0-rc.3`, protocol `1.0`, Visual Asset Demand `1.1` |
| Validator suite | PASS | 69 passed |
| Protocol suite | PASS | 33 passed |
| Generated Python and TypeScript types | PASS | Both released hashes match; both expose `interview_expression` |
| Builder mapping suite | PASS | 20 of 20 checks passed |

## Active and historical dependency treatment

`XDEP-003`, its 32 consuming Story metadata references, and the Release 1 subset now resolve through `contracts/integration/DELEGATION_CONTRACT_PIN.yaml`. No active dependency record selects RC1 or RC2.

The confirmed Epic proposal/inventory and prior Step 4 validation/readiness reports retain their accurate RC1/RC2 observations as historical records. They are superseded for current dependency resolution by the exact RC3 pin; they were not rewritten. `CURRENT_PROJECT_STATUS.md` is also left untouched because it was outside the permitted patch set; `PROGRAM_STATUS_EXPORT.yaml` and this receipt publish the current correction state.

## Builder-to-Delegation wire boundary

Builder may compile target specifications, populate the pinned generated RC3 type, validate against the external schema and compatibility policy, and emit a hashed handoff receipt. Builder may not copy the shared schema as local truth, implement the Delegation runtime, implement VAE realization, flatten semantic lineage, or guess source kind.

The wire compilation order is exact pin, authoritative source-kind resolution, lossless Activative lineage, monotonic wrong-reading locks, category/profile compatibility, external RC3 validation, then hashed handoff. Any partial or ambiguous state fails closed.

## Source-kind mapping

| Builder source | RC3 source kind | Constraint |
| --- | --- | --- |
| Interview Expression | `interview_expression` | Reaction Receipt and Expression Moment refs are non-empty |
| ReelCast | `interview_expression` | Reaction Receipt and Expression Moment refs are non-empty |
| Public Comment | `public_comment` | Authoritative public-comment evidence required |
| Reply / DM | `direct_message_reply` | Authoritative reply/direct-message evidence required |
| Operator-authored source | `authored_source` or `operator_supplied` | Select only from authoritative authorship/supply evidence; ambiguity is rejected |
| Live premise | `live_premise` | Authoritative live-premise classification required |
| Research-derived synthesis | `research_synthesis` | Research lineage required |
| Legacy migration | `legacy_migrated` | Traceable lossless migration receipt required |

Non-interview sources may omit interview-only refs. When those refs are present, they remain schema-valid and fully validated.

## Category and profile compatibility

All five categories are structurally compilable and contract-compatible. `2d_character_animation/minimal_coach_theatre` remains the benchmarked, limited-production, and production-certified reference profile. Short-form edited video, Carousels, Supervisuals, and Conversational Activation / Human Expression do not inherit that certification.

The four conversational profiles—`public_comment`, `reply_dm`, `reelcast_expression`, and `interview_expression`—are structurally compilable and RC3 contract-compatible, but not benchmarked, limited-production certified, or production certified. Interview Expression and ReelCast support stays structural until their owning product authorities approve final PRDs.

## Wrong-reading-lock inheritance

Every semantically generative or transformative Visual Asset Demand must carry non-empty wrong-reading locks. Deterministic delivery variants inherit every parent lock. Derivatives may add stricter locks, but cannot remove or weaken inherited locks. Relaxation requires a new authoritative upstream demand version. Builder emits and validates the rule; VAE owns realization enforcement.

## Activative lineage mapping

| Builder artifact | Delegation RC3 field |
| --- | --- |
| Activative Intelligence Pack | `/activative_semantic_lineage/activative_intelligence_pack_ref` |
| Identity DNA | `/activative_semantic_lineage/identity_dna_ref` |
| Context Premise | `/activative_semantic_lineage/context_premise_ref` |
| Resonance Map | `/activative_semantic_lineage/resonance_map_ref` |
| Matrix of Edging | `/activative_semantic_lineage/matrix_edge_product_ref` |
| Activative Call | `/activative_semantic_lineage/activative_call_refs` |
| Reaction Receipt | `/activative_semantic_lineage/reaction_receipt_refs` |
| Expression Moment | `/activative_semantic_lineage/expression_moment_refs` |
| Activation Contract | `/activation_contract` |
| Visual Semantic Pack | `/visual_semantic_pack` |
| Visual Narrative Program | `/visual_narrative_program` |
| Feature Contracts | `/feature_contracts` |
| T/V route | `/somatic_route_request` |
| Composition Intent | `/composition_intent` |

No required lineage maps to a generic notes field.

## Existing obligations and Stories

The correction is fully owned by existing obligations: `ADR-013`, `CONST-004`, `CONST-005`, `CONST-007`, `CONST-008`, `D004`, `FR-137`, `FR-139`–`FR-150` where category/source behavior applies, `FR-167`–`FR-180`, `NFR-CAT-001`–`NFR-CAT-003`, `NFR-COMPAT-002`, `NFR-EVAL-004`, `NFR-TRACE-001`, and `NFR-TRACE-003`.

Primary affected Stories are `ST-03.03`, `ST-06.01`, `ST-06.03`, `ST-06.05`, `ST-07.01`–`ST-07.04`, `ST-08.02`, `ST-08.03`, `ST-08.07`, `ST-12.03`, and `ST-12.04`. XDEP-003 remains metadata on its previously confirmed 32 consuming Stories; no Story outcome, ordering edge, acceptance criterion, or ownership assignment changed.

Exact row-level mappings are in `BUILDER_DELEGATION_RC3_TRACEABILITY.csv`. Every trace points to an existing obligation and Story, so a planning amendment and human inventory confirmation are not required.

## Existing artifacts affected

- TS-11: exact pin, source-kind, category/profile, wrong-reading, lineage, ownership, failures, tests, and compatibility.
- TS-15: Format 02 RC3 fixture boundary and conversational certification non-inheritance.
- ADR-007 addendum: governed source kind and interview provenance.
- ADR-013 addendum: exact external pin and schema ownership.
- ADR-018 addendum: RC3 demand lineage and wrong-reading-lock inheritance.
- Cross-repository dependency register: active XDEP-003 and Story dependency metadata.
- Release 1 Story subset: exact RC3 reference for the existing 69-Story subset.
- Program Status Export: correction PASS and pre-Step-4 stop state.

## Remaining gates

This integration correction is `PASS`, but RC3 is unsigned and not production-eligible. Overall Builder implementation readiness remains `FAIL`; HD-006, HD-007, BD-004, BD-007, BD-008, BD-010, and BD-014 remain unresolved, as do the previously reported artifact-integrity and Format 02 dependency-independence concerns. No production implementation is authorized.

## Stop condition

The requested correction is complete. Step 4 was not entered or rerun on the corrected baseline. Continue only through a later explicit Step 4 instruction.
