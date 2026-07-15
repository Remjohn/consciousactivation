# CMF Delegation Contracts

This directory is the Stage 3 canonical shared-contract source and generated
baseline. `src/` owns the message definitions, `tools/build_baseline.py`
generates schemas and fixtures, and `registry.json` binds each active message
to its producer, consumers, hashes, idempotency class, and lifecycle effects.

The active package version is `1.1.0-rc.2`. The envelope protocol remains
`1.0`, while `visual-asset-demand` is version `1.1`. It is a local release candidate,
not a published or signed contract release. Historical drafts under the root
`contracts/` directory are compatibility evidence only.

The Visual Asset Demand is constitution-complete: it preserves exact upstream
identity/version/hash/reference tuples, the Activation Contract, Visual
Semantic and Narrative programs, Feature Contracts, the T/V route request,
Reaction Receipt and Expression Moment lineage, and non-empty wrong-reading
locks. Legacy aliases are accepted only by the explicit lossless migration.
The governed `source_provenance.source_kind` discriminator is mandatory;
`interview_expression` requires non-empty Reaction Receipt and Expression
Moment references. Validators resolve only distribution-relative paths and run
unchanged from the source `packages/` root or a clean extracted release root.

Regenerate from the repository root:

```powershell
python packages/contracts/tools/build_baseline.py
```
