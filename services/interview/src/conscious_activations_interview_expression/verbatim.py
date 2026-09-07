from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from typing import Any

from .canonical import require_int, require_ref, require_sha, require_source_span, semantic_id
from .errors import ValidationError
from .repository import InterviewRepository

VERBATIM_POLICY_VERSION = "EXACT_CODEPOINT_SLICE_V1"
VERBATIM_OBJECT_TYPE = "verbatim_evidence"


def _require_exact_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or value == "":
        raise ValidationError(f"{name} must be a non-empty string")
    return value


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _same_ref(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    return (
        left.get("object_id") == right.get("object_id")
        and left.get("version") == right.get("version")
        and left.get("sha256") == right.get("sha256")
    )


class VerbatimEvidenceService:
    """Admits source-bound verbatim evidence without regenerating spoken text."""

    def __init__(self, repository: InterviewRepository):
        self.repository = repository

    def admit(
        self,
        *,
        source_package_ref: Mapping[str, Any],
        alignment_ref: Mapping[str, Any],
        phrase_refs: Sequence[Mapping[str, Any]],
        source_media_asset_id: str,
        source_media_sha256: str,
        source_span: Mapping[str, Any],
        transcript_text: str,
        transcript_sha256: str,
        character_start: int,
        character_end: int,
        quote_text: str,
        actor_id: str,
        limitations: Sequence[str] = (),
        idempotency_key: str,
    ) -> dict[str, Any]:
        source_ref = require_ref(source_package_ref, "source_package_ref")
        alignment = require_ref(alignment_ref, "alignment_ref")
        phrases = [
            require_ref(item, f"phrase_refs[{index}]")
            for index, item in enumerate(phrase_refs)
        ]
        if not phrases:
            raise ValidationError(
                "verbatim evidence requires at least one packed phrase reference",
                context={"classification": "PROVENANCE_ERROR"},
            )

        source_span_value = require_source_span(source_span, "source_span")
        media_id = _require_exact_text(source_media_asset_id, "source_media_asset_id")
        media_sha = require_sha(source_media_sha256, "source_media_sha256")
        transcript = _require_exact_text(transcript_text, "transcript_text")
        transcript_sha = require_sha(transcript_sha256, "transcript_sha256")
        quote = _require_exact_text(quote_text, "quote_text")
        start = require_int(character_start, "character_start", minimum=0)
        end = require_int(character_end, "character_end", minimum=1)
        actor = _require_exact_text(actor_id, "actor_id")

        if _sha256_text(transcript) != transcript_sha:
            raise ValidationError(
                "transcript_sha256 does not match the supplied transcript bytes",
                context={"classification": "PROVENANCE_ERROR"},
            )
        if end <= start:
            raise ValidationError(
                "character_end must be greater than character_start",
                context={"classification": "PROVENANCE_ERROR"},
            )
        if end > len(transcript):
            raise ValidationError(
                "character span exceeds transcript length",
                context={"classification": "PROVENANCE_ERROR"},
            )

        exact_slice = transcript[start:end]
        if quote != exact_slice:
            raise ValidationError(
                "verbatim quote must equal the exact transcript character slice; semantic equivalence is insufficient",
                context={"classification": "EDITORIAL_DRIFT"},
            )

        quote_sha = _sha256_text(quote)

        try:
            package_obj = self.repository.get_object_by_sha(
                source_ref["object_id"], source_ref["sha256"]
            )
        except Exception as exc:
            raise ValidationError(
                "source package reference is stale or missing",
                context={"classification": "PROVENANCE_ERROR"},
            ) from exc

        package = package_obj["payload"]
        media_assets = package.get("media_assets", [])
        matched_media = next(
            (
                asset
                for asset in media_assets
                if asset.get("asset_id") == media_id
                and asset.get("sha256") == media_sha
            ),
            None,
        )
        if matched_media is None:
            raise ValidationError(
                "source media asset identity or digest does not match the admitted source package",
                context={"classification": "PROVENANCE_ERROR"},
            )

        if source_span_value["source_id"] != source_ref["object_id"]:
            raise ValidationError(
                "source_span source_id must match source_package_ref.object_id",
                context={"classification": "PROVENANCE_ERROR"},
            )
        if source_span_value["source_version"] != source_ref["version"]:
            raise ValidationError(
                "source_span source_version must match source_package_ref.version",
                context={"classification": "PROVENANCE_ERROR"},
            )
        if source_span_value["source_sha256"] != source_ref["sha256"]:
            raise ValidationError(
                "source_span source_sha256 must match source_package_ref.sha256",
                context={"classification": "PROVENANCE_ERROR"},
            )
        duration_ms = matched_media.get("technical", {}).get("duration_ms")
        if isinstance(duration_ms, int) and source_span_value["end_ms"] > duration_ms:
            raise ValidationError(
                "source_span exceeds admitted media duration",
                context={"classification": "PROVENANCE_ERROR"},
            )

        try:
            alignment_obj = self.repository.get_object_by_sha(
                alignment["object_id"], alignment["sha256"]
            )
        except Exception as exc:
            raise ValidationError(
                "transcript alignment reference is stale or missing",
                context={"classification": "PROVENANCE_ERROR"},
            ) from exc
        alignment_payload = alignment_obj["payload"]
        if not _same_ref(alignment_payload.get("source_package_ref", {}), source_ref):
            raise ValidationError(
                "transcript alignment is not bound to the supplied source package revision",
                context={"classification": "PROVENANCE_ERROR"},
            )

        phrase_payloads: list[dict[str, Any]] = []
        for index, phrase_ref in enumerate(phrases):
            try:
                phrase_obj = self.repository.get_object_by_sha(
                    phrase_ref["object_id"], phrase_ref["sha256"]
                )
            except Exception as exc:
                raise ValidationError(
                    f"phrase_refs[{index}] is stale or missing",
                    context={"classification": "PROVENANCE_ERROR"},
                ) from exc
            payload = phrase_obj["payload"]
            if phrase_obj["object_type"] != "packed_phrase":
                raise ValidationError(
                    f"phrase_refs[{index}] must reference packed_phrase objects",
                    context={"classification": "PROVENANCE_ERROR"},
                )
            if not _same_ref(payload.get("source_package_ref", {}), source_ref):
                raise ValidationError(
                    f"phrase_refs[{index}] is not bound to the supplied source package revision",
                    context={"classification": "PROVENANCE_ERROR"},
                )
            if payload.get("speaker_id") != source_span_value["speaker_id"]:
                raise ValidationError(
                    f"phrase_refs[{index}] speaker does not match source_span speaker",
                    context={"classification": "PROVENANCE_ERROR"},
                )
            phrase_payloads.append(payload)

        phrase_start = min(int(item["start_ms"]) for item in phrase_payloads)
        phrase_end = max(int(item["end_ms"]) for item in phrase_payloads)
        if source_span_value["start_ms"] < phrase_start or source_span_value["end_ms"] > phrase_end:
            raise ValidationError(
                "source_span is outside the temporal range covered by its packed phrases",
                context={"classification": "PROVENANCE_ERROR"},
            )

        normalized_limitations = [
            _require_exact_text(value, "limitations[]")
            for value in limitations
        ]

        identity_core = {
            "source_package_ref": dict(source_ref),
            "alignment_ref": dict(alignment),
            "phrase_refs": sorted(
                [dict(item) for item in phrases], key=lambda item: item["object_id"]
            ),
            "source_media_asset_id": media_id,
            "source_media_sha256": media_sha,
            "source_span": source_span_value,
            "transcript_sha256": transcript_sha,
            "character_span": {"start": start, "end": end},
            "verbatim_policy_version": VERBATIM_POLICY_VERSION,
        }
        evidence_id = semantic_id("ie:verbatim-evidence", identity_core)
        payload = {
            "evidence_id": evidence_id,
            "version": "1.0.0",
            "source_package_ref": dict(source_ref),
            "alignment_ref": dict(alignment),
            "phrase_refs": identity_core["phrase_refs"],
            "source_media_ref": {
                "asset_id": media_id,
                "sha256": media_sha,
            },
            "source_span": source_span_value,
            "transcript_ref": {
                "sha256": transcript_sha,
                "character_start": start,
                "character_end": end,
            },
            "quote_text": quote,
            "quote_sha256": quote_sha,
            "verbatim_policy_version": VERBATIM_POLICY_VERSION,
            "validation": {
                "status": "PASS",
                "exact_character_slice": True,
                "source_digest_bound": True,
                "temporal_anchor_bound": True,
                "lineage_bound": True,
                "semantic_similarity_used": False,
                "limitations": normalized_limitations,
            },
            "actor_id": actor,
            "admission_receipt": {
                "command": "admit_verbatim_evidence",
                "mandate_id": "CA-M015",
                "source_package_ref": dict(source_ref),
                "source_media_ref": {"asset_id": media_id, "sha256": media_sha},
                "source_span": dict(source_span_value),
                "transcript_sha256": transcript_sha,
                "character_span": {"start": start, "end": end},
                "quote_sha256": quote_sha,
                "validation_status": "PASS",
                "semantic_similarity_used": False,
                "limitations": normalized_limitations,
                "actor_id": actor,
            },
            "lifecycle_state": "VALIDATED",
            "epistemic_state": "OBSERVED",
            "production_authorized": False,
            "revision_policy": "IMMUTABLE_PREVIOUS_REVISIONS",
        }

        result = self.repository.store_object(
            VERBATIM_OBJECT_TYPE,
            payload,
            object_id=evidence_id,
            idempotency_key=idempotency_key,
            lifecycle_state="VALIDATED",
        )
        self.repository.add_edge(
            source_ref["object_id"], evidence_id, "source_of_verbatim_evidence"
        )
        self.repository.add_edge(
            alignment["object_id"], evidence_id, "alignment_of_verbatim_evidence"
        )
        for phrase_ref in phrases:
            self.repository.add_edge(
                phrase_ref["object_id"], evidence_id, "phrase_supports_verbatim_evidence"
            )

        result["receipt"] = {
            "command": "admit_verbatim_evidence",
            "mandate_id": "CA-M015",
            "object_ref": {
                "object_id": result["object"]["object_id"],
                "version": result["object"]["version"],
                "sha256": result["object"]["sha256"],
            },
            "source_package_ref": dict(source_ref),
            "source_media_ref": {"asset_id": media_id, "sha256": media_sha},
            "source_span": dict(source_span_value),
            "transcript_sha256": transcript_sha,
            "character_span": {"start": start, "end": end},
            "quote_sha256": quote_sha,
            "validation_status": "PASS",
            "semantic_similarity_used": False,
            "limitations": normalized_limitations,
            "actor_id": actor,
        }
        return result

    def get(self, evidence_ref: Mapping[str, Any]) -> dict[str, Any]:
        ref = require_ref(evidence_ref, "verbatim_evidence_ref")
        return self.repository.get_object_by_sha(ref["object_id"], ref["sha256"])
