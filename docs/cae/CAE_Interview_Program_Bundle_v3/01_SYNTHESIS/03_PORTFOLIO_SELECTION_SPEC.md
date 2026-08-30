# Hypothesis Portfolio Selection Specification

**Status:** BUNDLE-PROVISIONAL

## 1. Goal

Select an approximately 16–24 line working hypothesis portfolio from the larger candidate field while preserving semantic diversity and operator control.

## 2. Selection dimensions

Each candidate should expose, where available:

`relevance`
`evidence_potential`
`guest_authority`
`audience_alignment`
`collision_strength`
`novelty`
`downstream_compatibility`
`research_grounding`
`distinctiveness`
`risk`
`confidence`
`portfolio_overlap`

These are selection diagnostics, not proof of truth.

## 3. Selection behavior

The system should:

1. reject structurally invalid candidates;
2. cluster semantically overlapping candidates;
3. score within clusters;
4. select across clusters for useful diversity;
5. allow Operator override;
6. preserve rejected/deferred candidates as lineage/history rather than deleting evidence;
7. produce a final selected working set only after explicit Operator approval.

## 4. No quota gaming

The system must never force 16–24 selections when candidate density or quality is insufficient. It may produce a smaller working set and report the insufficiency.

Likewise, the downstream target of ~32 content pieces must never be used to force hypotheses or evidence into unsupported structures.

## 5. Promotion boundary

The selected portfolio is a working program. It does not create or mutate canonical upstream AIR hypotheses unless the existing AIR authority explicitly provides that mutation operation and it is authorized by the owning service.
