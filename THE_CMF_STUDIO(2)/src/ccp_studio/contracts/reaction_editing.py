"""Reaction editing template contracts for live-filmed CMF formats."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class ReactionEditingTemplateCode(str, Enum):
    versus_split = "VRS-SPLIT"
    tier_list = "TRK-TIER"
    blind_ranking = "RNK-BLIND"
    proposal_ranking = "RNK-PROPOSAL"
    elimination_bracket = "ELM-BRACKET"
    mirror_quiz = "MIR-QUIZ"
    authority_ladder = "AUTH-LADDER"


class ReactionEditingFamily(str, Enum):
    versus = "versus"
    tier_list = "tier_list"
    ranking = "ranking"
    elimination = "elimination"
    mirror_quiz = "mirror_quiz"
    authority_quiz = "authority_quiz"


class LiveClipSlotKind(str, Enum):
    live_answer = "live_answer"
    option = "option"
    verdict = "verdict"
    rank_item = "rank_item"
    audience_mirror = "audience_mirror"
    authority_test = "authority_test"


class LiveClipSlotSpec(BaseModel):
    schema_version: Literal["cmf.live_clip_slot_spec.v1"] = "cmf.live_clip_slot_spec.v1"
    slot_key: str = Field(min_length=1)
    slot_kind: LiveClipSlotKind
    prompt_instruction: str = Field(min_length=1)
    source_requirement: str = Field(min_length=1)
    min_duration_seconds: float = Field(gt=0)
    max_duration_seconds: float = Field(gt=0)
    required_expression_state: str = Field(min_length=1)


class TemplateMotionGrammar(BaseModel):
    schema_version: Literal["cmf.template_motion_grammar.v1"] = "cmf.template_motion_grammar.v1"
    renderer_route: str = Field(min_length=1)
    composition_id: str = Field(min_length=1)
    scene_pattern: str = Field(min_length=1)
    overlay_roles: list[str] = Field(min_length=1)
    transition_rules: list[str] = Field(min_length=1)
    timing_rules: list[str] = Field(min_length=1)


class ReactionEditingTemplate(BaseModel):
    schema_version: Literal["cmf.reaction_editing_template.v1"] = "cmf.reaction_editing_template.v1"
    template_code: ReactionEditingTemplateCode
    display_name: str = Field(min_length=1)
    family: ReactionEditingFamily
    valid_content_format_codes: list[str] = Field(min_length=1)
    source_app_refs: list[str] = Field(min_length=1)
    alias_terms: list[str] = Field(min_length=1)
    interview_question_instruction: str = Field(min_length=1)
    live_clip_slots: list[LiveClipSlotSpec] = Field(min_length=1)
    motion_grammar: TemplateMotionGrammar
    primitive_eval_obligations: list[str] = Field(min_length=1)
    registry_refs: list[str] = Field(default_factory=list)
    active: bool = True


class ReactionTemplateRoute(BaseModel):
    schema_version: Literal["cmf.reaction_template_route.v1"] = "cmf.reaction_template_route.v1"
    reaction_template_route_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_moment_id: UUID
    asset_route_receipt_id: UUID
    template_code: ReactionEditingTemplateCode
    content_format_code: str = Field(min_length=1)
    source_support_evidence: list[str] = Field(min_length=1)
    live_clip_slot_specs: list[LiveClipSlotSpec] = Field(min_length=1)
    scene_spec_requirement_patch: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class ReactionTemplateRouteReceipt(BaseModel):
    schema_version: Literal["cmf.reaction_template_route_receipt.v1"] = "cmf.reaction_template_route_receipt.v1"
    reaction_template_route_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_moment_id: UUID
    asset_route_receipt_id: UUID
    reaction_template_route_id: UUID | None = None
    template_code: ReactionEditingTemplateCode | None = None
    content_format_code: str | None = None
    registry_version: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    source_support_evidence: list[str] = Field(default_factory=list)
    live_clip_slot_keys: list[str] = Field(default_factory=list)
    scene_spec_requirement_patch: dict[str, Any] = Field(default_factory=dict)
    evaluator_summary: str = Field(min_length=1)
    actor_id: UUID
    written_at: datetime


def reaction_template_registry_version(templates: list[ReactionEditingTemplate]) -> str:
    payload = json.dumps(
        [
            {
                "template_code": template.template_code.value,
                "active": template.active,
                "valid_content_format_codes": template.valid_content_format_codes,
                "source_app_refs": template.source_app_refs,
            }
            for template in sorted(templates, key=lambda item: item.template_code.value)
        ],
        sort_keys=True,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
    return f"cmf-reaction-template-registry:{digest}"


def default_reaction_editing_templates() -> list[ReactionEditingTemplate]:
    def slot(
        key: str,
        kind: LiveClipSlotKind,
        instruction: str,
        requirement: str,
        state: str,
        min_seconds: float = 3,
        max_seconds: float = 18,
    ) -> LiveClipSlotSpec:
        return LiveClipSlotSpec(
            slot_key=key,
            slot_kind=kind,
            prompt_instruction=instruction,
            source_requirement=requirement,
            min_duration_seconds=min_seconds,
            max_duration_seconds=max_seconds,
            required_expression_state=state,
        )

    return [
        ReactionEditingTemplate(
            template_code=ReactionEditingTemplateCode.versus_split,
            display_name="Versus Split Screen",
            family=ReactionEditingFamily.versus,
            valid_content_format_codes=["SV-RRC", "VPL-VRS", "VPL-WYR", "RCT-SEED"],
            source_app_refs=["apps/react-debate"],
            alias_terms=["debate", "this vs that", "versus", "would you rather", "split screen"],
            interview_question_instruction="Ask the guest to choose between two audience-relevant tensions and explain the hidden cost of the losing side.",
            live_clip_slots=[
                slot("option_a", LiveClipSlotKind.option, "Name side A in concrete audience language.", "two explicit sides are present", "contrast naming"),
                slot("option_b", LiveClipSlotKind.option, "Name side B in concrete audience language.", "two explicit sides are present", "contrast naming"),
                slot("verdict", LiveClipSlotKind.verdict, "Give the choice and the reason it matters now.", "clear stance and rationale", "decisive conviction"),
            ],
            motion_grammar=TemplateMotionGrammar(
                renderer_route="remotion_reaction_template",
                composition_id="reaction-versus-split",
                scene_pattern="split_screen_vs_with_live_guest_verdict",
                overlay_roles=["option_a_card", "option_b_card", "guest_cutaway", "verdict_tick", "comment_prompt"],
                transition_rules=["snap_into_two_sides", "pulse_selected_side", "end_on_verdict_card"],
                timing_rules=["hook_under_2s", "choice_reveal_before_6s", "guest_verdict_8_to_18s"],
            ),
            primitive_eval_obligations=["FBK:contrast_preserved", "TRG:audience_choice_pressure", "VSG:clear_binary_eye_path"],
        ),
        ReactionEditingTemplate(
            template_code=ReactionEditingTemplateCode.tier_list,
            display_name="Tier List Ranking",
            family=ReactionEditingFamily.tier_list,
            valid_content_format_codes=["SV-RRC", "SV-EDU", "CAR-LST", "RCT-SEED"],
            source_app_refs=["apps/react-tierlist"],
            alias_terms=["tier list", "rank these", "s tier", "a tier", "red flag tier"],
            interview_question_instruction="Ask the guest to rank a set of mistakes, beliefs, tactics, or audience behaviors from most harmless to most dangerous.",
            live_clip_slots=[
                slot("rank_items", LiveClipSlotKind.rank_item, "Collect 4-7 rankable items in the guest's own words.", "multiple concrete items", "rapid discernment", 5, 30),
                slot("top_tier_reason", LiveClipSlotKind.verdict, "Explain why the highest tier deserves its position.", "one clear top-tier rationale", "authority explanation"),
            ],
            motion_grammar=TemplateMotionGrammar(
                renderer_route="remotion_reaction_template",
                composition_id="reaction-tier-list",
                scene_pattern="animated_tier_board_with_live_guest_reason",
                overlay_roles=["tier_board", "item_cards", "guest_facecam", "top_tier_reveal", "caption_track"],
                transition_rules=["card_drop_to_tier", "lock_top_tier", "zoom_reason_clip"],
                timing_rules=["first_item_under_3s", "tier_lock_every_2_to_4s", "top_reason_8_to_20s"],
            ),
            primitive_eval_obligations=["STR:rank_logic_clear", "FBK:source_claim_trace", "VSG:board_readability"],
        ),
        ReactionEditingTemplate(
            template_code=ReactionEditingTemplateCode.blind_ranking,
            display_name="Blind Ranking",
            family=ReactionEditingFamily.ranking,
            valid_content_format_codes=["SV-RRC", "VPL-VRS", "RCT-SEED"],
            source_app_refs=["apps/react-blind-rank"],
            alias_terms=["blind ranking", "blind rank", "rank without knowing", "locked ranking"],
            interview_question_instruction="Give the guest items one by one and force placement before the next item is revealed.",
            live_clip_slots=[
                slot("sequential_items", LiveClipSlotKind.rank_item, "Capture each item before the guest knows the next one.", "ordered blind-rank items", "uncertain judgment", 5, 30),
                slot("regret_or_confirmation", LiveClipSlotKind.verdict, "Capture the final reaction after the last reveal.", "final confirmation or regret", "live reaction"),
            ],
            motion_grammar=TemplateMotionGrammar(
                renderer_route="remotion_reaction_template",
                composition_id="reaction-blind-ranking",
                scene_pattern="locked_slots_reveal_with_live_reaction",
                overlay_roles=["locked_slots", "incoming_item_card", "reaction_zoom", "final_board"],
                transition_rules=["item_reveal", "slot_lock", "final_board_snap"],
                timing_rules=["item_reveal_every_3_to_5s", "final_reaction_5_to_12s"],
            ),
            primitive_eval_obligations=["TRG:suspense_loop", "FBK:source_item_integrity", "VSG:locked_order_clarity"],
        ),
        ReactionEditingTemplate(
            template_code=ReactionEditingTemplateCode.proposal_ranking,
            display_name="Proposal Ranking Quiz",
            family=ReactionEditingFamily.ranking,
            valid_content_format_codes=["SV-EDU", "SV-RRC", "CAR-LST", "RCT-SEED"],
            source_app_refs=["apps/react-ranking-quiz"],
            alias_terms=["ranking quiz", "reorder", "proposal ranking", "rank proposal"],
            interview_question_instruction="Ask the guest to correct or reorder a proposed ranking and explain the hidden principle behind the correction.",
            live_clip_slots=[
                slot("proposed_order", LiveClipSlotKind.rank_item, "Present a proposed order for correction.", "initial order is explicit", "critical evaluation"),
                slot("corrected_order", LiveClipSlotKind.verdict, "Capture the corrected order and why.", "corrected order with rationale", "teaching verdict"),
            ],
            motion_grammar=TemplateMotionGrammar(
                renderer_route="remotion_reaction_template",
                composition_id="reaction-ranking-proposal",
                scene_pattern="proposal_board_reordered_by_guest_explanation",
                overlay_roles=["proposal_board", "drag_reorder_cards", "guest_explanation", "principle_card"],
                transition_rules=["show_wrong_order", "animate_reorder", "freeze_principle"],
                timing_rules=["wrong_order_under_4s", "reorder_4_to_12s", "principle_8_to_18s"],
            ),
            primitive_eval_obligations=["STR:principle_distilled", "FBK:correction_grounded", "VSG:reorder_legible"],
        ),
        ReactionEditingTemplate(
            template_code=ReactionEditingTemplateCode.elimination_bracket,
            display_name="Elimination Bracket",
            family=ReactionEditingFamily.elimination,
            valid_content_format_codes=["SV-RRC", "VPL-VRS", "RCT-SEED"],
            source_app_refs=["apps/react-elimination"],
            alias_terms=["elimination", "bracket", "knockout", "which one survives"],
            interview_question_instruction="Ask the guest to eliminate options until one cause, mistake, idea, or priority survives.",
            live_clip_slots=[
                slot("candidate_set", LiveClipSlotKind.option, "Collect the options that enter the bracket.", "clear option set", "comparison pressure"),
                slot("winner", LiveClipSlotKind.verdict, "Capture the surviving winner and why it beats the alternatives.", "final winner with rationale", "decisive synthesis"),
            ],
            motion_grammar=TemplateMotionGrammar(
                renderer_route="remotion_reaction_template",
                composition_id="reaction-elimination-bracket",
                scene_pattern="knockout_bracket_with_guest_winner",
                overlay_roles=["bracket_grid", "elimination_x", "winner_card", "guest_verdict"],
                transition_rules=["advance_winner", "cross_out_loser", "winner_flash"],
                timing_rules=["rounds_every_3_to_5s", "winner_reason_6_to_15s"],
            ),
            primitive_eval_obligations=["TRG:choice_escalation", "STR:final_reason_clear", "VSG:bracket_progression"],
        ),
        ReactionEditingTemplate(
            template_code=ReactionEditingTemplateCode.mirror_quiz,
            display_name="Mirror Quiz",
            family=ReactionEditingFamily.mirror_quiz,
            valid_content_format_codes=["SV-RRC", "VPL-WYR", "MEM-REL", "RCT-SEED"],
            source_app_refs=["apps/react-mirror-quiz"],
            alias_terms=["mirror quiz", "which one are you", "identity quiz", "audience mirror"],
            interview_question_instruction="Ask the guest to name the private sentence, behavior, or identity split the audience recognizes but rarely says publicly.",
            live_clip_slots=[
                slot("mirror_sentence", LiveClipSlotKind.audience_mirror, "Capture the audience's private self-description.", "specific audience self-recognition", "recognition"),
                slot("identity_label", LiveClipSlotKind.verdict, "Give the label or archetype that helps the audience see itself.", "clear identity label", "naming and recognition"),
            ],
            motion_grammar=TemplateMotionGrammar(
                renderer_route="remotion_reaction_template",
                composition_id="reaction-mirror-quiz",
                scene_pattern="identity_cards_with_live_guest_mirror",
                overlay_roles=["quiz_cards", "identity_labels", "guest_mirror_clip", "comment_prompt"],
                transition_rules=["card_flip", "label_snap", "comment_prompt_hold"],
                timing_rules=["identity_hook_under_3s", "mirror_clip_6_to_18s"],
            ),
            primitive_eval_obligations=["PSY:recognition_not_stereotype", "FBK:audience_truth_grounded", "VSG:quiz_card_readability"],
        ),
        ReactionEditingTemplate(
            template_code=ReactionEditingTemplateCode.authority_ladder,
            display_name="Authority Ladder Quiz",
            family=ReactionEditingFamily.authority_quiz,
            valid_content_format_codes=["SV-EDU", "SV-RRC", "RCT-SEED"],
            source_app_refs=["apps/react-authority-quiz"],
            alias_terms=["authority quiz", "expert test", "authority ladder", "level test"],
            interview_question_instruction="Ask the guest for the question or distinction that separates shallow advice from real understanding.",
            live_clip_slots=[
                slot("test_question", LiveClipSlotKind.authority_test, "Capture the expert diagnostic question.", "diagnostic question or gate", "authority test"),
                slot("level_explanation", LiveClipSlotKind.verdict, "Explain what the answer reveals about level of understanding.", "clear level distinction", "expert framing"),
            ],
            motion_grammar=TemplateMotionGrammar(
                renderer_route="remotion_reaction_template",
                composition_id="reaction-authority-ladder",
                scene_pattern="level_gates_with_guest_expert_test",
                overlay_roles=["level_ladder", "pass_fail_gate", "guest_explanation", "score_reveal"],
                transition_rules=["gate_light_up", "level_advance", "score_reveal"],
                timing_rules=["test_question_under_5s", "level_explanation_8_to_20s"],
            ),
            primitive_eval_obligations=["STR:expert_distinction_clear", "FBK:no_fake_authority", "VSG:level_path_legible"],
        ),
    ]


def new_reaction_template_route_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    expression_moment_id: UUID,
    asset_route_receipt_id: UUID,
    registry_version: str,
    decision_code: str,
    evaluator_summary: str,
    actor_id: UUID,
    reaction_template_route_id: UUID | None = None,
    template_code: ReactionEditingTemplateCode | None = None,
    content_format_code: str | None = None,
    source_support_evidence: list[str] | None = None,
    live_clip_slot_keys: list[str] | None = None,
    scene_spec_requirement_patch: dict[str, Any] | None = None,
) -> ReactionTemplateRouteReceipt:
    return ReactionTemplateRouteReceipt(
        reaction_template_route_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        expression_moment_id=expression_moment_id,
        asset_route_receipt_id=asset_route_receipt_id,
        reaction_template_route_id=reaction_template_route_id,
        template_code=template_code,
        content_format_code=content_format_code,
        registry_version=registry_version,
        decision_code=decision_code,
        source_support_evidence=source_support_evidence or [],
        live_clip_slot_keys=live_clip_slot_keys or [],
        scene_spec_requirement_patch=scene_spec_requirement_patch or {},
        evaluator_summary=evaluator_summary,
        actor_id=actor_id,
        written_at=utc_now(),
    )
