# Stage 1 Regression Cases

Required test manifest referenced by `SKILL.md` §1 and §12. Every case here must have an automated test before Stage 1 is considered built. Case 1 is not hypothetical — it's a confirmed defect in the legacy corpus.

---

### Case 1 — primitive-type leakage into slide_role (CONFIRMED, already occurred)

```text
given:
    slide_role = "flow_diagram"
    # flow_diagram is canonical under primitive_type, not under slide_role —
    # see contracts/taxonomy_bindings.json

expected:
    technical_status = FAIL
    error_code = ROLE_PRIMITIVE_TYPE_MISMATCH
```

Real evidence: `CAR-JUX-Congofash-4-5-12_VISUAL_SYNTAX_ANALYSIS.json` and `CAR-LST-Viralpost-3-4-8_VISUAL_SYNTAX_ANALYSIS.json` in the legacy corpus both have this exact defect. Use these two files as literal fixtures for this test, not synthetic data.

### Case 2 — novel role must be allowed

```text
given:
    a specimen whose visual structure doesn't match any entry in the
    slide_role registry, with sufficient observation evidence

expected:
    technical_status = REVIEW
    taxonomy_state = NOVEL_CANDIDATE
    NOT an error, NOT forced into an existing canonical role
```

### Case 3 — novel candidate must not silently become canonical

```text
given:
    a NOVEL_CANDIDATE from a prior harness run

expected:
    subsequent harnesses referencing the same visual pattern still resolve
    to NOVEL_CANDIDATE, not CANONICAL, until an explicit taxonomy-registry
    update event (outside Stage 1 execution) promotes it
```

### Case 4 — duplicate counts must agree with canonical syntax identity

```text
given:
    two slide analyses with the same syntax_hash

expected:
    they are reported as one entry in deduplication_summary
    (not two entries with matching layout_fingerprint prose but
    different syntax_hash — that must NOT collapse)
```

### Case 5 — zone/primitive incompatibility

```text
given:
    a primitive claimed to occupy a zone not in its allowed zone set
    per contracts/taxonomy_bindings.json

expected:
    technical_status = FAIL
    error_code = ZONE_PRIMITIVE_INCOMPATIBLE
```

### Case 6 — anchor claims require evidence

```text
given:
    a claimed persistent anchor with no evidence_refs

expected:
    technical_status = REVIEW or FAIL
    error_code = UNSUPPORTED_ANCHOR_CLAIM
```

### Case 7 — unsupported visual claims must not silently pass

```text
given:
    an inference with no evidence_refs resolving to any observation object

expected:
    technical_status != PASS
```

### Case 8 — valid taxonomy extension must remain possible end-to-end

```text
given:
    a well-evidenced NOVEL_CANDIDATE

expected:
    the harness can still reach technical_status = REVIEW,
    and can still reach STAGE1_COMPLETE on operator APPROVE
    (this is the check that Case 2's outcome isn't a dead end —
    see SKILL.md §8, the REVIEW+APPROVE path must work)
```

### Case 9 — structurally valid JSON with inadequate evidence must fail the evidence gate

```text
given:
    syntactically valid output where every field is present but
    evidence_refs are empty or don't resolve to real observation objects

expected:
    technical_status = FAIL
    error_code = INSUFFICIENT_EVIDENCE
```

### Case 10 — STAGE1_COMPLETE requires both gates, and neither alone is sufficient

```text
given A: technical_status = PASS,   operator_disposition = HOLD
given B: technical_status = BLOCKED, operator_disposition = APPROVE
given C: technical_status = FAIL,    operator_disposition = APPROVE
given D: technical_status = REVIEW,  operator_disposition = APPROVE
given E: technical_status = PASS,    operator_disposition = APPROVE

expected:
    A → NOT STAGE1_COMPLETE (no operator approval)
    B → NOT STAGE1_COMPLETE (technical block cannot be bypassed by approval)
    C → NOT STAGE1_COMPLETE (technical fail cannot be bypassed by approval)
    D → STAGE1_COMPLETE (REVIEW is a legitimate, approvable outcome — SKILL.md §8)
    E → STAGE1_COMPLETE
```

### Case 11 — data-integrity mismatch must surface, not silently pass

```text
given:
    source_zip_sha256_recorded != source_zip_sha256_observed_now

expected:
    technical_status = BLOCKED
    error_code = SOURCE_INTEGRITY_MISMATCH
    (this is a technical block per SKILL.md §3 — it says nothing about
    whether the source is licensed or usable, only that this specific
    execution can't be certified against the recorded input identity)
```

### Case 12 — undocumented pipeline deviation must be flagged, not absorbed

```text
given:
    vision_model_used or base_url differs from the documented default
    pipeline for this Skill

expected:
    deviation_from_documented_pipeline = true
    surfaced explicitly in the contract report
    (informational — does not by itself set technical_status = FAIL)
```
