"""CAE-M060 product E2E fixture and runtime proof harness.

This harness intentionally exercises the real CAE ProgramRegistry,
ProgramOperatorRuntimeService, UniversalProgramStateRuntime, and the durable
SqliteProgramStateStore. It does not replace a CAE runtime stage with a mock.
Only import-time compatibility shims for optional, unavailable repository
packages are allowed so the target runtime modules can be imported in a clean
sandbox.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import types
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence
from uuid import UUID, uuid5, NAMESPACE_URL


MANDATE_ID = "CAE-M060"
MANDATE_INVARIANT = "INV-PROOF-REAL-001"
PROGRAM_ID = "research_canonicalization_program"
EXPECTED_PROGRAM_VERSION = "1.0.0"
DECLARED_HARNESS = "RESEARCH_CANONICALIZATION_HARNESS_V1"
DECLARED_STATE_MACHINE = "RESEARCH_CANONICALIZATION_STATE_MACHINE_V1"
GATE_ID = "canonical_knowledge_commit_gate"
FIXTURE_NAME = "cae-m060-research-canonicalization"

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ARTIFACT_DIR = REPO_ROOT / ".cae-m060-artifacts"
MEDIA_FIXTURE = REPO_ROOT / "tests" / "api" / "fixtures" / "synthetic_interview.mp4"
TEXT_FIXTURE = REPO_ROOT / "tests" / "api" / "fixtures" / "untimed.txt"


class ProductE2EFixtureError(RuntimeError):
    """Raised for a fixture or evidence-contract failure."""


def _install_import_compatibility() -> None:
    """Make the repository's optional app dependencies importable without faking CAE runtime stages."""
    extra_paths = [
        REPO_ROOT / "packages" / "ca_contracts" / "src",
        REPO_ROOT / "packages" / "ca_runtime" / "src",
        REPO_ROOT / "packages" / "ca_delegation_rc4" / "src",
        *(sorted(REPO_ROOT.glob("services/*/src"))),
    ]
    for path in reversed(extra_paths):
        if path.is_dir() and str(path) not in sys.path:
            sys.path.insert(0, str(path))

    if "psycopg" not in sys.modules:
        try:
            __import__("psycopg")
        except ModuleNotFoundError:
            psycopg = types.ModuleType("psycopg")
            psycopg.Connection = object
            psycopg.Cursor = object
            psycopg.connect = lambda *_a, **_k: (_ for _ in ()).throw(
                RuntimeError("psycopg is unavailable in the fixture sandbox; SQLite is the governed local proof store")
            )
            psycopg_types = types.ModuleType("psycopg.types")
            psycopg_json = types.ModuleType("psycopg.types.json")
            psycopg_json.Jsonb = lambda value: value
            psycopg_types.json = psycopg_json
            psycopg.types = psycopg_types
            sys.modules.update(
                {
                    "psycopg": psycopg,
                    "psycopg.types": psycopg_types,
                    "psycopg.types.json": psycopg_json,
                }
            )

    missing_optional = {
        "cmf_builder.application.manifest_parser": {"OperatorManifestParser": type("OperatorManifestParser", (), {})},
        "cmf_builder.application.productization_contracts": {"OperatorManifestRequest": type("OperatorManifestRequest", (), {})},
        "cmf_builder.domain.portable_export": {
            "PortableAtomicHarnessDefinition": type("PortableAtomicHarnessDefinition", (), {}),
            "PortableDefinitionInvalid": type("PortableDefinitionInvalid", (Exception,), {}),
        },
    }
    for fullname, attrs in missing_optional.items():
        if fullname in sys.modules:
            continue
        parts = fullname.split(".")
        for index in range(1, len(parts)):
            package_name = ".".join(parts[:index])
            if package_name not in sys.modules:
                sys.modules[package_name] = types.ModuleType(package_name)
        module = types.ModuleType(fullname)
        for name, value in attrs.items():
            setattr(module, name, value)
        sys.modules[fullname] = module

    if "cmf_vae.application" not in sys.modules:
        cmf_vae = types.ModuleType("cmf_vae")
        cmf_vae_application = types.ModuleType("cmf_vae.application")
        cmf_vae_application.VAEApplication = type("VAEApplication", (), {})
        cmf_vae.application = cmf_vae_application
        sys.modules.update({"cmf_vae": cmf_vae, "cmf_vae.application": cmf_vae_application})


