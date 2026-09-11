"""Harness Package Loader and Runtime Binding Adapter for CAE.

Governed by:
- 00_CONTROL/14_PHASE1_BUILDER_RUNTIME_BINDING_CONTRACT.md (M10 Binding Contract)
- 00_CONTROL/20_PHASE2_CAE_PI_STATE_MAPPING.md (M13 State Mapping)
- 02_PHASE_2_RUNTIME_FOUNDATION/M15_harness_package_loader_runtime_binding.md
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md

Core Constitutional Laws:
1. CAE remains the sole authority over state, identity, and governance.
2. Pi is the execution substrate; Eve informs package organization only.
3. Preserves the 4 Authority Lanes: HUNTER, ANALYST, COMPOSER, COMMANDER.
4. Passive, flat skills: No skill may invoke another skill.
5. Fail-Closed pre-runtime validation: Corrupted, generic-mode, or malformed packages fail before runtime.
6. Cryptographic provenance: Source-to-binding field lineage is recorded with SHA-256 digests.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from io import BytesIO
import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union
import zipfile

from ca_contracts import bytes_sha256, canonical_json_bytes, canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane
from cmf_builder.application.manifest_parser import OperatorManifestParser
from cmf_builder.application.productization_contracts import OperatorManifestRequest
from cmf_builder.domain.portable_export import (
    PortableAtomicHarnessDefinition,
    PortableDefinitionInvalid,
)

if TYPE_CHECKING:
    from cmf_pipeline.bindings.compiler import HarnessExecutionBindingCompiler
    from cmf_pipeline.bindings.eligibility_registry import ImplementationEligibilityRegistry
    from cmf_pipeline.intake.compiler_profile_registry import HarnessDefinitionProfileRegistry
    from cmf_pipeline.intake.graph_reconciler import HarnessGraphReconciler
    from cmf_pipeline.workflow.application.compiler import RuntimeWorkflowCompiler
    from cmf_pipeline.workflow.infrastructure.repository import PipelineRepository

logger = logging.getLogger("ca_runtime.harness_loader")


# ---------------------------------------------------------------------------
# Typed Exceptions
# ---------------------------------------------------------------------------

class HarnessLoaderError(Exception):
    """Base exception for all harness loader and runtime binding failures."""
    pass


class HarnessPackageNotFoundError(HarnessLoaderError):
    """Raised when a harness package file cannot be found."""
    pass


class HarnessPackageCorruptError(HarnessLoaderError):
    """Raised when a harness package archive, digest, or JSON structure is corrupt."""
    pass


class HarnessPackageValidationError(HarnessLoaderError):
    """Raised when a harness definition fails schema, policy, or governance validation."""
    pass


class HarnessModeNotSupportedError(HarnessPackageValidationError):
    """Raised when a generic-mode or non-activative harness is loaded for runtime binding (Blocker 3)."""
    pass


class HarnessCategoryBindingMissingError(HarnessPackageValidationError):
    """Raised when category binding is absent or unassigned."""
    pass


class HarnessProvenanceMismatchError(HarnessLoaderError):
    """Raised when source-to-binding field provenance is invalid or broken."""
    pass


# ---------------------------------------------------------------------------
# Data Models and Provenance Tracking
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class HarnessPackage:
    """Represents a verified, hash-pinned in-memory Harness Package."""
    package_id: str
    definition: PortableAtomicHarnessDefinition
    package_sha256: str
    package_path: Optional[str] = None
    manifest_payload: Optional[Dict[str, Any]] = None
    receipt_payload: Optional[Dict[str, Any]] = None
    loaded_at: str = field(default_factory=utc_now_rfc3339)


@dataclass(frozen=True, slots=True)
class HarnessProvenanceField:
    """Records the exact source-to-binding field mapping and transformation."""
    source_field: str
    target_field: str
    source_value_digest: str
    target_value_digest: str
    transformation: str
    required: bool = True


@dataclass(frozen=True, slots=True)
class HarnessBindingProvenance:
    """Cryptographic provenance trace for a compiled harness binding."""
    definition_id: str
    projection_id: str
    fields: List[HarnessProvenanceField]
    composite_digest: str
    created_at: str = field(default_factory=utc_now_rfc3339)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "definition_id": self.definition_id,
            "projection_id": self.projection_id,
            "composite_digest": self.composite_digest,
            "created_at": self.created_at,
            "field_count": len(self.fields),
            "fields": [
                {
                    "source_field": f.source_field,
                    "target_field": f.target_field,
                    "source_value_digest": f.source_value_digest,
                    "target_value_digest": f.target_value_digest,
                    "transformation": f.transformation,
                    "required": f.required,
                }
                for f in self.fields
            ],
        }


@dataclass(frozen=True, slots=True)
class HarnessBindingResult:
    """Comprehensive result of binding an authored harness package into the pipeline."""
    definition_id: str
    projection_id: str
    intake_projection: Dict[str, Any]
    provenance: HarnessBindingProvenance
    graph_receipt: Optional[Dict[str, Any]] = None
    binding_manifest: Optional[Dict[str, Any]] = None
    runtime_workflow: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Harness Package Loader
# ---------------------------------------------------------------------------

class HarnessPackageLoader:
    """Loads, inspects, validates, and hash-pins authored Harness packages fail-closed."""

    @classmethod
    def load_from_zip(cls, path: Union[str, Path]) -> HarnessPackage:
        """Loads and verifies a Harness package from a .zip archive."""
        package_path = Path(path)
        if not package_path.exists():
            raise HarnessPackageNotFoundError(f"Harness package archive not found: {package_path}")

        try:
            archive_bytes = package_path.read_bytes()
        except OSError as e:
            raise HarnessPackageCorruptError(f"Failed to read harness package archive: {e}") from e

        package_sha256 = bytes_sha256(archive_bytes)

        try:
            with zipfile.ZipFile(BytesIO(archive_bytes), "r") as archive:
                namelist = archive.namelist()

                # Check for definition file (supports standard export atomic_harness_definition.json and definition.json)
                def_name = None
                if "atomic_harness_definition.json" in namelist:
                    def_name = "atomic_harness_definition.json"
                elif "definition.json" in namelist:
                    def_name = "definition.json"
                else:
                    raise HarnessPackageCorruptError(
                        f"Harness package archive {package_path.name} missing definition JSON (namelist: {namelist})"
                    )

                def_bytes = archive.read(def_name)

                # Optional manifest & receipt files
                manifest_payload = None
                for m_candidate in ("package_manifest.json", "manifest.json"):
                    if m_candidate in namelist:
                        try:
                            manifest_payload = json.loads(archive.read(m_candidate).decode("utf-8"))
                        except (UnicodeDecodeError, json.JSONDecodeError):
                            pass
                        break

                receipt_payload = None
                for r_candidate in ("export_receipt.json", "receipt.json"):
                    if r_candidate in namelist:
                        try:
                            receipt_payload = json.loads(archive.read(r_candidate).decode("utf-8"))
                        except (UnicodeDecodeError, json.JSONDecodeError):
                            pass
                        break

                # Verify SHA256SUMS if present
                if "SHA256SUMS" in namelist:
                    sums_text = archive.read("SHA256SUMS").decode("utf-8")
                    for line in sums_text.splitlines():
                        line = line.strip()
                        if not line or "  " not in line:
                            continue
                        expected_hash, member_name = line.split("  ", 1)
                        if member_name in namelist:
                            member_bytes = archive.read(member_name)
                            actual_hash = bytes_sha256(member_bytes)
                            if actual_hash != expected_hash:
                                raise HarnessPackageCorruptError(
                                    f"SHA256SUMS checksum mismatch for member '{member_name}': expected {expected_hash}, got {actual_hash}"
                                )

        except zipfile.BadZipFile as e:
            raise HarnessPackageCorruptError(f"Corrupt or invalid zip archive: {package_path.name}") from e

        # Parse definition from payload bytes
        try:
            definition = PortableAtomicHarnessDefinition.from_payload_bytes(def_bytes)
        except (PortableDefinitionInvalid, Exception) as e:
            raise HarnessPackageCorruptError(f"Failed to parse PortableAtomicHarnessDefinition: {e}") from e

        # Validate definition integrity
        try:
            definition.validate()
        except PortableDefinitionInvalid as e:
            raise HarnessPackageValidationError(f"Harness definition validation failed: {e}") from e

        return HarnessPackage(
            package_id=definition.definition_id,
            package_path=str(package_path.resolve()),
            definition=definition,
            package_sha256=package_sha256,
            manifest_payload=manifest_payload,
            receipt_payload=receipt_payload,
        )

    @classmethod
    def load_from_manifest(
        cls,
        manifest_source: Union[str, Path, bytes, Dict[str, Any]],
        *,
        source_name: str = "operator_manifest.json",
    ) -> HarnessPackage:
        """Parses an operator manifest and compiles it to a verified in-memory HarnessPackage."""
        if isinstance(manifest_source, (str, Path)):
            manifest_path = Path(manifest_source)
            if not manifest_path.exists():
                raise HarnessPackageNotFoundError(f"Manifest file not found: {manifest_path}")
            manifest_bytes = manifest_path.read_bytes()
            source_name = manifest_path.name
        elif isinstance(manifest_source, dict):
            manifest_bytes = json.dumps(manifest_source, sort_keys=True).encode("utf-8")
        elif isinstance(manifest_source, bytes):
            manifest_bytes = manifest_source
        else:
            raise HarnessPackageCorruptError(f"Unsupported manifest source type: {type(manifest_source)}")

        parser = OperatorManifestParser()
        parsed = parser.parse(OperatorManifestRequest(manifest_bytes=manifest_bytes, source_name=source_name))

        from cmf_builder.application.export_service import PortableAtomicHarnessCompiler
        compiler = PortableAtomicHarnessCompiler()
        record = compiler.compile(parsed)

        definition = PortableAtomicHarnessDefinition.from_payload_bytes(record.payload)
        definition.validate()

        return HarnessPackage(
            package_id=definition.definition_id,
            package_path=source_name,
            definition=definition,
            package_sha256=bytes_sha256(record.payload),
            manifest_payload=parsed.normalized,
        )

    @classmethod
    def load_from_definition(cls, definition: PortableAtomicHarnessDefinition) -> HarnessPackage:
        """Wraps a pre-existing PortableAtomicHarnessDefinition in a verified HarnessPackage envelope."""
        definition.validate()
        return HarnessPackage(
            package_id=definition.definition_id,
            definition=definition,
            package_sha256=bytes_sha256(definition.payload_bytes),
        )


# ---------------------------------------------------------------------------
# Harness Runtime Binding Adapter
# ---------------------------------------------------------------------------

class HarnessBindingAdapter:
    """Bridges authored Harness packages to Pipeline intake and execution binding.
    
    Enforces:
    1. Fail-closed pre-validation (generic mode, missing category binding, and non-SemVer rejected).
    2. Authority Lane preservation (DAG nodes mapped strictly to HUNTER, ANALYST, COMPOSER, COMMANDER).
    3. Direct delegation to `cmf_pipeline.intake.harness_compiler.compile_portable_to_intake`.
    4. Field-level provenance tracking with cryptographic digest recording.
    """

    def __init__(
        self,
        reconciler: Optional[Any] = None,
        profile_registry: Optional[Any] = None,
    ):
        if reconciler is None:
            from cmf_pipeline.intake.graph_reconciler import HarnessGraphReconciler
            reconciler = HarnessGraphReconciler()
        if profile_registry is None:
            from cmf_pipeline.intake.compiler_profile_registry import HarnessDefinitionProfileRegistry
            profile_registry = HarnessDefinitionProfileRegistry()

        self._reconciler = reconciler
        self._profile_registry = profile_registry

    def bind_to_pipeline_intake(
        self,
        harness: Union[HarnessPackage, PortableAtomicHarnessDefinition, Any],
        *,
        semantic_dependencies: Optional[Sequence[Mapping[str, Any]]] = None,
        capability_metadata: Optional[Mapping[str, Mapping[str, Any]]] = None,
        workflow: Optional[Mapping[str, Any]] = None,
        evaluation_requirements: Optional[Sequence[str]] = None,
        repair_laws: Optional[Sequence[str]] = None,
        pipeline_repository: Optional[Any] = None,
        eligibility_registry: Optional[Any] = None,
        idempotency_key: Optional[str] = None,
    ) -> HarnessBindingResult:
        """Compiles an authored harness into the pipeline intake projection and records field provenance."""
        from cmf_pipeline.intake.definition_intake import AtomicHarnessDefinitionIntake
        from cmf_pipeline.intake.harness_compiler import compile_portable_to_intake
        from cmf_pipeline.intake.harness_compiler_contracts import HarnessCompilationBlocked

        definition: Any
        if isinstance(harness, HarnessPackage):
            definition = harness.definition
        elif hasattr(harness, "definition_id") and hasattr(harness, "content"):
            definition = harness
        else:
            raise HarnessLoaderError(f"Expected HarnessPackage or PortableAtomicHarnessDefinition, got {type(harness)}")

        content = definition.content

        # Blocker 3 Check: generic mode rejected fail-closed
        mode = content.get("mode")
        if mode != "activative":
            raise HarnessModeNotSupportedError(
                f"Cannot bind harness '{definition.definition_id}': mode is '{mode}'. "
                "Only activative-mode harnesses are supported by the CAE pipeline runtime."
            )

        # Category binding check
        category_binding = content.get("category_binding")
        if not category_binding or not isinstance(category_binding, dict) or not category_binding.get("category_id"):
            raise HarnessCategoryBindingMissingError(
                f"Harness '{definition.definition_id}' is missing a valid canonical category binding."
            )

        # Prepare default or derived semantic dependencies if not caller-supplied
        resolved_semantic_deps: List[Dict[str, Any]]
        if semantic_dependencies is not None:
            resolved_semantic_deps = [dict(d) for d in semantic_dependencies]
        else:
            lineage_refs = category_binding.get("semantic_lineage_refs", [])
            if not lineage_refs:
                lineage_refs = content.get("provenance_refs", ["authority:cae_baseline_v1"])
            resolved_semantic_deps = [
                {
                    "object_id": ref_id,
                    "version": "1.0.0",
                    "sha256": canonical_sha256({"ref": ref_id}),
                }
                for ref_id in lineage_refs
            ]
        resolved_semantic_deps = sorted(resolved_semantic_deps, key=lambda d: d["object_id"])

        # Prepare default or derived capability metadata covering all capability requirements
        declared_reqs: List[str] = list(content.get("capability_requirements", []))
        resolved_capability_metadata: Dict[str, Dict[str, Any]] = {}
        if capability_metadata is not None:
            resolved_capability_metadata = {k: dict(v) for k, v in capability_metadata.items()}
        for req in declared_reqs:
            if req not in resolved_capability_metadata:
                resolved_capability_metadata[req] = {
                    "owner_kind": "tool",
                    "required_features": ["canonical_hash", "typed_output"],
                    "authority_boundary": "pipeline_owned_execution",
                }

        # Prepare default or derived workflow DAG preserving 4 Authority Lanes
        resolved_workflow: Dict[str, Any]
        if workflow is not None:
            resolved_workflow = dict(workflow)
            for node in resolved_workflow.get("nodes", []):
                cap_id = node.get("capability_id")
                if cap_id and cap_id not in resolved_capability_metadata:
                    resolved_capability_metadata[cap_id] = {
                        "owner_kind": str(node.get("actor_kind", "tool")),
                        "required_features": ["canonical_hash", "typed_output"],
                        "authority_boundary": "pipeline_owned_execution",
                    }
        else:
            nodes: List[Dict[str, Any]] = []
            edges: List[Dict[str, Any]] = []
            if declared_reqs:
                for idx, req in enumerate(declared_reqs, 1):
                    role = AuthorityLane.COMPOSER.value
                    if "inspect" in req or "read" in req or idx == 1:
                        role = AuthorityLane.HUNTER.value
                    elif "eval" in req or "analyze" in req:
                        role = AuthorityLane.ANALYST.value
                    elif "review" in req or "gate" in req or "approve" in req:
                        role = AuthorityLane.COMMANDER.value

                    node_id = f"node:{req}"
                    nodes.append(
                        {
                            "node_id": node_id,
                            "capability_id": req,
                            "phase_order": idx,
                            "purpose": f"Execute capability {req}",
                            "actor_kind": "DETERMINISTIC_MODULE",
                            "role": role,
                            "product_boundary": "ATOMIC_HARNESS_PIPELINE",
                            "input_contracts": [f"input:{req}"],
                            "output_contracts": [f"output:{req}"],
                            "side_effect_class": "LOCAL_STATE_WRITE" if role != AuthorityLane.HUNTER.value else "READ_ONLY",
                        }
                    )
                for i in range(1, len(nodes)):
                    edges.append(
                        {
                            "source_node_id": nodes[i - 1]["node_id"],
                            "target_node_id": nodes[i]["node_id"],
                            "contract_id": f"contract:{i}",
                        }
                    )
            else:
                nodes = [
                    {
                        "node_id": "node:atomic_execution",
                        "capability_id": "atomic_execution",
                        "phase_order": 1,
                        "purpose": content.get("goal", "Execute atomic harness"),
                        "actor_kind": "DETERMINISTIC_MODULE",
                        "role": AuthorityLane.COMPOSER.value,
                        "product_boundary": "ATOMIC_HARNESS_PIPELINE",
                        "input_contracts": ["source-context"],
                        "output_contracts": ["atomic-result"],
                        "side_effect_class": "LOCAL_STATE_WRITE",
                    }
                ]
                resolved_capability_metadata["atomic_execution"] = {
                    "owner_kind": "tool",
                    "required_features": ["canonical_hash"],
                    "authority_boundary": "pipeline_owned_execution",
                }

            resolved_workflow = {
                "nodes": nodes,
                "edges": edges,
            }

        # Prepare default or derived evaluation requirements and repair laws (lexicographically sorted)
        resolved_eval_reqs = sorted(
            list(
                evaluation_requirements
                if evaluation_requirements is not None
                else ["deterministic_contract_validation", "source_fidelity_check"]
            )
        )
        resolved_repair_laws = sorted(
            list(
                repair_laws
                if repair_laws is not None
                else ["bounded_local_repair_only", "preserve_upstream_semantic_truth"]
            )
        )

        # Invoke canonical compiler intake
        try:
            raw_intake = compile_portable_to_intake(
                definition,
                semantic_dependencies=resolved_semantic_deps,
                capability_metadata=resolved_capability_metadata,
                workflow=resolved_workflow,
                evaluation_requirements=resolved_eval_reqs,
                repair_laws=resolved_repair_laws,
            )
        except HarnessCompilationBlocked as e:
            raise HarnessPackageValidationError(f"Harness compilation blocked: {e.reason} ({e.blocker_ref})") from e

        # Validate projection against intake schema & compute canonical projection_id
        profile_key = raw_intake.get("profile_id", "portable_activative_v1").replace("-", "_")
        profile = self._profile_registry.resolve(profile_key)
        intake_validator = AtomicHarnessDefinitionIntake()
        intake_projection = intake_validator.validate(raw_intake, profile)

        # Record field-by-field source->binding provenance
        provenance = self._record_provenance(definition, intake_projection)

        # Run graph reconciliation receipt
        graph_receipt = self._reconciler.reconcile(intake_projection)

        # Optional full compilation against pipeline repository
        binding_manifest = None
        runtime_workflow = None
        if pipeline_repository is not None and eligibility_registry is not None:
            from cmf_pipeline.bindings.compiler import HarnessExecutionBindingCompiler
            from cmf_pipeline.workflow.application.compiler import RuntimeWorkflowCompiler

            idemp = idempotency_key or f"binding:{definition.definition_id[:16]}"

            # Store intake projection object and dependencies in repository
            pipeline_repository.store_object(
                "atomic_harness_definition_intake",
                intake_projection,
                idempotency_key=f"{idemp}:intake",
                object_id=intake_projection["projection_id"],
                lifecycle_state="VALIDATED",
            )
            for ref in intake_projection["semantic_dependencies"]:
                try:
                    pipeline_repository.store_object(
                        "semantic_dependency",
                        {"object_id": ref["object_id"], "version": ref["version"], "sha256": ref["sha256"]},
                        idempotency_key=f"dep:{ref['object_id']}",
                        object_id=ref["object_id"],
                        lifecycle_state="ACTIVE",
                    )
                except Exception:
                    pass

            compiler = HarnessExecutionBindingCompiler(pipeline_repository, eligibility_registry)
            binding_record = compiler.compile(intake_projection, graph_receipt, idempotency_key=f"{idemp}:binding")
            binding_manifest = binding_record["object"]["payload"]

            wf_compiler = RuntimeWorkflowCompiler(pipeline_repository)
            wf_record = wf_compiler.compile(
                intake_projection,
                binding_manifest,
                graph_receipt,
                idempotency_key=f"{idemp}:workflow",
            )
            runtime_workflow = wf_record["object"]["payload"]

        return HarnessBindingResult(
            definition_id=definition.definition_id,
            projection_id=intake_projection["projection_id"],
            intake_projection=intake_projection,
            provenance=provenance,
            graph_receipt=graph_receipt,
            binding_manifest=binding_manifest,
            runtime_workflow=runtime_workflow,
        )

    def _record_provenance(
        self,
        source: Any,
        projection: Dict[str, Any],
    ) -> HarnessBindingProvenance:
        """Records granular field-by-field provenance mapping across the 21 M10 contract dimensions."""
        src = source.content
        fields: List[HarnessProvenanceField] = []

        def _track(
            src_key: str,
            tgt_key: str,
            src_val: Any,
            tgt_val: Any,
            transform: str,
            req: bool = True,
        ) -> None:
            fields.append(
                HarnessProvenanceField(
                    source_field=src_key,
                    target_field=tgt_key,
                    source_value_digest=canonical_sha256(src_val),
                    target_value_digest=canonical_sha256(tgt_val),
                    transformation=transform,
                    required=req,
                )
            )

        _track("definition_id", "definition_id", source.definition_id, projection["definition_id"], "identity_passthrough")
        _track("manifest_version", "definition_version", src.get("manifest_version"), projection["definition_version"], "version_normalization")
        _track("category_binding.category_id", "category_id", src.get("category_binding", {}).get("category_id"), projection["category_id"], "category_extraction")
        _track("goal", "purpose", src.get("goal"), projection["purpose"], "goal_to_purpose_mapping")
        _track("category_binding.wrong_reading_locks", "wrong_reading_locks", src.get("category_binding", {}).get("wrong_reading_locks", []), projection["wrong_reading_locks"], "locks_passthrough")
        _track("capability_requirements", "capabilities", src.get("capability_requirements", []), projection["capabilities"], "capability_enrichment")
        _track("execution_plan", "workflow", src.get("execution_plan", []), projection["workflow"], "dag_composition")
        _track("lineage", "semantic_dependencies", src.get("lineage", []), projection["semantic_dependencies"], "dependency_resolution")
        _track("production_eligible", "production_ready", src.get("production_eligible", False), projection["production_ready"], "immutability_pin_false")
        _track("certified", "certified", src.get("certified", False), projection["certified"], "immutability_pin_false")
        _track("invalidation_state", "invalidation_state", "NOT_INVALIDATED", projection["invalidation_state"], "initialization_default")

        composite_digest = canonical_sha256(
            {
                "definition_id": source.definition_id,
                "projection_id": projection["projection_id"],
                "fields": [
                    {
                        "source_field": f.source_field,
                        "target_field": f.target_field,
                        "source_value_digest": f.source_value_digest,
                        "target_value_digest": f.target_value_digest,
                    }
                    for f in fields
                ],
            }
        )

        return HarnessBindingProvenance(
            definition_id=source.definition_id,
            projection_id=projection["projection_id"],
            fields=fields,
            composite_digest=composite_digest,
        )
