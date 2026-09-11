# CMF Delegation Contracts

This directory is the Stage 3 canonical shared-contract source and generated
baseline. `src/` owns the message definitions, `tools/build_baseline.py`
generates schemas and fixtures, and `registry.json` binds each active message
to its producer, consumers, hashes, idempotency class, and lifecycle effects.

The active package version is `1.0.0-rc.2`. It is a local release candidate,
not a published or signed contract release. Historical drafts under the root
`contracts/` directory are compatibility evidence only.

Regenerate from the repository root:

```powershell
python packages/contracts/tools/build_baseline.py
```
