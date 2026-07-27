# Implementation scope

Implement one vertical command/query slice that reads the exact active ST-03.03 HarnessIR and produces an immutable artifact set in the existing in-memory development/test persistence boundary.

The compiler must render exactly the 21 artifacts in `CONTRACT_AND_SCHEMA_REFERENCES.yaml`. Human shards are readable deterministic Markdown. OpenSpec and machine artifacts are canonical JSON views. All values must be selected from declared HarnessIR paths; unresolved, hypothesis, unratified, or `NOT_APPLICABLE` states remain explicit. A projection may not invent values, interpret category semantics, or claim executable behavior.

The command carries an explicit reproducible build configuration containing compiler ID/version, configuration version, and RFC3339 generation timestamp. The config is canonicalized and hash-bound. The compilation key is `(ir_hash, compiler_id, compiler_version, config_hash)`. Identical keys return byte-identical artifacts, manifest, and receipt. Changing the config creates a distinct immutable artifact-set identity.

Commit the 21 artifacts, manifest, run reference/event, command record, and receipt atomically. The run remains in `GENESIS`; ST-03.04 does not claim architecture compilation. Validate a supplied artifact byte map against the manifest, emit a typed drift report, quarantine mismatches, and never mutate HarnessIR. An authorized upstream reopen must invalidate the artifact-set descendant in the same additive chain as the HarnessIR invalidation.

Implementation requires additive code, tests, repository port behavior, run replay/invalidation state, and observations. It requires no schema file, database, network, external package, provider, runtime, UI, API, or generated workspace file.
