# Visual Evaluator Certification Evidence-Closure Plan

Date: 2026-07-14  
Profile: `character-scene-composition@1.1.0-draft`  
Current status: `specified_not_certified`

This plan closes H-005 without inventing thresholds or implying production certification. The existing dimension dictionary, applicability rules, hard-gate precedence, responsible-layer model, wrong-reading evaluation, and conditional delete-caption/no-text behavior remain unchanged.

## Required evidence packages

| Work package | Required closure evidence | Exit rule |
|---|---|---|
| Evaluator and program pins | Evaluator provider/model or weight digest, API/runtime version, prompt/program/template digest, credentials boundary, deterministic settings, independent-producer proof, supported media/profile matrix | Every evaluation receipt resolves immutable evaluator and program identities; an unavailable pin fails closed |
| Labeled calibration corpus | Versioned corpus manifest, source/consent/provenance, constitutional lineage, profile applicability, adjudicated labels for every dimension and responsible layer, ambiguity notes, class balance, reviewer agreement, corpus digest | Evaluation authority approves the corpus and label protocol; development and calibration partitions are reproducible |
| Protected regression set | Sealed manifest and digest, access controls, non-overlap proof, representative/golden/borderline/adversarial/repair/no-text/wrong-reading cases, release-use audit | Protected cases remain unseen during tuning and produce an independently retained release report |
| Non-compensable gates | Approved gate list and precedence for integrity, constitutional enforceability, activation direction, viewer role, Feature Contracts, wrong-reading locks, and applicable no-text survival | No ranking score or aesthetic/technical aggregate can compensate for a failed gate |
| Threshold calibration | Per-dimension/profile calibration method, score distributions, confidence/uncertainty treatment, candidate operating points, approval rationale, calibration version and digest | Evaluation and product authorities approve thresholds from empirical evidence; no threshold is inferred from the draft fixtures |
| False-positive/false-negative analysis | Confusion matrices and case reviews overall and by required profile slice; special analysis for dominant wrong readings, feature-contract failures, activation drift, affinity, and delete-caption collapse | Error ceilings and escalation/arbitration rules are approved, with critical false negatives treated as release blockers |
| Rollback baseline | Last-known-good evaluator/program/profile pins, comparison report, rollback trigger, compatibility window, retained artifacts, rehearsal receipt | A failed calibration, drift alarm, or regression can restore the exact prior certified configuration |
| Affinity terminology and alias policy | Canonical definition of `affinity`, decision on any `human_affinity` alias, migration rule for historical receipts, display/API naming, prohibited silent aliasing | One canonical term is approved; aliases are explicit, versioned, and lossless or rejected |

## Certification execution order

1. Freeze evaluator/program candidates and the corpus labeling protocol.
2. Materialize and adjudicate calibration data; seal the protected set before tuning.
3. Approve non-compensable gates independently of numeric thresholds.
4. Calibrate candidate thresholds and analyze false positives, false negatives, uncertainty, and slice disparities.
5. Run the protected set once under controlled release conditions and produce signed reports.
6. Rehearse rollback to the retained baseline.
7. Approve affinity terminology and any historical alias migration.
8. Publish a versioned certification receipt and update the registry status only if every applicable item passes.

## Status transition rule

The profile must remain `specified_not_certified` while any evidence package is missing or unapproved. A production-certified status requires immutable evidence references for every work package, passing non-compensable gates, approved empirical thresholds, and a successful rollback rehearsal. Batch B contract availability does not waive evaluator certification.
