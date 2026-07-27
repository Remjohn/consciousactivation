"""Doctrine and primitive eval selection for interview-first outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from ccp_studio.contracts.doctrine_evals import (
    DoctrineEvalDecision,
    DoctrineEvalDefinition,
    DoctrineEvalSelection,
    DoctrineEvalTargetInput,
    DoctrineEvidenceRequirement,
    PrimitiveEvalObligation,
    new_doctrine_eval_selection,
)
from ccp_studio.contracts.evaluation_receipts import (
    EvaluationCategory,
    EvaluationCategoryInput,
    EvaluationObjectType,
    EvaluationReceipt,
    EvidenceClaimScope,
    EvidencePointer,
)
from ccp_studio.services.evaluation_receipt_service import EvaluationReceiptService


def canonical_interview_brief_doctrine_eval_definition() -> DoctrineEvalDefinition:
    return DoctrineEvalDefinition(
        eval_definition_id="EVL-DOCTRINE-IAC-001",
        name="Interview Brief / Interview Asset Contract Doctrine Eval",
        object_types=[EvaluationObjectType.interview_brief, EvaluationObjectType.interview_asset_contract, EvaluationObjectType.skill_output],
        pipeline_stages=["4", "interview_intelligence", "conscious_interview_brief"],
        required_categories=[
            EvaluationCategory.doctrine_alignment,
            EvaluationCategory.ccf_orchestration_lineage,
            EvaluationCategory.primitive_registry_fidelity,
            EvaluationCategory.context_premise_integrity,
            EvaluationCategory.narrative_induction_integrity,
            EvaluationCategory.anchor_contract_integrity,
            EvaluationCategory.routeability,
            EvaluationCategory.evaluation_target_coverage,
        ],
        source_doctrine_refs=[
            "THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md",
            "THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md",
            "THE CMF STUDIO/Claude Ntahuga Interview Deck — V4.docx.md",
            "THE CMF STUDIO/Matrix of Edging.md",
            "THE CMF STUDIO/reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md",
            "THE CMF STUDIO/reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md",
            "THE CMF STUDIO/docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md",
            "THE CMF STUDIO/docs/methodology/4_Laws_of_Layered_Questions.md",
        ],
        evidence_requirements=[
            DoctrineEvidenceRequirement(
                route="cral_scre_signal",
                description="CRAL/SCRE finding or signal packet that makes the contract necessary.",
                maps_to_category=EvaluationCategory.ccf_orchestration_lineage,
            ),
            DoctrineEvidenceRequirement(
                route="audience_conversation",
                description="Audience comments, objections, search questions, or social debate evidence.",
                maps_to_category=EvaluationCategory.context_premise_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="context_premise",
                description="Approved Context Premise operationalized by the contract.",
                maps_to_category=EvaluationCategory.context_premise_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="audience_deep_trigger_map",
                description="Trigger map proving audience pressure and depth.",
                maps_to_category=EvaluationCategory.context_premise_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="interviewer_resonance",
                description="Interviewer Resonance Context shaping the high-identification field.",
                maps_to_category=EvaluationCategory.narrative_induction_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="matrix_of_edging",
                description="Matrix pressure, tension site, primitive pass, coalition, or edge product.",
                maps_to_category=EvaluationCategory.narrative_induction_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="primitive_registry",
                description="Active primitive refs and obligations from the project registry.",
                maps_to_category=EvaluationCategory.primitive_registry_fidelity,
            ),
            DoctrineEvidenceRequirement(
                route="first_line_anchors",
                description="Cinematic, emotional, and reels-hook First-Line Anchor options.",
                maps_to_category=EvaluationCategory.anchor_contract_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="depth_anchor",
                description="Depth Anchor preventing centroid or abstract answers.",
                maps_to_category=EvaluationCategory.anchor_contract_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="landing_eval_targets",
                description="Landing evaluation targets that preserve discovery rather than force an answer.",
                maps_to_category=EvaluationCategory.evaluation_target_coverage,
            ),
            DoctrineEvidenceRequirement(
                route="repair_followups",
                description="Repair followups for historical, abstract, flat, or non-clip-ready answers.",
                maps_to_category=EvaluationCategory.anchor_contract_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="route_target",
                description="Archetype, derivative, CMF route, and Guest Asset Pack route target.",
                maps_to_category=EvaluationCategory.routeability,
            ),
            DoctrineEvidenceRequirement(
                route="hard_negative",
                description="Hard negative or counterexample showing the cheap/generic failure mode.",
                maps_to_category=EvaluationCategory.evaluation_target_coverage,
            ),
        ],
        primitive_obligations=[
            PrimitiveEvalObligation(
                primitive_family="STR",
                registry_ref="registries/primitives/meaning_plane/narrative_structure",
                obligation="Narrative structure must create extractable scene or principle, not biography filler.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="TRG",
                registry_ref="registries/primitives/experience_plane/trigger_timing",
                obligation="Trigger timing must explain why the audience pressure is active now.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="PSY",
                registry_ref="registries/primitives/meaning_plane/psychological_diagnostics",
                obligation="Psychological diagnostic pressure must be evidence-backed, not personality typing.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="PRS",
                registry_ref="registries/primitives/meaning_plane/persuasion",
                obligation="Persuasion mechanics must support routeability without coercing the guest landing.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="FBK",
                registry_ref="registries/primitives/experience_plane/feedback_scoring",
                obligation="Evaluation feedback must expose primitive failure and repair action.",
                evidence_route="primitive_registry",
            ),
        ],
        threshold=0.86,
        hard_failure_codes=[
            "DOCTRINE_SOURCE_MISSING",
            "DOCTRINE_EVIDENCE_ROUTE_MISSING",
            "PRIMITIVE_OBLIGATION_MISSING",
        ],
    )


def canonical_brand_genesis_doctrine_eval_definition() -> DoctrineEvalDefinition:
    return DoctrineEvalDefinition(
        eval_definition_id="EVL-DOCTRINE-BGN-001",
        name="Brand Genesis / Brand Context Doctrine Eval",
        object_types=[
            EvaluationObjectType.brand_genesis_session,
            EvaluationObjectType.brand_context_version,
            EvaluationObjectType.skill_output,
        ],
        pipeline_stages=["brand_genesis", "brand_context_lock", "client_onboarding"],
        required_categories=[
            EvaluationCategory.doctrine_alignment,
            EvaluationCategory.brand_genesis_completeness,
            EvaluationCategory.asset_generation_policy,
            EvaluationCategory.identity_consistency,
            EvaluationCategory.negative_space,
            EvaluationCategory.micro_semiotic_integrity,
            EvaluationCategory.acting_library_coverage,
            EvaluationCategory.papercut_rig_integrity,
            EvaluationCategory.primitive_registry_fidelity,
            EvaluationCategory.evaluation_target_coverage,
        ],
        source_doctrine_refs=[
            "THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md",
            "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md",
            "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md",
            "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/03_IMPLEMENTATION_SEQUENCE_AND_RELEASE_GATES.md",
            "THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md",
            "THE CMF STUDIO/PROJECT_STRUCTURE.md",
            "THE CMF STUDIO/reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md",
        ],
        evidence_requirements=[
            DoctrineEvidenceRequirement(
                route="client_intake",
                description="Typed business, audience, platform, tone, visual preference, and forbidden-claim intake.",
                maps_to_category=EvaluationCategory.brand_genesis_completeness,
            ),
            DoctrineEvidenceRequirement(
                route="consent_record",
                description="Explicit consent covering photos, synthetic realistic derivatives, stylized avatars, memes, reuse, providers, and retention.",
                maps_to_category=EvaluationCategory.asset_generation_policy,
            ),
            DoctrineEvidenceRequirement(
                route="source_media_qc",
                description="Source photo/video quality check for face visibility, resolution, blur, lighting, angle diversity, expression diversity, and full-body availability.",
                maps_to_category=EvaluationCategory.identity_consistency,
            ),
            DoctrineEvidenceRequirement(
                route="business_intelligence",
                description="Offer, transformation promise, evidence, differentiation, claims boundaries, and business constraints.",
                maps_to_category=EvaluationCategory.brand_genesis_completeness,
            ),
            DoctrineEvidenceRequirement(
                route="tribe_soul",
                description="Audience intelligence including cultural context, anxieties, rituals, inside jokes, ordinary-life objects, and identity tensions.",
                maps_to_category=EvaluationCategory.brand_genesis_completeness,
            ),
            DoctrineEvidenceRequirement(
                route="character_lexicon",
                description="Signature terms, idioms, metaphors, phrase patterns, forbidden cliches, and platform variations.",
                maps_to_category=EvaluationCategory.brand_genesis_completeness,
            ),
            DoctrineEvidenceRequirement(
                route="voice_dna_negative_space",
                description="Voice DNA, Emotional DNA, Positive Space, Negative Space, confidence, provenance, and explicit do-not-change constraints.",
                maps_to_category=EvaluationCategory.negative_space,
            ),
            DoctrineEvidenceRequirement(
                route="visual_constitution",
                description="Approved and forbidden visual style constitution for realistic references, photo paper cutouts, and editorial PaperCut avatar modes.",
                maps_to_category=EvaluationCategory.identity_consistency,
            ),
            DoctrineEvidenceRequirement(
                route="identity_pack",
                description="Versioned Identity Pack with approved references, conditioning stack, worker digest, workflow hash, and forbidden runtime mutations.",
                maps_to_category=EvaluationCategory.identity_consistency,
            ),
            DoctrineEvidenceRequirement(
                route="acting_library_plan",
                description="64-state acting library plan and approval dependency before downstream CMF production.",
                maps_to_category=EvaluationCategory.acting_library_coverage,
            ),
            DoctrineEvidenceRequirement(
                route="papercut_rig_plan",
                description="PaperCut avatar and rig plan as a separate deterministic actor system.",
                maps_to_category=EvaluationCategory.papercut_rig_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="micro_semiotic_anchor_library",
                description="Approved anchor library with recognition effects, risk scores, subtle placement, and rights review.",
                maps_to_category=EvaluationCategory.micro_semiotic_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="genesis_clearance_certificate",
                description="Clearance certificate proving consent, identity summary, acting library, rig, negative space, visual constitution, and registries are approved.",
                maps_to_category=EvaluationCategory.evaluation_target_coverage,
            ),
        ],
        primitive_obligations=[
            PrimitiveEvalObligation(
                primitive_family="IDN",
                registry_ref="registries/primitives/identity_plane",
                obligation="Identity primitives must bind stable traits, source evidence, do-not-change constraints, and allowed style modes.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="AUD",
                registry_ref="registries/primitives/audience_plane",
                obligation="Audience and Tribe Soul primitives must ground ordinary-life objects and cultural recognition without stereotyping.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="VOI",
                registry_ref="registries/primitives/voice_plane",
                obligation="Voice DNA and Emotional DNA primitives must preserve Positive Space, Negative Space, source hierarchy, and confidence.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="VSG",
                registry_ref="registries/primitives/visual_plane",
                obligation="Visual primitives must constrain material style, composition preferences, and forbidden visual modes.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="SAF",
                registry_ref="registries/primitives/governance_plane",
                obligation="Consent, provider policy, likeness use, rights review, and human approvals must be explicit before generation or lock.",
                evidence_route="primitive_registry",
            ),
        ],
        threshold=0.88,
        hard_failure_codes=[
            "DOCTRINE_SOURCE_MISSING",
            "DOCTRINE_EVIDENCE_ROUTE_MISSING",
            "PRIMITIVE_OBLIGATION_MISSING",
        ],
    )


def canonical_acting_library_doctrine_eval_definition() -> DoctrineEvalDefinition:
    return DoctrineEvalDefinition(
        eval_definition_id="EVL-DOCTRINE-ACT-064-001",
        name="64-State Acting Library Doctrine Eval",
        object_types=[
            EvaluationObjectType.acting_library,
            EvaluationObjectType.acting_reference,
            EvaluationObjectType.brand_context_version,
        ],
        pipeline_stages=["acting_library_generation", "acting_library_review", "brand_genesis"],
        required_categories=[
            EvaluationCategory.doctrine_alignment,
            EvaluationCategory.acting_library_coverage,
            EvaluationCategory.asset_generation_policy,
            EvaluationCategory.identity_consistency,
            EvaluationCategory.likeness,
            EvaluationCategory.negative_space,
            EvaluationCategory.primitive_registry_fidelity,
            EvaluationCategory.evaluation_target_coverage,
        ],
        source_doctrine_refs=[
            "THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md",
            "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md",
            "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md",
            "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/03_IMPLEMENTATION_SEQUENCE_AND_RELEASE_GATES.md",
            "THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md",
        ],
        evidence_requirements=[
            DoctrineEvidenceRequirement(
                route="identity_pack",
                description="Approved Identity Pack with pinned references, worker digest, workflow hash, model settings, and immutable runtime policy.",
                maps_to_category=EvaluationCategory.identity_consistency,
            ),
            DoctrineEvidenceRequirement(
                route="human_approval_before_generation",
                description="Human approval of identity summary before 64-state generation starts.",
                maps_to_category=EvaluationCategory.asset_generation_policy,
            ),
            DoctrineEvidenceRequirement(
                route="acting_state_matrix_64",
                description="Complete 8 x 8 matrix of emotions and gesture/body-language families.",
                maps_to_category=EvaluationCategory.acting_library_coverage,
            ),
            DoctrineEvidenceRequirement(
                route="provider_receipts_64",
                description="Provider/model/version receipts for all generated acting cells or documented replacements.",
                maps_to_category=EvaluationCategory.asset_generation_policy,
            ),
            DoctrineEvidenceRequirement(
                route="cell_metadata",
                description="Per-cell metadata for emotion, communicative intent, gesture family, body language, facial expression, energy, framing, orientation, and layout bias.",
                maps_to_category=EvaluationCategory.acting_library_coverage,
            ),
            DoctrineEvidenceRequirement(
                route="auto_qc_scores",
                description="Auto-QC scores for likeness, emotion, gesture, hands, crop, artifact, wardrobe, and visual drift.",
                maps_to_category=EvaluationCategory.likeness,
            ),
            DoctrineEvidenceRequirement(
                route="human_review_grid",
                description="Human review grid with approved, needs-fix, rejected, and repair notes for all cells.",
                maps_to_category=EvaluationCategory.evaluation_target_coverage,
            ),
            DoctrineEvidenceRequirement(
                route="negative_space_updates",
                description="Approved update route for rejected patterns that become visual Negative Space.",
                maps_to_category=EvaluationCategory.negative_space,
            ),
            DoctrineEvidenceRequirement(
                route="library_lock_receipt",
                description="Lock receipt proving 64 approved cells, no missing cells, and no unapproved image retrieval.",
                maps_to_category=EvaluationCategory.evaluation_target_coverage,
            ),
        ],
        primitive_obligations=[
            PrimitiveEvalObligation(
                primitive_family="ACT",
                registry_ref="registries/primitives/visual_plane/acting",
                obligation="Acting primitives must represent communicative performance, not random posing.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="IDN",
                registry_ref="registries/primitives/identity_plane",
                obligation="Identity primitives must preserve stable traits, age, body type, hair, wardrobe, and source-evidence lineage.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="NEG",
                registry_ref="registries/primitives/negative_space",
                obligation="Rejected visual patterns must update Negative Space only after human approval.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="VSG",
                registry_ref="registries/primitives/visual_plane",
                obligation="Visual scoring primitives must gate likeness, emotion, gesture, hands, crop, and artifact risks.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="SAF",
                registry_ref="registries/primitives/governance_plane",
                obligation="Provider and likeness generation policy must be compatible with consent before dispatch.",
                evidence_route="primitive_registry",
            ),
        ],
        threshold=0.9,
        hard_failure_codes=[
            "DOCTRINE_SOURCE_MISSING",
            "DOCTRINE_EVIDENCE_ROUTE_MISSING",
            "PRIMITIVE_OBLIGATION_MISSING",
        ],
    )


def canonical_papercut_rig_doctrine_eval_definition() -> DoctrineEvalDefinition:
    return DoctrineEvalDefinition(
        eval_definition_id="EVL-DOCTRINE-PPR-RIG-001",
        name="PaperCut Rig / 2D Animation Doctrine Eval",
        object_types=[
            EvaluationObjectType.papercut_rig,
            EvaluationObjectType.rig_manifest,
            EvaluationObjectType.animation_plan,
        ],
        pipeline_stages=["avatar_generation", "layer_and_rig_build", "rig_review", "animation_planning"],
        required_categories=[
            EvaluationCategory.doctrine_alignment,
            EvaluationCategory.papercut_rig_integrity,
            EvaluationCategory.animation_readiness,
            EvaluationCategory.micro_semiotic_integrity,
            EvaluationCategory.motion_restraint,
            EvaluationCategory.style,
            EvaluationCategory.composition,
            EvaluationCategory.primitive_registry_fidelity,
            EvaluationCategory.evaluation_target_coverage,
        ],
        source_doctrine_refs=[
            "THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md",
            "THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md",
            "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md",
            "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md",
            "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI/03_IMPLEMENTATION_SEQUENCE_AND_RELEASE_GATES.md",
        ],
        evidence_requirements=[
            DoctrineEvidenceRequirement(
                route="approved_acting_library_version",
                description="Approved acting library version feeding the separate PaperCut avatar actor.",
                maps_to_category=EvaluationCategory.papercut_rig_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="required_avatar_asset_set",
                description="Required heads, eyes/brows, mouth shapes, body layers, and gesture variants.",
                maps_to_category=EvaluationCategory.papercut_rig_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="layer_decomposition",
                description="Semantic layer decomposition and precision segmentation for editable PaperCut layers.",
                maps_to_category=EvaluationCategory.papercut_rig_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="hidden_region_repair",
                description="Character-specific hidden-part repair or explicit no-repair-needed evidence.",
                maps_to_category=EvaluationCategory.papercut_rig_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="rig_manifest",
                description="Canonical rig manifest with layer IDs, z-order, anchors, pivots, parent-child links, bones, constraints, mouth maps, gesture presets, hashes, and coordinate system.",
                maps_to_category=EvaluationCategory.papercut_rig_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="editor_independence",
                description="Proof production renderer does not depend on proprietary editor-only project state.",
                maps_to_category=EvaluationCategory.papercut_rig_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="preview_tests",
                description="Preview pass for blink, nod, head bob, open-hands explanation, point, shrug, expression swap, mouth flap, stop-motion jitter, and mobile silhouette.",
                maps_to_category=EvaluationCategory.animation_readiness,
            ),
            DoctrineEvidenceRequirement(
                route="motion_constitution",
                description="Motion plan follows Paper gently coming alive: restrained intensity, low decorative motion, limited simultaneous layers, and voice-synced typography.",
                maps_to_category=EvaluationCategory.motion_restraint,
            ),
            DoctrineEvidenceRequirement(
                route="papercut_style_constitution",
                description="Material constitution: textured paper, cut edges, soft shadows, tactile grain, allowed/forbidden visual elements.",
                maps_to_category=EvaluationCategory.style,
            ),
            DoctrineEvidenceRequirement(
                route="composition_json_structure",
                description="Composition contract preserving Ideogram 4 scene specification, text areas, subject placement, metaphor objects, and layerability analysis.",
                maps_to_category=EvaluationCategory.composition,
            ),
            DoctrineEvidenceRequirement(
                route="micro_semiotic_anchor_refs",
                description="Approved 1-3 micro-semiotic anchors with subtle placement, recognition effects, and rights/stereotype risk review.",
                maps_to_category=EvaluationCategory.micro_semiotic_integrity,
            ),
            DoctrineEvidenceRequirement(
                route="rig_lock_receipt",
                description="Rig approval and lock receipt proving preview gates passed.",
                maps_to_category=EvaluationCategory.evaluation_target_coverage,
            ),
        ],
        primitive_obligations=[
            PrimitiveEvalObligation(
                primitive_family="RIG",
                registry_ref="registries/primitives/visual_plane/rigging",
                obligation="Rig primitives must make the actor reusable, inspectable, deterministic, and editable from manifest data.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="MOT",
                registry_ref="registries/primitives/motion_plane",
                obligation="Motion primitives must serve attention, meaning reveal, tactile realism, or emotional beat.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="VSG",
                registry_ref="registries/primitives/visual_plane",
                obligation="Visual primitives must enforce PaperCut materiality, layer quality, edge quality, and composition constraints.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="MSA",
                registry_ref="registries/primitives/audience_plane/micro_semiotic_anchors",
                obligation="Micro-semiotic primitives must trigger recognition without stereotype, distraction, or trademark misuse.",
                evidence_route="primitive_registry",
            ),
            PrimitiveEvalObligation(
                primitive_family="SAF",
                registry_ref="registries/primitives/governance_plane",
                obligation="Rights, consent, stereotype, and likeness constraints must govern avatar and anchor usage.",
                evidence_route="primitive_registry",
            ),
        ],
        threshold=0.88,
        hard_failure_codes=[
            "DOCTRINE_SOURCE_MISSING",
            "DOCTRINE_EVIDENCE_ROUTE_MISSING",
            "PRIMITIVE_OBLIGATION_MISSING",
        ],
    )


def canonical_doctrine_eval_definitions() -> list[DoctrineEvalDefinition]:
    return [
        canonical_interview_brief_doctrine_eval_definition(),
        canonical_brand_genesis_doctrine_eval_definition(),
        canonical_acting_library_doctrine_eval_definition(),
        canonical_papercut_rig_doctrine_eval_definition(),
    ]


@dataclass
class DoctrineEvaluationService:
    evaluation_service: EvaluationReceiptService = field(default_factory=EvaluationReceiptService)
    definitions: list[DoctrineEvalDefinition] = field(default_factory=canonical_doctrine_eval_definitions)

    def select_definition(self, target: DoctrineEvalTargetInput) -> DoctrineEvalSelection:
        definition = self._matching_definition(target)
        if definition is None:
            empty = canonical_interview_brief_doctrine_eval_definition()
            return new_doctrine_eval_selection(
                definition=empty,
                decision=DoctrineEvalDecision.not_applicable,
                missing_evidence_routes=[],
                missing_primitive_families=[],
                missing_source_doctrine_refs=[],
            )
        missing_routes = self._missing_evidence_routes(definition, target)
        missing_primitives = self._missing_primitive_families(definition, target)
        missing_doctrine_refs = self._missing_doctrine_refs(definition, target)
        decision = DoctrineEvalDecision.blocked if missing_routes or missing_primitives or missing_doctrine_refs else DoctrineEvalDecision.selected
        return new_doctrine_eval_selection(
            definition=definition,
            decision=decision,
            missing_evidence_routes=missing_routes,
            missing_primitive_families=missing_primitives,
            missing_source_doctrine_refs=missing_doctrine_refs,
        )

    def evaluate_doctrine(self, target: DoctrineEvalTargetInput) -> EvaluationReceipt:
        definition = self._matching_definition(target)
        if definition is None:
            raise ValueError(f"No doctrine eval definition matches {target.object_type.value} at stage {target.pipeline_stage}.")
        selection = self.select_definition(target)
        category_inputs = self._category_inputs(definition=definition, target=target, selection=selection)
        return self.evaluation_service.generate_evaluation_receipt(
            organization_id=target.organization_id,
            brand_id=target.brand_id,
            object_type=target.object_type,
            object_id=target.object_id,
            object_hash=target.object_hash,
            actor_id=target.actor_id,
            category_inputs=category_inputs,
            warnings=[] if selection.decision == DoctrineEvalDecision.selected else ["doctrine_eval_selection_blocked"],
        )

    def evaluate_interview_brief_doctrine(self, target: DoctrineEvalTargetInput) -> EvaluationReceipt:
        return self.evaluate_doctrine(target)

    def _matching_definition(self, target: DoctrineEvalTargetInput) -> DoctrineEvalDefinition | None:
        for definition in self.definitions:
            if target.object_type in definition.object_types and target.pipeline_stage in definition.pipeline_stages:
                return definition
        return None

    @staticmethod
    def _missing_evidence_routes(definition: DoctrineEvalDefinition, target: DoctrineEvalTargetInput) -> list[str]:
        return [
            requirement.route
            for requirement in definition.evidence_requirements
            if requirement.blocking and not target.evidence_routes.get(requirement.route)
        ]

    @staticmethod
    def _missing_primitive_families(definition: DoctrineEvalDefinition, target: DoctrineEvalTargetInput) -> list[str]:
        present = {family.upper() for family in target.primitive_families}
        return [
            obligation.primitive_family
            for obligation in definition.primitive_obligations
            if obligation.blocking and obligation.primitive_family.upper() not in present
        ]

    @staticmethod
    def _missing_doctrine_refs(definition: DoctrineEvalDefinition, target: DoctrineEvalTargetInput) -> list[str]:
        present = set(target.doctrine_refs)
        return [source for source in definition.source_doctrine_refs if source not in present]

    def _category_inputs(
        self,
        *,
        definition: DoctrineEvalDefinition,
        target: DoctrineEvalTargetInput,
        selection: DoctrineEvalSelection,
    ) -> list[EvaluationCategoryInput]:
        hard_failures_by_category: dict[EvaluationCategory, list[str]] = {}
        for route in selection.missing_evidence_routes:
            requirement = self._requirement_by_route(definition, route)
            hard_failures_by_category.setdefault(requirement.maps_to_category, []).append(route)
        if selection.missing_primitive_families:
            hard_failures_by_category.setdefault(EvaluationCategory.primitive_registry_fidelity, []).extend(
                selection.missing_primitive_families
            )
        if selection.missing_source_doctrine_refs:
            hard_failures_by_category.setdefault(EvaluationCategory.doctrine_alignment, []).extend(
                selection.missing_source_doctrine_refs
            )

        category_inputs: list[EvaluationCategoryInput] = []
        for category in EvaluationCategory:
            missing_items = hard_failures_by_category.get(category, [])
            category_inputs.append(
                EvaluationCategoryInput(
                    category=category,
                    score=0.2 if missing_items else self._score_for_category(definition, category),
                    evidence=self._evidence_for_category(category=category, target=target, missing_items=missing_items),
                    evaluator_version="cmf-doctrine-primitive-evaluator.v1",
                    hard_failure=bool(missing_items),
                    hard_failure_code=self._hard_failure_code(category) if missing_items else None,
                    hard_failure_message=self._hard_failure_message(category, missing_items) if missing_items else None,
                    approval_blocker_code=self._approval_blocker_code(category),
                )
            )
        return category_inputs

    @staticmethod
    def _requirement_by_route(definition: DoctrineEvalDefinition, route: str) -> DoctrineEvidenceRequirement:
        for requirement in definition.evidence_requirements:
            if requirement.route == route:
                return requirement
        raise ValueError(f"Unknown doctrine evidence route: {route}")

    @staticmethod
    def _score_for_category(definition: DoctrineEvalDefinition, category: EvaluationCategory) -> float:
        return max(definition.threshold, 0.92) if category in definition.required_categories else 0.92

    @staticmethod
    def _approval_blocker_code(category: EvaluationCategory) -> str:
        if category == EvaluationCategory.primitive_registry_fidelity:
            return "primitive_registry_failure"
        if category == EvaluationCategory.doctrine_alignment:
            return "doctrine_alignment_failure"
        return "doctrine_eval_hard_failure"

    @staticmethod
    def _hard_failure_code(category: EvaluationCategory) -> str:
        if category == EvaluationCategory.primitive_registry_fidelity:
            return "PRIMITIVE_OBLIGATION_MISSING"
        if category == EvaluationCategory.doctrine_alignment:
            return "DOCTRINE_SOURCE_MISSING"
        return "DOCTRINE_EVIDENCE_ROUTE_MISSING"

    @staticmethod
    def _hard_failure_message(category: EvaluationCategory, missing_items: Iterable[str]) -> str:
        missing = ", ".join(missing_items)
        return f"{category.value} failed because required doctrine/primitive evidence is missing: {missing}."

    @staticmethod
    def _evidence_for_category(
        *,
        category: EvaluationCategory,
        target: DoctrineEvalTargetInput,
        missing_items: list[str],
    ) -> list[EvidencePointer]:
        if missing_items:
            return [
                EvidencePointer(
                    source_type="doctrine_eval_gap",
                    source_id=item,
                    route=category.value,
                    claim_scope=EvidenceClaimScope.contradicts,
                    note=f"Missing required doctrine or primitive evidence for {category.value}.",
                )
                for item in missing_items
            ]
        source_ids = target.evidence_routes.get(category.value) or target.doctrine_refs or [target.object_hash]
        return [
            EvidencePointer(
                source_type="doctrine_eval_evidence",
                source_id=source_id,
                route=category.value,
                claim_scope=EvidenceClaimScope.supports,
                note=f"{category.value} supported by doctrine, registry, or source evidence.",
            )
            for source_id in source_ids[:3]
        ]
