# ST-07.04 Capsule Validation Report

Verdict: **PASS**

The ST-07.04 Development Capsule contains 18/18 immutable implementation inputs. Every recorded byte count and SHA-256 reproduces. Capsule manifest SHA-256 is `fd4046916b0723c2151591f832924ce20e68fce532652321e8c342702ddc919b`; bundle digest is `7950999b12694bd5416d47c6e66f873f69fe22a0e792b36cc274d06150de9b8c`.

The sole direct dependency, ST-07.02, has a validated PASS Story Completion Receipt at SHA-256 `ee13f9b6601ab1b166f16d2d30fb043f1441745d9e8146248d2d6d7d08caa681`. Its canonical completion payload, changed-file manifest, test evidence, and `427/427 PASS` repository regression are pinned by `DEPENDENCY_RECEIPT.yaml`. BF-AM-008 is independently pinned at receipt SHA-256 `8c03c818ab39a8b0056a2e12766aeffd902192c67f3b5e6a0b7d5c93e9a093d8` and makes ST-07.02 the only dependency in `ATOMIC_CONTENT_HARNESS_ONLY` mode. ST-07.03 and BD-014 remain preserved on the external-target branch and do not apply here.

The bounded outcome is independent validation of the exact active synthetic `AtomicHarnessDefinition`. ST-07.04 adds target-artifact completeness, target-specific gates, non-flattening, authority and lineage checks, deterministic portable reproduction, internal compatibility, and explicit synthetic non-certification. It does not recompile or execute the Harness.

The capsule maps FR-177 through FR-180, TS-11, and ADRs 004, 005, 013, 014, and 018. Acceptance criteria, deterministic tests, observability, rollback, failure behavior, security boundaries, and completion-receipt evidence are complete and contain no unresolved placeholders.

The allowlist is exact: two new source modules, four bounded existing source changes, five exact-source regression updates, six Story-local tests, and six completion outputs. It forbids schema changes, external dependencies, databases, transports, Format 02, VAE, Delegation runtime, external-target compatibility claims, production certification, ST-11.01 behavior, and later Stories.

External target compatibility must be recorded exactly as `NOT_EVALUATED_EXTERNAL_TARGET_BRANCH`; it may not be inherited as PASS. The synthetic definition must remain non-production, non-certified, and `synthetic_not_certifiable`.

ST-07.04 is READY and independently implementable in one focused Codex context. The human subsequently supplied the Synthetic Demonstration Completion Campaign authorization and the exact ST-07.04 phrase. The immutable 18-input bundle remains unchanged; bounded implementation is authorized through the excluded authorization-control artifacts.
