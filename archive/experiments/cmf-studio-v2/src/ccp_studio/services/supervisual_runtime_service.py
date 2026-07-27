from __future__ import annotations

from datetime import datetime, timezone

from ccp_studio.contracts.supervisual_runtime import (
    BuildRunStatus,
    CommandStatus,
    SuperVisualBlocker,
    SuperVisualBuildRun,
    SuperVisualCommand,
    SuperVisualEvent,
    SuperVisualLineage,
    SuperVisualProject,
    SuperVisualProjectDetailResponse,
    SuperVisualProjectStatus,
    SuperVisualRunMode,
    SuperVisualSnapshot,
    SuperVisualStepRun,
    SuperVisualVariant,
    SuperVisualVariantDetailResponse,
    SuperVisualVariantStatus,
    StepRunStatus,
    reject_delivery_frame_profile,
)
from ccp_studio.repositories.supervisual_runtime import InMemorySuperVisualRuntimeRepository


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


STATE_ORDER = [
    SuperVisualVariantStatus.DRAFT,
    SuperVisualVariantStatus.CONTEXT_READY,
    SuperVisualVariantStatus.PREPRODUCTION_READY,
    SuperVisualVariantStatus.REFERENCE_BOARD_READY,
    SuperVisualVariantStatus.COMPOSITION_OPTIONS_READY,
    SuperVisualVariantStatus.COMPOSITION_LOCKED,
    SuperVisualVariantStatus.MATERIALIZATION_PLANNED,
    SuperVisualVariantStatus.ASSETS_MATERIALIZED,
    SuperVisualVariantStatus.RENDER_READY,
    SuperVisualVariantStatus.RENDERED,
    SuperVisualVariantStatus.EVALUATED,
    SuperVisualVariantStatus.APPROVAL_READY,
    SuperVisualVariantStatus.APPROVED,
    SuperVisualVariantStatus.EXPORTED,
]
STATE_RANK = {state: i for i, state in enumerate(STATE_ORDER)}

STEP_TARGET_STATUS = {
    "context_hydrate": SuperVisualVariantStatus.CONTEXT_READY,
    "primitive_bind": SuperVisualVariantStatus.CONTEXT_READY,
    "visual_preproduction": SuperVisualVariantStatus.PREPRODUCTION_READY,
    "asset_reference_board": SuperVisualVariantStatus.REFERENCE_BOARD_READY,
    "composition_hypotheses": SuperVisualVariantStatus.COMPOSITION_OPTIONS_READY,
    "composition_lock": SuperVisualVariantStatus.COMPOSITION_LOCKED,
    "provider_blueprints": SuperVisualVariantStatus.MATERIALIZATION_PLANNED,
    "materialization": SuperVisualVariantStatus.ASSETS_MATERIALIZED,
    "render_contract": SuperVisualVariantStatus.RENDER_READY,
    "render": SuperVisualVariantStatus.RENDERED,
    "eval": SuperVisualVariantStatus.EVALUATED,
    "approval": SuperVisualVariantStatus.APPROVED,
    "export": SuperVisualVariantStatus.EXPORTED,
}


