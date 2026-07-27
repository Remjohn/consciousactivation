# CS-034 Event Schema Activation Monitor

## Research Basis

**Zacks Event Segmentation Theory (EST)** — Zacks & Tversky (2001), Zacks et al. (2007):
The brain parses continuous experience into discrete events at prediction boundaries. When a new event boundary is detected, attention and memory encoding spike. Schemas organize what constituents are expected within each event type; violating those schemas before they are established produces confusion rather than productive surprise.

**Narrative Schema Theory** — Mandler & Johnson (1977), Rumelhart (1975):
Stories activate familiar narrative schemata (e.g., problem → action → outcome). Audiences automatically apply these schemata. Violating schema *after* establishment creates meaningful surprise; violating *before* establishment creates incoherence.

**Metz Film Narratology** — Christian Metz (1974):
Film language is readable because viewers internalize syntagmatic sequences. Dense event boundaries undermine this readability when they appear before the viewer has acquired the local schema.

## Subsystem Role

CS-034 monitors two quantities across the assembled manifest:

1. **Schema activation score** — How well-established the current narrative schema is before key violation or transition points. Derived from the ratio of orientation beats to violation beats in the first half of the arc.

2. **Boundary density per beat** — Average number of narrative event boundaries per resolved beat. High density early in the arc indicates the schema has not had time to settle before being disrupted.

### Verdicts

| Condition | Verdict |
|---|---|
| density ≤ 0.50 AND activation ≥ 0.40 | PASS |
| density > 0.50 OR activation < 0.40 | REVISE |
| activation < 0.30 AND density > 0.70 | BLOCK |

## Output Fields

- `schema_activation_score` [0..1]: How established the schema is heading into the first major violation beat
- `boundary_density_verdict`: PASS / REVISE / BLOCK
- `segmentation_advice`: List of corrective moves from route_hints
- `violation_timing_list`: Beat indices where violations occurred before schema was activated