_install_import_compatibility()

from ca_contracts import canonical_sha256  # noqa: E402
from ca_runtime.pi_adapter import AuthorityLane  # noqa: E402
from ca_runtime.program_operator_runtime import ProgramOperatorRuntimeService  # noqa: E402
from ca_runtime.program_registry import ProgramRegistry  # noqa: E402
from ca_runtime.program_state_runtime import (  # noqa: E402
    ProgramStateAggregate,
    ProgramStateLifecycle,
    ProgramTransitionBlockedError,
    SqliteProgramStateStore,
    UniversalProgramStateRuntime,
)


TRANSITIONS: tuple[tuple[str, AuthorityLane, tuple[str, ...], str], ...] = (
    (
        "attach_sources",
        AuthorityLane.COMMANDER,
        ("workspace_active", "sources_verified"),
        "cae.research.attach_sources@1.0.0",
    ),
    (
        "extract_candidates",
        AuthorityLane.HUNTER,
        ("workspace_active", "sources_attached"),
        "cae.research.extract_candidates@1.0.0",
    ),
    (
        "canonicalize_candidates",
        AuthorityLane.ANALYST,
        ("workspace_active", "candidates_extracted", "false_merge_verified"),
        "cae.research.canonicalize@1.0.0",
    ),
    (
        "project_okf_bundle",
        AuthorityLane.COMPOSER,
        ("workspace_active", "canonical_nodes_resolved"),
        "cae.research.project_okf@1.0.0",
    ),
)

EXPECTED_STATE_PATH: tuple[str, ...] = (
    "INITIAL",
    "SOURCES_ATTACHED",
    "CANDIDATES_EXTRACTED",
    "CANONICALIZED",
    "OKF_PROJECTED",
)



def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()



def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())



def stable_digest(value: Any) -> str:
    return canonical_sha256(value)



def _json_dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, default=str), encoding="utf-8")


@dataclass(frozen=True)
class FixtureWorkspace:
    """Deterministic on-disk namespace for one product proof run."""

    root: Path
    workspace_id: UUID = field(default_factory=lambda: uuid5(NAMESPACE_URL, f"{MANDATE_ID}:{FIXTURE_NAME}"))

    @property
    def runtime_db(self) -> Path:
        return self.root / "runtime.sqlite3"

    @property
    def seed_file(self) -> Path:
        return self.root / "seed" / "fixture_seed.json"

    @property
    def receipt_dir(self) -> Path:
        return self.root / "evidence" / "receipts"

    @property
    def checkpoint_file(self) -> Path:
        return self.root / "evidence" / "checkpoints.json"

    @property
    def evidence_file(self) -> Path:
        return self.root / "evidence" / "m060_evidence.json"

    @property
    def failure_file(self) -> Path:
        return self.root / "evidence" / "failure.json"

    def prepare(self) -> dict[str, Any]:
        """Create a clean workspace and seed the real product input boundary."""
        if self.root.exists():
            if any(self.root.iterdir()):
                raise ProductE2EFixtureError(f"Fixture workspace is not clean: {self.root}")
        self.root.mkdir(parents=True, exist_ok=True)
        self.receipt_dir.mkdir(parents=True, exist_ok=True)

        for fixture in (MEDIA_FIXTURE, TEXT_FIXTURE):
            if not fixture.is_file():
                raise ProductE2EFixtureError(f"Required repository fixture is missing: {fixture}")

        seed = {
            "mandate_id": MANDATE_ID,
            "invariant": MANDATE_INVARIANT,
            "fixture_name": FIXTURE_NAME,
            "workspace_id": str(self.workspace_id),
            "program": {
                "id": PROGRAM_ID,
                "version": EXPECTED_PROGRAM_VERSION,
                "declared_harness": DECLARED_HARNESS,
                "declared_state_machine": DECLARED_STATE_MACHINE,
            },
            "source_records": [
                {
                    "source_record_id": "m060-source-001",
                    "kind": "text-fixture-reference",
                    "path": TEXT_FIXTURE.relative_to(REPO_ROOT).as_posix(),
                    "sha256": sha256_file(TEXT_FIXTURE),
                    "immutable": True,
                }
            ],
            "media_fixture_references": [
                {
                    "asset_id": "m060-media-001",
                    "path": MEDIA_FIXTURE.relative_to(REPO_ROOT).as_posix(),
                    "sha256": sha256_file(MEDIA_FIXTURE),
                    "reference_only": True,
                }
            ],
            "initial_state": {
                "fixture_name": FIXTURE_NAME,
                "source_record_refs": ["m060-source-001"],
                "source_evidence_hashes": [sha256_file(TEXT_FIXTURE)],
                "media_fixture_refs": ["m060-media-001"],
            },
        }
        seed["seed_sha256"] = stable_digest(seed)
        _json_dump(self.seed_file, seed)
        _json_dump(self.root / "workspace.json", {
            "workspace_id": str(self.workspace_id),
            "fixture_root": str(self.root),
            "clean_before_seed": True,
            "seed_sha256": seed["seed_sha256"],
        })
        return seed

    def clean_reset(self, *, preserve_failed_evidence: bool = True) -> None:
        """Remove only the controlled fixture namespace; failed evidence can be retained."""
        if not self.root.exists():
            return
        if preserve_failed_evidence and self.failure_file.exists():
            preserved = self.failure_file.read_bytes()
            archive_dir = self.root.parent / f"{self.root.name}.failed"
            archive_dir.mkdir(parents=True, exist_ok=True)
            (archive_dir / self.failure_file.name).write_bytes(preserved)
        shutil.rmtree(self.root)


