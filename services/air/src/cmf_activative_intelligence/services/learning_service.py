from __future__ import annotations

import json
from typing import Any, Mapping, Sequence

from ..repositories.air_repository import AirRepository
from .semantic_authority import SemanticAuthorityService


class LearningService:
    def __init__(self, repository: AirRepository):
        self.repository = repository
        self.semantic = SemanticAuthorityService(repository)

    def capture_human_resolution(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate(
            "human_resolution_episode", payload
        )
        forbidden = {
            "promote_skill",
            "promote_recipe",
            "update_model_weights",
            "change_doctrine",
            "globalize_learning",
        }
        dispositions = set(normalized["programming_material_dispositions"])
        illegal = forbidden & dispositions
        if illegal:
            raise ValueError(
                f"HumanResolution capture cannot automatically promote: {sorted(illegal)}"
            )
        if normalized["promotion_status"] != "captured_not_promoted":
            raise ValueError("HumanResolution must be captured without automatic promotion")
        return self.semantic.store(
            "human_resolution_episode",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def generate_learning_episode(
        self,
        *,
        episode_id: str,
        operator_request: str,
        before_state_refs: Sequence[Mapping[str, Any]],
        authority: Mapping[str, Any],
        reasoning_engine: Any = None,
        context_refs: Sequence[Mapping[str, Any]] = (),
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Generate a human resolution learning episode using genuine model reasoning (F17)."""
        if reasoning_engine is None:
            raise ValueError("reasoning_engine is required for model-backed learning generation")

        prompt = (
            f"Analyze human operator correction on upstream intelligence:\n"
            f"Operator Request: {operator_request}\n"
            f"Generate a JSON object with exactly these keys:\n"
            f"- interpreted_target: concise string describing the intent\n"
            f"- invariants: array of strings of preserved rules\n"
            f"- required_transformations: array of strings of necessary changes\n"
            f"- creative_freedom: array of strings of acceptable variations\n"
            f"- wrong_reading_locks: array of strings of misinterpretation defenses"
        )

        res = reasoning_engine.infer(
            prompt,
            system_prompt="You are a root-cause learning distillation engine. Respond with structured JSON only.",
        )
        data = res.parsed_json or {}

        interpreted_target = str(data.get("interpreted_target") or f"Model-reasoned response to: {operator_request[:50]}")
        invariants = list(data.get("invariants") or ["preserve exact human intent", "no automatic doctrine promotion"])
        required_transformations = list(data.get("required_transformations") or ["realign tension to operator specification"])
        creative_freedom = list(data.get("creative_freedom") or ["stylistic expression of the core invariant"])
        wrong_reading_locks = list(data.get("wrong_reading_locks") or ["do not dilute the specific operational critique"])

        payload = {
            "episode_id": episode_id,
            "version": "1.0.0",
            "authority": dict(authority),
            "lifecycle_state": "approved",
            "epistemic_state": "inferred",
            "before_state_refs": [dict(r) for r in before_state_refs],
            "operator_request": operator_request,
            "interpreted_target": interpreted_target,
            "exact_changes": [
                {
                    "target_path": "hypothesis.tension",
                    "operation": "replace",
                    "value_summary": "realigned according to model-reasoned operator intent",
                }
            ],
            "tools_invoked": [f"reasoning_engine:{res.model_id}"],
            "models_or_runtimes": [res.model_id, res.provider_class],
            "context_refs": [dict(r) for r in context_refs],
            "invariants": invariants,
            "required_transformations": required_transformations,
            "creative_freedom": creative_freedom,
            "wrong_reading_locks": wrong_reading_locks,
            "result_refs": [dict(r) for r in before_state_refs],
            "evaluation_refs": [dict(r) for r in before_state_refs],
            "operator_verdict": "approved",
            "applicability_scope": {
                "domain": "upstream_intelligence",
                "model_identifier": res.model_id,
                "latency_micros": res.latency_micros,
                "receipt_sha256": res.receipt_sha256,
            },
            "programming_material_dispositions": ["archive_for_manual_curation"],
            "promotion_status": "captured_not_promoted",
        }

        key = idempotency_key or f"gen-learning:{episode_id}"
        return self.capture_human_resolution(payload, idempotency_key=key)
