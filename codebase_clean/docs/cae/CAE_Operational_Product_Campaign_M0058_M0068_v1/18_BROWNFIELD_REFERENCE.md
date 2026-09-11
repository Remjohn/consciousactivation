# Brownfield Reference — M0058–M0068

## Required primary authority

- `docs/PRD/CURRENT.md`
- `docs/cae/PROMPT_REFERENCE_BLOCKS.md`
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_mandate_bundle/13_CA_M10_ASSET_INTELLIGENCE_EDROLL_MANDATE.md`
- `docs/cae/cae_mandate_bundle/14_CA_M11_PRODUCTION_SEMANTIC_PROGRAM_MANDATE.md`
- current operator gate/checklist
- current Program/runtime registry and state implementation

## Required product/runtime surfaces to inspect

- `packages/ca_runtime/`
- `programs/`
- `services/asset-intelligence/`
- `services/pipeline/`
- `services/production-program/`
- current video-edit media / EDL / bindings
- VAE/Delegation boundary
- existing evaluation / receipts / HumanResolutionEpisode paths
- actual OpenChatCut integration surface available to the repository

## Brownfield rule

A manifest, README, schema, import, placeholder adapter or test double is not evidence that the product can operate. For every mandate, the agent must trace the reachable path and identify whether the claimed behavior is:
`EXECUTABLE`, `SCHEMA`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`.

If the repository already has a canonical implementation, extend it instead of creating a second one.