class RuntimeHealthCheck:
    """Verifies that the test is bound to actual CAE runtime components, not a mock adapter."""

    def __init__(self, registry: ProgramRegistry, runtime: UniversalProgramStateRuntime) -> None:
        self.registry = registry
        self.runtime = runtime

    def run(self, workspace_id: str) -> dict[str, Any]:
        package = self.registry.get_program(PROGRAM_ID, EXPECTED_PROGRAM_VERSION)
        machine = self.runtime.get_state_machine(PROGRAM_ID)
        preflight = self.registry.preflight(
            program_id=PROGRAM_ID,
            workspace_id=workspace_id,
            context_refs=("workspace_active", "sources_verified", "false_merge_verified"),
            version=EXPECTED_PROGRAM_VERSION,
        )
        checks = {
            "registry_loaded": package.program_id == PROGRAM_ID,
            "manifest_version_pinned": package.manifest.version == EXPECTED_PROGRAM_VERSION,
            "state_machine_pinned": machine.machine_id == DECLARED_STATE_MACHINE,
            "sqlite_state_store": type(self.runtime.store) is SqliteProgramStateStore,
            "preflight_eligible": preflight.eligible,
            "declared_harness_present_in_manifest": package.manifest.harness == DECLARED_HARNESS,
        }
        if not all(checks.values()):
            raise ProductE2EFixtureError(f"Runtime health check failed: {checks}; issues={preflight.issues}")
        return {
            "checks": checks,
            "program": {
                "id": package.program_id,
                "version": package.version,
                "manifest_sha256": package.manifest_sha256,
                "package_sha256": package.package_sha256,
                "harness": package.manifest.harness,
                "state_machine": package.manifest.state_machine,
            },
            "preflight": preflight.model_dump(mode="json"),
            "runtime": {
                "state_authority": "cae.universal_program_state_runtime",
                "runtime_component": "ca_runtime.UniversalProgramStateRuntime",
                "state_store": type(self.runtime.store).__name__,
                "external_provider_mocks": False,
            },
        }


