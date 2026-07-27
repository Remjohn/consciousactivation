# Relevant Technical Specifications

## TS-11 - Category Constitutions and Target Compilers

Pinned SHA-256: `f6a269e974ef44dc169790b82effa6b1c00b880e5915fd52df2172eee4d64de3`.

ST-07.04 implements only the BF-AM-008 Atomic Content Harness validation branch of TS-11. It validates target artifact completeness, target-profile separation, deterministic package identity, authority gates, certification scope, internal compatibility and lossless lineage. It does not implement the TS-11 Visual Asset Editor or Delegation target compiler/runtime branches.

The target validation report must use the active `AtomicHarnessDefinition` as the sole compiled product input. Any missing artifact, inconsistent capability/module/phase/context/skill relationship, authority drift, universal-profile flattening, external-target field leakage, or certification upgrade fails closed.

External target compatibility is recorded as `NOT_EVALUATED_EXTERNAL_TARGET_BRANCH`, not PASS. Format 02 evaluation, benchmarks, production certification, visual execution and external interface validation remain outside this capsule.
