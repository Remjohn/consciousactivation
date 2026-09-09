# AGENT_HANDOFF — CA-M050 Cryptographic Evidence DAG

## Mandate ID & Title

- **Mandate ID:** CA-M050
- **Title:** Cryptographic Evidence DAG
- **Governing Invariant:** INV-DAG-001
- **Canonical Decision:** Q49

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/pipeline/src/cmf_pipeline/evidence/dag.py` | New module: `EvidenceDAG`, content-addressed nodes, multi-parent edges with cryptographic parent-hash, explicit `PRUNED_REJECTION`, cycle detection, workspace fencing, inferred-parent rejection, serialize/reopen with re-verification | INV-DAG-001 — durable strictly acyclic multi-parent causal DAG with parent-hash verification and explicit pruning |
| `services/pipeline/src/cmf_pipeline/evidence/__init__.py` | Package exports for the evidence topology subsystem | Public surface for INV-DAG-001 |
| `tests/pipeline/test_ca_m050_evidence_dag.py` | 26 unit tests covering positive multi-parent/hash/traversal/prune paths and negative cycle, missing-parent, cross-tenant, inferred-parent (false-proof), and hash-mismatch cases | Executable proof of INV-DAG-001 including false-proof countercase rejection |

## Files Added

| Relative repository path | Rationale |
|---|---|
| `services/pipeline/src/cmf_pipeline/evidence/__init__.py` | Package init exposing DAG types and errors |
| `services/pipeline/src/cmf_pipeline/evidence/dag.py` | Core implementation of the cryptographic evidence DAG (INV-DAG-001) |
| `tests/pipeline/test_ca_m050_evidence_dag.py` | Mandate-specific positive/negative tests including false-proof countercase |

## Files Modified

None. This mandate introduces a new evidence topology surface under `services/pipeline/src/cmf_pipeline/evidence/` without altering existing modules.

## Exact Paste Instructions

1. From the repository root, copy the bundle contents preserving paths:

```bash
cp -R CA-M050_BUNDLE/services/pipeline/src/cmf_pipeline/evidence services/pipeline/src/cmf_pipeline/
cp CA-M050_BUNDLE/tests/pipeline/test_ca_m050_evidence_dag.py tests/pipeline/
```

2. Ensure the parent package path exists (it already does in the clean tree):

```bash
ls services/pipeline/src/cmf_pipeline/
```

3. No migrations, schema changes, or environment variables are required. The DAG is an in-memory / serializable pure-Python structure with no database dependency.

## Post-Apply Commands

No migrations or service restarts are required. Optional smoke check:

```bash
python -c "from pathlib import Path; import importlib.util, sys; p=Path('services/pipeline/src/cmf_pipeline/evidence/dag.py'); s=importlib.util.spec_from_file_location('dag', p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print('OK', m.EVIDENCE_DAG_VERSION)"
```

## Test Command

```bash
python -m pytest tests/pipeline/test_ca_m050_evidence_dag.py -v --tb=short
```

## Expected Test Results

- **26** automated tests
- **All passing** (26 passed, 0 failed, 0 skipped)
- Coverage includes:
  - Construction of TEMPORAL_MOMENT, TRANSCRIPT, TENSION_MATRIX, SYNTHESIZED_MEDIA nodes
  - Multi-parent links with parent-content-hash verification
  - Deterministic topological order, ancestors, descendants
  - Explicit `PRUNED_REJECTION` (nodes and edges remain addressable)
  - Cycle rejection (self-loop, simple, transitive)
  - Missing-parent rejection
  - Cross-tenant rejection
  - Inferred-parent rejection at link time and on reopen
  - **False-proof countercase:** neat chronological list + successful topo sort still rejected when an inferred or cross-tenant parent is present
  - Parent-hash mismatch detection on reopen
  - Full serialize → reopen round-trip with re-verification
  - `evidence_refs` export

## Implementation Notes (INV-DAG-001)

- Edges point **child → parent** (backward provenance).
- Every active edge stores the parent’s `content_hash` at link time; reopen and `verify_all` re-check it.
- Rejected alternatives are marked `PRUNED` / `PRUNED_REJECTION` and are never silently discarded.
- Topological sort success alone is **not** treated as provenance proof (explicit false-proof tests enforce this).
- Workspace binding is enforced on every node add and edge link.
- Parent references must be explicitly persisted; `metadata.inferred=True` is refused.

## Limitations

- The DAG is a pure data-structure + validation layer. Integration into `program_operator_runtime` receipt handling or persistent storage is out of this mandate’s declared file boundary (`services/pipeline/.../evidence/dag.py`).
- No database schema or migration is introduced; callers serialize via `to_dict` / `from_dict`.
- Content hashing uses deterministic JSON (sort_keys, compact separators); floating-point values are not expected in payloads.

## Operator Decision Requested

**APPROVE** — INV-DAG-001 is physically evidenced within the declared scope (26/26 tests green, false-proof countercase rejected).
