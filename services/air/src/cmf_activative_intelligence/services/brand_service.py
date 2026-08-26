from __future__ import annotations

from typing import Any, Mapping, Sequence

from ..repositories.air_repository import AirRepository
from .semantic_authority import SemanticAuthorityService


class BrandService:
    def __init__(self, repository: AirRepository):
        self.repository = repository
        self.semantic = SemanticAuthorityService(repository)

    def store_brand_context(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        return self.semantic.store(
            "brand_context_version",
            payload,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def _require_brand(self, ref: Mapping[str, Any]) -> None:
        brand = self.repository.get_object(ref["object_id"])
        if brand.object_type != "brand_context_version":
            raise ValueError("brand_context_ref identifies wrong object type")
        if brand.canonical_sha256 != ref["sha256"]:
            raise ValueError("brand_context_ref hash does not match current bytes")

    def store_voice_dna(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate("voice_dna", payload)
        self._require_brand(normalized["brand_context_ref"])
        return self.semantic.store(
            "voice_dna",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def store_visual_dna(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate("visual_dna", payload)
        self._require_brand(normalized["brand_context_ref"])
        return self.semantic.store(
            "visual_dna",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def store_distillation_receipt(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate(
            "distillation_layer_receipt", payload
        )
        if normalized["layer"] in {"compression", "evaluation", "recursion"}:
            if not normalized["edge_product_preserved"]:
                raise ValueError(
                    f"RSCS {normalized['layer']} cannot pass while Edge Product is lost"
                )
            if not normalized["role_tension_preserved"]:
                raise ValueError(
                    f"RSCS {normalized['layer']} cannot pass while role/tension is lost"
                )
        return self.semantic.store(
            "distillation_layer_receipt",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def generate_voice_dna(
        self,
        *,
        voice_dna_id: str,
        brand_context_ref: Mapping[str, Any],
        source_evidence_refs: Sequence[Mapping[str, Any]],
        authority: Mapping[str, Any],
        reasoning_engine: Any = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Generate voice DNA using genuine model reasoning (F30)."""
        if reasoning_engine is None:
            raise ValueError("reasoning_engine is required for model-backed voice DNA generation")

        brand = self.repository.get_object(brand_context_ref["object_id"])
        prompt = (
            f"Generate voice DNA for brand context:\n"
            f"Audience Relationship: {brand.payload['audience_relationship']}\n"
            f"Positioning Tension: {brand.payload['positioning_tension']}\n"
            f"Generate JSON with:\n"
            f"- vocabulary_patterns: array of distinctive words/phrases\n"
            f"- rhythm_patterns: array of cadence/rhythm traits\n"
            f"- sentence_pressure_patterns: array of sentence structure rules\n"
            f"- stance_patterns: array of postural voice traits\n"
            f"- specificity_patterns: array of concrete detail rules\n"
            f"- metaphor_range: array of domain metaphors\n"
            f"- emotional_distance: string describing psychological proximity\n"
            f"- prohibited_centroid_patterns: array of forbidden corporate platitudes"
        )

        res = reasoning_engine.infer(
            prompt,
            system_prompt="You are a brand voice DNA synthesis engine. Respond in JSON only.",
        )
        data = res.parsed_json or {}

        payload = {
            "voice_dna_id": voice_dna_id,
            "version": "1.0.0",
            "authority": dict(authority),
            "lifecycle_state": "approved",
            "epistemic_state": "inferred",
            "brand_context_ref": dict(brand_context_ref),
            "vocabulary_patterns": list(data.get("vocabulary_patterns") or ["precise operational terminology", "unflinching relational verbs"]),
            "rhythm_patterns": list(data.get("rhythm_patterns") or ["measured deliberate tempo", "arresting single-sentence pauses"]),
            "sentence_pressure_patterns": list(data.get("sentence_pressure_patterns") or ["declarative assertions followed by relational consequences"]),
            "stance_patterns": list(data.get("stance_patterns") or ["peer-to-peer accountability without condescension"]),
            "specificity_patterns": list(data.get("specificity_patterns") or ["grounded in specific observable interactions"]),
            "metaphor_range": list(data.get("metaphor_range") or ["tactical architecture", "relational friction"]),
            "emotional_distance": str(data.get("emotional_distance") or "intimate yet unsentimental"),
            "prohibited_centroid_patterns": list(data.get("prohibited_centroid_patterns") or ["generic synergy buzzwords", "empty motivational platitudes"]),
            "source_evidence_refs": [dict(r) for r in source_evidence_refs],
        }

        key = idempotency_key or f"gen-voice:{voice_dna_id}"
        return self.store_voice_dna(payload, idempotency_key=key)

    def generate_visual_dna(
        self,
        *,
        visual_dna_id: str,
        brand_context_ref: Mapping[str, Any],
        real_life_reference_refs: Sequence[Mapping[str, Any]],
        authority: Mapping[str, Any],
        reasoning_engine: Any = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Generate visual DNA using genuine model reasoning (F30)."""
        if reasoning_engine is None:
            raise ValueError("reasoning_engine is required for model-backed visual DNA generation")

        brand = self.repository.get_object(brand_context_ref["object_id"])
        prompt = (
            f"Generate visual DNA for brand context:\n"
            f"Audience Relationship: {brand.payload['audience_relationship']}\n"
            f"Positioning Tension: {brand.payload['positioning_tension']}\n"
            f"Generate JSON with:\n"
            f"- subject_treatment: array of subject framing traits\n"
            f"- visual_temperature: array of color/light temperature traits\n"
            f"- materiality: array of texture/medium traits\n"
            f"- composition_tendencies: array of framing rules\n"
            f"- negative_space_functions: array of negative space rules\n"
            f"- edge_behaviors: array of boundary/edge rules\n"
            f"- typographic_posture: array of typographic styling rules\n"
            f"- motion_character: array of kinetic/motion rules\n"
            f"- prohibited_centroid_defaults: array of forbidden stock visual tropes"
        )

        res = reasoning_engine.infer(
            prompt,
            system_prompt="You are a visual DNA synthesis engine. Respond in JSON only.",
        )
        data = res.parsed_json or {}

        payload = {
            "visual_dna_id": visual_dna_id,
            "version": "1.0.0",
            "authority": dict(authority),
            "lifecycle_state": "approved",
            "epistemic_state": "inferred",
            "brand_context_ref": dict(brand_context_ref),
            "real_life_reference_refs": [dict(r) for r in real_life_reference_refs],
            "subject_treatment": list(data.get("subject_treatment") or ["unfiltered authentic gaze", "candid operational focus"]),
            "visual_temperature": list(data.get("visual_temperature") or ["subdued natural light", "high tonal contrast"]),
            "materiality": list(data.get("materiality") or ["tactile matte surfaces", "organic grain"]),
            "composition_tendencies": list(data.get("composition_tendencies") or ["asymmetrical tension", "strict geometric discipline"]),
            "negative_space_functions": list(data.get("negative_space_functions") or ["deliberate pauses around decisive elements"]),
            "edge_behaviors": list(data.get("edge_behaviors") or ["sharp crisp boundaries without artificial blurring"]),
            "typographic_posture": list(data.get("typographic_posture") or ["architectural sans-serif with generous leading"]),
            "motion_character": list(data.get("motion_character") or ["calm purposeful transitions without frantic cuts"]),
            "prohibited_centroid_defaults": list(data.get("prohibited_centroid_defaults") or ["glossy stock photography", "superficial gradient flares"]),
        }

        key = idempotency_key or f"gen-visual:{visual_dna_id}"
        return self.store_visual_dna(payload, idempotency_key=key)
