# Question Intelligence Synthesis — Provisional CAE Architecture

**Status:** BUNDLE-PROVISIONAL
**Build authority:** false
**Purpose:** capture the cross-book structural convergence identified in the supplied conversation before any Question Primitive is canonized.

## 1. First-principle convergence

### FP-01 — Question structure controls information quality
A question is an information-control stimulus. The useful unit is not grammatical simplicity alone; CAE needs a sufficiently isolated psychological/semantic target.

### FP-02 — The answer changes the state of the interview
Questioning is a state-transition process. The answer is an observation that changes the landscape of eligible next moves.

### FP-03 — First-pass answers are provisional
Completeness requires deliberate re-entry: breadth checks, specificity escalation, cross-checking, summary-and-confirm, or other targeted re-entry.

### FP-04 — Research creates an expected-state model
Research is operational when it establishes what would be expected, making confirmation, omission, discrepancy, anomaly, or novel branch observable.

### FP-05 — Information value and interactional fit are distinct
A question may be information-rich and interactionally wrong, or interactionally effective and semantically weak. Both dimensions matter.

### FP-06 — Specificity is a controllable resolution variable
Abstraction can be reduced by escalating toward concrete event, behavior, mechanism, evidence, chronology, or numerical detail as appropriate.

### FP-07 — Contradiction is evidence of discrepancy, not proof of deception
The correct operation is preservation and reconciliation of the discrepancy.

### FP-08 — Interpretation must remain corrigible
System interpretation must be distinguishable from Guest-stated evidence and may require Guest confirmation/correction before becoming accepted interpretation.

### FP-09 — Format and archetype constrain acquisition
A recognizable content syntax can reduce structural processing load; the interview should acquire response structures that remain compatible with intended downstream forms when such intent exists.

### FP-10 — Preparation and adaptation are complementary
The correct runtime pattern is a deterministic coverage spine plus bounded adaptive branching.

## 2. Candidate mechanism clusters

The following are **candidate families**, not canonical primitives.

| Cluster | Mechanism family | Primary transformation | Runtime trigger | Candidate disposition |
|---|---|---|---|---|
| QI-C01 | Answer Resolution Escalation | abstract/general → specific/episodic/mechanistic/evidential | low resolution | PROMOTION_CANDIDATE |
| QI-C02 | Second-Question State Routing | answer → information gap → next move | every answer | PROMOTION_CANDIDATE |
| QI-C03 | Prepared Spine / Adaptive Branch | fixed coverage + bounded adaptation | live state | PROMOTION_CANDIDATE |
| QI-C04 | Descriptive-Before-Explanatory | explanation-first → lived event/detail first | abstract account | PROMOTION_CANDIDATE |
| QI-C05 | Interpret-and-Return | system inference → Guest confirmation/correction | interpretation formed | PROMOTION_CANDIDATE |
| QI-C06 | Contradiction Repair | discrepancy → reconciliation/chronology | conflicting evidence | PROMOTION_CANDIDATE |
| QI-C07 | Breadth / What-Else Expansion | visible answer → missing dimensions | completeness deficit | PROMOTION_CANDIDATE |
| QI-C08 | Requirement-Led Lead Tracking | question sequence → unresolved requirement set | missing coverage | PROMOTION_CANDIDATE |
| QI-C09 | Research-to-Discrepancy | external evidence → expected state → compare | prepared discrepancy | PROMOTION_CANDIDATE |
| QI-C10 | Social / Contextual Reconstruction | individual account → social/system context | contextual gap | PROMOTION_CANDIDATE |
| QI-C11 | Premortem / Future-Failure | current belief → failure conditions | forward-risk gap | RESEARCH_MORE |
| QI-C12 | Past-Self Contrast | present stance → historical transformation | transformation hypothesis | PROMOTION_CANDIDATE |
| QI-C13 | Strategic Silence | verbal prompt → space for retrieval | reflective opportunity | RESEARCH_MORE / interaction operator |
| QI-C14 | Self-Generated Standard | answer → Guest's own evaluation criteria | normative ambiguity | RESEARCH_MORE |
| QI-C15 | Social Reference Reconstruction | stance → surrounding actors/authority | social field gap | RESEARCH_MORE |

## 3. Dimensions that must not be collapsed prematurely

These should remain explicitly distinguished even if implemented as fields rather than objects:

- question target resolution;
- answer resolution;
- information completeness;
- inquiry state transition;
- evidence mode;
- temporal orientation;
- social reference frame;
- interactional fit;
- epistemic posture;
- downstream composition compatibility.

## 4. Proposed state vocabulary

### Answer resolution
`abstract | general | specific | episodic | mechanistic | evidential`

### Information completeness
`unknown | partial | sufficient | verified | exhausted`

### Inquiry state transition
`stabilize | switch | expand | clarify | redistribute_agency | close`

### Evidence mode
`fact | story | feeling | interpretation | forecast | alternative | counterfactual`

### Temporal orientation
`past_reconstruction | present_observation | future_projection | counterfactual | premortem | historical_uncertainty`

### Social reference frame
`self | peer | authority | group | institution | audience`

These are **proposed derived/runtime dimensions**, not new canonical objects.

## 5. Cross-book merge principle

Do not create separate primitives simply because different sources use different names. Promote only after identifying a stable mechanism boundary. Example: single-target questioning, specifying probes, and specificity escalation may collapse into an Answer Resolution controller with parameterized forms.

## 6. Format/archetype integration

Question Intelligence is part of semantic/syntax intelligence, not an isolated information-extraction layer.

Required relation:

`active audience cognitive state + guest territory + world signal + edge + format/archetype intent`
`→ collision hypothesis`
`→ evidence requirement`
`→ question objective`
`→ primitive coalition`
`→ Question IR`
`→ semantic acquisition`

The same answer should not be forced into an archetype simply because the system preselected it; compatibility constrains acquisition and interpretation but cannot override evidence reality.

## 7. Promotion rule

No item in this synthesis is a canonical Question Primitive until a later promotion decision records:

- stable boundary;
- source lineage;
- distinctiveness from existing primitives;
- input/trigger conditions;
- transformation/response shape;
- downstream compatibility;
- failure modes;
- evidence of usefulness;
- canonical owner;
- versioning and conflict rules.
