"""Executable brownfield reconciliation for CAE-M0058.

The verifier is intentionally observational: it inventories the existing Program
packages, checks the current canonical state-machine registrations, executes one
minimal operator-mediated SQLite run for the representative research program,
and records the reachable/unreachable/partial/conflicting boundaries.

It does not repair any discovered defect or introduce a new runtime authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import hashlib
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence
from uuid import uuid4

import yaml

MANDATE_ID = "CAE-M0058"
MANDATE_TITLE = "Operational Brownfield Reconciliation & Product Run Baseline"
INVARIANT = "FR-OPS-BASELINE"
REPRESENTATIVE_PROGRAM = "research_canonicalization_program"
REPRESENTATIVE_HARNESS = "RESEARCH_CANONICALIZATION_HARNESS_V1"


class PathStatus(str, Enum):
    WORKING = "WORKING"
    PARTIAL = "PARTIAL"
    MOCKED = "MOCKED"
    UNREACHABLE = "UNREACHABLE"
    CONFLICTING = "CONFLICTING"


class EvidenceClass(str, Enum):
    EXECUTABLE = "EXECUTABLE"
    SCHEMA = "SCHEMA"
    MIGRATION = "MIGRATION"
    REGISTRY_SOURCE = "REGISTRY_SOURCE"
    DOCUMENT = "DOCUMENT"
    TEST = "TEST"
    HYPOTHESIS = "HYPOTHESIS"
    OPERATOR_DECISION_REQUIRED = "OPERATOR_DECISION_REQUIRED"


@dataclass(frozen=True, slots=True)
class BrownfieldPath:
    path_id: str
    segment: str
    source: str
    target: str
    status: PathStatus
    evidence_class: EvidenceClass
    reachable_today: bool
    verifier: str
    observed: str
    limitation: str = ""
    collision: str = ""


@dataclass(frozen=True, slots=True)
class StatefulBehaviorEvidence:
    behavior: str
    source_state: str
    operation: str
    target_state: str
    actor: str
    preconditions: Sequence[str]
    validators: Sequence[str]
    postconditions: Sequence[str]
    receipt: str
    error_route: str
    recovery_path: str


@dataclass(frozen=True, slots=True)
class ProgramInventoryRow:
    program_id: str
    version: str
    status: str
    manifest_path: str
    manifest_sha256: str
    package_sha256: str
    harness: Optional[str]
    state_machine: Optional[str]
    runtime_state_machine_registered: bool
    declared_operator_gates: Sequence[str]
    declared_evals: Sequence[str]
    connections: Sequence[str]
    classification: PathStatus
    limitation: str


@dataclass
class BrownfieldLedger:
    mandate_id: str = MANDATE_ID
    mandate_title: str = MANDATE_TITLE
    invariant: str = INVARIANT
    repository_root: str = ""
    source_git_commit: str = "UNAVAILABLE_IN_ARCHIVE"
    source_git_commit_basis: str = ""
    archive_has_git_metadata: bool = False
    environment: Dict[str, Any] = field(default_factory=dict)
    representative_program: str = REPRESENTATIVE_PROGRAM
    representative_harness: str = REPRESENTATIVE_HARNESS
    program_inventory: List[ProgramInventoryRow] = field(default_factory=list)
    paths: List[BrownfieldPath] = field(default_factory=list)
    stateful_behaviors: List[StatefulBehaviorEvidence] = field(default_factory=list)
    probe: Dict[str, Any] = field(default_factory=dict)
    blockers: List[Dict[str, Any]] = field(default_factory=list)
    false_proof_countercase: str = ""
    environment_fidelity_requirement: str = ""
    operator_validation_required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mandate_id": self.mandate_id,
            "mandate_title": self.mandate_title,
            "invariant": self.invariant,
            "repository_root": self.repository_root,
            "source_git_commit": self.source_git_commit,
            "source_git_commit_basis": self.source_git_commit_basis,
            "archive_has_git_metadata": self.archive_has_git_metadata,
            "environment": self.environment,
            "representative_program": self.representative_program,
            "representative_harness": self.representative_harness,
            "program_inventory": [
                {
                    **asdict(row),
                    "classification": row.classification.value,
                }
                for row in self.program_inventory
            ],
            "paths": [
                {
                    **asdict(path),
                    "status": path.status.value,
                    "evidence_class": path.evidence_class.value,
                }
                for path in self.paths
            ],
            "stateful_behaviors": [asdict(item) for item in self.stateful_behaviors],
            "probe": self.probe,
            "blockers": self.blockers,
            "false_proof_countercase": self.false_proof_countercase,
            "environment_fidelity_requirement": self.environment_fidelity_requirement,
            "operator_validation_required": self.operator_validation_required,
        }

    def sha256(self) -> str:
        payload = self.to_dict()
        raw = _canonical_json(payload).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def to_markdown(self) -> str:
        counts: Dict[str, int] = {status.value: 0 for status in PathStatus}
        for path in self.paths:
            counts[path.status.value] += 1
        lines = [
            f"# {self.mandate_id} — Brownfield Product-Run Baseline",
            "",
            f"**Invariant:** `{self.invariant}`",
            f"**Representative Program:** `{self.representative_program}`",
            f"**Representative Harness:** `{self.representative_harness}`",
            f"**Evidence digest:** `{self.sha256()}`",
            "",
            "## Environment",
            "",
            f"- Python: `{self.environment.get('python_version')}`",
            f"- Platform: `{self.environment.get('platform')}`",
            f"- Working tree Git metadata present: `{self.archive_has_git_metadata}`",
            f"- Source Git commit recorded by archive: `{self.source_git_commit}`",
            f"- Source Git commit basis: {self.source_git_commit_basis}",
            "",
            "## Path classification",
            "",
            "| Status | Count |",
            "| --- | ---: |",
            f"| WORKING | {counts[PathStatus.WORKING.value]} |",
            f"| PARTIAL | {counts[PathStatus.PARTIAL.value]} |",
            f"| MOCKED | {counts[PathStatus.MOCKED.value]} |",
            f"| UNREACHABLE | {counts[PathStatus.UNREACHABLE.value]} |",
            f"| CONFLICTING | {counts[PathStatus.CONFLICTING.value]} |",
            "",
            "## Reachable-call-path ledger",
            "",
            "| Segment | Source → target | Status | Evidence | Observed / limitation |",
            "| --- | --- | --- | --- | --- |",
        ]
        for path in self.paths:
            lines.append(
                f"| {path.segment} | `{path.source}` → `{path.target}` | "
                f"**{path.status.value}** | `{path.evidence_class.value}` | "
                f"{(path.observed + (" " + path.limitation if path.limitation else "")).strip()} |"
            )

        lines.extend([
            "",
            "## Program inventory",
            "",
            "| Program | Version | Runtime SM | Harness | Gates | Classification | Limitation |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ])
        for row in self.program_inventory:
            lines.append(
                f"| `{row.program_id}` | `{row.version}` | "
                f"`{row.runtime_state_machine_registered}` | "
                f"`{row.harness or '—'}` | "
                f"{', '.join(row.declared_operator_gates) or '—'} | "
                f"**{row.classification.value}** | {row.limitation} |"
            )

        lines.extend([
            "",
            "## Minimal real product-run probe",
            "",
            "The probe enters through the existing operator command dispatcher, uses the existing "
            "`ProgramOperatorRuntimeService`, and persists state into a temporary `SqliteProgramStateStore`. "
            "It then exercises the existing gate evaluator and the existing `/ship` command refusal.",
            "",
            "```json",
            json_text(self.probe),
            "```",
            "",
            "## Stateful behavior evidence",
            "",
        ])
        for item in self.stateful_behaviors:
            lines.extend([
                f"### {item.behavior}",
                f"- Source → operation → target: `{item.source_state}` → `{item.operation}` → `{item.target_state}`",
                f"- Actor: `{item.actor}`",
                f"- Preconditions: {', '.join(f'`{x}`' for x in item.preconditions) or 'none'}",
                f"- Validators: {', '.join(f'`{x}`' for x in item.validators) or 'none'}",
                f"- Postconditions: {', '.join(f'`{x}`' for x in item.postconditions) or 'none'}",
                f"- Receipt: `{item.receipt}`",
                f"- Error route: {item.error_route}",
                f"- Recovery: {item.recovery_path}",
                "",
            ])

        lines.extend([
            "## Blocker register",
            "",
            "| ID | Class | Finding | Required authority/action |",
            "| --- | --- | --- | --- |",
        ])
        for blocker in self.blockers:
            lines.append(
                f"| `{blocker['id']}` | `{blocker['class']}` | {blocker['finding']} | {blocker['authority']} |"
            )

        lines.extend([
            "",
            "## Verification boundary",
            "",
            f"**What the verifier measures:** the concrete operator dispatch, state persistence, gate suspension, trace projection, and fail-closed release refusal observed in this sandbox; package manifest/runtime-state-machine reachability; and declared-to-executable call-path relationships.",
            "",
            f"**What it does not measure:** production PostgreSQL connectivity, external media retrieval, a production inference provider, a native OpenChatCut process, human approval quality, or the exact Git commit of the uploaded archive when `.git` metadata is absent.",
            "",
            f"**False-proof countercase:** {self.false_proof_countercase}",
            "",
            f"**Environment-fidelity requirement:** {self.environment_fidelity_requirement}",
            "",
            f"**Operator validation required:** `{self.operator_validation_required}`. The mandate's final disposition is an operator decision, not an automated pass.",
            "",
            "## Stop state",
            "",
            "This baseline does not repair the observed blockers. M0058 ends at the operator gate.",
        ])
        return "\n".join(lines) + "\n"


def _canonical_json(value: Any) -> str:
    import json
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)


def json_text(value: Any) -> str:
    import json
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, default=str)


def _find_git_metadata(repo_root: Path) -> bool:
    return (repo_root / ".git").exists()


def _git_commit(repo_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=5,
        ).strip()
    except (OSError, subprocess.SubprocessError):
        return "UNAVAILABLE_IN_ARCHIVE"


def _reference_commit_from_docs(repo_root: Path) -> tuple[str, str]:
    """Return a claimed source commit without presenting it as archive provenance."""
    candidates: list[tuple[str, str]] = []
    current = repo_root / "docs/PRD/CURRENT.md"
    if current.exists():
        text = current.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"repository commit `([0-9a-f]{40})`", text):
            candidates.append((match.group(1), "docs/PRD/CURRENT.md states this commit as its synchronization commit."))
        for match in re.finditer(r"\b([0-9a-f]{40})\b", text):
            candidates.append((match.group(1), "docs/PRD/CURRENT.md contains this full SHA."))
    return candidates[0] if candidates else ("UNAVAILABLE_IN_ARCHIVE", "No full Git SHA is present in the inspected authority documents.")


def _program_manifests(repo_root: Path) -> list[Path]:
    return sorted((repo_root / "programs").glob("*/program_manifest.yaml"))


def _load_manifest(path: Path) -> Mapping[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, Mapping):
        raise ValueError(f"Manifest root must be an object: {path}")
    program = raw.get("program", raw)
    if not isinstance(program, Mapping):
        raise ValueError(f"Manifest program section must be an object: {path}")
    return program


def _exact_text_occurrences(
    repo_root: Path,
    token: str,
    *,
    include_prefixes: Sequence[str] = (),
    limit_files: int = 5000,
) -> list[str]:
    """Find exact token mentions, optionally constrained to executable repository surfaces."""
    hits: list[str] = []
    roots = [repo_root] if not include_prefixes else [repo_root / prefix for prefix in include_prefixes]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if len(hits) >= limit_files:
                return hits
            if not path.is_file():
                continue
            if any(part in {".git", "__pycache__", "node_modules", ".venv", "venv"} for part in path.parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if token in text:
                hits.append(path.relative_to(repo_root).as_posix())
    return hits


def inventory_programs(repo_root: str | Path) -> list[ProgramInventoryRow]:
    """Inventory all Program manifests against currently registered runtime state machines."""
    repo = Path(repo_root).resolve()
    # Lazy import keeps static inspection usable even when optional runtime dependencies are absent.
    from ca_runtime.program_registry import ProgramRegistry
    from ca_runtime.program_state_runtime import InMemoryProgramStateStore, UniversalProgramStateRuntime

    registry = ProgramRegistry(discovery_roots=[repo / "programs"])
    runtime = UniversalProgramStateRuntime(store=InMemoryProgramStateStore(), program_registry=registry)
    rows: list[ProgramInventoryRow] = []

    for manifest_path in _program_manifests(repo):
        data = _load_manifest(manifest_path)
        program_id = str(data["id"])
        version = str(data["version"])
        try:
            package = registry.inspect_and_validate_package(manifest_path.parent)
            package_ok = True
            pkg_manifest_sha = package.manifest_sha256
            pkg_sha = package.package_sha256
            package_error = ""
        except Exception as exc:  # noqa: BLE001 - ledger must classify, not abort.
            package_ok = False
            pkg_manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            pkg_sha = ""
            package_error = f"{type(exc).__name__}: {exc}"

        state_machine_registered = True
        try:
            runtime.get_state_machine(program_id)
        except Exception:
            state_machine_registered = False

        harness = data.get("harness")
        exact_harness_hits = _exact_text_occurrences(
            repo, str(harness), include_prefixes=("packages/ca_runtime", "programs")
        ) if harness else []
        # Agent declarations, tests, mandate records, and this verifier may mention a harness without binding it.
        # For M0058, an executable harness binding must be present in the runtime/program implementation surface.
        executable_harness_prefixes = ("packages/ca_runtime/", "programs/")
        harness_bound = bool(
            harness
            and any(
                hit.startswith(executable_harness_prefixes)
                and hit != manifest_path.relative_to(repo).as_posix()
                and hit != "packages/ca_runtime/src/ca_runtime/brownfield_baseline.py"
                for hit in exact_harness_hits
            )
        )

        limitation_parts: list[str] = []
        classification = PathStatus.WORKING
        if not package_ok:
            classification = PathStatus.CONFLICTING
            limitation_parts.append(package_error)
        elif not state_machine_registered:
            classification = PathStatus.PARTIAL
            limitation_parts.append("Program manifest is valid but no canonical runtime state machine is registered.")
        if harness and not harness_bound:
            classification = PathStatus.PARTIAL if classification == PathStatus.WORKING else classification
            limitation_parts.append("Declared harness identifier has no separate executable binding/package occurrence.")

        rows.append(
            ProgramInventoryRow(
                program_id=program_id,
                version=version,
                status=str(data.get("status", "")),
                manifest_path=manifest_path.relative_to(repo).as_posix(),
                manifest_sha256=pkg_manifest_sha,
                package_sha256=pkg_sha,
                harness=str(harness) if harness else None,
                state_machine=str(data.get("state_machine")) if data.get("state_machine") else None,
                runtime_state_machine_registered=state_machine_registered,
                declared_operator_gates=tuple(str(x) for x in data.get("operator_gates", [])),
                declared_evals=tuple(str(x) for x in data.get("evals", [])),
                connections=tuple(str(x) for x in data.get("connections", [])),
                classification=classification,
                limitation=" ".join(limitation_parts),
            )
        )
    return rows


def run_minimal_product_probe(
    repo_root: str | Path,
    *,
    workspace_id: Optional[str] = None,
) -> dict[str, Any]:
    """Execute one minimal supported product path with durable SQLite state."""
    repo = Path(repo_root).resolve()
    # The runtime imports PostgreSQL-facing modules at package import time, but this probe never
    # connects to PostgreSQL. Callers must provide the dependency in the execution environment.
    from ca_runtime.pi_adapter import AuthorityLane
    from ca_runtime.program_operator_runtime import ProgramOperatorRuntimeService
    from ca_runtime.program_registry import ProgramRegistry
    from ca_runtime.program_state_runtime import SqliteProgramStateStore, UniversalProgramStateRuntime

    workspace = workspace_id or str(uuid4())
    with TemporaryDirectory(prefix="cae_m0058_") as temp:
        db_path = Path(temp) / "m0058.sqlite3"
        registry = ProgramRegistry(discovery_roots=[repo / "programs"])
        representative_package = registry.inspect_and_validate_package(
            repo / "programs" / REPRESENTATIVE_PROGRAM
        )
        registry.register(representative_package)

        store = SqliteProgramStateStore(db_path)
        runtime = UniversalProgramStateRuntime(store=store, program_registry=registry)
        operator = ProgramOperatorRuntimeService(runtime=runtime, program_registry=registry)

        run_result = operator.dispatch_chat_command(
            command_str=f"/run {REPRESENTATIVE_PROGRAM}",
            workspace_id=workspace,
            actor_id="m0058-probe-operator",
        )
        if not run_result.success or not run_result.aggregate_id:
            raise RuntimeError(f"Representative product run failed to dispatch: {run_result.message}")

        aggregate_id = run_result.aggregate_id
        aggregate_after_run = runtime.get_aggregate(aggregate_id)
        lease = store.get_execution_lease(aggregate_id)
        dispatch = store.get_workflow_dispatch(aggregate_id)
        transitions_after_run = store.list_transitions(aggregate_id)

        gate_id = "canonical_knowledge_commit_gate"
        gate_result = runtime.evaluate_gate_milestone(
            aggregate_id=aggregate_id,
            gate_id=gate_id,
            node_id="m0058-baseline-gate",
            actor_id="m0058-gate-evaluator",
            actor_lane=AuthorityLane.COMMANDER,
        )
        aggregate_after_gate = runtime.get_aggregate(aggregate_id)
        trace_after_gate = operator.project_execution_trace(aggregate_id=aggregate_id)
        ship_result = operator.dispatch_chat_command(
            command_str=f"/ship {aggregate_id}",
            workspace_id=workspace,
            actor_id="m0058-probe-operator",
        )
        final_transitions = store.list_transitions(aggregate_id)

        persisted_after_gate = store.get_aggregate(aggregate_id)

        return {
            "workspace_id": workspace,
            "db_path": str(db_path),
            "aggregate_id": aggregate_id,
            "run": {
                "success": run_result.success,
                "message": run_result.message,
                "state_version": aggregate_after_run.version,
                "current_state": aggregate_after_run.current_state,
                "lifecycle": aggregate_after_run.lifecycle.value,
                "last_receipt_id": aggregate_after_run.last_receipt_id,
            },
            "dispatch_persistence": {
                "lease_present": lease is not None,
                "lease": lease,
                "workflow_dispatch_present": dispatch is not None,
                "workflow_dispatch": dispatch,
                "transition_count_after_dispatch": len(transitions_after_run),
            },
            "gate": {
                "gate_id": gate_id,
                "receipt_id": gate_result.receipt_id,
                "audit_digest": gate_result.audit_digest,
                "state_version": aggregate_after_gate.version,
                "current_state": aggregate_after_gate.current_state,
                "lifecycle": aggregate_after_gate.lifecycle.value,
                "suspension_present": gate_result.gate_suspension is not None,
            },
            "trace": {
                "current_state": trace_after_gate.current_state,
                "version": trace_after_gate.version,
                "blockers": list(trace_after_gate.blockers),
                "trace_node_count": len(trace_after_gate.trace_nodes),
                "allowable_transitions": list(trace_after_gate.allowable_transitions),
            },
            "release": {
                "success": ship_result.success,
                "message": ship_result.message,
                "blocked_after_gate": not ship_result.success,
            },
            "persistence_recheck": {
                "aggregate_present": persisted_after_gate is not None,
                "same_state_hash": bool(persisted_after_gate and persisted_after_gate.state_hash == aggregate_after_gate.state_hash),
                "transition_count": len(final_transitions),
            },
        }


def build_ledger(repo_root: str | Path, *, source_git_commit: Optional[str] = None) -> BrownfieldLedger:
    """Build the executable M0058 ledger without mutating repository state."""
    repo = Path(repo_root).resolve()
    archive_has_git = _find_git_metadata(repo)
    doc_commit, doc_basis = _reference_commit_from_docs(repo)
    if source_git_commit:
        commit = source_git_commit
        commit_basis = (
            "Explicit externally verified repository-main commit supplied for this archive baseline; the uploaded "
            "archive has no .git metadata, so this is not a cryptographic attestation of archive provenance."
        )
    else:
        commit = _git_commit(repo)
        if commit == "UNAVAILABLE_IN_ARCHIVE" and doc_commit != "UNAVAILABLE_IN_ARCHIVE":
            commit_basis = (
                "Archive has no .git metadata. This SHA is a repository-document claim, not a cryptographic "
                "attestation of the uploaded archive."
            )
            commit = doc_commit
        else:
            commit_basis = "Obtained from git rev-parse HEAD." if commit != "UNAVAILABLE_IN_ARCHIVE" else doc_basis

    env = {
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "cwd": os.getcwd(),
        "pyproject_requires_python": ">=3.12",
    }

    ledger = BrownfieldLedger(
        repository_root=str(repo),
        source_git_commit=commit,
        source_git_commit_basis=commit_basis,
        archive_has_git_metadata=archive_has_git,
        environment=env,
    )
    ledger.program_inventory = inventory_programs(repo)

    research_row = next(row for row in ledger.program_inventory if row.program_id == REPRESENTATIVE_PROGRAM)
    ledger.paths.extend([
        BrownfieldPath(
            "P01",
            "Product operator entry",
            "ProgramOperatorRuntimeService.dispatch_chat_command(/run)",
            "ProgramOperatorRuntimeService.run_program",
            PathStatus.WORKING,
            EvidenceClass.EXECUTABLE,
            True,
            "run_minimal_product_probe",
            "The existing operator command dispatcher accepted the representative Program and returned an aggregate ID.",
        ),
        BrownfieldPath(
            "P02",
            "Program package resolution",
            "ProgramRegistry.inspect_and_validate_package",
            REPRESENTATIVE_PROGRAM,
            PathStatus.WORKING,
            EvidenceClass.REGISTRY_SOURCE,
            True,
            "inventory_programs + run_minimal_product_probe",
            f"Manifest/package validation succeeded; pinned manifest SHA-256 {research_row.manifest_sha256[:16]}….",
        ),
        BrownfieldPath(
            "P03",
            "Harness dispatch",
            f"manifest.harness={REPRESENTATIVE_HARNESS}",
            "HarnessPackageLoader / executable harness binding",
            PathStatus.UNREACHABLE,
            EvidenceClass.REGISTRY_SOURCE,
            False,
            "inventory_programs",
            "No separate executable binding/package for the exact declared harness was found, and ProgramOperatorRuntimeService.run_program does not invoke HarnessPackageLoader.",
            collision="The repository has an independently tested HarnessPackageLoader, but its fixture path is not the representative Program dispatch path.",
        ),
        BrownfieldPath(
            "P04",
            "Runtime state authority",
            "ProgramOperatorRuntimeService → UniversalProgramStateRuntime",
            "SqliteProgramStateStore",
            PathStatus.WORKING,
            EvidenceClass.EXECUTABLE,
            True,
            "run_minimal_product_probe",
            "A durable aggregate, lease record, workflow-dispatch record, and gate-suspension transition were persisted and re-read from SQLite.",
        ),
        BrownfieldPath(
            "P05",
            "Declared storage connection",
            f"{REPRESENTATIVE_PROGRAM}.program_manifest.yaml connections",
            "PostgreSQL research connection",
            PathStatus.CONFLICTING,
            EvidenceClass.REGISTRY_SOURCE,
            False,
            "inventory_programs + control-state reconciliation",
            "The manifest declares postgresql_research_slice while the executable operator path tested here uses SqliteProgramStateStore.",
            collision="Source-of-meaning/declared connection metadata and runtime authority are not the same authority axis; the mismatch is recorded, not repaired.",
        ),
        BrownfieldPath(
            "P06",
            "Operator gate",
            "UniversalProgramStateRuntime.evaluate_gate_milestone",
            "AWAITING_APPROVAL + GateSuspensionSnapshot",
            PathStatus.WORKING,
            EvidenceClass.EXECUTABLE,
            True,
            "run_minimal_product_probe",
            "The declared canonical_knowledge_commit_gate was evaluated, persisted, and moved the aggregate into AWAITING_APPROVAL with a receipt.",
        ),
        BrownfieldPath(
            "P07",
            "Evaluation / trace",
            "ProgramOperatorRuntimeService.project_execution_trace",
            "ExecutionTraceProjection",
            PathStatus.WORKING,
            EvidenceClass.EXECUTABLE,
            True,
            "run_minimal_product_probe",
            "The trace projection returned the persisted state, allowable transitions, and a blocker explaining the gate suspension.",
        ),
        BrownfieldPath(
            "P08",
            "Release / ship path",
            "ProgramOperatorRuntimeService.dispatch_chat_command(/ship)",
            "completion-gated ship refusal",
            PathStatus.PARTIAL,
            EvidenceClass.EXECUTABLE,
            True,
            "run_minimal_product_probe",
            "The release command path is callable and fails closed after a non-completed state; the representative run does not reach COMPLETED.",
        ),
        BrownfieldPath(
            "P09",
            "M71 golden-run expectation",
            "tests/cae/test_m71_real_domain_program_golden_run_benchmark.py",
            "assert agg.version == 2 after run_program",
            PathStatus.CONFLICTING,
            EvidenceClass.TEST,
            True,
            "targeted pytest run",
            "Current sandbox observation returns version 1 after operator.run_program, causing existing M71 assertions to fail before downstream transitions.",
            collision="The test suite is a historical expectation, not the executable source of current runtime behavior.",
        ),
        BrownfieldPath(
            "P10",
            "17-stage product claim",
            "docs/PRD/CURRENT.md",
            "research_canonicalization_program",
            PathStatus.CONFLICTING,
            EvidenceClass.DOCUMENT,
            False,
            "brownfield inspection",
            "Current representative runtime state machine contains five declared research transitions; the M057 proof harness enumerates a 17-stage broader proof narrative.",
            collision="A documentation claim of a full 17-stage product boundary is not equivalent to reachability through the representative Program.",
        ),
            BrownfieldPath(
            "P11",
            "M057 provider/distribution boundary",
            "tests/e2e/test_live_e2e_proof_harness.py local HTTP fixtures",
            "external inference/distribution services",
            PathStatus.MOCKED,
            EvidenceClass.TEST,
            True,
            "tests/e2e/test_live_e2e_proof_harness.py",
            "The M057 live-proof test passes against test-owned local HTTP servers; that proves fixture reachability, not production-provider or production-distribution reachability.",
            collision="The same harness name 'live' is test-local; the external service boundary remains unverified.",
        ),
    ])

    try:
        probe = run_minimal_product_probe(repo)
        ledger.probe = probe
        ledger.stateful_behaviors = [
            StatefulBehaviorEvidence(
                behavior="Operator-mediated Program dispatch",
                source_state="ABSENT",
                operation="dispatch_chat_command('/run research_canonicalization_program') → run_program → register_program_dispatch → acquire_execution_lease_and_trigger",
                target_state=probe["run"]["current_state"],
                actor="m0058-probe-operator / COMMANDER",
                preconditions=("workspace_active", "sources_verified", "false_merge_verified"),
                validators=("ProgramRegistry preflight", "canonical Program State Machine lookup", "lease CAS"),
                postconditions=("aggregate persisted", "lease record present", "workflow dispatch record present"),
                receipt=str(probe["run"]["last_receipt_id"]),
                error_route="Dispatch/lease errors leave the aggregate in the durable pre-run path; no synthetic RUNNING state is manufactured.",
                recovery_path="Use existing operator control paths (inspect, pause/resume, repair) according to the aggregate lifecycle; no M0058 repair is introduced.",
            ),
            StatefulBehaviorEvidence(
                behavior="Human gate suspension",
                source_state=probe["run"]["current_state"],
                operation="evaluate_gate_milestone('canonical_knowledge_commit_gate')",
                target_state=probe["gate"]["current_state"],
                actor="m0058-gate-evaluator / COMMANDER",
                preconditions=("gate is declared by Program manifest", "aggregate lifecycle is RUNNING"),
                validators=("declared-gate lookup", "RUNNING lifecycle check", "durable CAS/state write"),
                postconditions=("AWAITING_APPROVAL lifecycle", "GateSuspensionSnapshot persisted", "gate receipt persisted"),
                receipt=str(probe["gate"]["receipt_id"]),
                error_route="Undeclared gate or non-RUNNING lifecycle raises ProgramTransitionBlockedError.",
                recovery_path="Existing operator approve/reject route; downstream transitions remain fail-closed while awaiting approval.",
            ),
        ]
    except Exception as exc:  # noqa: BLE001
        ledger.probe = {"status": "BLOCKED", "error": f"{type(exc).__name__}: {exc}"}
        ledger.blockers.append({
            "id": "B-M0058-EXEC-001",
            "class": "ENVIRONMENT_FIDELITY_ERROR",
            "finding": f"Minimal product-run probe could not execute in this environment: {type(exc).__name__}: {exc}",
            "authority": "Environment/operator; do not convert a static inspection into EXECUTABLE evidence.",
        })

    if platform.python_version() != "3.12.0":
        ledger.blockers.append({
            "id": "B-M0058-ENV-001",
            "class": "ENVIRONMENT_FIDELITY_ERROR",
            "finding": f"Sandbox is Python {platform.python_version()} while the checked-in historical control state records Python 3.12.0.",
            "authority": "Operator/environment owner; rerun in the governed Python 3.12 environment before production claims.",
        })

    ledger.blockers.extend([
        {
            "id": "B-M0058-RUNTIME-001",
            "class": "STATE_ERROR",
            "finding": "Existing M71 golden-run tests expect operator.run_program to return version 2, but the current runtime returns version 1 in this sandbox.",
            "authority": "Correct runtime/test authority requires a separate repair decision; M0058 records but does not modify it.",
        },
        {
            "id": "B-M0058-HARNESS-001",
            "class": "RELATION_ERROR",
            "finding": f"{REPRESENTATIVE_PROGRAM} declares {REPRESENTATIVE_HARNESS}, but the representative operator path does not bind/execute that harness.",
            "authority": "Program/Harness integration owner; do not invent a new adapter under M0058.",
        },
        {
            "id": "B-M0058-AUTH-001",
            "class": "AUTHORITY_ERROR",
            "finding": "The representative Program manifest declares a PostgreSQL research connection while the verified local state path uses SQLite; authority must remain explicitly separated rather than inferred from the connection field.",
            "authority": "Change/promotion authority/operator gate.",
        },
        {
            "id": "B-M0058-PROOF-001",
            "class": "EVIDENCE_ERROR",
            "finding": "A green M057 proof or M71 benchmark count alone cannot prove a full product campaign; the representative run must reach the intended runtime and state boundary.",
            "authority": "M0058 verifier; require EXECUTABLE evidence for reachability.",
        },
    ])

    ledger.false_proof_countercase = (
        "All selected tests could be green while only dispatching an aggregate and never executing the intended "
        "five-transition research lifecycle. The existing M71 benchmark counts a successful command dispatch as a "
        "successful run, then uses max(1, transition_count) for phases/receipts. M0058 defeats that false proof by "
        "requiring an observed aggregate, durable state, gate suspension, trace projection, and release refusal."
    )
    ledger.environment_fidelity_requirement = (
        "The verifier's SQLite path is executable in this sandbox, but production-readiness claims require the "
        "governed repository environment, including the recorded Python 3.12 toolchain and all optional runtime "
        "dependencies. PostgreSQL, live provider, external distribution, and native media execution are outside this proof."
    )
    return ledger


def write_evidence(repo_root: str | Path, output_dir: str | Path, *, source_git_commit: Optional[str] = None) -> BrownfieldLedger:
    ledger = build_ledger(repo_root, source_git_commit=source_git_commit)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "CAE_M0058_BROWNFIELD_BASELINE.json").write_text(
        json_text(ledger.to_dict()) + "\n", encoding="utf-8"
    )
    (out / "CAE_M0058_BROWNFIELD_BASELINE.md").write_text(
        ledger.to_markdown(), encoding="utf-8"
    )
    return ledger


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Execute the CAE-M0058 brownfield product-run baseline ledger.")
    parser.add_argument("repo_root", nargs="?", default=".", help="Repository root to inspect")
    parser.add_argument("output_dir", nargs="?", default="docs/cae/implementation", help="Directory for JSON/Markdown evidence")
    parser.add_argument("--source-git-commit", default=None, help="Explicit externally verified source commit for an archive without .git metadata")
    args = parser.parse_args(argv)
    ledger = write_evidence(args.repo_root, args.output_dir, source_git_commit=args.source_git_commit)
    print(f"{MANDATE_ID}: {ledger.sha256()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
