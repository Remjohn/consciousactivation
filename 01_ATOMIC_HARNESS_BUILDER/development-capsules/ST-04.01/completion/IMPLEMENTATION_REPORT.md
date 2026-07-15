# ST-04.01 implementation report

Verdict: `PASS`

## Outcome

The Builder now reads the exact, hash-pinned `skills.capabilities` set from the active synthetic Harness IR and compiles a deterministic, immutable capability-ownership graph and receipt. All three capabilities have one explicit `CODE` owner, an authority boundary, attributable reliability evidence, and bounded cost evidence. The graph preserves Source Lock, atomic-boundary, human-ratification, Draft Harness Model, Harness IR, artifact-set, constitutional-report, and constitutional-receipt lineage.

The governed empty-skill registry is verified only as evidence that this repository-owned synthetic proof requires no external or dynamic skill. The implementation does not discover, select, package, or execute skills and makes no real-profile or production inference.

## Behavior delivered

- Exact 3/3 capability inventory and no implicit owner defaults.
- Typed `CODE`, `AGENT`, `HUMAN`, `EXTERNAL`, and `HYBRID` decision vocabulary; the bounded fixture uses only explicit `CODE` decisions.
- Fail-closed non-code and hybrid authority, participant, evidence, and handoff contracts.
- Content-addressed graph and receipt identities with canonical decision order.
- Atomic graph, event, command-record, and receipt persistence.
- Payload-safe duplicate-command replay and conflicting-payload rejection.
- Exact active-parent validation through the ST-03.05 report and receipt.
- Linked downstream invalidation on an authorized atomic-boundary reopen; immutable history remains readable.
- Required success, replay, rejection, and invalidation observations without source payload logging.

## Preserved boundaries

No Format 02, VAE, Delegation runtime, GPU, visual production, conversational activation, external provider, workflow execution, Control Tower, production certification, later-Story behavior, dependency, database, or schema file was added. Existing run identity, lifecycle, authority, replay, checkpoint, artifact, and constitutional-precedence behavior remains intact.

## Validation summary

- Capsule inputs: `PASS_18_OF_18`
- Capsule manifest: `1c672badc3b9f8fa570bb5d8df2694f9aa14201938534046dd9f74da2f777253`
- Capsule bundle: `41a8dbc87ef3e92e5632b0a8c98227ddc218122a809bd1cfc8500c8765df31f5`
- Preimplementation regression: `PASS_186_OF_186`
- ST-04.01 suite run 1: `PASS_33_OF_33`
- ST-04.01 suite run 2: `PASS_33_OF_33`
- Original predecessor set: `PASS_186_OF_186`
- Updated predecessor tree: `PASS_188_OF_188`
- Architecture/failure/replay subset: `PASS_41_OF_41`
- Full repository: `PASS_221_OF_221`
- Mandatory skips: `0`

The only warning was the pre-existing `pytest-asyncio` default-loop-scope deprecation warning; it does not affect Story behavior or test results.

## Limitations

This is a synthetic, repository-owned, non-production, non-certified ownership proof using development/test in-memory persistence. It does not compile responsibility-centered modules, phase/context assignments, Workflow IR, an Atomic Harness Definition, or a compiled Harness Development Capsule.
