# CAE Object Constitution Author Skill

**Skill ID:** `cae_object_constitution_author`  
**Maturity:** `development_uncertified`  
**Authority:** Procedural control only; operates under Definition Grammar Bundle and Phase 0 Object Constitution Protocol.  

---

## 1. Purpose & Lane

The `cae_object_constitution_author` provides a structured procedure for drafting an Object Constitution for a candidate CAE artifact that has already passed scope and authority mapping.

It enforces the fundamental constitutional laws:
1. **Meta-Law:** Role and class MUST be established before schema convenience.
2. **Single Primary Class:** Every object belongs to exactly one primary artifact class from the 18-class matrix.
3. **26 Constitutional Dimensions:** All 26 dimensions MUST be explicitly addressed and classified as `APPLICABLE`, `INAPPLICABLE_WITH_REASON`, or `PENDING_WITH_BLOCKER`.
4. **No Synthetic Evidence:** Missing facts or unverified behaviors must remain `PENDING_WITH_BLOCKER`; placeholder prose is strictly forbidden.

---

## 2. Inputs & Preconditions

- Input MUST conform to `input_schema.yaml`.
- Requires validated Scope & Authority Mapping output (`cae_scope_authority_mapper`).
- Requires candidate identity, primary class selection, and class-specific grammar inputs.

---

## 3. Procedure

1. **Verify Scope & Authority Prerequisite:** Ensure the candidate object has a validated mapping from `cae_scope_authority_mapper`.
2. **Route to Class-Specific Grammar:** Select exactly one primary artifact class from the 18 allowed classes (Entity, Value Object, Relation, State, Event, Immutable Evidence, Canonical Ontology, Structural Grammar, Operator/Primitive, Policy/Contract, Derived Semantic Artifact, Execution Packet, Adversarial Evaluation Asset, Receipt/Evaluation Record, Crosswalk/Mapping Object, Longitudinal Memory Record, Intermediate Representation, Experience/Perceptual Function).
3. **Author 26 Dimensions in Sequence:**
   - I. Canonical Identity
   - II. Artifact Class
   - III. Ontological Plane
   - IV. Architectural Role
   - V. Definition (using class-specific grammar)
   - VI. Semantic Boundary
   - VII. Nearest Neighbors
   - VIII. Taxonomic Position
   - IX. Lifecycle / Canonicity
   - X. Attributes
   - XI. Relationships
   - XII. State Model
   - XIII. Events
   - XIV. Provenance
   - XV. Invariants
   - XVI. Authority / Owner
   - XVII. Authorized Operations
   - XVIII. Prohibited Operations
   - XIX. Validators
   - XX. Error Taxonomy
   - XXI. Storage Representation
   - XXII. Runtime Consumers
   - XXIII. Questions This Object Answers
   - XXIV. Examples (at least one positive)
   - XXV. Hard Negatives (at least one nearest-neighbor contrast)
   - XXVI. Version History
4. **Classify Every Dimension:** Assign dimension status (`APPLICABLE`, `INAPPLICABLE_WITH_REASON`, or `PENDING_WITH_BLOCKER`).
5. **Enforce Negative Constraints:** Confirm prohibited operations, aliases, and near-neighbor contrasts are unambiguous.
6. **Emit Constitution & Receipt:** Produce markdown artifact and execution receipt conforming to schemas.

---

## 4. Prohibitions

- MUST NOT assign an artifact class based on database table or JSON schema convenience.
- MUST NOT fill an inapplicable dimension with generic filler prose.
- MUST NOT fabricate evidence or claim unverified runtime truth.
- MUST NOT create SQL schemas, migrations, or runtime code.

---

## 5. Escalation & Stop Conditions

- **Stop as `REJECTED_AMBIGUOUS_CLASS`:** If the artifact attempts to combine multiple primary classes into one un-split object.
- **Stop as `PENDING_BLOCKED`:** If essential brownfield lineage or definition grammar cannot be resolved.