class CheckpointAsserter:
    """Assert semantic product checkpoints while excluding run-specific IDs/timestamps."""

    def assert_checkpoint(self, stage: str, aggregate: ProgramStateAggregate, expected_state: str) -> dict[str, Any]:
        if aggregate.current_state != expected_state:
            raise ProductE2EFixtureError(
                f"Checkpoint {stage} expected state {expected_state}, got {aggregate.current_state}"
            )
        if aggregate.workspace_id == "":
            raise ProductE2EFixtureError(f"Checkpoint {stage} has an empty workspace ID")
        return {
            "stage": stage,
            "state": aggregate.current_state,
            "lifecycle": aggregate.lifecycle.value,
            "state_data_digest": stable_digest(aggregate.state_data),
        }

    def assert_gate(self, aggregate: ProgramStateAggregate, gate_id: str) -> dict[str, Any]:
        if aggregate.lifecycle != ProgramStateLifecycle.AWAITING_APPROVAL:
            raise ProductE2EFixtureError(
                f"Gate checkpoint expected AWAITING_APPROVAL, got {aggregate.lifecycle.value}"
            )
        snapshot = aggregate.state_data.get("gate_suspension")
        if not isinstance(snapshot, dict):
            raise ProductE2EFixtureError("Gate checkpoint is missing its durable suspension payload")
        raw_snapshot = snapshot.get("snapshot")
        if not isinstance(raw_snapshot, dict) or raw_snapshot.get("gate_id") != gate_id:
            raise ProductE2EFixtureError(
                f"Gate checkpoint expected declared gate {gate_id}, got {raw_snapshot}"
            )
        return {
            "stage": "gate",
            "gate_id": gate_id,
            "state": aggregate.current_state,
            "lifecycle": aggregate.lifecycle.value,
            "snapshot_hash": raw_snapshot.get("snapshot_hash"),
        }

    def deterministic_signature(self, aggregate: ProgramStateAggregate, transitions: Sequence[Any]) -> dict[str, Any]:
        gate = aggregate.state_data.get("gate_suspension") or {}
        gate_snapshot = gate.get("snapshot") if isinstance(gate, dict) else {}
        gate_event = gate.get("event") if isinstance(gate, dict) else {}
        stable_state_data = {
            "fixture_name": aggregate.state_data.get("fixture_name"),
            "source_record_refs": aggregate.state_data.get("source_record_refs", []),
            "source_evidence_hashes": aggregate.state_data.get("source_evidence_hashes", []),
            "media_fixture_refs": aggregate.state_data.get("media_fixture_refs", []),
            "gate_suspensions": [
                {"gate_id": item.get("gate_id"), "state_version": item.get("state_version")}
                for item in aggregate.state_data.get("gate_suspensions", [])
                if isinstance(item, dict)
            ],
            "gate_snapshot": {
                "gate_id": gate_snapshot.get("gate_id"),
                "required_lane": gate_snapshot.get("required_lane"),
                "current_state": gate_snapshot.get("current_state"),
                "node_id": gate_snapshot.get("node_id"),
                "candidate_outputs": gate_snapshot.get("candidate_outputs", {}),
                "violations": gate_snapshot.get("violations", []),
                "thresholds": gate_snapshot.get("thresholds", {}),
            },
            "gate_event": {
                "gate_id": gate_event.get("gate_id"),
                "invariant": gate_event.get("invariant"),
                "reason_code": gate_event.get("reason_code"),
                "required_lane": gate_event.get("required_lane"),
                "violations": gate_event.get("violations", []),
                "thresholds": gate_event.get("thresholds", {}),
            },
        }
        return {
            "program_id": aggregate.program_id,
            "program_version": aggregate.program_version,
            "current_state": aggregate.current_state,
            "lifecycle": aggregate.lifecycle.value,
            "state_data_semantics_digest": stable_digest(stable_state_data),
            "transition_signature": [
                {
                    "transition_name": t.transition_name,
                    "from_state": t.from_state,
                    "to_state": t.to_state,
                    "lane": t.lane.value,
                    "actor_id": t.actor_id,
                    "trigger_operation": t.trigger_operation,
                    "payload_digest": stable_digest(t.payload),
                }
                for t in transitions
            ],
        }


