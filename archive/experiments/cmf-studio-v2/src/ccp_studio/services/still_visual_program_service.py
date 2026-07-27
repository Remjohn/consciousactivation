"""Still visual parent program service for TS-CMF-133 through TS-CMF-135."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.asset_program_compilers import PrimitiveTriadContract
from ccp_studio.contracts.composition_runtime import ApprovalStatus
from ccp_studio.contracts.still_visuals import (
    ProviderMaterializationPlan,
    StillVisualApprovalReceipt,
    StillVisualCompositionProgram,
    StillVisualCompositionRequest,
    StillVisualEvalSummary,
    StillVisualExportManifest,
    StillVisualFamilyRoute,
    StillVisualRenderManifest,
    StillVisualReviewReadModel,
    StillVisualRevisionCommand,
    StillVisualStageState,
    TelegramStillVisualReviewCard,
    still_visual_hash,
)
from ccp_studio.contracts.supervisual_grammar import (
    SuperVisualFeelMatrixEntry,
    SuperVisualGrammarRecord,
    SuperVisualGrammarRouteDecision,
    SuperVisualGrammarRouteRequest,
    SuperVisualPrimitiveCoverageReceipt,
    SuperVisualSubtype,
)
from ccp_studio.repositories.still_visuals import InMemoryStillVisualRepository
from ccp_studio.services.asset_program_compiler_service import AssetProgramCompilerService


class StillVisualProgramServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class StillVisualProgramService:
    repository: InMemoryStillVisualRepository = field(default_factory=InMemoryStillVisualRepository)
    asset_compiler: AssetProgramCompilerService = field(default_factory=AssetProgramCompilerService)

    def create_program(
        self,
        *,
        workspace_id: UUID,
        brand_context_version_ref: str,
        source_evidence_refs: list[str],
        target_format_family: str,
        package_slot: str,
        platform: str = "instagram",
    ) -> StillVisualCompositionProgram:
        request = StillVisualCompositionRequest(
            workspace_id=workspace_id,
            brand_context_version_ref=brand_context_version_ref,
            source_evidence_refs=source_evidence_refs,
            target_format_family=target_format_family,  # type: ignore[arg-type]
            package_slot=package_slot,
            platform=platform,  # type: ignore[arg-type]
        )
        stages = [
            StillVisualStageState(stage_code="request", status="completed", artifact_refs=[f"request:{request.still_visual_composition_request_id}"]),
            StillVisualStageState(stage_code="route", status="pending"),
            StillVisualStageState(stage_code="materialize", status="pending"),
            StillVisualStageState(stage_code="render", status="pending"),
            StillVisualStageState(stage_code="evaluate", status="pending"),
            StillVisualStageState(stage_code="review", status="pending"),
            StillVisualStageState(stage_code="approval", status="pending"),
            StillVisualStageState(stage_code="export", status="pending"),
        ]
        program = StillVisualCompositionProgram(
            request=request,
            manifest_snapshot_ref="manifest_snapshot:still-visual-production-v1",
            stage_states=stages,
            program_hash=still_visual_hash(request.model_dump(mode="json")),
        )
        return self.repository.put_program(program)

    def seed_supervisual_grammar(self) -> list[SuperVisualGrammarRecord]:
        if self.repository.grammar_records:
            return list(self.repository.grammar_records.values())
        triads = self.asset_compiler._primitive_triads_for_route("SV-FRB")
        records = [
            SuperVisualGrammarRecord(
                grammar_code="SPV-CON-DEBATE-PANEL",
                subtype="SPV-CON",
                display_name="Conceptual Contrast Debate Panel",
                composition_purpose="Make a contradiction visually inspectable with opposing sides, proof labels, and one audience decision.",
                required_zones=["headline", "left_claim", "right_claim", "human_reaction", "vote_prompt"],
                required_contrast_axes=["belief_vs_belief", "cost_vs_benefit"],
                skia_scene_obligations=["two_sided_layout", "editable_text", "primitive_evidence_labels"],
                primitive_triads=triads,
            ),
            SuperVisualGrammarRecord(
                grammar_code="SPV-SYM-METAPHOR-ANCHOR",
                subtype="SPV-SYM",
                display_name="Symbolic Metaphor Anchor",
                composition_purpose="Translate a guest idea into a single symbolic image whose meaning is explicitly anchored.",
                required_zones=["symbol", "meaning_label", "guest_cutout", "source_caption"],
                symbol_explanation_required=True,
                skia_scene_obligations=["symbol_layer", "meaning_annotation", "source_caption"],
                primitive_triads=triads,
            ),
            SuperVisualGrammarRecord(
                grammar_code="SPV-PRM-AUTHORITY-PROOF",
                subtype="SPV-PRM",
                display_name="Authority Proof Frame",
                composition_purpose="Show earned proof with one source artifact, one human stance, and one concise conclusion.",
                required_zones=["proof_artifact", "authority_claim", "human_stance", "source_badge"],
                authority_evidence_required=True,
                skia_scene_obligations=["proof_asset_layer", "source_badge", "editable_claim"],
                primitive_triads=triads,
            ),
        ]
        for record in records:
            self.repository.put_grammar_record(record)
        for subtype, required_feel, avoid in [
            ("SPV-CON", "high-clarity contrast with visible tension and no generic debate-card collapse", ["same-feel-as-paper-cut", "unearned outrage"]),
            ("SPV-SYM", "symbolic, precise, and explainable without becoming mystical decoration", ["unexplained symbol", "stock metaphor"]),
            ("SPV-PRM", "authority-forward proof with source-truth humility", ["fake certainty", "uncited proof"]),
        ]:
            self.repository.put_feel_matrix_entry(
                SuperVisualFeelMatrixEntry(
                    subtype=subtype,  # type: ignore[arg-type]
                    required_feel=required_feel,
                    must_avoid=avoid,
                    minimum_primitive_score=0.84,
                )
            )
        return records

    def route_supervisual_grammar(
        self,
        *,
        program: StillVisualCompositionProgram,
        archetype_ref: str,
        target_subtype_hint: SuperVisualSubtype | None = None,
    ) -> tuple[SuperVisualGrammarRouteDecision, SuperVisualPrimitiveCoverageReceipt]:
        records = self.seed_supervisual_grammar()
        subtype = target_subtype_hint or ("SPV-CON" if "challenger" in archetype_ref or "contrast" in archetype_ref else "SPV-SYM")
        selected = next(record for record in records if record.subtype == subtype)
        request = SuperVisualGrammarRouteRequest(
            program_ref=f"still_visual_program:{program.still_visual_composition_program_id}",
            brand_context_ref=program.request.brand_context_version_ref,
            archetype_ref=archetype_ref,
            target_subtype_hint=target_subtype_hint,
            platform=program.request.platform,
            source_evidence_refs=program.request.source_evidence_refs,
        )
        primitive_ids = [triad.primitive_id for triad in selected.primitive_triads]
        blockers: list[str] = []
        if len(primitive_ids) < 3:
            blockers.append("SUPERVISUAL_PRIMITIVE_MINIMUM_NOT_MET")
        decision = self.repository.put_grammar_route_decision(
            SuperVisualGrammarRouteDecision(
                route_request_id=request.supervisual_grammar_route_request_id,
                selected_grammar_code=selected.grammar_code,
                selected_subtype=selected.subtype,
                primitive_coverage_ids=primitive_ids,
                feel_matrix_ref=f"supervisual_feel_matrix:{selected.subtype}",
                skia_scene_obligation_refs=selected.skia_scene_obligations,
                decision_code="SUPERVISUAL_GRAMMAR_ROUTE_ACCEPTED" if not blockers else "SUPERVISUAL_GRAMMAR_ROUTE_BLOCKED",
                blocker_codes=blockers,
            )
        )
        coverage = self.repository.put_primitive_coverage_receipt(
            SuperVisualPrimitiveCoverageReceipt(
                route_decision_id=decision.supervisual_grammar_route_decision_id,
                primitive_score=0.92 if not blockers else 0.4,
                role_coverage={"meaning_transform": True, "delivery_shape": True, "format_material": True},
                decision_code="SUPERVISUAL_PRIMITIVE_COVERAGE_ACCEPTED" if not blockers else "SUPERVISUAL_PRIMITIVE_COVERAGE_BLOCKED",
                blocker_codes=blockers,
            )
        )
        return decision, coverage

    def route_program(
        self,
        *,
        program_id: UUID,
        archetype_ref: str = "archetype.challenger_frame_breaker.v1",
        target_subtype_hint: SuperVisualSubtype | None = "SPV-CON",
    ) -> StillVisualCompositionProgram:
        program = self._program(program_id)
        primitive_ids = self.asset_compiler._primitive_ids_for_route("SV-FRB")
        grammar_ref = None
        if program.request.target_format_family == "supervisual":
            grammar_decision, coverage = self.route_supervisual_grammar(program=program, archetype_ref=archetype_ref, target_subtype_hint=target_subtype_hint)
            grammar_ref = f"supervisual_grammar_route:{grammar_decision.supervisual_grammar_route_decision_id}"
            primitive_ids = grammar_decision.primitive_coverage_ids
        route = self.repository.put_route(
            StillVisualFamilyRoute(
                program_id=program_id,
                selected_family=program.request.target_format_family,
                selected_builder_ref=self._builder_ref(program.request.target_format_family),
                atlas_binding_ref=f"atlas:{program.request.target_format_family}:default",
                grammar_binding_ref=grammar_ref,
                primitive_validation_ids=primitive_ids,
                decision_code="STILL_VISUAL_ROUTE_LOCKED",
            )
        )
        return self._update_program(
            program,
            family_route=route,
            stage_updates={"route": ("completed", [f"still_visual_route:{route.still_visual_family_route_id}"], [f"route_receipt:{route.still_visual_family_route_id}"])},
        )

    def materialize_program(self, *, program_id: UUID) -> StillVisualCompositionProgram:
        program = self._program(program_id)
        if not program.family_route:
            raise StillVisualProgramServiceError("STILL_VISUAL_ROUTE_REQUIRED", "Route must be locked before provider materialization.")
        plan = self.repository.put_provider_plan(
            ProviderMaterializationPlan(
                program_id=program_id,
                provider_job_refs=["provider_job:ideogram_4:composition-reference", "provider_job:qwen_layered:layer-decomposition", "provider_job:sam3:mask-refinement"],
                layer_materialization_refs=["layer:background", "layer:hero", "layer:editable_text", "layer:source_badge"],
                decision_code="PROVIDER_MATERIALIZATION_READY",
            )
        )
        return self._update_program(
            program,
            provider_plan=plan,
            stage_updates={"materialize": ("completed", [f"provider_plan:{plan.provider_materialization_plan_id}"], [f"provider_materialization:{plan.provider_materialization_plan_id}"])},
        )

    def render_program(self, *, program_id: UUID, runtime_lock_ref: str = "runtime_lock:skia") -> StillVisualCompositionProgram:
        program = self._program(program_id)
        if not program.provider_plan:
            raise StillVisualProgramServiceError("STILL_VISUAL_PROVIDER_PLAN_REQUIRED", "Provider materialization must complete before render.")
        render_hash = still_visual_hash({"program_id": program_id, "runtime_lock_ref": runtime_lock_ref, "provider_plan": program.provider_plan.model_dump(mode="json")})
        manifest = self.repository.put_render_manifest(
            StillVisualRenderManifest(
                program_id=program_id,
                skia_scene_ref=f"skia_scene:{program_id}",
                runtime_lock_ref=runtime_lock_ref,
                render_ref=f"render://still-visual/{program_id}.png",
                render_hash=render_hash,
            )
        )
        return self._update_program(
            program,
            render_manifest=manifest,
            stage_updates={"render": ("completed", [manifest.render_ref], [f"render_manifest:{manifest.still_visual_render_manifest_id}"])},
        )

    def evaluate_program(self, *, program_id: UUID, source_truth_score: float = 0.94) -> StillVisualCompositionProgram:
        program = self._program(program_id)
        if not program.render_manifest:
            raise StillVisualProgramServiceError("STILL_VISUAL_RENDER_REQUIRED", "Render must complete before eval.")
        blockers: list[str] = []
        if len(program.family_route.primitive_validation_ids if program.family_route else []) < 3:
            blockers.append("STILL_VISUAL_PRIMITIVE_TRIAD_MISSING")
        if source_truth_score < 0.84:
            blockers.append("STILL_VISUAL_SOURCE_TRUTH_BELOW_THRESHOLD")
        summary = self.repository.put_eval_summary(
            StillVisualEvalSummary(
                program_id=program_id,
                primitive_score=0.92 if not blockers else 0.4,
                doctrine_score=0.91 if not blockers else 0.4,
                grammar_score=0.93 if program.request.target_format_family == "supervisual" else 0.88,
                source_truth_score=source_truth_score,
                platform_fit_score=0.9,
                decision="approved" if not blockers else "blocked",
                blocker_codes=blockers,
                receipt_refs=[f"primitive_eval:{program_id}", f"grammar_eval:{program_id}", f"source_truth_eval:{program_id}"],
            )
        )
        return self._update_program(
            program,
            eval_summary=summary,
            blocker_codes=blockers,
            stage_updates={"evaluate": ("completed" if not blockers else "blocked", [f"eval_summary:{summary.still_visual_eval_summary_id}"], summary.receipt_refs)},
        )

    def build_review_read_model(self, *, program_id: UUID) -> StillVisualReviewReadModel:
        program = self._program(program_id)
        blockers = self._program_blockers(program)
        read_model = self.repository.put_review_read_model(
            StillVisualReviewReadModel(
                program_id=program_id,
                approval_status=program.approval_status,
                stage_states=program.stage_states,
                preview_refs=[program.render_manifest.render_ref] if program.render_manifest else [],
                blockers=blockers,
                repair_commands=self._repair_commands(blockers),
                approval_eligible=not blockers and program.eval_summary is not None and program.eval_summary.decision == "approved",
            )
        )
        return read_model

    def build_telegram_card(self, *, program_id: UUID) -> TelegramStillVisualReviewCard:
        read_model = self.build_review_read_model(program_id=program_id)
        card = TelegramStillVisualReviewCard(
            program_id=program_id,
            title=f"Review {self._program(program_id).request.target_format_family} still visual",
            preview_ref=read_model.preview_refs[0] if read_model.preview_refs else "preview://missing",
            blocker_count=len(read_model.blockers),
            commands=["approve", "reject", "revise", "waive", "export"],
        )
        return self.repository.put_telegram_card(card)

    def approve_program(self, *, program_id: UUID, operator_id: UUID) -> StillVisualApprovalReceipt:
        program = self._program(program_id)
        blockers = self._program_blockers(program)
        decision = "approved" if not blockers and program.eval_summary is not None and program.eval_summary.decision == "approved" else "blocked"
        receipt = self.repository.put_approval_receipt(
            StillVisualApprovalReceipt(
                program_id=program_id,
                operator_id=operator_id,
                decision=decision,
                blocker_codes=blockers if decision == "blocked" else [],
                evidence_refs=[f"still_visual_program:{program_id}", f"eval_summary:{program.eval_summary.still_visual_eval_summary_id}" if program.eval_summary else "eval_summary:missing"],
            )
        )
        status = ApprovalStatus.approved if decision == "approved" else ApprovalStatus.blocked
        self._update_program(
            program,
            approval_status=status,
            blocker_codes=receipt.blocker_codes,
            stage_updates={"approval": ("completed" if decision == "approved" else "blocked", [f"approval:{receipt.still_visual_approval_receipt_id}"], [f"approval_receipt:{receipt.still_visual_approval_receipt_id}"])},
        )
        return receipt

    def reject_program(self, *, program_id: UUID, operator_id: UUID, reason: str) -> StillVisualApprovalReceipt:
        receipt = self.repository.put_approval_receipt(
            StillVisualApprovalReceipt(
                program_id=program_id,
                operator_id=operator_id,
                decision="blocked",
                blocker_codes=["STILL_VISUAL_OPERATOR_REJECTED"],
                evidence_refs=[reason],
            )
        )
        program = self._program(program_id)
        self._update_program(program, approval_status=ApprovalStatus.blocked, blocker_codes=receipt.blocker_codes)
        return receipt

    def revise_program(self, *, program_id: UUID, revision_scope: str, reason: str) -> StillVisualRevisionCommand:
        command = StillVisualRevisionCommand(
            program_id=program_id,
            revision_scope=revision_scope,  # type: ignore[arg-type]
            reason=reason,
            command_ref=f"command:still-visual-revision:{program_id}:{revision_scope}",
        )
        return self.repository.put_revision_command(command)

    def export_program(self, *, program_id: UUID) -> StillVisualExportManifest:
        program = self._program(program_id)
        approvals = [item for item in self.repository.approval_receipts.values() if item.program_id == program_id and item.decision == "approved"]
        if not approvals or program.approval_status != ApprovalStatus.approved:
            raise StillVisualProgramServiceError("STILL_VISUAL_APPROVAL_REQUIRED", "Still visual export requires approved program.")
        manifest = self.repository.put_export_manifest(
            StillVisualExportManifest(
                program_id=program_id,
                exported_asset_refs=[program.render_manifest.render_ref if program.render_manifest else f"render://still-visual/{program_id}.png"],
                package_handoff_ref=f"package_handoff:still-visual:{program_id}",
                approval_receipt_ref=f"still_visual_approval_receipt:{approvals[-1].still_visual_approval_receipt_id}",
            )
        )
        self._update_program(
            program,
            stage_updates={"export": ("completed", manifest.exported_asset_refs, [f"export_manifest:{manifest.still_visual_export_manifest_id}"])},
        )
        return manifest

    def _builder_ref(self, family: str) -> str:
        return {
            "carousel": "CarouselBuilderProgram",
            "supervisual": "SuperVisualSingleImageSkiaBuilder",
            "visual_poll": "VisualPollSkiaBuilder",
            "tweet_quote": "TweetLikeQuoteSkiaBuilder",
            "meme": "MemeSkiaBuilder",
            "reaction_still": "ReactionStillSkiaBuilder",
        }[family]

    def _program(self, program_id: UUID) -> StillVisualCompositionProgram:
        try:
            return self.repository.programs[program_id]
        except KeyError as exc:
            raise StillVisualProgramServiceError("STILL_VISUAL_PROGRAM_NOT_FOUND", str(program_id)) from exc

    def _update_program(self, program: StillVisualCompositionProgram, *, stage_updates: dict | None = None, **updates) -> StillVisualCompositionProgram:
        stage_states = program.stage_states
        if stage_updates:
            next_states: list[StillVisualStageState] = []
            for stage in stage_states:
                if stage.stage_code in stage_updates:
                    status, artifacts, receipts = stage_updates[stage.stage_code]
                    next_states.append(
                        stage.model_copy(
                            update={
                                "status": status,
                                "artifact_refs": artifacts,
                                "receipt_refs": receipts,
                                "blocker_codes": updates.get("blocker_codes", []),
                            }
                        )
                    )
                else:
                    next_states.append(stage)
            stage_states = next_states
        next_program = program.model_copy(update={**updates, "stage_states": stage_states})
        self.repository.programs[next_program.still_visual_composition_program_id] = next_program
        return next_program

    def _program_blockers(self, program: StillVisualCompositionProgram) -> list[str]:
        blockers = list(program.blocker_codes)
        if not program.family_route:
            blockers.append("STILL_VISUAL_ROUTE_MISSING")
        if not program.provider_plan:
            blockers.append("STILL_VISUAL_PROVIDER_PLAN_MISSING")
        if not program.render_manifest:
            blockers.append("STILL_VISUAL_RENDER_MISSING")
        if not program.eval_summary:
            blockers.append("STILL_VISUAL_EVAL_MISSING")
        elif program.eval_summary.decision != "approved":
            blockers.extend(program.eval_summary.blocker_codes)
        return sorted(set(blockers))

    @staticmethod
    def _repair_commands(blockers: list[str]) -> list[str]:
        mapping = {
            "STILL_VISUAL_ROUTE_MISSING": "route",
            "STILL_VISUAL_PROVIDER_PLAN_MISSING": "materialize",
            "STILL_VISUAL_RENDER_MISSING": "render",
            "STILL_VISUAL_EVAL_MISSING": "evaluate",
            "STILL_VISUAL_SOURCE_TRUTH_BELOW_THRESHOLD": "revise-source-evidence",
            "STILL_VISUAL_PRIMITIVE_TRIAD_MISSING": "revise-primitive-triad",
        }
        return [mapping.get(blocker, "revise") for blocker in blockers]
