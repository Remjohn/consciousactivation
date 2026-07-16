# Relevant Technical Specifications

- `TS-05` owns typed decision nodes, dependency eligibility, one-question interaction,
  recommendations, immutable state and replay.
- `TS-04` owns the unratified Draft Harness Model and frozen boundary entry state.
- `TS-01` owns governed run identity and lifecycle; no lifecycle edge is advanced here.
- `TS-11`, `TS-12`, `TS-13`, `TS-14` constrain categories, projection,
  authorization and future runtime but are not implemented by this increment.

Failure behavior: reject unsupported paths, missing evidence, premature nodes,
incomplete alternatives or recommendations that imply ratification. Test seam:
public command, graph query, observation and rollback seams. Compatibility: additive
immutable artifacts only; no IR or external schema mutation.
