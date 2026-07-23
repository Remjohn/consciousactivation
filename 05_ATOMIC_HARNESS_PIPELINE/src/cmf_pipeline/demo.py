from __future__ import annotations

import json
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from ca_contracts import bytes_sha256, canonical_json_bytes, canonical_sha256

from .adapters import SyntheticDeterministicAdapter
from .application import PipelineApplication


def ref(object_id: str, seed: str) -> dict[str, str]:
    return {"object_id": object_id, "version": "1.0.0", "sha256": canonical_sha256({"seed": seed})}


def write_demo_harness(path: Path) -> dict[str, Any]:
    definition = {
        "definition_id": "harness:phase3-reference",
        "definition_version": "1.0.0",
        "category_id": "short_form_edited_video",
        "profile_id": "format07_direct_coaching_a_roll",
        "purpose": "Compile a bounded source-led reference program without changing AIR meaning.",
        "semantic_dependencies": sorted(
            [
                ref("air:activation-transfer:reference", "transfer"),
                ref("air:final-script:reference", "script"),
                ref("interview:source-package:reference", "source"),
            ],
            key=lambda item: item["object_id"],
        ),
        "capabilities": [
            {
                "capability_id": "compile_program",
                "owner_kind": "CODE",
                "required_features": ["canonical_hash", "typed_output"],
                "authority_boundary": "execute approved semantic program only",
            },
            {
                "capability_id": "inspect_source",
                "owner_kind": "CODE",
                "required_features": ["canonical_hash", "read_only"],
                "authority_boundary": "inspect exact source references only",
            },
            {
                "capability_id": "operator_review",
                "owner_kind": "HUMAN",
                "required_features": ["attributable_decision", "typed_handoff"],
                "authority_boundary": "approve bounded transition only",
            },
        ],
        "workflow": {
            "nodes": [
                {
                    "node_id": "node:compose",
                    "capability_id": "compile_program",
                    "phase_order": 2,
                    "purpose": "Compile the typed source-backed execution program.",
                    "actor_kind": "DETERMINISTIC_MODULE",
                    "role": "COMPOSER",
                    "product_boundary": "ATOMIC_HARNESS_PIPELINE",
                    "input_contracts": ["source-inspection"],
                    "output_contracts": ["draft-program"],
                    "side_effect_class": "LOCAL_STATE_WRITE",
                },
                {
                    "node_id": "node:inspect",
                    "capability_id": "inspect_source",
                    "phase_order": 1,
                    "purpose": "Inspect the exact source package references.",
                    "actor_kind": "DETERMINISTIC_MODULE",
                    "role": "HUNTER",
                    "product_boundary": "ATOMIC_HARNESS_PIPELINE",
                    "input_contracts": [],
                    "output_contracts": ["source-inspection"],
                    "side_effect_class": "READ_ONLY",
                },
                {
                    "node_id": "node:review",
                    "capability_id": "operator_review",
                    "phase_order": 3,
                    "purpose": "Record an attributable operator transition decision.",
                    "actor_kind": "HUMAN_GATE",
                    "role": "COMMANDER",
                    "product_boundary": "CONSCIOUS_ACTIVATIONS_STUDIO",
                    "input_contracts": ["draft-program"],
                    "output_contracts": ["approved-program"],
                    "side_effect_class": "HUMAN_DECISION",
                },
            ],
            "edges": [
                {"source_node_id": "node:compose", "target_node_id": "node:review", "contract_id": "draft-program"},
                {"source_node_id": "node:inspect", "target_node_id": "node:compose", "contract_id": "source-inspection"},
            ],
        },
        "evaluation_requirements": ["deterministic_contract_validation", "source_lineage_validation"],
        "repair_laws": ["descendant_only_rerun", "preserve_upstream_semantic_truth"],
        "wrong_reading_locks": ["do_not_replace_source_expression", "do_not_rewrite_air_meaning"],
        "production_ready": False,
        "certified": False,
        "invalidation_state": "ACTIVE",
    }
    definition_bytes = canonical_json_bytes(definition)
    manifest_basis = {
        "schema_version": "ca-builder-portable-manifest/v1",
        "definition_sha256": bytes_sha256(definition_bytes),
        "package_profile": "portable_activative_v1",
    }
    receipt = {
        "schema_version": "ca-builder-portable-receipt/v1",
        "definition_id": definition["definition_id"],
        "definition_sha256": canonical_sha256(definition),
        "manifest_semantic_sha256": canonical_sha256(manifest_basis),
        "production_ready": False,
        "certified": False,
    }
    receipt_bytes = canonical_json_bytes(receipt)
    manifest = {**manifest_basis, "receipt_sha256": bytes_sha256(receipt_bytes)}
    manifest_bytes = canonical_json_bytes(manifest)
    sums = "\n".join(
        [
            f"{bytes_sha256(definition_bytes)}  definition.json",
            f"{bytes_sha256(manifest_bytes)}  manifest.json",
            f"{bytes_sha256(receipt_bytes)}  receipt.json",
        ]
    ) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in (
            ("definition.json", definition_bytes),
            ("manifest.json", manifest_bytes),
            ("receipt.json", receipt_bytes),
            ("SHA256SUMS", sums.encode("utf-8")),
        ):
            info = zipfile.ZipInfo(name)
            info.date_time = (2026, 7, 23, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    return definition


def run_demo(database_path: str | Path | None = None) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="ca-phase3-demo-") as temp_dir:
        root = Path(temp_dir)
        db = Path(database_path) if database_path else root / "pipeline.sqlite3"
        package = root / "reference-harness.zip"
        write_demo_harness(package)
        app = PipelineApplication(db)
        app.initialize()
        candidates = app.load_default_development_candidates()
        imported = app.import_harness_package(package, idempotency_key="phase3-demo-import")
        binding_result = app.compile_binding(
            imported["projection"],
            imported["graph_receipt"],
            idempotency_key="phase3-demo-binding",
        )
        binding = binding_result["object"]["payload"]
        workflow_result = app.compile_workflow(
            imported["projection"],
            binding,
            imported["graph_receipt"],
            idempotency_key="phase3-demo-workflow",
        )
        workflow = workflow_result["object"]["payload"]
        binding_ref = ref(binding["manifest_id"], binding_result["object"]["canonical_sha256"])
        run = app.runs.create_run(
            workflow["workflow_id"],
            binding_manifest_ref=binding_ref,
            context_refs=imported["projection"]["semantic_dependencies"],
            batch_ref=None,
            idempotency_key="phase3-demo-run",
        )
        run_id = run["run_id"]
        synthetic = SyntheticDeterministicAdapter()
        outputs = []
        for ordinal, node_id in enumerate(workflow["topological_order"], 1):
            ready = app.runs.ready_nodes(run_id)
            if node_id not in ready:
                raise RuntimeError(f"demo node not ready in deterministic order: {node_id}; ready={ready}")
            app.runs.dispatch_node(
                run_id,
                node_id,
                context_refs=imported["projection"]["semantic_dependencies"],
                allowed_actions=["inspect" if ordinal == 1 else "compile" if ordinal == 2 else "record_decision"],
                forbidden_actions=["change_air_meaning", "execute_external_provider"],
                tool_ids=["synthetic-development-adapter"],
                idempotency_key=f"phase3-demo-dispatch-{ordinal}",
            )
            app.runs.start_node(run_id, node_id, idempotency_key=f"phase3-demo-start-{ordinal}")
            synthetic_result = synthetic.execute(node_id=node_id, input_refs=imported["projection"]["semantic_dependencies"])
            output_ref = ref(f"output:{node_id}", synthetic_result["payload_sha256"])
            outputs.append(output_ref)
            app.runs.complete_node(
                run_id,
                node_id,
                output_ref=output_ref,
                validation_receipt_refs=[f"validation:{ordinal}"],
                idempotency_key=f"phase3-demo-complete-{ordinal}",
            )
            if ordinal == 1:
                app.runs.checkpoint(run_id, idempotency_key="phase3-demo-checkpoint")
        replay = app.runs.replay(run_id)
        candidate_portfolio = app.candidates.evaluate(
            [
                {
                    "candidate_id": "candidate:a",
                    "artifact_ref": outputs[1],
                    "quality_score_bps": 8200,
                    "cost_units": 3,
                    "sequence": 1,
                    "eligible": True,
                    "failure_codes": [],
                },
                {
                    "candidate_id": "candidate:b",
                    "artifact_ref": outputs[2],
                    "quality_score_bps": 9000,
                    "cost_units": 4,
                    "sequence": 2,
                    "eligible": True,
                    "failure_codes": [],
                },
            ],
            max_candidates=3,
            budget_units=10,
            quality_threshold_bps=8800,
            plateau_window=2,
            plateau_delta_bps=50,
        )
        fingerprint = app.assurance.execution_fingerprint(
            contract_release_ref=ref("contract:activative-production-spine", "contract"),
            implementation_ref=ref("implementation:synthetic-compose", "implementation"),
            runtime_ref=ref("runtime:python312", "runtime"),
            tool_refs=[ref("tool:synthetic-development-adapter", "tool")],
            evaluator_ref=None,
            model_ref=None,
            hardware_profile="development_cpu",
            precision="not_applicable_deterministic_code",
        )
        sandbox = app.assurance.sandbox_declaration(
            implementation_ref=fingerprint["implementation_ref"],
            allowed_actions=["compile", "inspect"],
            forbidden_actions=["network", "production_publish"],
            allowed_relative_paths=[".conscious-activations/dev"],
            network_policy="DENY_ALL",
            secret_reference_ids=[],
            resource_limits={"max_memory_mb": 512, "max_runtime_ms": 30000},
        )
        assurance = app.assurance.assurance_check(
            target_ref=ref(run_id, replay["event_stream_sha256"]),
            fingerprint=fingerprint,
            sandbox=sandbox,
            observed_contract_release_ref=fingerprint["contract_release_ref"],
        )
        invalidation = app.invalidation.plan(
            root_ids=["node:compose"],
            reason="reference local change",
            preserved_ids=["node:inspect"],
            replacement_refs=[],
            idempotency_key="phase3-demo-invalidation",
        )["object"]["payload"]
        rerun_plan = app.invalidation.rerun_plan(invalidation, reusable_checkpoint_ids=[])
        return {
            "phase": "PHASE_03_ATOMIC_HARNESS_PIPELINE_CORE",
            "harness_package_id": imported["package"]["object_id"],
            "projection_id": imported["projection"]["projection_id"],
            "binding_manifest_id": binding["manifest_id"],
            "workflow_id": workflow["workflow_id"],
            "run_id": run_id,
            "run_state": app.runs.status(run_id)["state"],
            "event_count": replay["event_count"],
            "event_stream_sha256": replay["event_stream_sha256"],
            "candidate_portfolio_id": candidate_portfolio["portfolio_id"],
            "best_candidate_id": candidate_portfolio["best_candidate_id"],
            "assurance_result": assurance["result"],
            "invalidation_plan_id": invalidation["plan_id"],
            "rerun_plan_id": rerun_plan["rerun_plan_id"],
            "development_candidate_count": len(candidates),
            "production_authorized": False,
            "certified": False,
            "format02_activated": False,
            "real_external_calls": 0,
        }