class ReceiptCollector:
    """Persist run evidence, receipts, checkpoints, and explicit proof limitations."""

    def __init__(self, workspace: FixtureWorkspace) -> None:
        self.workspace = workspace
        self.receipts: list[dict[str, Any]] = []
        self.checkpoints: list[dict[str, Any]] = []

    def add_receipt(self, label: str, receipt: Mapping[str, Any]) -> None:
        payload = {"label": label, "receipt": dict(receipt)}
        self.receipts.append(payload)
        receipt_id = str(payload["receipt"].get("receipt_id", label))
        _json_dump(self.workspace.receipt_dir / f"{receipt_id}.json", payload)

    def add_checkpoint(self, checkpoint: Mapping[str, Any]) -> None:
        self.checkpoints.append(dict(checkpoint))
        _json_dump(self.workspace.checkpoint_file, self.checkpoints)

    def write_evidence(self, evidence: Mapping[str, Any]) -> Path:
        _json_dump(self.workspace.evidence_file, {
            **dict(evidence),
            "receipts": self.receipts,
            "checkpoints": self.checkpoints,
        })
        return self.workspace.evidence_file

    def write_failure(self, failure: BaseException, *, step: str, diagnostic: Mapping[str, Any]) -> Path:
        payload = {
            "invariant": MANDATE_INVARIANT,
            "status": "EXPECTED_FAILURE" if isinstance(failure, ProgramTransitionBlockedError) else "FAILURE",
            "step": step,
            "exception": type(failure).__name__,
            "message": str(failure),
            "diagnostic": dict(diagnostic),
        }
        _json_dump(self.workspace.failure_file, payload)
        return self.workspace.failure_file


