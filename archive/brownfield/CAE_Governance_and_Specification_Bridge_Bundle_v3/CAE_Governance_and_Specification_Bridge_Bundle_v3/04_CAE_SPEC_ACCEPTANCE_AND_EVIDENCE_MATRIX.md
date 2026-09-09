# CAE Specification Acceptance & Evidence Matrix v2.0

## Purpose

This matrix prevents implementation specifications from gaining authority through prose quality alone.

## Evidence classes

| Evidence | Examples | Authority |
|---|---|---|
| Runtime repository evidence | code, migrations, tests, observed behavior | highest for current implementation facts |
| Canonical registry evidence | SDA/SFL/Primitive YAML, versioned registry | highest for inherited semantic definitions |
| Immutable human evidence | interview transcript, director note, research source | highest for represented reality claims |
| Ratified architecture | CAE constitutional / ontology docs | highest for target design intent |
| PRD / FR | approved requirements | implementation requirement authority |
| Hypothesis | theoretical rationale | provisional |
| Unvalidated prose | brainstorms, drafts | non-authoritative |

## Acceptance status

A specification can receive only one status:

- `DRAFT`
- `EVIDENCE_COMPLETE`
- `BROWNFIELD_RECONCILED`
- `ARCHITECTURALLY_APPROVED`
- `READY_FOR_DEVELOPMENT`
- `IMPLEMENTED`
- `VERIFIED`
- `SUPERSEDED`

## Minimum evidence for READY_FOR_DEVELOPMENT

1. Relevant phase validation is complete.
2. All major objects have constitutional roles.
3. All referenced inherited registry records are verified.
4. Existing code integration is explicit.
5. Schema contracts are typed.
6. Relations and state transitions are defined.
7. Authorized operations are defined.
8. Error taxonomy exists.
9. Acceptance criteria are measurable.
10. Tests are named.
11. Migration/rollback is defined where brownfield code is affected.
12. Receipt lineage is defined for meaningful runtime actions.
13. Minimum environment fidelity is declared for each material claim.
14. At least one proxy-gaming / false-proof case is defined for each material evaluator.
15. Taste / anti-centroid criteria are defined where the claim is semantically or perceptually sensitive.

## Review questions

A reviewer should be able to answer:

- Why does this object exist?
- Why does it belong to this artifact class?
- Why is it stored this way?
- Why is this relation directional?
- What evidence authorizes this claim?
- What changes over time?
- What must never be mutated?
- Who owns it?
- What agent is permitted to operate on it?
- What SQL view/function exposes it?
- How does failure get classified?
- How can the result be reproduced?

## Reality-contact review

A reviewer MUST distinguish:

- structural validity;
- environment fidelity;
- reward-hacking resistance;
- taste / anti-centroid integrity;
- observed real-world evidence.

No lower evidence level may be reported as a higher one.

## Anti-genericity review

A spec fails if the core design could be copied into another product without changing its architectural reasoning.

Project-specificity must be visible in:

- existing object IDs;
- inherited registry lineage;
- repository paths;
- domain-specific relations;
- CAE error taxonomy;
- Matrix of Edging constraints;
- authenticated evidence requirements;
- SDA/SFL/Primitive interactions;
- runtime receipts.
