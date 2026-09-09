# CAE Phase Validation Protocol v2.0

**Status:** Mandatory governance protocol
**Scope:** CAE Phases 0–7

## 1. Purpose

The CAE Phase Validation Protocol prevents architectural documents from being treated as implementation truth merely because they are conceptually coherent.

Each phase is evaluated across five independent dimensions:

- Architectural Fidelity
- Brownfield Fidelity
- Ontological Fidelity
- Implementation Readiness
- Verification Readiness
- Reality-Contact Readiness
- Reward-Hacking Resistance
- Taste / Anti-Centroid Integrity

A phase may be accepted architecturally while remaining unready for implementation. A phase may also have passing documentation and fixture checks while remaining unproven against the environment, reward-hacking, or taste claims it makes.

## 2. Evidence classes

Every important claim MUST be classified as exactly one primary evidence status:

| Status | Meaning |
|---|---|
| `VERIFIED` | Confirmed directly by current repository/code/schema/test evidence. |
| `INHERITED` | Supplied by a canonical predecessor artifact/registry and preserved intentionally. |
| `RATIFIED` | Deliberately approved architectural doctrine. |
| `PROPOSED` | Intended design, not yet validated against implementation. |
| `INFERRED` | Reasoned from evidence but not directly observed. |
| `MISSING` | Required information is absent. |
| `CONTRADICTED` | Reliable sources disagree and no resolution exists. |
| `DEPRECATED` | Formerly valid but explicitly superseded. |
| `HYPOTHESIS` | Scientific/theoretical claim used provisionally without sufficient evidence. |

No `PROPOSED`, `INFERRED`, or `HYPOTHESIS` statement may silently be promoted to `VERIFIED`.

## 3. Validation dimensions

### 3.1 Architectural fidelity

Questions:

- Does the phase preserve the ratified CAE causal chain?
- Does it preserve World → Context/State → SDA → Edging → Interview → Evidence → Primitive → Coalition → Edge → Archetype/SFL → Composition → IR → Runtime → Outcome?
- Does it preserve the Meaning / Experience separation where applicable?
- Does it preserve the role-before-schema rule?

### 3.2 Brownfield fidelity

Questions:

- Which objects already exist in code?
- Which exist only in YAML registries?
- Which exist only in docs?
- Which are duplicated under different names?
- Which relations are absent?
- Which state transitions are absent?
- Which runtime consumers are absent?
- Which validators are absent?

### 3.3 Ontological fidelity

Every object MUST have:

- architectural class
- ontological plane
- role
- semantic boundary
- nearest neighbors
- lifecycle/canonicity
- owner

The object constitution must be internally consistent with its class-specific definition grammar.

### 3.4 Implementation readiness

A phase is implementation-ready only if its requirements resolve into:

- typed schemas;
- relationship constraints;
- state transitions;
- events;
- authorized operations;
- validators;
- error taxonomy;
- storage representation;
- runtime consumers;
- acceptance criteria.

### 3.5 Verification readiness

Each requirement MUST have a verification path:

```text
Claim → Evidence → Contract → Test → Receipt
```

### 3.6 Reality-contact readiness

Each material requirement MUST declare its minimum environment fidelity:

`E0_SYNTHETIC`, `E1_REALISTIC_FIXTURE`, `E2_REPOSITORY_INTEGRATED`, `E3_PRODUCTION_SHAPED`, or `E4_REAL_WORLD_OBSERVED`.

The evidence level MUST be sufficient for the claim. A test running at E0 cannot prove an E4 human-response claim.

### 3.7 Reward-hacking resistance

Each material evaluator MUST have at least one false-proof or proxy-gaming case. The validation record MUST answer:

- what proxy is measured;
- what the intended property is;
- how an optimizing implementation could game the proxy;
- what counter-test would expose the gaming.

### 3.8 Taste / anti-centroid integrity

For claims involving human quality, meaning, expression, or perceptual force, phase validation MUST include contrastive evidence for generic/centroid failure. Structural validity alone is insufficient.

Taste validation MUST remain architecture-specific and MUST preserve Matrix of Edging, SDA, SFL, authenticated evidence, and anti-centroid law.

## 4. Phase evidence matrix

For every phase, create a table with these fields:

| Requirement / Claim | Source | Evidence Status | Existing Implementation | Canonical Registry | Minimum Fidelity | Reward-Hack Test | Taste/Reality Test | Gap | Contradiction | Verification | Decision |
|---|---|---|---|---|---|---|---|---|

`Decision` MUST be one of:

- `ADOPT`
- `ADOPT_WITH_MIGRATION`
- `REVISE`
- `DEFER`
- `REJECT`
- `QUARANTINE_PENDING_EVIDENCE`

## 5. Object-level reconciliation

Every object referenced by a phase MUST be reconciled against the repository and registries.

Minimum fields:

```yaml
object_id:
canonical_name:
architectural_class:
ontological_plane:
phase_claim:
evidence_status:
exists_in_code:
exists_in_db:
exists_in_registry:
exists_in_docs:
existing_ids: []
owner:
existing_schema:
existing_relations: []
existing_states: []
existing_events: []
runtime_consumers: []
validators: []
migration_required:
open_questions: []
resolution:
```

## 6. Registry reconciliation

Inherited registries are not redesign targets during phase validation.

For SDA/SFL/Primitive registries:

- preserve original IDs;
- preserve version numbers;
- preserve source lineage;
- preserve crosswalk rationale;
- record integrity gaps separately;
- do not invent missing records merely to make references pass.

A registry integrity gap becomes an explicit migration requirement.

## 7. Acceptance thresholds

A phase may be marked:

### `ARCHITECTURALLY RATIFIED`
When architectural fidelity is high and unresolved issues are explicitly recorded.

### `BROWNFIELD VALIDATED`
When all major claims have evidence status and all referenced inherited assets have been reconciled.

### `IMPLEMENTATION READY`
Only when Functional Requirements and Tech-Spec contracts exist and verification paths are defined.

No phase may skip directly from `ARCHITECTURALLY RATIFIED` to `IMPLEMENTATION READY`.

## 8. Required output

Each Phase Validation report MUST produce:

1. phase evidence matrix;
2. object reconciliation matrix;
3. relation/state gap matrix;
4. registry reconciliation result;
5. contradiction log;
6. implementation gap inventory;
7. FR candidates;
8. spec candidates;
9. unresolved architectural decisions;
10. final phase status.

## 9. Fatal validation conditions

The phase MUST NOT be promoted if any of the following exist without explicit quarantine:

- hallucinated registry IDs;
- an object with ambiguous ontological class;
- implementation requirement with no source/evidence;
- stateful behavior represented as a mutable static field with no history model;
- canonical data proposed to overwrite immutable evidence;
- existing service duplicated without an explicit replacement decision;
- validator required by architecture but absent from implementation or test plan;
- a requirement whose success cannot be objectively verified;
- a human-quality claim with no taste/reality-contact evidence;
- a material evaluator with no identified reward-hacking scenario;
- a production claim supported only by synthetic fixtures.
