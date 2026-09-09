---
name: harness-gap-analysis-and-build
description: "Use this skill when the operator wants to know which Harnesses are missing from the Conscious Activations Harness Library, or wants to author new Harnesses from reference material into that library. Triggers include: 'which harnesses are we missing', 'build the harness for X', 'here's the reference zip for our harnesses', 'populate the harness library', or any request to add to CA_HARNESS_LIBRARY_ROOT. Do NOT use this for running campaigns, VAE work, or Studio work — those are separate subsystems. This skill only covers Builder-side harness authoring: gap analysis against the canonical category registry, and driving the real `cmf-builder` CLI (ingest → build → export) to produce library-ready packages. It does not touch Pipeline's campaign-creation code path or Blocker 5/Blocker 2 — those are a separate, later gate, and this skill explicitly does not require them resolved."
---

# Harness Gap Analysis & Build

## What this skill is for

The Conscious Activations Harness Library (`CA_HARNESS_LIBRARY_ROOT`, defaults to `{CA_DATA_ROOT}/harness-library`) is currently empty. Harnesses are the job templates a campaign selects at creation time (`api/routers/campaigns.py::create_campaign` calls `find_by_definition_id(library_root, body.harness_definition_id)`). This skill governs two jobs:

1. **Gap analysis** — figure out which Harnesses should exist but don't, against the canonical category registry and whatever reference material the operator provides.
2. **Build** — turn operator-supplied reference material into real, valid `PortableAtomicHarnessDefinition` packages in the library, using the real Builder CLI — not a hand-rolled script, and not a guess at the format.

