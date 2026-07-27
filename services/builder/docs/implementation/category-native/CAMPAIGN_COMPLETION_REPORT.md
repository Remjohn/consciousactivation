# BD-004/BD-007 Evidence Qualification and Category-Native Compilation Campaign

Verdict: `PASS_EVIDENCE_QUALIFICATION_STOPPED_AT_VALID_BLOCKER`

The campaign completed its authorized evidence work and did not manufacture the
authority, provider results, scores, thresholds, or certification needed to implement
ST-06.03. No production or test source changed.

## Baseline

- Active receipts: `28/28 PASS`; confirmed Stories complete: `27/69`.
- ST-06.01 and ST-06.02 completion manifests: `PASS`.
- Recovered archive identity: exact SHA-256
  `403bd07f8ca3feae94a991b16a08270fb799ffea87a05ab108163b4e1dee37b0`.
- Baseline regression: `909/909 PASS`; Python compilation: `PASS`.
- Source tree SHA-256:
  `504155c80e7794dcbeed93ae0efbd557758a556580832a8776999c3a138428e6`.
- Receipt-index SHA-256:
  `d8e75ea8519225e7f849ddd656ca7042a2b6165fc8c9aff6a1ae9ee54a7dae31`.

## BD-004 archive qualification

Disposition: `BLOCKED_OPERATOR_AUTHORITY`.

- All `1,434/1,434` members were streamed, hashed and CRC-read without extracting
  untrusted archive members into the Builder repository.
- No traversal paths, exact or case-insensitive collisions, symlinks, special files,
  encryption, malformed filenames, unsupported compression, CRC failures or archive
  bomb thresholds were found.
- The first nested ZIP was inspected in memory and passed the same bounded checks.
- Six duplicate-content groups cover 17 files; mixed V1.1/V1.2 material and generated
  cache/bytecode are recorded limitations.
- The archive contains potentially useful Format 02 and other category syntax and
  sequencing material, but no archive-wide source profile, complete item-level
  provenance, or governed legal/organizational Builder usage-adoption declaration.
- The archive is therefore not admitted as a
  `development_only_non_certifying_reference_corpus`.

Evidence hashes:

- inventory: `e279ed8e549d205e2a00b4cfd3285bae284c24c1450eec8b49ecd2e60995d263`;
- member-inventory digest: `333834dc95e7e214ff2363ed11b50db83a7c6c02bff3460bfb57d97105419ece`;
- authority receipt: `692d9c76cdac59135a3a8a838110a0260f4974ade90e0abe3d0853f1c93730c9`;
- ST-06.03 disposition: `6bfc9ccb434be0549517358ebd95b55cb33d1e6111f3efd790bf642341f34692`.

The exact truthful declaration and member-admission decision required from the operator
are recorded in `BD004_OPERATOR_AUTHORITY_DECISION.yaml`. The broader Format 02,
benchmark, production and certification scopes remain open.

## BD-007 empirical baseline

Disposition: `BLOCKED_EXTERNAL_PROVIDER`.

- Locally present but ineligible surfaces: OpenAI CLI/SDK `1.59.7`, LiteLLM `1.58.0`,
  and the Codex desktop command surface.
- Eligible provider configurations: `0`; governed Builder provider adapters: `0`;
  credential sources: `0`.
- Provider calls, admitted cases, paired outputs, repeat runs, scores and output hashes:
  `0`.
- No development threshold was established. Production and certification thresholds
  are not applicable to this development-only branch.
- No archive member was used because BD-004 did not admit the corpus.

The provider-neutral protocol, paired case template, repeat policy, score dimensions,
non-compensable failures and exact later execution package are recorded without
claiming an empirical result. The BD-007 disposition SHA-256 is
`4587dfb755bc4caab4a2ba15838b38d53ec053e1799c2978ec1d8abb096d6eb9`.

## Story gates

- ST-06.03: `BLOCKED_EVIDENCE`. Its capsule is complete as
  `PASS_CONDITIONAL_BLOCKED_EVIDENCE`, with manifest
  `0a231d36e38dd505aaf960e98c6aecae27aab727b4646495321d74f4041eeed5`
  and bundle
  `e6b0e363328f7fb459ed81de2855c94d671f70ae907a3174e1bf38d2ba354bac`.
  No implementation, active Story tests, or completion receipt exists.
- ST-06.04: `BLOCKED_PRIOR_STORY`; no additional disposition was inherited.
- ST-06.05: not implemented. Its read-only audit preserves HD-006, HD-007, source-human
  reaction authority, Reaction Receipt provenance, Expression Moment lineage and human
  Identity DNA amendment approval.

Exact current minimum cut:

1. BD-004 — truthful operator authority bound to the archive hash, explicit admitted
   member selection and a governed admission receipt preserving limitations.
2. BD-007 — at least one eligible immutable provider configuration and governed runner
   for the Story-scoped internal baseline, followed by repeated category-native versus
   flattened-generic evidence without a non-compensable failure. Two materially
   distinct configurations remain required for the broader provider-comparison scope.

## Completion validation

- Fresh-process regression 1: `909/909 PASS`, zero mandatory skips, 187.07 seconds.
- Fresh-process regression 2: `909/909 PASS`, zero mandatory skips, 202.76 seconds.
- Python compilation: `PASS`, 87 source files.
- Active receipts: `28/28 PASS`.
- ST-06.03 capsule: `18/18` artifacts and `18/18` immutable inputs hash-valid.
- Evidence YAML/JSON, cross-lane archive identity and all embedded hashes: `PASS`.
- Portable-path and secret scans: `PASS`.
- Path conflicts and unauthorized writes: `0`.

Parallel lane times were approximately 25 minutes for BD-004, 24 minutes for BD-007,
and 18 minutes for the ST-06.03 capsule. Integrator elapsed time from baseline record
to final verification was approximately 35 minutes.

Confirmed Stories remain `27/69`; `42` remain. No Story is READY on this campaign
path. Production readiness and certification remain false.
