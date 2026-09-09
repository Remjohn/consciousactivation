applies to: one Harness, one run. Re-run this prompt per harness. Do not batch.

---

INPUT: a single folder/zip of raw reference material for ONE harness (e.g. `supervisuals/TWQ-IMG-Portrait/`, `carousels/CAR-LST-Cultbrand-3-4-11/`, `format01_story_video/`).

OUTPUT: one file, `manifest.json`, ready for `cmf-builder ingest`. Nothing else is required to proceed to build.

---

## Do this, in order

1. **Classify.** Which of the 5 canonical categories does this belong to? Only these five are valid — do not invent a sixth:
   `short_form_edited_video` | `2d_character_animation` | `carousels` | `supervisuals` | `conversational_activation_expression`
   If ambiguous, stop and ask. Do not guess.

2. **Look at every file in the folder.** Note what it actually is (images, slide sequence, scene template JSON, video). This is context for step 3, not something that gets zipped into the ingest input — the CLI takes one JSON manifest, not raw media.

3. **Fill the manifest below.** Two different bars apply to different fields — do not blur them:

   - **`task.*` and 6 of the 7 `activative_input` refs** (`source_premise_ref`, `identity_dna_ref`, `context_premise_ref`, `resonance_map_ref`, `matrix_of_edging_ref`, `activative_intelligence_pack_ref`, `evaluation_contract_ref`, `evidence_provenance_refs`) — these are **attestation, not live content**. Nothing downstream ever reads them again after Builder validates them. They still must be real, not fabricated — point at real reference material or ask what they should point to — but don't agonize over making them bespoke to a hypothetical future client. They just need to honestly represent this format.
   - **`activative_input.wrong_reading_locks`** — this is the one field with a confirmed live effect on real campaign execution. Give this the real thinking time: what's the specific wrong interpretation this format's visual/narrative language could produce, that this harness must lock out? Non-empty, non-generic, format-specific.

4. **Leave `task.capability_requirements: []`.** Non-empty values here will fail at campaign-creation time today (unresolved gate, not this harness's problem to solve).

5. **Stop. Report back before running the CLI.** State: category, what's real vs. what you had to ask about, and your `wrong_reading_locks` reasoning in one line. Wait for a go-ahead on this one harness before building it, and before starting the next one.

---

## The manifest

```jsonc
{
  "manifest_id": "operator-manifest-<slug>",
  "manifest_version": "1.0.0",
  "task_id": "<task_slug>_v1",
  "mode": "activative",
  "category_id": "<one of the 5 above>",
  "task": {
    "goal": "...",
    "success_condition": "...",
    "atomic_boundary": "...",
    "input_contract": { "type": "object", "required": [...], "properties": {...} },
    "output_contract": { "type": "object", "required": [...], "properties": {...} },
    "required_context": [...],
    "capability_requirements": [],
    "acceptance_tests": [...],
    "authority_ref": "<authority-doc>@<version>#sha256:<hash>",
    "provenance_refs": ["<provenance-ref>@<version>#sha256:<hash>"]
  },
  "activative_input": {
    "source_premise_ref": "...",
    "identity_dna_ref": "...",
    "context_premise_ref": "...",
    "resonance_map_ref": "...",
    "matrix_of_edging_ref": "...",
    "activative_intelligence_pack_ref": "...",
    "evaluation_contract_ref": "...",
    "evidence_provenance_refs": ["<evidence-ref>@<version>#sha256:<hash>"],
    "hidden_pressure": "...",
    "activation_directions": [...],
    "roles": [...],
    "stance": "...",
    "stakes": [...],
    "identity_urges": [...],
    "participation_design": "...",
    "intended_reaction": "...",
    "smallest_useful_commitment": "...",
    "wrong_reading_locks": ["<real, format-specific, non-empty>"]
  }
}
```

Reference working example: `services/builder/tests/fixtures/productization/manifests/activative_expression.json`.

---

## After go-ahead: build this one harness

```bash
cd services/builder
python -m cmf_builder.cli ingest path/to/manifest.json      # → artifact_id
python -m cmf_builder.cli build --artifact-id <artifact_id>
python -m cmf_builder.cli inspect --artifact-id <artifact_id>   # sanity check before export
python -m cmf_builder.cli export --artifact-id <artifact_id> --output /tmp/<definition_id>.zip
cp /tmp/<definition_id>.zip "${CA_HARNESS_LIBRARY_ROOT:-$CA_DATA_ROOT/harness-library}/"
```

Verify: `curl -s localhost:8000/api/harnesses | jq '.[] | {definition_id, category_id, production_ready}'`
`production_ready: false` is correct and expected — not a bug.

Report result. Only then move to the next harness.
