# Wrong-Reading Locks — Visual Syntax Reconstruction Analyst

## Skill Self-Governance Locks

1. **Do Not Judge Licensing:** This Skill must never contain logic that
   evaluates whether a harness's source media is licensed, cleared, or
   provenance-complete. Harness selection by the operator is the only
   admission event this system recognizes. If an unrelated artifact
   elsewhere claims exclusion/admission authority over harnesses, this
   Skill does not consult it, does not block on it, and records its
   existence in `fyi` at most.

2. **Do Not Cross Registries:** A `primitive_type` value must never satisfy
   a `slide_role` field, and a `slide_role` value must never satisfy a
   `primitive_type` field. These are separate canonical lists, checked
   independently.

3. **Do Not Force Novel Structures Into Existing Categories:** A specimen
   that doesn't match the canonical taxonomy becomes a documented
   `NOVEL_CANDIDATE`, never a mis-forced canonical match.

4. **Do Not Silently Promote Candidates:** A `NOVEL_CANDIDATE` state must
   never be rewritten to `CANONICAL` within this Skill's execution.
   Promotion is a separate, explicit, out-of-band event.

5. **Do Not Trust Prose Fingerprints:** Deduplication decisions must be
   based on `syntax_hash`, never on `layout_fingerprint` text similarity.

6. **Do Not Manufacture Evidence:** Every inference must carry
   `evidence_refs` resolving to real observation objects. An unsupported
   claim is invalid, not merely lower-confidence.

7. **Do Not Hardcode Subjective Thresholds:** Evidence sufficiency checks
   presence and resolvability of references, not an invented minimum count,
   unless that count is grounded in an existing contract outside this Skill.

8. **Do Not Batch:** This Skill processes exactly one harness per
   invocation and stops after the contract report, regardless of outcome.

9. **Do Not Self-Certify:** This Skill never sets `stage1_complete: true`.
   That field is only ever set true downstream, after an operator records
   `APPROVE` against a technical status that is not `BLOCKED` or `FAIL`.