class ProductE2ERunner:
    """Executes the real research Program boundary in a fresh durable workspace."""

    def __init__(self, workspace: FixtureWorkspace) -> None:
        self.workspace = workspace
        self.registry = ProgramRegistry(discovery_roots=[REPO_ROOT / "programs"])
        self.registry.discover()
        self.store: SqliteProgramStateStore | None = None
        self.runtime: UniversalProgramStateRuntime | None = None
        self.operator: ProgramOperatorRuntimeService | None = None
        self.health: RuntimeHealthCheck | None = None
        self.checkpoints = CheckpointAsserter()
        self.receipts = ReceiptCollector(workspace)

    def _initialize_runtime(self) -> None:
        self.store = SqliteProgramStateStore(self.workspace.runtime_db)
        self.runtime = UniversalProgramStateRuntime(store=self.store, program_registry=self.registry)
        self.operator = ProgramOperatorRuntimeService(runtime=self.runtime, program_registry=self.registry)
        self.health = RuntimeHealthCheck(self.registry, self.runtime)

    def _assert_clean_runtime(self) -> None:
        if self.runtime is None:
            raise ProductE2EFixtureError("Runtime is not initialized")
        preexisting = self.runtime.list_aggregates(workspace_id=str(self.workspace.workspace_id), program_id=PROGRAM_ID)
        if preexisting:
            raise ProductE2EFixtureError(
                "False-proof protection failed: pre-existing program aggregate exists in the clean fixture workspace"
            )

    def run(self) -> dict[str, Any]:
        seed = self.workspace.prepare()
        self._initialize_runtime()
        self._assert_clean_runtime()
        assert self.health is not None
        health = self.health.run(str(self.workspace.workspace_id))
        self.receipts.write_evidence({
            "invariant": MANDATE_INVARIANT,
            "status": "RUNNING",
            "health": health,
            "seed_sha256": seed["seed_sha256"],
        })

        initial_claims = ("workspace_active", "sources_verified", "false_merge_verified")
        assert self.operator is not None
        assert self.store is not None
        assert self.runtime is not None
        started = self.operator.run_program(
            program_id=PROGRAM_ID,
            workspace_id=str(self.workspace.workspace_id),
            actor_id="m060-command-operator",
            initial_data=seed["initial_state"],
            context_claims=initial_claims,
        )
        self.receipts.add_receipt("run", {"receipt_id": started.last_receipt_id, "state_hash": started.state_hash, "lifecycle": started.lifecycle.value})
        self.receipts.add_checkpoint(self.checkpoints.assert_checkpoint("run", started, "INITIAL"))
        self.receipts.receipts[-1]["lease"] = self.store.get_execution_lease(started.aggregate_id) or {}

        aggregate = started
        for transition_name, lane, claims, operation in TRANSITIONS:
            payload: dict[str, Any] = {
                "fixture_name": FIXTURE_NAME,
                "source_record_refs": seed["initial_state"]["source_record_refs"],
                "source_evidence_hashes": seed["initial_state"]["source_evidence_hashes"],
                "media_fixture_refs": seed["initial_state"]["media_fixture_refs"],
            }
            if transition_name == "project_okf_bundle":
                payload["gate_id"] = GATE_ID
                payload["candidate_outputs"] = {
                    "canonical_node_count": 1,
                    "okf_bundle_digest": stable_digest({"seed": seed["seed_sha256"], "operation": operation}),
                }
            result = self.runtime.execute_transition(
                aggregate_id=aggregate.aggregate_id,
                transition_name=transition_name,
                payload=payload,
                actor_id={
                    AuthorityLane.COMMANDER: "m060-command-operator",
                    AuthorityLane.HUNTER: "m060-hunter",
                    AuthorityLane.ANALYST: "m060-analyst",
                    AuthorityLane.COMPOSER: "m060-composer",
                }[lane],
                actor_lane=lane,
                context_claims=claims,
                expected_version=aggregate.version,
            )
            aggregate = result.aggregate
            self.receipts.add_receipt(transition_name, result.receipt if isinstance(result.receipt, Mapping) else {"receipt_id": result.receipt_id})
            expected_state = {
                "attach_sources": "SOURCES_ATTACHED",
                "extract_candidates": "CANDIDATES_EXTRACTED",
                "canonicalize_candidates": "CANONICALIZED",
                "project_okf_bundle": "OKF_PROJECTED",
            }[transition_name]
            if transition_name == "project_okf_bundle":
                self.receipts.add_checkpoint(self.checkpoints.assert_checkpoint(transition_name, aggregate, expected_state))
                self.receipts.add_checkpoint(self.checkpoints.assert_gate(aggregate, GATE_ID))
            else:
                self.receipts.add_checkpoint(self.checkpoints.assert_checkpoint(transition_name, aggregate, expected_state))

        transitions = self.store.list_transitions(aggregate.aggregate_id)
        if [t.transition_name for t in transitions] != [
            "attach_sources",
            "extract_candidates",
            "canonicalize_candidates",
            "project_okf_bundle",
            "gate_suspend:canonical_knowledge_commit_gate",
        ]:
            raise ProductE2EFixtureError(
                f"Unexpected durable transition sequence: {[t.transition_name for t in transitions]}"
            )

        signature = self.checkpoints.deterministic_signature(aggregate, transitions)
        evidence = {
            "invariant": MANDATE_INVARIANT,
            "status": "PASS",
            "mandate_id": MANDATE_ID,
            "fixture": {
                "workspace_id": str(self.workspace.workspace_id),
                "root": str(self.workspace.root),
                "seed_sha256": seed["seed_sha256"],
                "runtime_db_sha256": sha256_file(self.workspace.runtime_db),
            },
            "environment": {
                "python": sys.version.split()[0],
                "platform": sys.platform,
                "runtime": health["runtime"],
            },
            "product_boundary": {
                "program_id": PROGRAM_ID,
                "program_version": EXPECTED_PROGRAM_VERSION,
                "declared_harness": DECLARED_HARNESS,
                "state_machine": DECLARED_STATE_MACHINE,
                "checkpoint_states": list(EXPECTED_STATE_PATH),
                "final_verified_state": aggregate.current_state,
                "final_lifecycle": aggregate.lifecycle.value,
                "durable_transition_count": len(transitions),
            },
            "receipts": {
                "run_receipt_id": started.last_receipt_id,
                "transition_receipt_ids": [t.receipt_id for t in transitions],
                "unique_receipt_ids": len({t.receipt_id for t in transitions}),
            },
            "deterministic_signature": signature,
            "evidence_classes": ["EXECUTABLE", "REGISTRY_SOURCE", "TEST", "DOCUMENT"],
            "what_verifier_measures": [
                "clean fixture workspace before dispatch",
                "real ProgramRegistry package discovery and preflight",
                "real ProgramOperatorRuntimeService run entrypoint",
                "real UniversalProgramStateRuntime transitions and gate suspension",
                "durable SQLite aggregate, lease, transition, and receipt identities",
                "stable semantic checkpoint signature across independent clean runs",
            ],
            "what_verifier_does_not_measure": [
                "production PostgreSQL connectivity",
                "external model/provider reachability",
                "native OpenChatCut process execution",
                "human approval quality",
                "the missing repository executable binding for the declared harness identifier",
            ],
            "false_proof_countercase": {
                "attack": "reuse an earlier SQLite aggregate and report its terminal checkpoint without reseeding or redispatching",
                "defense": "clean workspace reset plus pre-dispatch aggregate emptiness check plus per-run receipt identities and seed digest",
                "expected_result": "reuse is rejected before product execution because pre-existing aggregate state makes the workspace non-clean",
            },
            "environment_fidelity_requirement": "The local proof is E3_PRODUCTION_SHAPED: real CAE runtime/state authority with SQLite; production-readiness still requires the governed service environment and optional production dependencies.",
            "operator_validation_required": True,
        }
        self.receipts.write_evidence(evidence)
        return evidence

    def run_expected_failure(self) -> dict[str, Any]:
        seed = self.workspace.prepare()
        self._initialize_runtime()
        self._assert_clean_runtime()
        assert self.operator is not None
        assert self.runtime is not None
        try:
            self.operator.run_program(
                program_id=PROGRAM_ID,
                workspace_id=str(self.workspace.workspace_id),
                actor_id="m060-negative-operator",
                initial_data=seed["initial_state"],
                context_claims=("workspace_active", "sources_verified"),
            )
        except ProgramTransitionBlockedError as exc:
            if self.runtime.list_aggregates(workspace_id=str(self.workspace.workspace_id), program_id=PROGRAM_ID):
                raise ProductE2EFixtureError("Negative fixture created an aggregate despite failed preflight") from exc
            self.receipts.write_failure(
                exc,
                step="run/preflight",
                diagnostic={
                    "missing_precondition": "false_merge_verified",
                    "workspace_id": str(self.workspace.workspace_id),
                    "aggregates_after_failure": 0,
                },
            )
            return json.loads(self.workspace.failure_file.read_text(encoding="utf-8"))
        raise ProductE2EFixtureError("Intentionally failing fixture unexpectedly passed")