class SuperVisualRuntimeService:
    def __init__(self, repository: InMemorySuperVisualRuntimeRepository | None = None):
        self.repository = repository or InMemorySuperVisualRuntimeRepository()

    def create_project(
        self,
        *,
        brand_id: str,
        brand_context_version_id: str,
        title: str,
        source_context_refs: list[str] | None = None,
        target_platforms: list[str] | None = None,
        default_frame_profile: str = "1:1_SOFT_ROUNDED_EDITORIAL",
        created_by_actor_id: str | None = None,
        create_initial_variant: bool = True,
    ) -> SuperVisualProject:
        reject_delivery_frame_profile(default_frame_profile)
        project = SuperVisualProject(
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            title=title,
            source_context_refs=source_context_refs or [],
            target_platforms=target_platforms or ["instagram"],
            default_frame_profile=default_frame_profile,
            created_by_actor_id=created_by_actor_id,
            status=SuperVisualProjectStatus.ACTIVE,
        )
        self.repository.create_project(project)
        self.append_event(project.supervisual_project_id, None, brand_id, brand_context_version_id, "project.created", created_by_actor_id, {"title": title})
        if create_initial_variant:
            variant = self.create_variant(project.supervisual_project_id, variant_label="Variant A", frame_profile=default_frame_profile, actor_id=created_by_actor_id)
            project.current_variant_id = variant.supervisual_variant_id
            project.updated_at = _now_iso()
            self.repository.update_project(project)
        return project

    def list_projects(self, brand_id: str | None = None) -> list[SuperVisualProject]:
        return self.repository.list_projects(brand_id=brand_id)

    def get_project_detail(self, project_id: str) -> SuperVisualProjectDetailResponse:
        project = self.repository.get_project(project_id)
        current_variant = self.repository.get_variant(project.current_variant_id) if project.current_variant_id else None
        latest_snapshot = self.repository.get_latest_snapshot(current_variant.supervisual_variant_id) if current_variant else None
        return SuperVisualProjectDetailResponse(
            project=project,
            current_variant=current_variant,
            latest_snapshot=latest_snapshot,
            events=self.repository.list_events(project_id),
            available_actions=self.available_actions(current_variant.status if current_variant else SuperVisualVariantStatus.DRAFT),
            blockers=[],
        )

    def create_variant(self, project_id: str, *, variant_label: str, frame_profile: str | None = None, actor_id: str | None = None, clone_from_variant_id: str | None = None) -> SuperVisualVariant:
        project = self.repository.get_project(project_id)
        profile = frame_profile or project.default_frame_profile
        reject_delivery_frame_profile(profile)
        lineage = SuperVisualLineage(source_context_refs=project.source_context_refs)
        if clone_from_variant_id:
            source_variant = self.repository.get_variant(clone_from_variant_id)
            lineage = source_variant.lineage
        variant = SuperVisualVariant(
            supervisual_project_id=project_id,
            brand_id=project.brand_id,
            brand_context_version_id=project.brand_context_version_id,
            variant_label=variant_label,
            frame_profile=profile,
            lineage=lineage,
        )
        self.repository.create_variant(variant)
        if not project.current_variant_id:
            project.current_variant_id = variant.supervisual_variant_id
            project.updated_at = _now_iso()
            self.repository.update_project(project)
        self.append_event(project_id, variant.supervisual_variant_id, project.brand_id, project.brand_context_version_id, "variant.created", actor_id, {"variant_label": variant_label})
        self.save_snapshot(variant.supervisual_variant_id, step="variant.created", display_payload={"variant_label": variant_label})
        return variant

    def get_variant_detail(self, variant_id: str) -> SuperVisualVariantDetailResponse:
        variant = self.repository.get_variant(variant_id)
        latest_snapshot = self.repository.get_latest_snapshot(variant_id)
        return SuperVisualVariantDetailResponse(
            variant=variant,
            latest_snapshot=latest_snapshot,
            events=self.repository.list_events(variant.supervisual_project_id, variant_id),
            available_actions=self.available_actions(variant.status),
            blockers=self.blockers_for_variant(variant),
        )

    def list_variants(self, project_id: str) -> list[SuperVisualVariant]:
        return self.repository.list_variants(project_id)

    def start_build_run(self, variant_id: str, *, run_mode: SuperVisualRunMode = SuperVisualRunMode.FULL_BUILD, requested_steps: list[str] | None = None, actor_id: str | None = None) -> SuperVisualBuildRun:
        variant = self.repository.get_variant(variant_id)
        if self.repository.list_active_build_runs(variant_id):
            raise ValueError("only one active build run is allowed per SuperVisual variant")
        run = SuperVisualBuildRun(
            supervisual_project_id=variant.supervisual_project_id,
            supervisual_variant_id=variant_id,
            brand_id=variant.brand_id,
            brand_context_version_id=variant.brand_context_version_id,
            run_mode=run_mode,
            requested_steps=requested_steps or [],
            status=BuildRunStatus.RUNNING,
        )
        self.repository.create_build_run(run)
        self.append_event(variant.supervisual_project_id, variant_id, variant.brand_id, variant.brand_context_version_id, "build_run.started", actor_id, {"build_run_id": run.supervisual_build_run_id})
        return run

    def get_build_run(self, build_run_id: str) -> SuperVisualBuildRun:
        return self.repository.get_build_run(build_run_id)

    def run_step(self, build_run_id: str, step_name: str, *, input_refs: list[str] | None = None, output_refs: list[str] | None = None, receipt_refs: list[str] | None = None, target_status: SuperVisualVariantStatus | None = None, actor_id: str | None = None) -> SuperVisualStepRun:
        run = self.repository.get_build_run(build_run_id)
        variant = self.repository.get_variant(run.supervisual_variant_id)
        self.assert_mutable(variant)
        step = SuperVisualStepRun(
            supervisual_build_run_id=build_run_id,
            supervisual_project_id=variant.supervisual_project_id,
            supervisual_variant_id=variant.supervisual_variant_id,
            brand_id=variant.brand_id,
            brand_context_version_id=variant.brand_context_version_id,
            step_name=step_name,
            status=StepRunStatus.RUNNING,
            input_refs=input_refs or [],
        )
        self.repository.create_step_run(step)
        self.append_event(variant.supervisual_project_id, variant.supervisual_variant_id, variant.brand_id, variant.brand_context_version_id, "step.started", actor_id, {"step_name": step_name})
        step.status = StepRunStatus.SUCCEEDED
        step.output_refs = output_refs or []
        step.receipt_refs = receipt_refs or []
        step.completed_at = _now_iso()
        self.repository.update_step_run(step)
        new_status = target_status or STEP_TARGET_STATUS.get(step_name)
        if new_status:
            self.advance_variant_status(variant, new_status)
        self.append_event(variant.supervisual_project_id, variant.supervisual_variant_id, variant.brand_id, variant.brand_context_version_id, "step.completed", actor_id, {"step_name": step_name, "step_run_id": step.supervisual_step_run_id})
        self.save_snapshot(variant.supervisual_variant_id, step=step_name, display_payload={"last_step": step_name, "output_refs": step.output_refs})
        return step

    def save_snapshot(self, variant_id: str, *, step: str, display_payload: dict | None = None, preview_ref: str | None = None, blockers: list[SuperVisualBlocker] | None = None) -> SuperVisualSnapshot:
        variant = self.repository.get_variant(variant_id)
        snapshot = SuperVisualSnapshot(
            supervisual_project_id=variant.supervisual_project_id,
            supervisual_variant_id=variant_id,
            brand_id=variant.brand_id,
            brand_context_version_id=variant.brand_context_version_id,
            status=variant.status,
            step=step,
            preview_ref=preview_ref,
            display_payload=display_payload or {},
            blockers=blockers or self.blockers_for_variant(variant),
            available_actions=self.available_actions(variant.status),
        )
        self.repository.create_snapshot(snapshot)
        self.append_event(variant.supervisual_project_id, variant_id, variant.brand_id, variant.brand_context_version_id, "snapshot.created", None, {"snapshot_id": snapshot.supervisual_snapshot_id, "step": step})
        return snapshot

    def append_event(self, project_id: str, variant_id: str | None, brand_id: str, brand_context_version_id: str, event_type: str, actor_id: str | None, payload: dict | None = None) -> SuperVisualEvent:
        event = SuperVisualEvent(
            supervisual_project_id=project_id,
            supervisual_variant_id=variant_id,
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            event_type=event_type,
            actor_id=actor_id,
            payload=payload or {},
        )
        return self.repository.append_event(event)

    def list_events(self, variant_id: str) -> list[SuperVisualEvent]:
        variant = self.repository.get_variant(variant_id)
        return self.repository.list_events(variant.supervisual_project_id, variant_id)

    def execute_command(self, command: SuperVisualCommand) -> SuperVisualCommand:
        existing = self.repository.get_command_by_idempotency_key(command.idempotency_key)
        if existing and existing.status == CommandStatus.COMPLETED:
            return existing
        command.status = CommandStatus.RUNNING
        command = self.repository.create_command(command)
        self.append_event(command.supervisual_project_id or command.target_id, command.supervisual_variant_id, self._brand_for_command(command), self._bcv_for_command(command), "command.created", command.actor_id, {"command_type": command.command_type})
        command.status = CommandStatus.COMPLETED
        command.completed_at = _now_iso()
        command.result_refs.append(command.target_id)
        self.repository.update_command(command)
        self.append_event(command.supervisual_project_id or command.target_id, command.supervisual_variant_id, self._brand_for_command(command), self._bcv_for_command(command), "command.completed", command.actor_id, {"command_id": command.command_id})
        return command

    def lock_composition(self, variant_id: str, *, composition_decision_receipt_id: str, actor_id: str | None = None) -> SuperVisualVariant:
        variant = self.repository.get_variant(variant_id)
        self.assert_mutable(variant)
        if not self.status_at_least(variant.status, SuperVisualVariantStatus.COMPOSITION_OPTIONS_READY):
            raise ValueError("Cannot lock composition before composition options exist")
        variant.lineage.composition_decision_receipt_id = composition_decision_receipt_id
        variant.status = SuperVisualVariantStatus.COMPOSITION_LOCKED
        variant.updated_at = _now_iso()
        self.repository.update_variant(variant)
        self.append_event(variant.supervisual_project_id, variant_id, variant.brand_id, variant.brand_context_version_id, "composition.locked", actor_id, {"composition_decision_receipt_id": composition_decision_receipt_id})
        self.save_snapshot(variant_id, step="composition.locked", display_payload={"composition_decision_receipt_id": composition_decision_receipt_id})
        return variant

    def record_provider_blueprint(self, variant_id: str, provider_job_blueprint_id: str, *, actor_id: str | None = None) -> SuperVisualVariant:
        variant = self.repository.get_variant(variant_id)
        self.assert_mutable(variant)
        if not self.status_at_least(variant.status, SuperVisualVariantStatus.COMPOSITION_LOCKED):
            raise ValueError("Cannot create provider blueprints before composition_locked")
        if provider_job_blueprint_id not in variant.lineage.provider_job_blueprint_ids:
            variant.lineage.provider_job_blueprint_ids.append(provider_job_blueprint_id)
        variant.status = SuperVisualVariantStatus.MATERIALIZATION_PLANNED
        variant.updated_at = _now_iso()
        self.repository.update_variant(variant)
        self.append_event(variant.supervisual_project_id, variant_id, variant.brand_id, variant.brand_context_version_id, "provider.blueprint.created", actor_id, {"provider_job_blueprint_id": provider_job_blueprint_id})
        return variant

    def record_provider_receipt(self, variant_id: str, provider_job_receipt_id: str, *, actor_id: str | None = None) -> SuperVisualVariant:
        variant = self.repository.get_variant(variant_id)
        self.assert_mutable(variant)
        if not variant.lineage.provider_job_blueprint_ids:
            raise ValueError("Cannot record provider receipts before provider blueprints exist")
        if provider_job_receipt_id not in variant.lineage.provider_job_receipt_ids:
            variant.lineage.provider_job_receipt_ids.append(provider_job_receipt_id)
        variant.status = SuperVisualVariantStatus.ASSETS_MATERIALIZED
        variant.updated_at = _now_iso()
        self.repository.update_variant(variant)
        self.append_event(variant.supervisual_project_id, variant_id, variant.brand_id, variant.brand_context_version_id, "provider.job.completed", actor_id, {"provider_job_receipt_id": provider_job_receipt_id})
        return variant

    def record_render_receipt(self, variant_id: str, render_receipt_id: str, *, render_contract_id: str | None = None, actor_id: str | None = None) -> SuperVisualVariant:
        variant = self.repository.get_variant(variant_id)
        self.assert_mutable(variant)
        if not self.status_at_least(variant.status, SuperVisualVariantStatus.COMPOSITION_LOCKED):
            raise ValueError("Cannot render before composition lock")
        variant.lineage.render_receipt_id = render_receipt_id
        if render_contract_id:
            variant.lineage.render_contract_id = render_contract_id
        variant.status = SuperVisualVariantStatus.RENDERED
        variant.updated_at = _now_iso()
        self.repository.update_variant(variant)
        self.append_event(variant.supervisual_project_id, variant_id, variant.brand_id, variant.brand_context_version_id, "render.completed", actor_id, {"render_receipt_id": render_receipt_id})
        self.save_snapshot(variant_id, step="render.completed", preview_ref=render_receipt_id, display_payload={"render_receipt_id": render_receipt_id})
        return variant

    def record_eval_receipt(self, variant_id: str, evaluation_receipt_id: str, *, passed: bool, actor_id: str | None = None) -> SuperVisualVariant:
        variant = self.repository.get_variant(variant_id)
        self.assert_mutable(variant)
        if not self.status_at_least(variant.status, SuperVisualVariantStatus.RENDERED):
            raise ValueError("Cannot evaluate before render")
        variant.lineage.evaluation_receipt_id = evaluation_receipt_id
        variant.status = SuperVisualVariantStatus.APPROVAL_READY if passed else SuperVisualVariantStatus.REVISION_REQUIRED
        variant.approval_status = "ready" if passed else "blocked"
        variant.updated_at = _now_iso()
        self.repository.update_variant(variant)
        self.append_event(variant.supervisual_project_id, variant_id, variant.brand_id, variant.brand_context_version_id, "eval.completed", actor_id, {"evaluation_receipt_id": evaluation_receipt_id, "passed": passed})
        return variant

    def approve_variant(self, variant_id: str, *, approval_receipt_id: str, actor_id: str | None = None) -> SuperVisualVariant:
        variant = self.repository.get_variant(variant_id)
        if variant.status != SuperVisualVariantStatus.APPROVAL_READY:
            raise ValueError("Cannot approve before evaluation passes and variant is approval_ready")
        variant.lineage.approval_receipt_id = approval_receipt_id
        variant.status = SuperVisualVariantStatus.APPROVED
        variant.approval_status = "approved"
        variant.updated_at = _now_iso()
        self.repository.update_variant(variant)
        self.append_event(variant.supervisual_project_id, variant_id, variant.brand_id, variant.brand_context_version_id, "variant.approved", actor_id, {"approval_receipt_id": approval_receipt_id})
        return variant

    def create_export_pack(self, variant_id: str, *, export_pack_id: str, actor_id: str | None = None) -> SuperVisualVariant:
        variant = self.repository.get_variant(variant_id)
        if variant.status != SuperVisualVariantStatus.APPROVED:
            raise ValueError("Cannot export before approval")
        variant.lineage.export_pack_id = export_pack_id
        variant.status = SuperVisualVariantStatus.EXPORTED
        variant.updated_at = _now_iso()
        self.repository.update_variant(variant)
        self.append_event(variant.supervisual_project_id, variant_id, variant.brand_id, variant.brand_context_version_id, "export.created", actor_id, {"export_pack_id": export_pack_id})
        return variant

    def apply_revision(self, variant_id: str, *, revision_note: str, actor_id: str | None = None) -> SuperVisualVariant:
        variant = self.repository.get_variant(variant_id)
        self.assert_mutable(variant)
        variant.status = SuperVisualVariantStatus.REVISION_REQUIRED
        variant.updated_at = _now_iso()
        self.repository.update_variant(variant)
        self.append_event(variant.supervisual_project_id, variant_id, variant.brand_id, variant.brand_context_version_id, "revision.requested", actor_id, {"revision_note": revision_note})
        return variant

    def available_actions(self, status: SuperVisualVariantStatus) -> list[str]:
        mapping = {
            SuperVisualVariantStatus.DRAFT: ["build.start", "context_hydrate"],
            SuperVisualVariantStatus.CONTEXT_READY: ["visual_preproduction"],
            SuperVisualVariantStatus.PREPRODUCTION_READY: ["asset_reference_board"],
            SuperVisualVariantStatus.REFERENCE_BOARD_READY: ["composition.hypotheses"],
            SuperVisualVariantStatus.COMPOSITION_OPTIONS_READY: ["composition.lock", "revision.apply"],
            SuperVisualVariantStatus.COMPOSITION_LOCKED: ["provider_blueprints.compile", "render_contract.compile", "render.run"],
            SuperVisualVariantStatus.MATERIALIZATION_PLANNED: ["materialize.run"],
            SuperVisualVariantStatus.ASSETS_MATERIALIZED: ["render_contract.compile", "render.run"],
            SuperVisualVariantStatus.RENDER_READY: ["render.run"],
            SuperVisualVariantStatus.RENDERED: ["eval.run", "revision.apply"],
            SuperVisualVariantStatus.EVALUATED: ["variant.approve", "revision.apply"],
            SuperVisualVariantStatus.APPROVAL_READY: ["variant.approve", "revision.apply"],
            SuperVisualVariantStatus.APPROVED: ["variant.export"],
            SuperVisualVariantStatus.EXPORTED: ["view_export"],
        }
        return mapping.get(status, [])

    def blockers_for_variant(self, variant: SuperVisualVariant) -> list[SuperVisualBlocker]:
        blockers: list[SuperVisualBlocker] = []
        if variant.status == SuperVisualVariantStatus.DRAFT:
            blockers.append(SuperVisualBlocker(code="not_built", message="Variant has not started production yet.", severity="info"))
        if variant.status == SuperVisualVariantStatus.REVISION_REQUIRED:
            blockers.append(SuperVisualBlocker(code="revision_required", message="Variant requires revision before approval."))
        return blockers

    def assert_mutable(self, variant: SuperVisualVariant) -> None:
        if variant.status in {SuperVisualVariantStatus.APPROVED, SuperVisualVariantStatus.EXPORTED, SuperVisualVariantStatus.ARCHIVED}:
            raise ValueError("Approved/exported/archived variants cannot be mutated in place")

    def status_at_least(self, current: SuperVisualVariantStatus, required: SuperVisualVariantStatus) -> bool:
        if current not in STATE_RANK or required not in STATE_RANK:
            return False
        return STATE_RANK[current] >= STATE_RANK[required]

    def advance_variant_status(self, variant: SuperVisualVariant, target_status: SuperVisualVariantStatus) -> None:
        self.assert_mutable(variant)
        if target_status in STATE_RANK and variant.status in STATE_RANK:
            if STATE_RANK[target_status] < STATE_RANK[variant.status]:
                return
        variant.status = target_status
        variant.updated_at = _now_iso()
        self.repository.update_variant(variant)

    def _brand_for_command(self, command: SuperVisualCommand) -> str:
        if command.supervisual_variant_id:
            return self.repository.get_variant(command.supervisual_variant_id).brand_id
        if command.supervisual_project_id:
            return self.repository.get_project(command.supervisual_project_id).brand_id
        return "unknown"

    def _bcv_for_command(self, command: SuperVisualCommand) -> str:
        if command.supervisual_variant_id:
            return self.repository.get_variant(command.supervisual_variant_id).brand_context_version_id
        if command.supervisual_project_id:
            return self.repository.get_project(command.supervisual_project_id).brand_context_version_id
        return "unknown"
