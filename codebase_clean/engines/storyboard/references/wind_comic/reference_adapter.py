"""M0074 isolated Wind Comic -> CAE storyboard reference adapter.

This module is deliberately dependency-free and does not own CAE semantic meaning.
It extracts bounded production-workshop behaviors as pure transformations/validators:
- shot-keyed pull-sheet round-trip and changed-field summaries
- deterministic timeline geometry/audit
- explicit sketch-lock declarations carrying source lineage
- scene/style continuity checks against CAE-supplied canonical references
- immutable operator-feedback/revision append semantics

It never calls a generation provider, persists canonical state, or mutates CAE objects.
The caller remains responsible for CAE authorization, canonical persistence, receipts,
and operator promotion gates.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from copy import deepcopy
import csv
import hashlib
import io
import json
from typing import Any, Iterable, Mapping, Sequence


IMPORTABLE_FIELDS: tuple[str, ...] = (
    "sceneDescription",
    "scene",
    "characters",
    "dialogue",
    "duration",
    "shotSize",
    "composition",
    "cameraAngle",
    "cameraMovement",
    "lens",
    "lightingIntent",
    "editPattern",
    "scoreMood",
    "soundDesign",
    "diegeticSound",
    "storyBeat",
    "whyThisChoice",
)

NON_ROUNDTRIP_FIELDS: tuple[str, ...] = ("startSec", "endSec")


class AdapterValidationError(ValueError):
    """Fail-closed validation error for this isolated reference."""


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def export_pull_sheet(shots: Sequence[Mapping[str, Any]]) -> str:
    """Export a deterministic CSV projection keyed by shot number.

    startSec/endSec are derived for inspection only and intentionally never become
    editable round-trip fields.
    """
    ordered = sorted((dict(s) for s in shots), key=lambda s: int(s["shotNumber"]))
    fieldnames = ["shotNumber", *IMPORTABLE_FIELDS, *NON_ROUNDTRIP_FIELDS]
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for shot in ordered:
        row: dict[str, Any] = {"shotNumber": shot["shotNumber"]}
        for field in IMPORTABLE_FIELDS:
            value = shot.get(field, "")
            if isinstance(value, (list, tuple)):
                row[field] = "、".join(str(v) for v in value)
            else:
                row[field] = "" if value is None else value
        row["startSec"] = shot.get("startSec", "")
        row["endSec"] = shot.get("endSec", "")
        writer.writerow(row)
    return out.getvalue()


def parse_roundtrip_csv(text: str) -> list[dict[str, Any]]:
    """Parse CSV with BOM/quotes/newlines and report malformed/unknown rows by rejection."""
    text = text.lstrip("\ufeff")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if not reader.fieldnames or "shotNumber" not in reader.fieldnames:
        raise AdapterValidationError("missing required shotNumber column")
    rows: list[dict[str, Any]] = []
    for raw in reader:
        try:
            shot_number = int(str(raw.get("shotNumber", "")).strip().lstrip("Ss"))
        except ValueError as exc:
            raise AdapterValidationError("malformed shotNumber") from exc
        if shot_number <= 0:
            raise AdapterValidationError("shotNumber must be positive")
        fields = {
            key: str(raw.get(key, "")).strip()
            for key in IMPORTABLE_FIELDS
            if raw.get(key) not in (None, "", "—")
        }
        # Timing columns are observation-only. They are parsed nowhere and cannot
        # become changes even if a user edits them.
        rows.append({"shotNumber": shot_number, "fields": fields})
    return rows


def merge_pull_sheet(
    baseline_shots: Sequence[Mapping[str, Any]],
    imported_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[int]]:
    """Return (proposal, changed_fields, unknown_shots) without mutating baseline."""
    proposal = deepcopy([dict(s) for s in baseline_shots])
    by_num = {int(s["shotNumber"]): s for s in proposal}
    changes: list[dict[str, Any]] = []
    unknown: list[int] = []

    for row in imported_rows:
        number = int(row["shotNumber"])
        shot = by_num.get(number)
        if shot is None:
            unknown.append(number)
            continue
        fields = row.get("fields", {})
        if not isinstance(fields, Mapping):
            raise AdapterValidationError("row fields must be a mapping")
        for field in IMPORTABLE_FIELDS:
            if field not in fields:
                continue
            raw = str(fields[field]).strip()
            if raw in ("", "—"):
                continue
            if field == "duration":
                try:
                    next_value: Any = float(raw)
                except ValueError as exc:
                    raise AdapterValidationError(f"duration is not numeric for shot {number}") from exc
                if next_value <= 0:
                    raise AdapterValidationError(f"duration must be positive for shot {number}")
                if next_value.is_integer():
                    next_value = int(next_value)
            elif field == "characters":
                next_value = [p.strip() for p in raw.replace(";", "、").replace(",", "、").replace("/", "、").split("、") if p.strip()]
            else:
                next_value = raw
            current = shot.get(field, []) if field == "characters" else shot.get(field, "")
            cur_norm = "、".join(map(str, current)) if isinstance(current, (list, tuple)) else str(current or "")
            next_norm = "、".join(map(str, next_value)) if isinstance(next_value, list) else str(next_value)
            if cur_norm == next_norm:
                continue
            changes.append({
                "shotNumber": number,
                "field": field,
                "from": cur_norm[:120],
                "to": next_norm[:120],
            })
            shot[field] = next_value

    return proposal, changes, sorted(set(unknown))


@dataclass(frozen=True)
class SketchLock:
    """A declared composition lock; it is not an image generator or authority."""

    shot_number: int
    sketch_ref: str
    source_sha256: str
    locked_fields: tuple[str, ...] = ("composition", "shotSize", "cameraAngle")
    style_anchor_ref: str | None = None
    scene_anchor_ref: str | None = None

    def validate(self) -> None:
        if self.shot_number <= 0:
            raise AdapterValidationError("sketch lock shot_number must be positive")
        if not self.sketch_ref:
            raise AdapterValidationError("sketch_ref required")
        if len(self.source_sha256) != 64 or any(c not in "0123456789abcdef" for c in self.source_sha256.lower()):
            raise AdapterValidationError("source_sha256 must be a 64-character hex digest")
        if not self.locked_fields:
            raise AdapterValidationError("at least one locked field is required")


def audit_timeline(
    shots: Sequence[Mapping[str, Any]],
    *,
    timeline_duration_sec: float | None = None,
    epsilon: float = 1e-9,
) -> dict[str, Any]:
    """Deterministically audit shot timing without changing canonical timeline state."""
    ordered = sorted((dict(s) for s in shots), key=lambda s: int(s["shotNumber"]))
    errors: list[str] = []
    observations: list[dict[str, Any]] = []
    cursor = 0.0
    previous_number: int | None = None
    for shot in ordered:
        number = int(shot.get("shotNumber", 0))
        duration = float(shot.get("duration", 0))
        start = float(shot.get("startSec", cursor))
        end = float(shot.get("endSec", start + duration))
        if number <= 0:
            errors.append("invalid_shot_number")
        if duration <= 0:
            errors.append(f"non_positive_duration:S{number}")
        if end - start <= epsilon:
            errors.append(f"non_positive_span:S{number}")
        if start < -epsilon:
            errors.append(f"negative_start:S{number}")
        if previous_number is not None and start < cursor - epsilon:
            errors.append(f"overlap_or_backtrack:S{previous_number}->S{number}")
        if abs((end - start) - duration) > epsilon:
            errors.append(f"duration_mismatch:S{number}")
        observations.append({"shotNumber": number, "startSec": start, "endSec": end, "duration": duration})
        cursor = max(cursor, end)
        previous_number = number

    total = cursor
    if timeline_duration_sec is not None and total > float(timeline_duration_sec) + epsilon:
        errors.append("timeline_duration_exceeded")
    return {
        "ok": not errors,
        "errors": errors,
        "totalDurationSec": total,
        "shots": observations,
        "digest": canonical_digest({"shots": observations, "errors": errors, "totalDurationSec": total}),
    }


def compile_roundtrip_proposal(
    baseline_shots: Sequence[Mapping[str, Any]],
    imported_rows: Sequence[Mapping[str, Any]],
    *,
    expected_baseline_digest: str,
    current_baseline_digest: str,
    operator_authorized: bool,
) -> dict[str, Any]:
    """Compile a bounded proposal only when the upstream caller proves authority + freshness.

    This mirrors the existing CAE CAS/stale-edit pattern without owning canonical state.
    """
    if not operator_authorized:
        raise AdapterValidationError("operator authorization required")
    if expected_baseline_digest != current_baseline_digest:
        raise AdapterValidationError("stale baseline; refresh before compiling proposal")
    proposal, changes, unknown = merge_pull_sheet(baseline_shots, imported_rows)
    return {
        "baseline_digest": current_baseline_digest,
        "proposal": proposal,
        "changes": changes,
        "unknown_shots": unknown,
        "requires_promotion": True,
    }


def validate_scene_consistency(
    shots: Sequence[Mapping[str, Any]],
    *,
    required_style_anchor_ref: str | None = None,
    scene_anchor_by_name: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Check that each shot explicitly carries the same CAE-supplied lineage anchors."""
    errors: list[str] = []
    inspected: list[dict[str, Any]] = []
    anchors = scene_anchor_by_name or {}
    for shot in shots:
        number = int(shot.get("shotNumber", 0))
        scene = str(shot.get("scene", "")).strip()
        style_ref = shot.get("styleAnchorRef")
        scene_ref = shot.get("sceneAnchorRef")
        if required_style_anchor_ref and style_ref != required_style_anchor_ref:
            errors.append(f"style_anchor_mismatch:S{number}")
        if scene and scene in anchors and scene_ref != anchors[scene]:
            errors.append(f"scene_anchor_mismatch:S{number}")
        inspected.append({"shotNumber": number, "scene": scene, "styleAnchorRef": style_ref, "sceneAnchorRef": scene_ref})
    return {"ok": not errors, "errors": errors, "shots": inspected, "digest": canonical_digest(inspected)}


