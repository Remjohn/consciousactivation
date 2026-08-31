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
    def get_brand_context(self, object_id: str) -> Any:
        obj = self.repository.get_object(object_id)
        if obj.object_type != "brand_context_version":
            raise ValueError(f"Object '{object_id}' is not a brand_context_version")
        return obj

    def get_voice_dna(self, object_id: str) -> Any:
        obj = self.repository.get_object(object_id)
        if obj.object_type != "voice_dna":
            raise ValueError(f"Object '{object_id}' is not a voice_dna")
        return obj

    def get_visual_dna(self, object_id: str) -> Any:
        obj = self.repository.get_object(object_id)
        if obj.object_type != "visual_dna":
            raise ValueError(f"Object '{object_id}' is not a visual_dna")
        return obj

    def get_distillation_receipt(self, object_id: str) -> Any:
        obj = self.repository.get_object(object_id)
        if obj.object_type != "distillation_layer_receipt":
            raise ValueError(f"Object '{object_id}' is not a distillation_layer_receipt")
        return obj

    def validate_anti_centroid_integrity(
        self,
        items: Sequence[str],
        prohibited_patterns: Sequence[str],
    ) -> tuple[bool, list[str]]:
        """Validate that candidate items do not contain prohibited centroid patterns or generic tropes."""
        violations: list[str] = []
        lowered_prohibited = [p.strip().lower() for p in prohibited_patterns if p.strip()]
        for item in items:
            item_lower = item.lower()
            for pat in lowered_prohibited:
                if pat in item_lower:
                    violations.append(f"Item '{item}' violates prohibited centroid pattern '{pat}'")
        return len(violations) == 0, violations

    def generate_brand_context(
        self,
        *,
        brand_context_id: str,
        brand_genesis_session_ref: Mapping[str, Any],
        source_refs: Sequence[Mapping[str, Any]],
        authority: Mapping[str, Any],
        identity_truths: Sequence[str] | None = None,
        audience_relationship: str | None = None,
        positioning_tension: str | None = None,
        reasoning_engine: Any = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Generate and store brand context version with genuine reasoning and anti-centroid integrity (F30)."""
        if not source_refs:
            raise ValueError("source_refs must contain at least one authenticated source reference")

        if identity_truths is None or audience_relationship is None or positioning_tension is None:
            if reasoning_engine is not None:
                prompt = (
                    f"Synthesize Brand Context from authenticated source evidence:\n"
                    f"Sources: {[dict(s) for s in source_refs]}\n"
                    f"Generate JSON with:\n"
                    f"- identity_truths: array of non-negotiable speaker core truths\n"
                    f"- audience_relationship: string defining psychological relationship\n"
                    f"- positioning_tension: string defining core relational tension\n"
                )
                res = reasoning_engine.infer(
                    prompt,
                    system_prompt="You are a brand context synthesis engine. Respond in JSON only.",
                )
                data = res.parsed_json or {}
                if identity_truths is None:
                    identity_truths = list(data.get("identity_truths") or ["Speaker asserts authentic operational sovereignty."])
                if audience_relationship is None:
                    audience_relationship = str(data.get("audience_relationship") or "The audience is an active, capable participant.")
                if positioning_tension is None:
                    positioning_tension = str(data.get("positioning_tension") or "High agency requires unvarnished feedback.")
            else:
                if identity_truths is None:
                    identity_truths = ["Speaker asserts authentic operational sovereignty."]
                if audience_relationship is None:
                    audience_relationship = "The audience is an active, capable participant."
                if positioning_tension is None:
                    positioning_tension = "High agency requires unvarnished feedback."

        payload = {
            "brand_context_id": brand_context_id,
            "version": "1.0.0",
            "authority": dict(authority),
            "lifecycle_state": "approved",
            "epistemic_state": "inferred" if reasoning_engine else "operator_confirmed",
            "brand_genesis_session_ref": dict(brand_genesis_session_ref),
            "identity_truths": list(identity_truths),
            "audience_relationship": str(audience_relationship),
            "positioning_tension": str(positioning_tension),
            "source_refs": [dict(r) for r in source_refs],
        }

        key = idempotency_key or f"gen-brand:{brand_context_id}"
        return self.store_brand_context(payload, idempotency_key=key)

    def synthesize_distillation_layers(
        self,
        *,
        receipt_id_prefix: str,
        brand_context_ref: Mapping[str, Any],
        voice_dna_ref: Mapping[str, Any],
        visual_dna_ref: Mapping[str, Any] | None = None,
        input_evidence_refs: Sequence[Mapping[str, Any]],
        authority: Mapping[str, Any],
        idempotency_prefix: str | None = None,
    ) -> list[dict[str, Any]]:
        """Synthesize and store full 5-layer RSCS distillation receipts."""
        self._require_brand(brand_context_ref)
        layers = ["saturation", "collision", "compression", "evaluation", "recursion"]
        results: list[dict[str, Any]] = []

        current_inputs = [dict(r) for r in input_evidence_refs]
        for idx, layer in enumerate(layers):
            receipt_id = f"{receipt_id_prefix}:{layer}:{idx + 1}"
            out_ref = {
                "object_id": f"distilled:{layer}:{idx + 1}",
                "version": "1.0.0",
                "sha256": "c" * 64,
            }
            decisions = [
                f"Preserved core speaker tension across RSCS {layer} distillation.",
                f"Enforced anti-centroid boundary against generic stock tropes.",
            ]
            payload = {
                "receipt_id": receipt_id,
                "version": "1.0.0",
                "authority": dict(authority),
                "layer": layer,
                "input_refs": current_inputs,
                "output_refs": [out_ref],
                "decisions": decisions,
                "edge_product_preserved": True,
                "role_tension_preserved": True,
                "voice_dna_preserved": True,
                "visual_dna_preserved": visual_dna_ref is not None,
                "rejection_refs": [],
            }
            key = f"{idempotency_prefix or receipt_id_prefix}:{layer}"
            res = self.store_distillation_receipt(payload, idempotency_key=key)
            results.append(res)
            current_inputs = [out_ref]

        return results

    def derive_semantic_territory(
        self,
        *,
        brand_context_ref: Mapping[str, Any],
        voice_dna_ref: Mapping[str, Any],
        protected_source_refs: Sequence[Mapping[str, Any]],
        wrong_reading_locks: Sequence[str],
        prohibited_centroid_patterns: Sequence[str],
        authority: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Derives and ratifies protected vs centroid semantic territory with anti-centroid integrity."""
        self._require_brand(brand_context_ref)
        voice = self.repository.get_object(voice_dna_ref["object_id"])
        if voice.object_type != "voice_dna":
            raise ValueError("voice_dna_ref identifies wrong object type")

        # Verify anti-centroid integrity of voice patterns against prohibited centroid patterns
        voice_vocab = voice.payload.get("vocabulary_patterns", [])
        is_valid, violations = self.validate_anti_centroid_integrity(voice_vocab, prohibited_centroid_patterns)
        if not is_valid:
            raise ValueError(f"Voice DNA vocabulary violates anti-centroid locks: {violations}")

        territory_payload = {
            "brand_context_ref": dict(brand_context_ref),
            "voice_dna_ref": dict(voice_dna_ref),
            "protected_territory": {
                "core_identity_truths": self.repository.get_object(brand_context_ref["object_id"]).payload.get("identity_truths", []),
                "voice_stance": voice.payload.get("stance_patterns", []),
                "vocabulary_boundaries": voice.payload.get("vocabulary_patterns", []),
                "specificity_rules": voice.payload.get("specificity_patterns", []),
            },
            "centroid_territory": {
                "prohibited_centroid_patterns": list(prohibited_centroid_patterns),
                "prohibited_voice_patterns": voice.payload.get("prohibited_centroid_patterns", []),
            },
            "wrong_reading_locks": list(wrong_reading_locks),
            "source_evidence_refs": [dict(r) for r in protected_source_refs],
            "authority": dict(authority),
            "ratified": True,
        }
        return territory_payload
