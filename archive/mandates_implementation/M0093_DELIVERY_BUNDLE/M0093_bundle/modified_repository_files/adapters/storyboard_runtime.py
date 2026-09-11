"""Shared governed boundary for storyboard runtime adapters (CAE-M0093).

This module is intentionally downstream of the canonical storyboard programs. It accepts only
an already validated, operator-approved M0079 revision plus its M0079 compile evidence. Runtime
adapters may project that expression into downstream syntax, but they may not invent semantic
meaning, replace the evidence lineage, or mutate CAE state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit
from html import escape

from ca_contracts import canonical_sha256
from ca_runtime.storyboard_programs import StoryboardExpression, get_storyboard_program
from ca_runtime.storyboard_session import (
    StoryboardCompileReceipt,
    StoryboardElement,
    StoryboardRevision,
    StoryboardValidationReport,
    VisualAssetReference,
)


class StoryboardRuntimeAdapterError(RuntimeError):
    """Base error for fail-closed runtime compilation."""


class StoryboardRuntimeAuthorizationError(StoryboardRuntimeAdapterError):
    """The runtime input lacks valid CAE compile/approval evidence."""


class StoryboardRuntimeStaleError(StoryboardRuntimeAuthorizationError):
    """Runtime evidence refers to a different revision/session/workspace."""


class StoryboardRuntimeValidationError(StoryboardRuntimeAdapterError):
    """Runtime-specific constraints or source references are malformed."""


@dataclass(frozen=True, slots=True)
class GovernedStoryboardRuntimeInput:
    """Immutable handoff bundle from the canonical storyboard layer."""

    revision: StoryboardRevision
    expression: StoryboardExpression
    validation_report: StoryboardValidationReport
    compile_receipt: StoryboardCompileReceipt


@dataclass(frozen=True, slots=True)
class RuntimeArtifact:
    """Deterministic downstream artifact and its CAE lineage."""

    artifact_id: str
    runtime: str
    format_id: str
    revision_id: str
    expression_sha256: str
    artifact_sha256: str
    lineage_sha256: str
    payload: Mapping[str, Any]
    native_reachability_proven: bool = False
    environment_requirements: tuple[str, ...] = ()

    def manifest(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "runtime": self.runtime,
            "format_id": self.format_id,
            "revision_id": self.revision_id,
            "expression_sha256": self.expression_sha256,
            "artifact_sha256": self.artifact_sha256,
            "lineage_sha256": self.lineage_sha256,
            "native_reachability_proven": self.native_reachability_proven,
            "environment_requirements": list(self.environment_requirements),
        }



def validate_runtime_input(
    handoff: GovernedStoryboardRuntimeInput, *, expected_program_id: str, expected_format_id: str
) -> StoryboardExpression:
    """Prove that runtime inputs still bind to an authoritative compiled revision.

    The runtime re-runs the canonical program compiler and compares the supplied expression
    digest. This makes a visually plausible but semantically altered expression fail closed.
    """

    revision = handoff.revision
    expression = handoff.expression
    report = handoff.validation_report
    receipt = handoff.compile_receipt

    if not report.passed:
        raise StoryboardRuntimeAuthorizationError("runtime compilation requires a passing validation report")

    if receipt.status != "COMPILE_READY":
        raise StoryboardRuntimeAuthorizationError(
            f"runtime compilation requires COMPILE_READY receipt; got {receipt.status!r}"
        )

    if len(revision.canonical_sha256) != 64 or any(c not in "0123456789abcdef" for c in revision.canonical_sha256):
        raise StoryboardRuntimeAuthorizationError("revision canonical_sha256 is malformed")

    identity_pairs = (
        ("workspace_id", revision.workspace_id, report.workspace_id),
        ("session_id", revision.session_id, report.session_id),
        ("revision_id", revision.revision_id, report.revision_id),
        ("workspace_id", revision.workspace_id, receipt.workspace_id),
        ("session_id", revision.session_id, receipt.session_id),
        ("revision_id", revision.revision_id, receipt.revision_id),
        ("editorial_storyboard_id", revision.editorial_storyboard_id, receipt.editorial_storyboard_id),
        ("semantic_program_id", revision.semantic_program_id, receipt.semantic_program_id),
        ("harness_id", revision.harness_id, receipt.harness_id),
        ("validation_report_id", report.report_id, receipt.validation_report_id),
    )
    for field, expected, observed in identity_pairs:
        if expected != observed:
            raise StoryboardRuntimeStaleError(
                f"runtime evidence mismatch for {field}: expected {expected!r}, observed {observed!r}"
            )

    if expression.status != "COMPILED":
        raise StoryboardRuntimeAuthorizationError(
            f"runtime compilation requires COMPILED expression; got {expression.status!r}"
        )
    expression_pairs = (
        ("format_id", expected_format_id, expression.format_id),
        ("program_id", expected_program_id, expression.program_id),
        ("session_id", revision.session_id, expression.session_id),
        ("revision_id", revision.revision_id, expression.revision_id),
        ("editorial_storyboard_id", revision.editorial_storyboard_id, expression.editorial_storyboard_id),
        ("semantic_program_id", revision.semantic_program_id, expression.semantic_program_id),
        ("harness_id", revision.harness_id, expression.harness_id),
    )
    for field, expected, observed in expression_pairs:
        if expected != observed:
            raise StoryboardRuntimeStaleError(
                f"expression mismatch for {field}: expected {expected!r}, observed {observed!r}"
            )

    expected_report_sha = canonical_sha256(
        {
            "workspace_id": report.workspace_id,
            "session_id": report.session_id,
            "revision_id": report.revision_id,
            "passed": report.passed,
            "checks": report.checks,
            "errors": report.errors,
            "warnings": report.warnings,
        }
    )
    if report.report_sha256 != expected_report_sha:
        raise StoryboardRuntimeAuthorizationError("validation report digest does not match its contents")

    expected_receipt_sha = canonical_sha256(
        {
            "workspace_id": receipt.workspace_id,
            "session_id": receipt.session_id,
            "revision_id": receipt.revision_id,
            "editorial_storyboard_id": receipt.editorial_storyboard_id,
            "semantic_program_id": receipt.semantic_program_id,
            "harness_id": receipt.harness_id,
            "validation_report_id": receipt.validation_report_id,
            "status": receipt.status,
            "revision_sha256": revision.canonical_sha256,
        }
    )
    if receipt.lineage_sha256 != expected_receipt_sha:
        raise StoryboardRuntimeAuthorizationError("compile receipt lineage digest does not match its contents")

    canonical_program = get_storyboard_program(expected_format_id)
    expected_expression = canonical_program.compile(revision)
    if expression.model_dump(exclude={"canonical_sha256"}) != expected_expression.model_dump(exclude={"canonical_sha256"}):
        raise StoryboardRuntimeStaleError(
            "supplied storyboard expression does not match the canonical program projection of the revision"
        )
    if expression.canonical_sha256 != expected_expression.canonical_sha256:
        raise StoryboardRuntimeStaleError(
            "supplied storyboard expression digest does not match the canonical program projection of the revision"
        )

    return expected_expression


def safe_source_uri(asset: VisualAssetReference) -> str | None:
    uri = asset.source_uri
    if uri is None:
        return None
    value = uri.strip()
    if not value:
        return None
    parsed = urlsplit(value)
    if parsed.scheme.lower() in {"http", "https"}:
        return value
    if not parsed.scheme and value.startswith(("/", "./")):
        return value
    raise StoryboardRuntimeValidationError(
        f"asset '{asset.asset_id}' source_uri must be http(s) or a relative/absolute web path"
    )


def render_element_html(element: StoryboardElement) -> str:
    """Render a semantically transparent HTML projection of one canonical element."""

    element_id = escape(element.element_id, quote=True)
    purpose = escape(element.semantic_purpose, quote=False)
    evidence = escape(",".join(element.source_evidence_refs), quote=True)
    media_parts: list[str] = []
    for asset in element.asset_references:
        uri = safe_source_uri(asset)
        if uri is None:
            continue
        media_parts.append(
            '<img class="cae-source-asset" '
            f'data-cae-asset-id="{escape(asset.asset_id, quote=True)}" '
            f'data-cae-rights-status="{escape(asset.rights_status, quote=True)}" '
            f'data-cae-source-quality="{escape(asset.source_quality, quote=True)}" '
            f'src="{escape(uri, quote=True)}" '
            f'alt="{purpose}" loading="lazy">'
        )
    media = "\n".join(media_parts)
    return (
        f'<article class="cae-element" data-cae-element-id="{element_id}" '
        f'data-cae-evidence-refs="{evidence}">\n'
        f'<h3>{purpose}</h3>\n'
        f'{media}\n'
        '</article>'
    )


def render_slide_html(*, scene_id: str, semantic_purpose: str, elements: Sequence[StoryboardElement], width: int, height: int) -> str:
    """Build a full-size HTML document for carousel preview/export handoff."""

    body = "\n".join(render_element_html(element) for element in elements)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width={width}, height={height}, initial-scale=1">
<title>{escape(semantic_purpose, quote=True)}</title>
<style>
html, body {{ margin: 0; width: {width}px; height: {height}px; }}
body {{ background: #fff; font-family: system-ui, sans-serif; overflow: hidden; }}
.cae-slide {{ box-sizing: border-box; width: {width}px; height: {height}px; padding: 64px; overflow: hidden; }}
.cae-element {{ margin: 0 0 28px; }}
.cae-element h3 {{ margin: 0 0 18px; font-size: 42px; line-height: 1.08; }}
.cae-source-asset {{ display: block; max-width: 100%; max-height: {max(1, height - 320)}px; object-fit: contain; }}
</style>
</head>
<body>
<main class="cae-slide" data-cae-scene-id="{escape(scene_id, quote=True)}">
<h2>{escape(semantic_purpose, quote=False)}</h2>
{body}
</main>
</body>
</html>'''


def open_carrusel_dimensions(aspect_ratio: str) -> tuple[int, int]:
    dimensions = {"1:1": (1080, 1080), "4:5": (1080, 1350), "9:16": (1080, 1920)}
    try:
        return dimensions[aspect_ratio]
    except KeyError as exc:
        raise StoryboardRuntimeValidationError(f"unsupported Open Carrusel aspect ratio: {aspect_ratio!r}") from exc


def expression_runtime_sha(payload: Mapping[str, Any]) -> str:
    """Expose one deterministic hash for the produced downstream artifact."""

    return canonical_sha256(payload)


__all__ = [
    "GovernedStoryboardRuntimeInput",
    "RuntimeArtifact",
    "StoryboardRuntimeAdapterError",
    "StoryboardRuntimeAuthorizationError",
    "StoryboardRuntimeStaleError",
    "StoryboardRuntimeValidationError",
    "expression_runtime_sha",
    "open_carrusel_dimensions",
    "render_element_html",
    "render_slide_html",
    "safe_source_uri",
    "validate_runtime_input",
]
