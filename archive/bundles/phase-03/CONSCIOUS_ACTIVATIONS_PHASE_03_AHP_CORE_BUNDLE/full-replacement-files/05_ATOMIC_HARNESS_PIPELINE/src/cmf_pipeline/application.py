from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping

from .adapters import register_default_synthetic_candidates
from .assurance import AssuranceService
from .authority import ProgramAuthorityService
from .batch import ContentBatchService
from .bindings import BindingInvalidationProjector, HarnessExecutionBindingCompiler, ImplementationEligibilityRegistry
from .candidates import CandidateSearchService
from .intake import AtomicHarnessDefinitionIntake, HarnessDefinitionProfileRegistry, HarnessGraphReconciler, HarnessPackageVerifier
from .workflow import RuntimeDependencyGraph, RuntimeInvalidationPlanner, RuntimeWorkflowCompiler, WorkflowRunService
from .workflow.infrastructure import PipelineRepository


class PipelineApplication:
    def __init__(self, database_path: str | Path | None = None):
        self.repository = PipelineRepository(database_path)
        self.authority = ProgramAuthorityService(self.repository)
        self.package_verifier = HarnessPackageVerifier()
        self.profile_registry = HarnessDefinitionProfileRegistry()
        self.definition_intake = AtomicHarnessDefinitionIntake()
        self.graph_reconciler = HarnessGraphReconciler()
        self.eligibility = ImplementationEligibilityRegistry()
        self.bindings = HarnessExecutionBindingCompiler(self.repository, self.eligibility)
        self.binding_invalidation = BindingInvalidationProjector(self.repository)
        self.batches = ContentBatchService(self.repository)
        self.workflow_compiler = RuntimeWorkflowCompiler(self.repository)
        self.runs = WorkflowRunService(self.repository)
        self.graph = RuntimeDependencyGraph(self.repository)
        self.invalidation = RuntimeInvalidationPlanner(self.repository)
        self.assurance = AssuranceService(self.repository)
        self.candidates = CandidateSearchService()

    def initialize(self) -> dict[str, Any]:
        return self.repository.initialize()

    def load_default_development_candidates(self) -> list[dict[str, Any]]:
        return register_default_synthetic_candidates(self.eligibility)

    def import_harness_package(self, package_path: str | Path, *, idempotency_key: str) -> dict[str, Any]:
        package = self.package_verifier.verify(package_path)
        profile = self.profile_registry.resolve(package["manifest"]["package_profile"])
        projection = self.definition_intake.validate(package["definition"], profile)
        graph = self.graph_reconciler.reconcile(projection)
        package_object = self.repository.store_object(
            "harness_package_import",
            {key: value for key, value in package.items() if key not in {"definition", "manifest", "receipt"}},
            idempotency_key=f"{idempotency_key}:package",
            object_id=package["package_id"],
            lifecycle_state="VERIFIED",
        )
        projection_object = self.repository.store_object(
            "harness_requirement_graph_projection",
            projection,
            idempotency_key=f"{idempotency_key}:projection",
            object_id=projection["projection_id"],
            lifecycle_state="RECONCILED",
        )
        graph_object = self.repository.store_object(
            "harness_graph_reconciliation_receipt",
            graph,
            idempotency_key=f"{idempotency_key}:graph",
            object_id=f"graph-receipt:{graph['runtime_projection_digest']}",
            lifecycle_state="PASS",
        )
        self.repository.add_edge(package["package_id"], projection["projection_id"], "contains_definition_projection")
        self.repository.add_edge(projection["projection_id"], graph_object["object"]["object_id"], "validated_by_graph_receipt")
        return {
            "package": package_object["object"],
            "projection": projection_object["object"]["payload"],
            "graph_receipt": graph_object["object"]["payload"],
            "compiler_profile": asdict(profile),
        }

    def compile_binding(
        self,
        projection: Mapping[str, Any],
        graph_receipt: Mapping[str, Any],
        *,
        idempotency_key: str,
    ) -> dict[str, Any]:
        return self.bindings.compile(projection, graph_receipt, idempotency_key=idempotency_key)

    def compile_workflow(
        self,
        projection: Mapping[str, Any],
        binding_manifest: Mapping[str, Any],
        graph_receipt: Mapping[str, Any],
        *,
        idempotency_key: str,
    ) -> dict[str, Any]:
        stored = self.workflow_compiler.compile(
            projection,
            binding_manifest,
            graph_receipt,
            idempotency_key=idempotency_key,
        )
        self.runs.register_workflow(stored["object"]["payload"])
        return stored

    def status(self) -> dict[str, Any]:
        return {
            **self.repository.health(),
            "lifecycle_state": "phase_03_pipeline_core",
            "claim_ceiling": "AHP_PHASE_03_CORE_IMPLEMENTED_DEVELOPMENT_PASS",
            "harness_execution_runtime": True,
            "real_media_execution": False,
            "external_product_execution": False,
            "production_authorized": False,
            "certified": False,
            "format02_activated": False,
            "vae_stage5_started": False,
        }
