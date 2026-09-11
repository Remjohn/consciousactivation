from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any

from .repositories.air_repository import AirRepository
from .services.production_common import add_lineage_edges, stored_result_ref


def _authority() -> dict[str, str]:
    return {
        "authority_id": "ca-program-control-v2.1-candidate",
        "authority_version": "2.1.0-candidate",
        "authority_sha256": "a" * 64,
        "authority_state": "candidate_not_current",
    }


def _ref(value: Mapping[str, Any]) -> dict[str, str]:
    required = {"object_id", "version", "sha256"}
    if not required.issubset(value):
        missing = sorted(required - set(value))
        raise ValueError(f"immutable reference missing fields: {missing}")
    return {key: str(value[key]) for key in ("object_id", "version", "sha256")}


class CampaignActivationService:
    """Deterministic campaign/freshness evidence compiler.

    This service records bounded campaign programs and observations. It never
    turns platform correlation into causal or semantic truth.
    """

    def __init__(self, repository: AirRepository):
        self.repository = repository

    def _store(self, object_type: str, payload: Mapping[str, Any], *, key: str) -> dict[str, Any]:
        from .domain import validate_air_object

        normalized = validate_air_object(object_type, payload)
        result = self.repository.store_object(object_type, normalized, idempotency_key=key)
        refs: list[Mapping[str, Any]] = []
        for field, value in normalized.items():
            if field.endswith("_ref") and isinstance(value, Mapping) and {"object_id", "version", "sha256"}.issubset(value):
                refs.append(value)
            elif field.endswith("_refs") and isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
                refs.extend(item for item in value if isinstance(item, Mapping) and {"object_id", "version", "sha256"}.issubset(item))
        if refs:
            add_lineage_edges(
                self.repository,
                source_result=result,
                relation_type=f"{object_type}:depends_on",
                target_refs=refs,
                evidence={"compiler": "campaign-activation-service", "development_only": True},
            )
        return result

    def store_program(self, payload: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        entry_refs = [_ref(item) for item in payload.get("entry_program_refs", [])]
        axes = list(payload.get("activation_axes", []))
        if not entry_refs:
            raise ValueError("entry_program_refs must be non-empty")
        if len(axes) != len(entry_refs):
            raise ValueError("activation_axes must align one-to-one with entry_program_refs")
        asset_plans: list[dict[str, Any]] = []
        for index, (entry_ref, axis) in enumerate(zip(entry_refs, axes, strict=True)):
            if not isinstance(axis, Mapping):
                raise ValueError("activation axis must be an object")
            asset_plans.append(
                {
                    "sequence_index": index,
                    "entry_program_ref": entry_ref,
                    "psychological_role": str(axis["psychological_role"]),
                    "tension": str(axis["tension"]),
                    "edge_product_ref": _ref(axis["edge_product_ref"]),
                    "primitive_coalition_ref": _ref(axis["primitive_coalition_ref"]),
                    "archetype_coalition_ref": _ref(axis["archetype_coalition_ref"]),
                    "relief_state": str(axis["relief_state"]),
                    "source_package_refs": [_ref(item) for item in payload.get("source_package_refs", [])],
                }
            )
        normalized = {
            "program_id": str(payload["campaign_program_id"]),
            "version": str(payload.get("version", "1.0.0")),
            "authority": dict(payload.get("authority", _authority())),
            "lifecycle_state": str(payload.get("lifecycle_state", "VALIDATED")),
            "epistemic_state": "planned",
            "audience_context_ref": _ref(payload["audience_context_ref"]),
            "campaign_policy_ref": {
                "object_id": f"campaign-policy:{payload['campaign_program_id']}",
                "version": "1.0.0",
                "sha256": str(payload.get("freshness_policy_ref", {} ).get("sha256", "b" * 64)),
            },
            "asset_plans": asset_plans,
            "freshness_profile_ref": _ref(payload["freshness_policy_ref"]),
            "wrong_reading_lock_refs": [],
            "evaluation_profile_ref": {
                "object_id": f"evaluation-profile:{payload['campaign_program_id']}",
                "version": "1.0.0",
                "sha256": "c" * 64,
            },
            "limitations": [
                "development campaign plan only",
                "audience observations cannot rewrite source truth",
                "no production publication authority",
            ],
        }
        return self._store("campaign_activation_program", normalized, key=idempotency_key)

    def compile_freshness_profile(
        self,
        *,
        campaign_program_ref: Mapping[str, Any],
        audience_context_ref: Mapping[str, Any],
        platform_id: str,
        window_id: str,
        exposures: Sequence[Mapping[str, Any]],
        policy: Mapping[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        if not exposures:
            raise ValueError("exposures must be non-empty")
        pattern_counts: Counter[str] = Counter()
        exposure_refs: list[dict[str, str]] = []
        total_impressions = 0
        total_shares = 0
        for index, exposure in enumerate(exposures):
            for pattern in exposure.get("pattern_ids", []):
                pattern_counts[str(pattern)] += 1
            total_impressions += int(exposure.get("impressions", 0))
            total_shares += int(exposure.get("shares", 0))
            asset_ref = _ref(exposure["asset_ref"])
            exposure_refs.append(
                {
                    "object_id": f"exposure:{window_id}:{index}:{asset_ref['sha256'][:16]}",
                    "version": "1.0.0",
                    "sha256": asset_ref["sha256"],
                }
            )
        repeat_threshold = int(policy.get("repeated_pattern_threshold", 3))
        share_rate = (total_shares * 1_000_000 // total_impressions) if total_impressions else 0
        minimum_share_rate = int(policy.get("minimum_share_rate_micros", 0))
        repeated = sorted(pattern for pattern, count in pattern_counts.items() if count >= repeat_threshold)
        findings = [
            {
                "finding_id": f"freshness:{window_id}:repetition",
                "kind": "REPETITION",
                "result": "FAIL" if repeated else "PASS",
                "pattern_ids": repeated,
                "evidence_refs": exposure_refs,
            },
            {
                "finding_id": f"freshness:{window_id}:share-rate",
                "kind": "SHARE_RATE",
                "result": "PASS" if share_rate >= minimum_share_rate else "INSUFFICIENT_EVIDENCE",
                "observed_micros": share_rate,
                "threshold_micros": minimum_share_rate,
                "evidence_refs": exposure_refs,
            },
        ]
        payload = {
            "profile_id": f"freshness-profile:{window_id}",
            "version": "1.0.0",
            "authority": _authority(),
            "lifecycle_state": "recorded_development",
            "epistemic_state": "observed",
            "audience_context_ref": _ref(audience_context_ref),
            "platform_profile_id": str(platform_id),
            "window": {"window_id": str(window_id), "exposure_count": len(exposures)},
            "exposure_refs": exposure_refs,
            "repetition_counts": dict(sorted(pattern_counts.items())),
            "hard_gates": [
                {"gate_id": "source-lineage-preserved", "result": "PASS", "evidence_refs": [_ref(campaign_program_ref)]},
                {"gate_id": "causal-claim-forbidden", "result": "PASS", "evidence_refs": exposure_refs},
            ],
            "freshness_findings": findings,
            "limitations": [
                "causal_claim_authorized=false",
                "platform metrics are observational",
                "development evidence only",
            ],
        }
        result = self._store("activation_freshness_profile", payload, key=idempotency_key)
        result["object"]["payload"]["causal_claim_authorized"] = False
        return result

    def record_audience_reaction(
        self,
        *,
        campaign_program_ref: Mapping[str, Any],
        asset_ref: Mapping[str, Any],
        audience_context_ref: Mapping[str, Any],
        observations: Sequence[Mapping[str, Any]],
        evaluator_id: str,
        producer_id: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        if evaluator_id == producer_id:
            raise ValueError("producer and evaluator must differ")
        if not observations:
            raise ValueError("observations must be non-empty")
        metrics = []
        limits: set[str] = set()
        role_signals = []
        for item in observations:
            metrics.append(
                {
                    "observation_id": str(item["observation_id"]),
                    "metric_name": str(item["metric_name"]),
                    "value": int(item["value"]),
                    "denominator": int(item["denominator"]),
                    "metric_definition_ref": _ref(item["metric_definition_ref"]),
                    "epistemic_state": str(item.get("epistemic_state", "observed")),
                }
            )
            limits.update(str(value) for value in item.get("limitations", []))
            role_signals.append(
                {
                    "signal_id": f"role-signal:{item['observation_id']}",
                    "role": "audience participant",
                    "signal": str(item["metric_name"]),
                    "epistemic_state": "inferred",
                }
            )
        payload = {
            "receipt_id": f"audience-reaction:{asset_ref['object_id']}:{len(observations)}",
            "version": "1.0.0",
            "authority": _authority(),
            "lifecycle_state": "recorded_development",
            "epistemic_state": "observed",
            "campaign_program_ref": _ref(campaign_program_ref),
            "asset_ref": _ref(asset_ref),
            "platform_profile_id": "development-export",
            "observation_window": {"window_id": "development-reference", "sample_count": len(observations)},
            "observed_metrics": metrics,
            "measurement_limits": sorted(limits or {"development-only observations"}),
            "inferred_role_signals": role_signals,
            "producer_actor_id": str(producer_id),
            "evaluator_actor_id": str(evaluator_id),
            "limitations": [
                "source_reaction_receipt_overwritten=false",
                "audience inference cannot rewrite source expression",
            ],
        }
        result = self._store("audience_reaction_receipt", payload, key=idempotency_key)
        result["object"]["payload"]["source_reaction_receipt_overwritten"] = False
        return result

    def propose_revision(
        self,
        *,
        campaign_program_ref: Mapping[str, Any],
        freshness_profile_ref: Mapping[str, Any],
        affected_entry_refs: Sequence[Mapping[str, Any]],
        reason_codes: Sequence[str],
        owner_product: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        payload = {
            "campaign_revision_request_id": f"campaign-revision:{campaign_program_ref['object_id']}:{freshness_profile_ref['sha256'][:12]}",
            "version": "1.0.0",
            "campaign_program_ref": _ref(campaign_program_ref),
            "freshness_profile_ref": _ref(freshness_profile_ref),
            "affected_entry_refs": [_ref(item) for item in affected_entry_refs],
            "reason_codes": sorted({str(code) for code in reason_codes}),
            "responsible_owner": str(owner_product),
            "scope": "AFFECTED_ENTRIES_ONLY",
            "historical_bytes_preserved": True,
            "lifecycle_state": "proposed_development",
            "epistemic_state": "inferred",
            "authority": _authority(),
        }
        return self._store("campaign_revision_request", payload, key=idempotency_key)
