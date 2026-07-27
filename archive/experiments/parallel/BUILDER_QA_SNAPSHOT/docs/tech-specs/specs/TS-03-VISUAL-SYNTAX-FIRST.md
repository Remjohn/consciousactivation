# TS-03: Visual Syntax First

Status: `EMPIRICAL_SPEC_COMPLETE_PENDING_BD-004_BD-007`

## Traceability

- Owned: FR-019 through FR-031.
- Decisions: D007, D008, D011, D012, D014, D023, D030, D031.
- Supporting NFRs: NFR-CAT-001, NFR-EVAL-001, NFR-EVAL-002, NFR-TRACE-001, NFR-TRACE-004.

## Responsibility And Authority

Own deterministic specimen normalization, syntax-level parse structures, geometry, spatial/hierarchy/temporal graphs, BBOX observations, category-adapted variables, cross-specimen induction, and draft hypotheses. It does not ratify meaning, atomicity, category constitution, or creative policy.

Deterministic code owns media decoding, geometry, coordinate transforms, schema validation, aggregation, and provenance. Bounded multimodal agents propose labels, functions, and hypotheses. Independent evaluators score parses. Humans adjudicate ontology/category changes and disputed high-impact hypotheses.

## Modules And Components

`visual/normalization.py`, `visual/ontology.py`, `visual/geometry.py`, `visual/spatial_graph.py`, `visual/temporal.py`, `visual/provider_port.py`, `visual/induction.py`, and `visual/evaluation.py`.

## Canonical Data Structures

- `NormalizedSpecimen { specimen_ref, normalization_version, canvas, frames_or_slides, timing_map, artifact_hash }`
- `VisualElement { element_id, class_ref, bbox_norm, mask_ref?, confidence, observed_by, provenance }`
- `SpatialEdge { from_id, relation, to_id, measured_value?, confidence }`
- `HierarchyNode { element_ref, salience, reading_order, parent_ref? }`
- `TemporalSegment { start_ms, end_ms, state, transition_in, transition_out, synchronized_audio_ref? }`
- `CompositionVariable { ontology_ref, value, observation_refs, category_adaptation_ref? }`
- `FunctionHypothesis { observation_refs, hypothesis, confidence, alternatives, status=DRAFT }`
- `VisualGrammar { specimen_set_hash, motifs, constraints, transitions, exceptions, induction_receipt }`

Coordinates are normalized to `[0,1]` while preserving source pixel dimensions. Observation and hypothesis fields are distinct schema branches; promotion requires explicit authority.

## APIs, Commands, Events, Persistence

- Commands: `NormalizeSpecimen`, `ParseVisualSyntax`, `ParseTemporalSyntax`, `InduceVisualGrammar`, `DraftActivativeHypotheses`, `AdjudicateParse`.
- Provider port: `parse(task, artifact_refs, ontology_ref, output_schema, budget) -> ProviderObservation`.
- Events: `SpecimenNormalized`, `VisualSyntaxParsed`, `TemporalSyntaxParsed`, `VisualGrammarInduced`, `HypothesisDrafted`, `ParseRejected`, `ParseAdjudicated`.
- Persistence: normalized media and overlays in CAS; typed parses and grammars as Harness IR-owned artifacts; provider raw output retained as non-authoritative evidence.

## Dependency, Invalidation, Idempotency, Resume

Cache key includes specimen hash, normalization version, ontology version, parser/provider policy, prompt/capsule hash, and model version. Ontology or normalization changes invalidate dependent parses. One failed specimen does not discard completed siblings. Induction runs only over a complete declared specimen set and is invalidated when set membership or any parse identity changes.

## Security And Isolation

Provider adapters receive only authorized derived media, never unrelated sources or protected benchmark labels. PII/redaction policy runs before remote calls. Raw model text cannot write IR directly. Model/network access is explicit per workflow node.

## Observability, Cost, And Performance

Record frame/slide counts, parse latency and cost, provider/model identity, schema-repair count, confidence calibration, inter-evaluator agreement, geometry error, temporal boundary error, and cache reuse. Exact production thresholds remain empirical under BD-007.

## Failures And Recovery

Decode errors quarantine the specimen. Schema-invalid provider output gets one bounded repair attempt, then fails. Low confidence remains explicit and blocks saturation where required. Provider disagreement produces alternatives; it is not averaged into false certainty. Deterministic fallback may produce geometry-only output but cannot claim semantic completeness.

## Acceptance Tests

1. Normalization is deterministic and preserves source-to-normalized coordinates.
2. Every element and relation traces to specimen/frame evidence.
3. BBOX observations cannot contain WHY claims.
4. Time-based Format 02 evidence has ordered segments and legal transitions.
5. Duplicate specimens do not inflate grammar support.
6. Induction changes when specimen membership changes and reuses unchanged parses.
7. Hidden provider text cannot bypass schema validation.
8. Protected cases show measured parse quality above ratified thresholds before production use.

## Implementation Tasks

1. Ratify ontology and Format 02 category adaptation.
2. Implement normalization and deterministic geometry baseline.
3. Implement provider port and two benchmark adapters.
4. Implement parse/grammar schemas and validators.
5. Build overlay and temporal inspection artifacts.
6. Run prototype corpus, calibration, adversarial, and provider-failure experiments.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Separate harness-development Visual Syntax First from runtime Activation First | visual_understanding_owner | Parser discovers syntax and expression evidence; it cannot author runtime semantic intent | syntax observation, function hypothesis, Activative Intelligence Pack ref, `knowledge_status` | Reject semantic promotion, runtime-order inversion, or syntax-derived invention | dual-order negative fixture across visual and interview specimens | Syntax evidence precedes hypotheses in development while runtime outputs begin from frozen Activative Intelligence | Clarifies existing Visual Syntax behavior; no valid V1.1 observation is discarded |

## Non-Goals And Migration

No image generation, ComfyUI, LoRA training, GPU scheduling, final semantic authority, or V2.1 parser migration is included.
