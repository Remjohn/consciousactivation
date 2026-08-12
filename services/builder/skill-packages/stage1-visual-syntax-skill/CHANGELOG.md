# Changelog

## v1 — legacy pipeline (pre-audit)
`tools/harness_vision_analyst.py`, prose-governed, batch-oriented. Produced 49 JSON files. No enforcement mechanism beyond "does the JSON parse." Audited and found to contain: a confirmed primitive/role taxonomy leak (`flow_diagram`), 7 files with a source hash that no longer matches the recorded value, 24 files with no matching source zip in the delivered export, 4 files silently produced by an undocumented alternate tool/model, and a completion summary that inaccurately claimed no manifest work existed yet.

## v2 — first rebuild mandate
Introduced: the operator-authority principle (no automated licensing/exclusion logic — that decision belongs to the human operator, made by selection); observation/interpretation separation; taxonomy discovery with explicit candidate states; deterministic dedup via syntax identity instead of prose fingerprints; semantic + evidence validators; data-integrity receipt (sha256 + tool disclosure) as a technical, non-licensing check; one-harness-at-a-time execution via operator-issued calls, replacing the idea of a second-model "independent evaluator."

## v3 — this version
Incorporated external review, adopted 4 of 5 proposed refinements and modified the 5th:

1. **Source-integrity mismatch now sets technical_status = BLOCKED**, not merely informational — framed strictly as "this execution can't be certified against the recorded input identity," never as a usability/licensing judgment. (`invariants.json`: `SOURCE_INTEGRITY_MISMATCH`)
2. **`STAGE1_COMPLETE` is now a derived, enforced field** requiring `operator_disposition == APPROVE AND technical_status IN [PASS, REVIEW]` — codified directly in `operator_review.schema.json` and `receipt.schema.json`, not left as prose. **Modified from the external proposal**: `REVIEW` remains approvable, because a `REVIEW` status is the expected shape of a well-evidenced novel taxonomy candidate (v2 §21/v3 SKILL.md §10) — only `BLOCKED`/`FAIL` are hard-blocked from completion regardless of operator input. Making `REVIEW` unapprovable would have made every novel-candidate discovery a dead end, contradicting the document's own stated goal of letting specimens teach the taxonomy.
3. **No hardcoded subjective evidence thresholds** (e.g. a fixed "3 specimens minimum") unless grounded in an existing repository contract — stated explicitly in `SKILL.md` §7 and reflected in `invariants.json`'s evidence rules, which check presence/resolvability, not counts.
4. **Renamed "independent evaluation" to "operator-controlled certification boundary"** throughout — `SKILL.md` §9. More accurate: the mechanism is governance via mandatory per-harness review, not statistical independence from a second model.
5. **Added the explicit boundary**: "Python validates the representation, not the visual truth of the representation" — `SKILL.md` §7, closing note.

Also restructured the entire document from a single prose file into an actual Skill package (`SKILL.md` + `contracts/*.schema.json` + `state_machine.md` + `prompt_snippet_template.md` + `tests/regression_cases.md`) so the rules live in one enforceable place and the per-harness invocation (the Prompt Snippet) stays thin and never duplicates them.