def run_twice_from_clean_state(base_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    run_one_dir = base_dir / "run-one"
    run_two_dir = base_dir / "run-two"
    for path in (run_one_dir, run_two_dir):
        if path.exists():
            raise ProductE2EFixtureError(f"Refusing to reuse non-clean deterministic-run directory: {path}")

    first = ProductE2ERunner(FixtureWorkspace(run_one_dir)).run()
    second = ProductE2ERunner(FixtureWorkspace(run_two_dir)).run()
    if first["deterministic_signature"] != second["deterministic_signature"]:
        raise ProductE2EFixtureError(
            "Deterministic checkpoint mismatch across two clean runs: "
            f"first={first['deterministic_signature']} second={second['deterministic_signature']}"
        )
    return first, second


def clean_reset(path: Path) -> None:
    """CLI clean reset for a controlled M060 fixture namespace."""
    workspace = FixtureWorkspace(path)
    workspace.clean_reset(preserve_failed_evidence=True)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CAE-M060 product E2E fixture harness")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="run the real product boundary from a clean workspace")
    run.add_argument("--workspace-root", type=Path, default=DEFAULT_ARTIFACT_DIR / "single-run")

    repeat = sub.add_parser("repeat", help="run the real product boundary twice from clean workspaces")
    repeat.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_DIR / "repeat")

    negative = sub.add_parser("negative", help="run the intentionally failing fixture and capture diagnostics")
    negative.add_argument("--workspace-root", type=Path, default=DEFAULT_ARTIFACT_DIR / "negative")

    reset = sub.add_parser("clean-reset", help="remove only the controlled fixture namespace")
    reset.add_argument("workspace_root", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)
    if args.command == "run":
        evidence = ProductE2ERunner(FixtureWorkspace(args.workspace_root)).run()
        print(json.dumps({"status": evidence["status"], "evidence": str(FixtureWorkspace(args.workspace_root).evidence_file)}, sort_keys=True))
        return 0
    if args.command == "repeat":
        first, second = run_twice_from_clean_state(args.artifact_root)
        print(json.dumps({
            "status": "PASS",
            "runs": 2,
            "deterministic_signature": first["deterministic_signature"],
            "evidence": [
                str(args.artifact_root / "run-one" / "evidence" / "m060_evidence.json"),
                str(args.artifact_root / "run-two" / "evidence" / "m060_evidence.json"),
            ],
            "receipt_identity_distinct": first["receipts"]["run_receipt_id"] != second["receipts"]["run_receipt_id"],
        }, sort_keys=True))
        return 0
    if args.command == "negative":
        failure = ProductE2ERunner(FixtureWorkspace(args.workspace_root)).run_expected_failure()
        print(json.dumps(failure, sort_keys=True))
        return 0
    if args.command == "clean-reset":
        clean_reset(args.workspace_root)
        print(json.dumps({"status": "CLEAN", "workspace_root": str(args.workspace_root)}, sort_keys=True))
        return 0
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())


