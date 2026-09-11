"""Presentation runtime adapters for CAE-M0093.

Slidev and reveal.js remain replaceable downstream runtimes. The adapter emits native syntax for
both runtimes while retaining CAE lineage metadata and never mutating canonical state.
"""

from __future__ import annotations

from html import escape
import json
from typing import Any, Literal

from ca_runtime.storyboard_programs import StoryboardFormat
from adapters.storyboard_runtime import (
    GovernedStoryboardRuntimeInput,
    RuntimeArtifact,
    StoryboardRuntimeValidationError,
    expression_runtime_sha,
    safe_source_uri,
    validate_runtime_input,
)

SLIDEV_UPSTREAM = {
    "repository": "https://github.com/slidevjs/slidev",
    "tag": "v52.19.1",
    "commit": "dbc307b",
    "license": "MIT",
}
REVEALJS_UPSTREAM = {
    "repository": "https://github.com/hakimel/reveal.js",
    "tag": "6.0.1",
    "commit": "52c6c8b",
    "license": "MIT",
}


class PresentationStoryboardRuntimeAdapter:
    """Compile the canonical presentation storyboard into Slidev or reveal.js source."""

    program_id = "presentation_storyboard_program"
    format_id = StoryboardFormat.PRESENTATION

    def __init__(self, *, runtime: Literal["slidev", "revealjs"] = "slidev") -> None:
        if runtime not in {"slidev", "revealjs"}:
            raise StoryboardRuntimeValidationError(f"unsupported presentation runtime: {runtime!r}")
        self.runtime = runtime

    def compile(self, handoff: GovernedStoryboardRuntimeInput) -> RuntimeArtifact:
        expression = validate_runtime_input(
            handoff,
            expected_program_id=self.program_id,
            expected_format_id=self.format_id,
        )
        if self.runtime == "slidev":
            payload = self._compile_slidev(handoff, expression)
            environment = ("Slidev v52.19.1", "Node.js environment with Slidev installed")
        else:
            payload = self._compile_reveal(handoff, expression)
            environment = ("reveal.js 6.0.1", "Browser/Node environment with reveal.js installed")
        artifact_sha = expression_runtime_sha(payload)
        return RuntimeArtifact(
            artifact_id=f"presentation-{self.runtime}-{handoff.revision.revision_id}",
            runtime=self.runtime,
            format_id=self.format_id,
            revision_id=handoff.revision.revision_id,
            expression_sha256=expression.canonical_sha256,
            artifact_sha256=artifact_sha,
            lineage_sha256=handoff.compile_receipt.lineage_sha256,
            payload=payload,
            native_reachability_proven=False,
            environment_requirements=environment,
        )

    def _compile_slidev(self, handoff: GovernedStoryboardRuntimeInput, expression) -> dict[str, Any]:
        sections: list[str] = []
        for scene in expression.scenes:
            sections.append(_slidev_scene(scene))
        slides_md = """---
title: %s
---

<!-- cae-revision-id: %s -->
<!-- cae-compile-receipt-id: %s -->

%s
""" % (
            json.dumps(handoff.revision.editorial_storyboard_id, ensure_ascii=False),
            handoff.revision.revision_id,
            handoff.compile_receipt.receipt_id,
            "\n\n---\n\n".join(sections),
        )
        return {
            "entrypoint": "slides.md",
            "slides_md": slides_md,
            "lineage": _lineage(handoff, expression.canonical_sha256),
        }

    def _compile_reveal(self, handoff: GovernedStoryboardRuntimeInput, expression) -> dict[str, Any]:
        sections: list[str] = []
        for scene in expression.scenes:
            sections.append(_reveal_scene(scene))
        html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(handoff.revision.editorial_storyboard_id, quote=True)}</title>
