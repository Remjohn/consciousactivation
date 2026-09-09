# Phase 3 Relationship / State Matrix

| Object | Source | Target | Cardinality | Temporal? | Evidence Required | Derived? | Typical States |
|---|---|---|---|---|---|---|---|
| GuestExperiencedTension | Guest | Tension | many-to-many | yes | required | usually no | observed, historical, uncertain, superseded |
| AudienceTensionRelation | Audience/State | Tension | many-to-many | yes | required | mixed | latent, active, saturated, resolved, blocked, superseded |
| GuestAudienceRelation | Guest | Audience | many-to-many | yes | required | yes | candidate, assessed, strong, weak, divergent, stale |
| SchemaCrossing | GuestSchema/AudienceSchema | Schema | many-to-many | yes | required | yes | hypothesized, supported, contradicted, stale |
| CongruenceAssessment | Relation | Dimension Set | one-to-many | yes | required | yes | provisional, validated, disputed, superseded |
| ResonanceCandidate | Guest+Audience+Context | Pressure/Relation | many-to-many | yes | required | yes | candidate, ranked, rejected, selected, expired |
| PressureFieldCandidate | Relational evidence | Pressure field | many-to-many | yes | required | yes | candidate, supported, weak, rejected, routed |
| RelationalObservation | source event | relation/object | many-to-many | yes | immutable | no | recorded |
| RelationalReceipt | runtime execution | relation/plan | many-to-many | yes | execution trace | derived | complete, failed, repaired |
