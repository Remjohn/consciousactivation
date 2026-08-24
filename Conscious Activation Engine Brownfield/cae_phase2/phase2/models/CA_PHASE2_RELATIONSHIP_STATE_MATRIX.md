# Phase 2 Relationship & State Matrix

| Source | Relation / State | Target | Type | Key constraints |
|---|---|---|---|---|
| Audience | has_schema | AudienceSchema | 1:N/versioned | Schema is structural, not state |
| Audience | has_context_premise_observation | ContextPremise | 1:N | Evidence-bearing, provenance required |
| Audience | has_state | AudienceState | 1:N temporal | Append-preserving |
| Audience | has_tension | TensionWebhook | 1:N derived | Evidence + lifecycle required |
| Guest | has_schema | GuestSchema | 1:N/versioned | Persistent semantic structure |
| Guest | has_voice_dna | VoiceDNA | 1:N/versioned | Canonical definition vs state separate |
| Guest | has_state | GuestState | 1:N temporal | Historical states retained |
| Culture | produces_signal | ResearchSignal | 1:N | Immutable provenance |
| ResearchSignal | supports | ContextPremise | N:M | Evidence lineage |
| ContextPremise | informs | AudienceSchema | N:M | Inference trace required |
| ContextPremise | contributes_to | AudienceState | N:M | Derived, confidence-bearing |
| AudienceState | activates | TensionWebhook | N:M | Time-scoped |
| TensionWebhook | supported_by | Evidence | N:M | Corroboration required |
| AudienceState | has_affective_state | AffectiveState | 1:N temporal | Arousal × valence |
| AudienceState | has_media_motive | MediaMotiveState | 1:N temporal | Separate from tension |
| AudienceState | has_maturity_state | MaturityState | 1:N temporal | Evidence-driven |