def test_m060_real_runtime_happy_path(tmp_path: Path) -> None:
    evidence = ProductE2ERunner(FixtureWorkspace(tmp_path / "happy")).run()
    assert evidence["status"] == "PASS"
    assert evidence["invariant"] == MANDATE_INVARIANT
    assert evidence["product_boundary"]["program_id"] == PROGRAM_ID
    assert evidence["product_boundary"]["final_verified_state"] == "OKF_PROJECTED"
    assert evidence["product_boundary"]["final_lifecycle"] == "AWAITING_APPROVAL"
    assert evidence["product_boundary"]["durable_transition_count"] == 5
    assert evidence["receipts"]["unique_receipt_ids"] == 5
    assert evidence["operator_validation_required"] is True


def test_m060_deterministic_checkpoints_from_two_clean_runs(tmp_path: Path) -> None:
    first, second = run_twice_from_clean_state(tmp_path / "repeat")
    assert first["deterministic_signature"] == second["deterministic_signature"]
    assert first["fixture"]["workspace_id"] == second["fixture"]["workspace_id"]
    assert first["receipts"]["run_receipt_id"] != second["receipts"]["run_receipt_id"]


def test_m060_intentionally_failing_fixture_is_diagnosable(tmp_path: Path) -> None:
    failure = ProductE2ERunner(FixtureWorkspace(tmp_path / "negative")).run_expected_failure()
    assert failure["status"] == "EXPECTED_FAILURE"
    assert failure["exception"] == "ProgramTransitionBlockedError"
    assert failure["diagnostic"]["missing_precondition"] == "false_merge_verified"
    assert failure["diagnostic"]["aggregates_after_failure"] == 0


def test_m060_false_proof_reuse_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "reuse"
    first = ProductE2ERunner(FixtureWorkspace(root)).run()
    assert first["status"] == "PASS"
    reused = ProductE2ERunner(FixtureWorkspace(root))
    try:
        reused.run()
    except ProductE2EFixtureError as exc:
        assert "not clean" in str(exc).lower() or "pre-existing" in str(exc).lower()
    else:
        raise AssertionError("False-proof countercase was not rejected")


def test_m060_clean_reset_removes_only_controlled_namespace(tmp_path: Path) -> None:
    root = tmp_path / "reset"
    runner = ProductE2ERunner(FixtureWorkspace(root))
    runner.run_expected_failure()
    failure_copy = root.parent / f"{root.name}.failed" / "failure.json"
    clean_reset(root)
    assert not root.exists()
    assert failure_copy.exists()