def append_feedback(
    history: Sequence[Mapping[str, Any]],
    *,
    revision_id: str,
    actor_id: str,
    target_ref: str,
    feedback: str,
    created_at: str,
) -> list[dict[str, Any]]:
    """Append an immutable feedback record; return a new list, never mutate input."""
    if not revision_id or not actor_id or not target_ref or not feedback.strip() or not created_at:
        raise AdapterValidationError("feedback record requires revision_id, actor_id, target_ref, feedback and created_at")
    if any(str(item.get("revisionId")) == revision_id for item in history):
        raise AdapterValidationError("revision_id already exists")
    next_history = deepcopy(list(history))
    next_history.append({
        "revisionId": revision_id,
        "actorId": actor_id,
        "targetRef": target_ref,
        "feedback": feedback.strip(),
        "createdAt": created_at,
    })
    return next_history


def adapter_receipt(
    *,
    operation: str,
    input_digest: str,
    output: Mapping[str, Any],
    evidence_class: str = "EXECUTABLE",
) -> dict[str, Any]:
    """Create a deterministic receipt payload for the surrounding CAE receipt system."""
    return {
        "mandate": "M0074",
        "operation": operation,
        "evidence_class": evidence_class,
        "input_digest": input_digest,
        "output_digest": canonical_digest(output),
        "adapter": "wind_comic_surgical_storyboard_v1",
    }