<!-- cae-revision-id: {escape(handoff.revision.revision_id, quote=True)} -->
<!-- cae-compile-receipt-id: {escape(handoff.compile_receipt.receipt_id, quote=True)} -->
<link rel="stylesheet" href="dist/reset.css">
<link rel="stylesheet" href="dist/reveal.css">
<link rel="stylesheet" href="dist/theme/black.css">
</head>
<body>
<div class="reveal"><div class="slides">
{chr(10).join(sections)}
</div></div>
<script src="dist/reveal.js"></script>
<script>
Reveal.initialize({{ hash: true }});
</script>
</body>
</html>'''
        return {
            "entrypoint": "index.html",
            "index_html": html,
            "lineage": _lineage(handoff, expression.canonical_sha256),
        }


def _lineage(handoff: GovernedStoryboardRuntimeInput, expression_sha256: str) -> dict[str, Any]:
    return {
        "workspace_id": handoff.revision.workspace_id,
        "session_id": handoff.revision.session_id,
        "revision_id": handoff.revision.revision_id,
        "editorial_storyboard_id": handoff.revision.editorial_storyboard_id,
        "semantic_program_id": handoff.revision.semantic_program_id,
        "harness_id": handoff.revision.harness_id,
        "expression_sha256": expression_sha256,
        "validation_report_id": handoff.validation_report.report_id,
        "compile_receipt_id": handoff.compile_receipt.receipt_id,
    }


def _slidev_scene(scene: dict[str, Any]) -> str:
    build_order = {item["element_id"]: item["build_step"] for item in scene["build_order"]}
    body = [f"<!-- cae-scene-id: {escape(scene['scene_id'])} -->", f"# {escape(scene['semantic_purpose'])}"]
    elements = sorted(scene["shots"], key=lambda shot: shot.get("start_ms", 0))
    for shot in elements:
        for payload in shot.get("elements", []):
            step = build_order[payload["element_id"]]
            attrs = (
                f'data-cae-element-id="{escape(payload["element_id"], quote=True)}" '
                f'data-cae-evidence-refs="{escape(",".join(payload.get("source_evidence_refs", [])), quote=True)}"'
            )
            body.append(f'<div v-click="{step}" class="cae-element" {attrs}>')
            body.append(escape(payload["semantic_purpose"]))
            for asset in payload.get("asset_references", []):
                uri = safe_source_uri(_asset_from_payload(asset))
                if uri:
                    body.append(
                        f'<img data-cae-asset-id="{escape(asset["asset_id"], quote=True)}" '
                        f'src="{escape(uri, quote=True)}" alt="{escape(payload["semantic_purpose"], quote=True)}">'
                    )
            body.append("</div>")
    return "\n".join(body)


def _reveal_scene(scene: dict[str, Any]) -> str:
    build_order = {item["element_id"]: item["build_step"] for item in scene["build_order"]}
    elements: list[str] = []
    for shot in sorted(scene["shots"], key=lambda item: item.get("start_ms", 0)):
        for payload in shot.get("elements", []):
            step = build_order[payload["element_id"]]
            evidence = escape(",".join(payload.get("source_evidence_refs", [])), quote=True)
            block = [
                f'<div class="fragment" data-fragment-index="{step}" '
                f'data-cae-element-id="{escape(payload["element_id"], quote=True)}" '
                f'data-cae-evidence-refs="{evidence}">',
                escape(payload["semantic_purpose"]),
            ]
            for asset in payload.get("asset_references", []):
                uri = safe_source_uri(_asset_from_payload(asset))
                if uri:
                    block.append(
                        f'<img src="{escape(uri, quote=True)}" '
                        f'data-cae-asset-id="{escape(asset["asset_id"], quote=True)}" '
                        f'alt="{escape(payload["semantic_purpose"], quote=True)}">'
                    )
            block.append("</div>")
            elements.append("\n".join(block))
    return (
        f'<section data-cae-scene-id="{escape(scene["scene_id"], quote=True)}">\n'
        f'<h2>{escape(scene["semantic_purpose"])}</h2>\n'
        + "\n".join(elements)
        + "\n</section>"
    )


def _asset_from_payload(asset: dict[str, Any]):
    from types import SimpleNamespace
    return SimpleNamespace(asset_id=asset["asset_id"], source_uri=asset.get("source_uri"))


__all__ = ["PresentationStoryboardRuntimeAdapter", "SLIDEV_UPSTREAM", "REVEALJS_UPSTREAM"]
