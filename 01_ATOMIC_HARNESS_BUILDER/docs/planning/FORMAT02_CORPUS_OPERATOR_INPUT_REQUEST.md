# Format 02 Corpus Operator Input Request

Request ID: `BD-004-FORMAT02-INPUT-001`  
For: Product lead and evidence steward  
Placement: `reference-corpora/format02_minimal_coach_theatre/operator-input/`  
Purpose: Supply the missing authoritative evidence needed to govern the Format 02 corpus sub-scope for `ST-01.02`.

This is the single operator request for the bounded Format 02 path. Do not include Conversational Activation, Interview Expression, ReelCast, VAE production outputs, Delegation runtime traffic, or future-category material.

## Required input set

Place the following in the directory above:

1. `SOURCE_PROFILE.yaml` — the proposed authoritative Format 02 source profile.
2. `CORPUS_MANIFEST.yaml` — one row/record per supplied source file or immutable reference.
3. `AUTHORITY_AND_USAGE_EVIDENCE.yaml` — authority, ownership, license, and permitted-use evidence for every manifest item, with documentary references where applicable.
4. `OPERATOR_DECISIONS.yaml` — signed/attributable product-lead and evidence-steward decisions listed below.
5. `examples/` — accessible source bytes, or `IMMUTABLE_REFERENCES.yaml` when bytes are held in an approved content-addressed/object store.

If the historical archive is the intended authority, supply the exact file `VISUAL SYNTAX BUILDER (2)(2).zip` whose SHA-256 is `403bd07f8ca3feae94a991b16a08270fb799ffea87a05ab108163b4e1dee37b0`. If that archive is not authoritative, identify the governed superseding bundle and provide its complete manifest and hash. A machine-local `/mnt/data` path is not an acceptable portable reference.

## Minimum examples

Supply at least three attributable target candidates for governance review:

- Two included Format 02 examples representing distinct scene/sequence situations. Each must include an inspectable final reference artifact plus the source material needed to understand its Format 02 role, such as script/transcript, scene/beat description, frames/images, and referenced visual or character inputs where those materials exist.
- One explicit exclusion/boundary example showing a non-Format-02 or invalid candidate and the authoritative reason it must be rejected by the profile.

This three-candidate intake minimum is for corpus-governance evaluation only. It is not a benchmark-size claim and does not confer certification.

## Acceptable formats

- Video/audio: `mp4`, `mov`, `webm`, `wav`, `mp3`.
- Images/design references: `png`, `jpg`, `jpeg`, `svg`, `pdf`.
- Text/structured evidence: UTF-8 `md`, `txt`, `json`, `yaml`, `yml`, `csv`.
- Bundles: `zip` only; nested archives must be declared and must stay within the TS-02 safety limits.
- Immutable remote material: versioned URI plus SHA-256, byte size, retrieval authority, and a statement that mutable-latest URLs are prohibited.

Every supplied byte or immutable reference must have a SHA-256. Do not submit screenshots or copied text as substitutes for an authoritative source when the original is available.

## Required `SOURCE_PROFILE.yaml` fields

- `profile_id: format02_minimal_coach_theatre`
- `profile_version`
- `compilation_target: atomic_content_harness`
- `category_id: 2d_character_animation`
- `target_kind`
- `authority_owner`
- `required_roles`
- `recommended_roles`
- `optional_roles`
- `prohibited_roles`
- `allowed_media`
- `discovery_rules`
- `safety_limits`
- `target_candidate_rules`
- `saturation_contract_ref`
- `privacy_policy_ref`
- `amendment_authority`

The profile must identify a real accessible target-candidate boundary and must not silently default missing roles or infer authority.

## Required `CORPUS_MANIFEST.yaml` fields per item

- stable `source_id` and relative path or immutable URI;
- byte size and SHA-256;
- media/content type and Format 02 evidence role;
- originating source and complete provenance chain;
- authority owner and precedence status;
- ownership or license evidence reference;
- permitted Builder uses, derivative/test rights, distribution limits, and expiry if any;
- privacy classification and access restrictions;
- inclusion rationale or exclusion rationale;
- `protected_example: true|false`;
- `benchmark_eligible: true|false` with decision authority and rationale;
- known limitations and any required redaction.

Unknown license, authority, privacy, or benchmark-eligibility values must be recorded as blocking; the Builder must not guess them.

## Required decisions

`OPERATOR_DECISIONS.yaml` must identify the human authority, date, and decision receipt for:

1. Which supplied bundle/items are the authoritative Format 02 corpus for this bounded Builder path.
2. Approval of the source profile and its required/recommended/optional/prohibited roles.
3. Approval of the two inclusion examples and one exclusion/boundary example.
4. Whether each item may be used for Builder development tests, evaluation, protected evaluation, and/or later benchmark design.
5. Which examples are protected and who may access their labels.
6. Whether the historical `SRC-004` archive is adopted, partially selected, or superseded.
7. Approval of known limitations and the amendment procedure.

## Acceptance bar

The input closes this request only when all referenced files resolve, hashes verify, authority/usage evidence covers every item, the source profile is internally consistent, and product lead plus evidence steward issue an attributable approval. The Builder will then create the governed corpus package and validation receipt in a separate bounded planning action.

Governance of the corpus will not mean benchmarked, limited-production-certified, production-certified, or production-authorized.

