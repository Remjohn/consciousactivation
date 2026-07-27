# Implementation Scope

Implement one deterministic validator that consumes only the exact active ST-07.02 `AtomicHarnessDefinition` and the hash-pinned synthetic target-validation policy. The validator emits an immutable `AtomicContentHarnessValidationReport`, receipt, run reference, deterministic observations and descendant invalidation behavior.

The report validates:

- all 20 definition sections and every required target artifact reference;
- exact source, authority, constitutional, Genesis, IR, artifact, module, phase, handoff, context and skill lineage;
- capability/module/phase/context/skill agreement;
- input/output and acceptance-test contracts;
- deterministic identity, canonical bytes and portability;
- Atomic Content Harness target/profile separation and absence of external-target field leakage;
- explicit `synthetic_not_certifiable`, non-production and non-certified state;
- target-specific evaluation and authorization gates;
- internal Atomic Content Harness compatibility;
- external target compatibility disposition `NOT_EVALUATED_EXTERNAL_TARGET_BRANCH`.

The validator does not compile another Harness Definition, execute a Harness or workflow, generate an ST-11.01 Development Capsule, validate Format 02, compile VAE/Delegation packages, call external runtimes, or claim production/certification.
