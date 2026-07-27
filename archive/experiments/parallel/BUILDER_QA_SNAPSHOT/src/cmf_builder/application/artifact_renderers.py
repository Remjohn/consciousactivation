from __future__ import annotations

import json
from typing import Iterable

from cmf_builder.domain.generated_artifacts import (
    ARTIFACT_AUTHORITY_CLASS,
    ARTIFACT_PATHS,
    HUMAN_ARTIFACT_PATHS,
    ArtifactDependencyInvalid,
    ArtifactDependencySelector,
    ArtifactIntegrityInvalid,
    GeneratedArtifact,
    ReproducibleBuildConfig,
)
from cmf_builder.domain.harness_ir import HarnessIR


_SECTION_BY_ARTIFACT = {
    "human/product.md": ("identity", "evidence", "contracts", "authorization"),
    "human/syntax.md": ("syntax",),
    "human/activative-program.md": ("activative_semantics",),
    "human/runtime-architecture.md": ("phases", "contexts", "modules", "budgets", "implementation_units"),
    "human/skill-system.md": ("skills", "references"),
    "human/evaluation.md": ("evaluators",),
    "human/repair.md": ("repairs",),
    "human/handoff.md": ("contracts", "references", "authorization"),
    "openspec/change.json": ("identity", "evidence", "contracts", "authorization"),
    "openspec/harness-ir-view.schema.json": (
        "identity", "evidence", "syntax", "activative_semantics", "phases", "contexts",
        "contracts", "modules", "skills", "references", "evaluators", "repairs", "budgets",
        "implementation_units", "authorization",
    ),
    "openspec/implementation-governance.json": ("modules", "implementation_units", "authorization"),
    "machine/registry-view.json": ("identity", "references"),
    "machine/contract-view.json": ("contracts", "authorization"),
    "machine/graph-view.json": ("phases", "contexts", "modules", "references"),
    "machine/skill-manifest-view.json": ("skills",),
    "machine/evaluation-manifest-view.json": ("evaluators",),
    "machine/repair-policy-view.json": ("repairs",),
    "machine/dashboard-config-view.json": ("identity", "phases", "authorization"),
    "machine/fixture-view.json": ("identity", "evidence", "syntax", "contracts"),
    "machine/traceability-map.json": (
        "identity", "evidence", "syntax", "activative_semantics", "phases", "contexts",
        "contracts", "modules", "skills", "references", "evaluators", "repairs", "budgets",
        "implementation_units", "authorization",
    ),
    "machine/implementation-ticket-view.json": ("identity", "modules", "implementation_units", "authorization"),
}


def dependency_selectors(ir: HarnessIR) -> tuple[ArtifactDependencySelector, ...]:
    selectors = []
    for path in ARTIFACT_PATHS:
        prefixes = _SECTION_BY_ARTIFACT[path]
        source_paths = tuple(
            sorted(
                item.path
                for item in ir.material_values
                if item.path.split(".", 1)[0] in prefixes
            )
        )
        selector = ArtifactDependencySelector(path, source_paths)
        selector.validate(ir)
        selectors.append(selector)
    return tuple(selectors)


def render_artifacts(
    ir: HarnessIR,
    config: ReproducibleBuildConfig,
) -> tuple[GeneratedArtifact, ...]:
    ir.validate()
    config.validate()
    by_path = {item.path: item for item in ir.material_values}
    rendered: list[GeneratedArtifact] = []
    for selector in dependency_selectors(ir):
        selected = tuple(by_path[path] for path in selector.source_node_paths)
        if selector.artifact_path in HUMAN_ARTIFACT_PATHS:
            content = _render_markdown(selector.artifact_path, ir, selected)
            media_type = "text/markdown"
        else:
            content = _render_json(selector.artifact_path, ir, selected)
            media_type = "application/json"
        artifact = GeneratedArtifact.create(
            path=selector.artifact_path,
            media_type=media_type,
            ir=ir,
            selector=selector,
            config=config,
            content=content,
        )
        _validate_safe_projection(artifact)
        rendered.append(artifact)
    ordered = tuple(sorted(rendered, key=lambda item: item.path))
    if tuple(item.path for item in ordered) != ARTIFACT_PATHS:
        raise ArtifactDependencyInvalid("Renderer did not produce the closed artifact inventory.")
    return ordered


def _render_markdown(path: str, ir: HarnessIR, values: Iterable[object]) -> bytes:
    title = path.removeprefix("human/").removesuffix(".md").replace("-", " ").title()
    lines = [
        f"# {title}",
        "",
        "Generated projection status: `NON_EXECUTABLE`",
        f"Authority: `{ARTIFACT_AUTHORITY_CLASS}`",
        f"Source Harness IR: `{ir.ir_id}` (`{ir.ir_hash}`)",
        "",
        "This immutable view is subordinate to HarnessIR and cannot authorize execution.",
        "",
        "## Governed values",
        "",
    ]
    for value in values:
        canonical = value.canonical_dict()  # type: ignore[attr-defined]
        lines.extend(
            (
                f"### `{canonical['path']}`",
                "",
                "```json",
                json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False),
                "```",
                "",
            )
        )
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def _render_json(path: str, ir: HarnessIR, values: Iterable[object]) -> bytes:
    payload = {
        "artifact_path": path,
        "authority_class": ARTIFACT_AUTHORITY_CLASS,
        "executable": False,
        "projection_only": True,
        "source_ir_id": ir.ir_id,
        "source_ir_hash": ir.ir_hash,
        "source_nodes": [value.canonical_dict() for value in values],  # type: ignore[attr-defined]
        "view_schema": "cmf-builder-generated-view/v1@1.0.0",
    }
    return (
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def _validate_safe_projection(artifact: GeneratedArtifact) -> None:
    lowered = artifact.content.lower()
    forbidden = (
        b"http://",
        b"https://",
        b"file://",
        b"<script",
        b"subprocess",
        b'"secret":',
        b'"token":',
        b"api_key",
        b"bearer ",
    )
    matched = next((token.decode("ascii") for token in forbidden if token in lowered), None)
    if matched is not None:
        raise ArtifactIntegrityInvalid(
            "Generated projection contains a prohibited external or executable reference.",
            path=artifact.path,
            token=matched,
        )
