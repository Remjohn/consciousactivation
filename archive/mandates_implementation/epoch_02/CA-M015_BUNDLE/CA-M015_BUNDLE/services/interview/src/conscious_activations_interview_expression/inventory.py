from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .canonical import require_ref, semantic_id
from .errors import ValidationError
from .repository import InterviewRepository


class AssetInventoryService:
    def __init__(self, repository: InterviewRepository):
        self.repository = repository

    def _resolve_verbatim_evidence(
        self,
        *,
        source_package_ref: Mapping[str, Any],
        selected_phrase_refs: Mapping[str, Mapping[str, Any]],
        explicit_refs: Sequence[Mapping[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        source_ref = require_ref(source_package_ref, "source_package_ref")
        selected_phrase_ids = set(selected_phrase_refs)
        if explicit_refs is None:
            candidates = []
            for obj in self.repository.list_objects("verbatim_evidence"):
                payload = obj["payload"]
                if payload.get("source_package_ref") != source_ref:
                    continue
                phrase_ids = {
                    ref.get("object_id")
                    for ref in payload.get("phrase_refs", [])
                    if isinstance(ref, Mapping)
                }
                if phrase_ids & selected_phrase_ids:
                    candidates.append(obj)
        else:
            candidates = []
            for index, value in enumerate(explicit_refs):
                ref = require_ref(value, f"verbatim_evidence_refs[{index}]")
                try:
                    obj = self.repository.get_object_by_sha(ref["object_id"], ref["sha256"])
                except Exception as exc:
                    raise ValidationError(
                        f"verbatim_evidence_refs[{index}] is stale or missing",
                        context={"classification": "PROVENANCE_ERROR"},
                    ) from exc
                candidates.append(obj)

        covered: dict[str, dict[str, Any]] = {}
        for obj in candidates:
            payload = obj["payload"]
            if obj["object_type"] != "verbatim_evidence":
                raise ValidationError(
                    "asset inventory may consume only canonical verbatim_evidence objects",
                    context={"classification": "COMPOSITION_ERROR"},
                )
            if payload.get("source_package_ref") != source_ref:
                raise ValidationError(
                    "verbatim evidence source package does not match inventory source package",
                    context={"classification": "PROVENANCE_ERROR"},
                )
            validation = payload.get("validation", {})
            if validation.get("status") != "PASS" or not validation.get("exact_character_slice"):
                raise ValidationError(
                    "unvalidated verbatim evidence cannot enter asset composition",
                    context={"classification": "COMPOSITION_ERROR"},
                )
            for phrase_ref in payload.get("phrase_refs", []):
                phrase_id = phrase_ref.get("object_id") if isinstance(phrase_ref, Mapping) else None
                expected_ref = selected_phrase_refs.get(phrase_id)
                if phrase_id in selected_phrase_ids and expected_ref is not None:
                    if not isinstance(phrase_ref, Mapping) or dict(phrase_ref) != dict(expected_ref):
                        raise ValidationError(
                            f"verbatim evidence for phrase {phrase_id} is bound to a different phrase revision",
                            context={"classification": "PROVENANCE_ERROR"},
                        )
                    if phrase_id in covered and covered[phrase_id]["object_id"] != obj["object_id"]:
                        raise ValidationError(
                            f"multiple canonical verbatim evidence objects cover phrase {phrase_id}",
                            context={"classification": "COMPOSITION_ERROR"},
                        )
                    covered[phrase_id] = obj

        missing = sorted(selected_phrase_ids - set(covered))
        if missing:
            raise ValidationError(
                f"asset inventory cannot compose ungrounded quote material; missing verbatim evidence for phrases {missing}",
                context={"classification": "COMPOSITION_ERROR"},
            )

        unique: dict[str, dict[str, Any]] = {obj["object_id"]: obj for obj in covered.values()}
        return [unique[key] for key in sorted(unique)]

    def compile(
        self,
        *,
        source_package_ref: Mapping[str, Any],
        expression_moment_refs: list[Mapping[str, Any]],
        phrase_pack_ref: Mapping[str, Any],
        visual_index_ref: Mapping[str, Any],
        reaction_receipt_refs: list[Mapping[str, Any]],
        idempotency_key: str,
        verbatim_evidence_refs: list[Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        source_ref = require_ref(source_package_ref)
        moment_refs = [require_ref(r) for r in expression_moment_refs]
        if not moment_refs:
            raise ValidationError("asset inventory requires approved Expression Moments")

        moments = []
        for r in moment_refs:
            obj = self.repository.get_object(r["object_id"])
            if obj["payload"]["lifecycle_state"] != "APPROVED":
                raise ValidationError("asset inventory cannot consume unapproved moment")
            moments.append(obj["payload"])

        phrase_ref = require_ref(phrase_pack_ref)
        visual_ref = require_ref(visual_index_ref)
        reactions = [require_ref(r) for r in reaction_receipt_refs]
        self.repository.get_object_by_sha(phrase_ref["object_id"], phrase_ref["sha256"])
        visual = self.repository.get_object_by_sha(visual_ref["object_id"], visual_ref["sha256"])["payload"]
        selected_phrase_refs = {
            phrase_ref["object_id"]: dict(phrase_ref)
            for moment in moments
            for phrase_ref in moment["phrase_refs"]
        }

        verbatim_objects = self._resolve_verbatim_evidence(
            source_package_ref=source_ref,
            selected_phrase_refs=selected_phrase_refs,
            explicit_refs=verbatim_evidence_refs,
        )
        selected_phrase_ids = set(selected_phrase_refs)
        quote_candidates = []
        for obj in verbatim_objects:
            payload = obj["payload"]
            covered_phrase_ids = sorted(
                {
                    ref["object_id"]
                    for ref in payload["phrase_refs"]
                    if ref["object_id"] in selected_phrase_ids
                }
            )
            quote_candidates.append(
                {
                    "evidence_ref": {
                        "object_id": obj["object_id"],
                        "version": obj["version"],
                        "sha256": obj["sha256"],
                    },
                    "phrase_ids": covered_phrase_ids,
                    "text": payload["quote_text"],
                    "speaker_id": payload["source_span"]["speaker_id"],
                    "start_ms": payload["source_span"]["start_ms"],
                    "end_ms": payload["source_span"]["end_ms"],
                    "character_start": payload["transcript_ref"]["character_start"],
                    "character_end": payload["transcript_ref"]["character_end"],
                    "transcript_sha256": payload["transcript_ref"]["sha256"],
                    "source_media_sha256": payload["source_media_ref"]["sha256"],
                    "quote_sha256": payload["quote_sha256"],
                    "transformation_state": "SOURCE_VERBATIM",
                }
            )

        keyframes = [
            {
                "candidate_id": k["candidate_id"],
                "timestamp_ms": k["timestamp_ms"],
                "logical_uri": k["logical_uri"],
                "sha256": k["sha256"],
                "shot_id": k["shot_id"],
            }
            for k in visual["keyframes"]
        ]
        core = {
            "source_package_ref": source_ref,
            "expression_moment_refs": sorted(moment_refs, key=lambda x: x["object_id"]),
            "reaction_receipt_refs": sorted(reactions, key=lambda x: x["object_id"]),
            "phrase_pack_ref": phrase_ref,
            "visual_index_ref": visual_ref,
            "verbatim_evidence_refs": [
                {
                    "object_id": obj["object_id"],
                    "version": obj["version"],
                    "sha256": obj["sha256"],
                }
                for obj in verbatim_objects
            ],
            "quote_candidates": quote_candidates,
            "keyframe_candidates": keyframes,
            "voiceover_spans": [s for m in moments for s in m["source_spans"]],
            "animation_reference_inputs": keyframes,
            "semantic_programs_created": False,
            "final_scripts_created": False,
            "production_authorized": False,
        }
        object_id = semantic_id("ie:asset-package-spec", core)
        payload = {"asset_package_spec_id": object_id, "version": "1.0.0", **core}
        result = self.repository.store_object(
            "asset_package_spec",
            payload,
            object_id=object_id,
            idempotency_key=idempotency_key,
            lifecycle_state="COMPILED",
        )
        for r in moment_refs:
            self.repository.add_edge(r["object_id"], object_id, "expression_ingredient")
        for obj in verbatim_objects:
            self.repository.add_edge(obj["object_id"], object_id, "verbatim_grounding")
        return result

    def observed_evidence_pack(
        self,
        *,
        source_package_ref: Mapping[str, Any],
        expression_moment_refs: list[Mapping[str, Any]],
        reaction_receipt_refs: list[Mapping[str, Any]],
        tag_assertion_refs: list[Mapping[str, Any]],
        idempotency_key: str,
    ) -> dict[str, Any]:
        source_ref = require_ref(source_package_ref)
        core = {
            "source_package_ref": source_ref,
            "expression_moment_refs": sorted(
                [require_ref(r) for r in expression_moment_refs], key=lambda x: x["object_id"]
            ),
            "reaction_receipt_refs": sorted(
                [require_ref(r) for r in reaction_receipt_refs], key=lambda x: x["object_id"]
            ),
            "tag_assertion_refs": sorted(
                [require_ref(r) for r in tag_assertion_refs], key=lambda x: x["object_id"]
            ),
            "owner": "INTERVIEW_EXPRESSION",
            "semantic_interpretation_owner": "ACTIVATIVE_INTELLIGENCE_RUNTIME",
            "epistemic_state": "OBSERVED",
            "production_authorized": False,
        }
        object_id = semantic_id("ie:observed-evidence-pack", core)
        payload = {"observed_evidence_pack_id": object_id, "version": "1.0.0", **core}
        return self.repository.store_object(
            "observed_expression_evidence_pack",
            payload,
            object_id=object_id,
            idempotency_key=idempotency_key,
            lifecycle_state="VALIDATED",
        )