**Important, verified fact this skill relies on:** authoring a Harness (this skill's job) is architecturally independent of Blocker 5 and the related capability_metadata gap (see `docs/PRD/CURRENT.md` §1.7, §1.10#1, §1.14). Those gates fire only inside `compile_portable_to_intake()`, which runs at *campaign-creation* time, not at Harness-authoring time. You can — and should — proceed with this skill regardless of whether Blocker 5 is resolved yet. What you build now will sit in the library correctly; it just won't be selectable into a *running* campaign until that separate gate closes.

**Before doing anything else, re-verify the facts in this skill against the live repo.** This document was written against a specific commit; file layouts, the CLI's argument surface, and the canonical category list can all have moved since. Specifically re-check:
- `services/builder/src/cmf_builder/domain/category_binding.py` — the canonical category list (`_CATEGORIES`)
- `services/builder/src/cmf_builder/cli/{parser.py,commands.py}` — the CLI's exact verbs and arguments
- `services/builder/src/cmf_builder/domain/portable_export.py` — the exported definition's required fields
- `api/routers/harnesses.py` — the library's on-disk format (what the API actually scans for)

If any of these have changed, trust the code over this skill and update this file afterward.

---

## Step 1 — Gap analysis

### 1a. Get the canonical category list

As of this writing, `CanonicalCategoryRegistry` (`category_binding.py`) hardcodes exactly five categories:

| category_id | canonical_name |
|---|---|
| `short_form_edited_video` | Short-Form Edited Video |
| `2d_character_animation` | 2D Character Animation |
| `carousels` | Carousels |
| `supervisuals` | Supervisuals |
| `conversational_activation_expression` | Conversational Activation / Human Expression |

Every **activative**-mode Harness binds to exactly one of these (`CategoryBinding.create()` rejects anything else, or more than one). A **generic** Harness (non-Activative, `mode: "generic"`) binds to none — it's the escape hatch for category-neutral tasks and is not what real content-production Harnesses should use; per doctrine (§1.2 of `CURRENT.md`), production Harnesses should be `activative`.

### 1b. Enumerate what's already in the library

```bash
ls "${CA_HARNESS_LIBRARY_ROOT:-$CA_DATA_ROOT/harness-library}"/*.zip 2>/dev/null
```
For each `.zip`, extract `atomic_harness_definition.json` and read `definition.category_binding.category_id` to see which category it covers. (Or just call `GET /api/harnesses` if the API is running — it returns this already, see `HarnessSummary` in `api/routers/harnesses.py`.)

### 1c. Cross-reference against the operator's reference material

**Corrected 2026-08-01, tenth pass — read this before Step 2, it changes what you're actually authoring.** `activative_input`'s 7 refs (`identity_dna_ref` through `source_premise_ref`) are validated once by Builder at export time and then never read again by any live code — `services/pipeline/.../intake/harness_compiler.py::compile_portable_to_intake()` (the real bridge from a built Harness into a runnable campaign) never touches them. **They are harness-level attestation and lineage evidence — proof the harness was designed against real, non-fabricated reference material — not live per-campaign semantic content.** The one exception is `wrong_reading_locks`, which does survive into real execution (traced through `category_binding.py::CategoryBinding.create()` into `category_binding["wrong_reading_locks"]`, which the compile step forwards). Real per-campaign content (Identity DNA, Resonance Map, etc. for a specific client) is meant to arrive later, at campaign-creation time, as a separate `semantic_dependencies` parameter — which nothing in the live system currently produces (a genuine, separate open gap, not this skill's job to fill). Don't let that gap change what you author here: the 7 refs still must be real, not fabricated, to pass Builder's `validate()` — they just don't need to anticipate any specific future client, since nothing downstream reads them as if they did.

For each item in the operator's reference zip, determine:
- Which of the 5 canonical categories it belongs to (ask the operator if it's ambiguous — don't guess at doctrine-sensitive classification).
- Whether a category_id already has a library entry. **Note:** nothing currently stops two harnesses from sharing a category_id (they'd differ by `manifest_id`/`format_profile` or similar) — check whether the operator's model is "one harness per category" or "many harnesses per category, keyed by format/derivative type" before treating "category already covered" as "done." If unsure, ask.
- Whether the reference material contains everything `Step 2` needs to build a valid manifest. If not, list precisely what's missing and ask the operator rather than fabricating placeholder values — an invented `wrong_reading_locks` defeats the one part of this system that actually matters at runtime; an invented identity/context ref defeats Builder's governance gate even though nothing downstream reads it, which is arguably worse, since a false attestation is worse than a merely-unused one.

**Output of this step:** a table — category_id, harness(es) wanted, harness(es) present, harness(es) to build this pass, and what reference material is or isn't sufficient for each. Report this back before building anything.

---

## Step 2 — Build one pilot harness first

Do not batch-author everything in one pass. Build **one** Harness end to end, verify it, then proceed to the rest. This catches format/environment problems (missing `ffmpeg`, wrong Python env, a category-binding validation error) once instead of N times, and gives the operator a real artifact to sanity-check before the rest are produced.

### 2a. Construct the operator manifest

This is the real, verified schema (mirrors `services/builder/tests/fixtures/productization/manifests/activative_expression.json` exactly — read that file for a complete working example before writing a new one):

```jsonc
{
  "manifest_id": "operator-manifest-<slug>",
  "manifest_version": "1.0.0",
  "task_id": "<task_slug>_v1",
  "mode": "activative",
  "category_id": "<one of the 5 canonical category_ids>",
  "task": {
    "goal": "...",
    "success_condition": "...",
    "atomic_boundary": "...",
    "input_contract": { "type": "object", "required": [...], "properties": {...} },
    "output_contract": { "type": "object", "required": [...], "properties": {...} },
    "required_context": [...],
    "capability_requirements": [ /* see caveat below — [] is safest for now */ ],
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
    "hidden_pressure": "...",
    "activation_directions": [...],
    "roles": [...],
    "stance": "...",
    "stakes": [...],
    "identity_urges": [...],
    "participation_design": "...",
    "intended_reaction": "...",
    "smallest_useful_commitment": "...",
    "evidence_provenance_refs": ["<evidence-ref>@<version>#sha256:<hash>"],
    "evaluation_contract_ref": "...",
    "wrong_reading_locks": ["<at least one — required, cannot be empty>"]
  }
}
```

**Hard requirements, verified against `category_binding.py` — the build will reject the manifest without these:**
- All seven `activative_input` ref fields (`source_premise_ref` through `evaluation_contract_ref`) must be present and non-empty strings.
- `activative_input.evidence_provenance_refs` must be a non-empty list of strings (combined with the 7 refs above, this is where the exported definition's "≥8 semantic lineage refs" requirement comes from — 7 + at least 1 provenance ref).
- `activative_input.wrong_reading_locks` must be a non-empty list.
- `category_id` must be exactly one of the 5 canonical IDs.

**Caveat on `task.capability_requirements`:** leave this `[]` for now unless the operator specifically wants to test the campaign-creation path today. Any non-empty value here will make this Harness fail at *campaign-creation* time (Blocker 2 — `capability_metadata` is hardcoded to `{}` in `api/routers/campaigns.py`, see `CURRENT.md` §1.7/§1.10#1) with a currently-mislabeled error. That doesn't block *authoring* — it only matters once someone tries to run a campaign against this Harness before workstream 1-C lands.

Where do real refs (`identity_dna_ref`, `matrix_of_edging_ref`, etc.) come from? They should point at real upstream artifacts (Identity DNA, Resonance Map, etc. per the doctrine chain in `CURRENT.md` §1.2) if the operator has them, or the operator's reference zip should specify what these should be. Do not invent hashes or content for these — ask if they're not in the reference material.

**Corrected 2026-08-01, tenth pass — what these refs are actually for.** Traced `intake/harness_compiler.py::compile_portable_to_intake()` (the real, working bridge from a built Harness into a runnable campaign) in full: it reads `category_id`, `profile_id`, `production_ready`, `certified`, and `wrong_reading_locks` from the built Harness — **it never reads any of the other six `activative_input` refs.** They exist purely to satisfy Builder's own governance gate (proof the harness was designed against real reference material, not fabricated) — not as content a running campaign will later consult. Real per-campaign content for a specific client is a separate thing entirely (a `semantic_dependencies` parameter, supplied fresh at campaign-creation time — nothing in the live system currently produces this, a genuine open gap unrelated to harness authoring). Practically: still don't fabricate these six refs — a false attestation is worse than an honest placeholder — but don't over-invest in making them client-specific or perfectly bespoke either, since nothing reads them that way. `wrong_reading_locks` is different: it's the one field of the eight with a confirmed live effect on real campaign execution, and deserves real, format-specific care.

### 2b. Run the CLI

```bash
cd services/builder
python -m cmf_builder.cli ingest path/to/manifest.json
# → returns an artifact_id (JSON output: --format json)

python -m cmf_builder.cli build --artifact-id <artifact_id>

python -m cmf_builder.cli inspect --artifact-id <artifact_id>
# → sanity-check the compiled content before exporting

python -m cmf_builder.cli export --artifact-id <artifact_id> --output /tmp/<definition_id>.zip
```
(Re-verify the exact invocation — `services/builder/src/cmf_builder/cli/__main__.py` reads `CMF_BUILDER_DB` for its local SQLite store; confirm what bootstraps `ProductizationApplicationService` in `cli/bootstrap.py` before assuming this exact command line, especially whether it needs to run from a particular working directory or virtualenv.)

### 2c. Verify and install into the library

The exported zip's internal filename for the definition must be `atomic_harness_definition.json` (see `DEFINITION_ENTRY` in `api/routers/harnesses.py`), and the zip itself should be named `{definition_id}.zip` when placed in the library (see `find_by_definition_id()` in the same file — it looks up `root / f"{definition_id}.zip"`). Confirm the CLI's `export` step already names it this way; if not, rename before copying.

```bash
cp /tmp/<definition_id>.zip "${CA_HARNESS_LIBRARY_ROOT:-$CA_DATA_ROOT/harness-library}/"
```

Then confirm it's visible:
```bash
curl -s localhost:8000/api/harnesses | jq '.[] | {definition_id, category_id, production_ready}'
```
`production_ready` and `certified` will correctly show `false` — that's expected and by design (`certification_state: "uncertified_nonproduction"` / `"STRUCTURAL_UNCERTIFIED"`), not a bug to fix here.

### 2d. Report back before continuing

Stop after the pilot. Report to the operator: which category it covers, whether it round-tripped cleanly, and anything that had to be worked around. Only proceed to the rest of the batch once the operator confirms the pilot looks right — a format problem caught once is cheap; caught after building 15 harnesses, it's 15x the rework.

---

## Step 3 — Batch-build the rest

Repeat Step 2 per remaining harness identified in Step 1's gap table. Keep `capability_requirements: []` for all of them unless workstream 1-C (`CURRENT.md` §1.14) has landed and real `capability_metadata` sourcing exists — otherwise you're building Harnesses that will all hit the same currently-unresolved gate the moment anyone tries to run a campaign against them.

After each batch, update `docs/PRD/CURRENT.md` §1.4 (Builder) and §1.7 with what the library now contains — count, categories covered, categories still missing — per the document's own maintenance rule (§1.12). Do not leave this for a later summary pass.

---

## Known open question this skill does not resolve

Whether "one Harness per category" or "many Harnesses per category" (keyed by format profile, derivative type, or something else) is the operator's intended model is not settled anywhere in `CURRENT.md` as of this skill's writing. If the reference zip implies multiple harnesses per category, flag this as a new open decision for §1.10 rather than picking a convention unilaterally.
