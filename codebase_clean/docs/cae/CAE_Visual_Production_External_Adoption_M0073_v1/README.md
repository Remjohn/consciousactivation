# M0073 External Repository Adoption Registry

**Evidence class:** SCHEMA / REGISTRY_SOURCE  
**Status:** BLOCKED — OPERATOR REVIEW REQUIRED

This registry freezes the intended upstream-to-CAE boundary without importing upstream authority.

Required per-entry fields are:
`name`, `url`, `license`, `source_ref`, `source_commit_sha`, `source_paths`, `adopted_behavior`, `excluded_behavior`, `cae_destination`, `process_boundary`, `integration_owner`, `status`, `evidence_class`, and `verification_note`.

`source_commit_sha` is nullable only while `status` is a blocking status. A record may not be promoted to `READY` while its exact source reference is unresolved.

The registry deliberately distinguishes:
- behavioral references;
- isolated upstream dependencies;
- embedded primitives;
- runtimes;
- visual-intelligence engines.

No entry grants semantic, state, provenance, promotion, or operator authority to an upstream repository.
