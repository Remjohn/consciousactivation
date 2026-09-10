# Execution Sequence — Component Factory → Assembly → Certification

This campaign is intentionally split into **component construction** and **final assembly**. Component mandates return isolated bundles first. Only assembly mandates may modify shared integration surfaces or compose independently proven bundles into the canonical CAE worktree.

| Phase | Mandate | Depends on | Parallel group | Primary agent | Mode |
|---|---|---|---|---|---|
| P0 Authority | M0073 | M72 | S0 | Claude | sequential; freezes Authority Pack + registry |
| P1 Extraction | M0074 | M0073 | P1 | Claude | parallel isolated external-repo extraction |
| P1 Extraction | M0075 | M0073 | P1 | ChatGPT | parallel isolated external-repo extraction |
| P1 Extraction | M0076 | M0073 | P1 | Grok | parallel isolated external-repo extraction |
| P1 Extraction | M0077 | M0073 | P1 | ChatGPT | parallel isolated external-repo extraction |
| P1 Extraction | M0078 | M0073 | P1 | Claude | parallel isolated external-repo extraction |
| P2 Foundation | M0079 | M0073 | S1 | ChatGPT | isolated CAE domain component; re-run if prior no-write blocker occurred |
| P2 Foundation | M0080 | M0079 | S2 | Claude | isolated format-program contracts |
| P3 Grammar | M0081 | M0080 | P3 | Claude | parallel component |
| P3 Grammar | M0082 | M0080 | P3 | ChatGPT | parallel component |
| P3 Grammar | M0083 | M0080 | P3 | Claude | parallel component |
| P3 Grammar | M0084 | M0080 | P3 | Claude | parallel component |
| P4 Studio | M0085 | M0079–M0084 | S3 | ChatGPT | isolated Visual Asset Studio component |
| P5 Research | M0086 | M0085 | P5 | Claude | parallel capability branch |
| P5 Research | M0087 | M0085/M0086 | P5 | ChatGPT | depends on research contract; candidate UI component |
| P5 Research | M0088 | M0085/M0083 | P5 | Grok | Visual Chat component |
| P5 Research | M0089 | M0085/M0079 | P5 | Claude | operator feedback component |
| P6 Vision/Visual | M0090 | M0083/M0084 | P6 | Claude | SAM3 tracking component |
| P6 Vision/Visual | M0091 | M0083/M0084 | P6 | ChatGPT | SuperVisual editor component |
| P6 Vision/Visual | M0092 | M0081–M0084 | P6 | Claude | Final-Hit / MotionPlan component |
| P7 Runtime Adaptation | M0093 | M0092/M0085 | S4 | ChatGPT | isolated adapters; may build against frozen component contracts |
| P7 Runtime Adaptation | M0094 | M0092/M0085 | S4 | ChatGPT | OpenChatCut adapter/handoff component |
| P8 Assembly | M0095 | M0074–M0094 | S5 | Grok | **sequential assembly only; canonical shared files** |
| P9 Certification | M0096 | M0095 | S6 | ChatGPT | **sequential live proof/certification** |

## Parallelism rules

### Safe parallel groups

`P1` is fully parallel because each mandate inspects a distinct external repository and returns an isolated component/extraction bundle. `P3`, `P5`, and `P6` are parallel where each mandate owns a distinct component boundary and consumes only frozen upstream contracts.

### Sequential boundaries

`M0073`, `M0079`, `M0080`, `M0085`, `M0093`, `M0094`, `M0095`, and `M0096` are controlled gates because they freeze shared authority or define integration contracts. `M0095` is the **final puzzle assembly** and MUST NOT be parallelized with other mandates. `M0096` is the certification gate and runs only after assembly and native/live evidence are available.

## Bundle assembly rule

Every mandate returns an isolated `[MANDATE_ID]_BUNDLE.zip`. The operator maintains an external assembly directory containing only accepted bundles. No downstream mandate may claim access to another mandate's uncommitted work unless the required bundle has been explicitly supplied as an input.
