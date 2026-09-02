# Baseline Authority Read Set — M49–M64

Read these sources in full before action, then add the mandate-specific reads.

## CAE authority
- `docs/PRD/CURRENT.md`
- `docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md`
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `governance/program-control/`
- `docs/cae/constitutions/`
- `docs/cae/implementation/`

## Existing runtime
- `packages/ca_runtime/`
- `services/pipeline/AGENTS.md`
- `services/pipeline/src/cmf_pipeline/workflow/`
- `services/pipeline/src/cmf_pipeline/reasoning/`
- `services/pipeline/src/cmf_pipeline/programmed_model_engine.py`
- `services/pipeline/src/cmf_pipeline/retrieval_engine.py`
- `packages/ca_runtime/src/ca_runtime/agent_team.py`
- `packages/ca_runtime/src/ca_runtime/context_capsule.py`
- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`
- relevant tests
- `00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md`

## Existing Program packages
- `programs/research_canonicalization_program/`
- `programs/script_program/`
- affected Program packages discovered during mandate-specific inventory

## Reference factory
- SSSF README and example branch
- `sssf.config.yaml`
- starter ADWs, especially `adw_simple_sdlc.py`
- output envelope and gate modules
- Pi adapter
- visualizer
- justfile/operator commands

## Brownfield rule

A directory name is not evidence that contents were read. Search exact symbols/callers before editing. If current code contradicts a target statement, classify the discrepancy and stop rather than silently redesigning it.
