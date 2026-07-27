# Runtime Workflows

## 1. Pre-interview compilation workflow

```text
Load immutable Brand Context
→ Assemble research field
→ Compile Context Premises
→ Select candidate archetypes and asset portfolio
→ Generate sequence hypotheses
→ Derive ingredient requirements
→ Deduplicate requirements
→ Generate acquisition instruments
→ Construct Interview Asset Contracts
→ Simulate coverage
→ Human review
→ Freeze Interview Brief V2
```

### DSPy programs

- `AssetPortfolioPlanner`
- `SequenceHypothesisCompiler`
- `IngredientRequirementCompiler`
- `InterviewAssetContractCompiler`
- `CoverageSimulationEvaluator`

The programs produce typed outputs. No program writes directly to persistent state.

---

## 2. Live session workflow

Inputs:

- approved Interview Brief V2;
- active Interview Asset Contract;
- streaming transcript and timestamps;
- current interviewer / guest state;
- prior ingredient coverage;
- doctrine and safety state.

The live assistant performs:

```text
segment ingestion
→ lightweight ingredient detection
→ coverage-state update
→ state and safety check
→ optional cue proposal
→ interviewer accepts / ignores
→ timestamp and event recording
```

The assistant should prefer concise cues and should not produce full scripted follow-ups unless requested.

---

## 3. Post-session extraction workflow

```text
Master media ingest
→ transcript / diarization / alignment
→ anchor hit detection
→ Expression Moment extraction
→ ingredient extraction
→ ingredient classification
→ provenance binding
→ primitive and edge tagging
→ quality evaluation
→ relation graph construction
→ human review
→ inventory freeze
```

### DSPy programs

- `ExpressionIngredientExtractor`
- `IngredientRoleClassifier`
- `IngredientQualityEvaluator`
- `IngredientRelationCompiler`
- `GapAndPickupPlanner`

---

## 4. Sequence compilation workflow

```text
Load approved inventory
→ rank sequence hypotheses against actual ingredient quality
→ discover stronger unplanned hypotheses
→ choose pattern
→ bind ingredients to beats
→ validate open-loop closure
→ compile emotional and information curves
→ apply format adapter
→ run doctrine and source-grounding evals
→ operator review
→ freeze ContentSequenceProgram
```

### Ranking principles

1. Prefer unexpected authentic high-quality ingredients.
2. Prefer planned high-quality ingredients.
3. Use approved evidence and Brand Memory for contextual support.
4. Request a pickup when a required human payoff is missing.
5. Abandon a recipe rather than fabricate its central truth.

---

## 5. Composition handoff

The sequence compiler does not specify raw pixels. It emits composition functions such as:

```text
unexpected_closeup
memory_object_insert
paper_note_sequence
contrast_panel
framework_reveal
reaction_pause
poll_choice_state
signature_end_card
```

Format-specific composition engines map those functions to:

- video scene templates;
- carousel composition grammars;
- single-image attention paths;
- 2D character performance cues;
- caption, annotation, and sound-event plans.

---

## 6. Learning workflow

After publication, the system joins:

- sequence pattern;
- ingredient roles;
- acquisition instruments;
- format adapter;
- composition grammar;
- audience telemetry;
- operator revisions.

It learns:

- which questions reliably acquire specific ingredients;
- which Depth Anchors produce useful mechanisms or costs;
- which patterns retain attention without distorting truth;
- which payoffs create saves or shares;
- which package orders create return behavior;
- which ingredients are repeatedly missing.

Learning updates registry recommendations, not immutable historical objects.
