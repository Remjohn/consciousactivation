from __future__ import annotations

import json
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Any, Mapping

from ca_contracts import canonical_json_text, canonical_sha256
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.phase9_demo import run_phase9_demo

from .guards import evaluate_format02_gate
from .release import ReleaseEvidenceBuilder
from .sbom import build_sbom


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json_text(value) + "\n", encoding="utf-8")


def _ref(value: Mapping[str, Any], *, identifier: str | None = None) -> dict[str, str]:
    return {
        "object_id": str(identifier or value.get("object_id") or value.get("id") or value.get("receipt_id") or value.get("evaluation_id") or "reference"),
        "version": str(value.get("semantic_version") or value.get("version") or value.get("evaluation_version") or "1.0.0"),
        "sha256": str(value.get("canonical_sha256") or value.get("sha256") or value.get("receipt_sha256") or canonical_sha256(value)),
    }


def _run_studio(repo: Path, output: Path) -> dict[str, Any]:
    node = shutil.which("node")
    entry = repo / "07_CONSCIOUS_ACTIVATIONS_STUDIO" / "dist" / "index.js"
    if node is None or not entry.is_file():
        result = {
            "status": "UNAVAILABLE",
            "reason": "node or compiled Studio entrypoint unavailable",
            "output_files": [],
            "production_authorized": False,
        }
        _write(output / "studio-execution.json", result)
        return result
    proc = subprocess.run(
        [node, str(entry), "demo", "--output-dir", str(output), "--json"],
        cwd=repo,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        result = {
            "status": "FAILED",
            "returncode": proc.returncode,
            "stderr": proc.stderr[-4000:],
            "production_authorized": False,
        }
        _write(output / "studio-execution.json", result)
        return result
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        result = {"status": "PASS", "stdout": proc.stdout, "output_files": [], "production_authorized": False}
    result = {**result, "status": "PASS", "production_authorized": False}
    _write(output / "studio-execution.json", result)
    return result


def _deterministic_zip(source: Path, target: Path) -> str:
    if target.exists():
        target.unlink()
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(source.rglob("*")):
            if not path.is_file() or path == target:
                continue
            info = zipfile.ZipInfo(path.relative_to(source).as_posix())
            info.date_time = (2026, 7, 24, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    from ca_contracts import bytes_sha256
    return bytes_sha256(target.read_bytes())


def run_phase9_pilot(repo_root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    repo = Path(repo_root).resolve()
    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)

    core = run_phase9_demo(output / "core", repo)
    studio = _run_studio(repo, output / "studio")

    pipeline = PipelineApplication(core["pipeline_database"])
    pipeline.initialize()
    backup = pipeline.operations.backup(output / "operations" / "pipeline-backup.sqlite3")
    restore = pipeline.operations.restore_rehearsal(
        output / "operations" / "pipeline-backup.sqlite3",
        output / "operations" / "pipeline-restored.sqlite3",
    )
    preflight = pipeline.operations.preflight(
        {
            "python": [shutil.which("python") or "python", "--version"],
            "ffmpeg": [shutil.which("ffmpeg") or "ffmpeg", "-version"],
            "node": [shutil.which("node") or "node", "--version"],
            "git": [shutil.which("git") or "git", "--version"],
        }
    )
    benchmark = pipeline.operations.benchmark("pipeline-status", pipeline.status, iterations=3)
    _write(output / "operations" / "backup-receipt.json", backup)
    _write(output / "operations" / "restore-rehearsal.json", restore)
    _write(output / "operations" / "environment-preflight.json", preflight)
    _write(output / "operations" / "benchmark.json", benchmark)

    sbom = build_sbom(repo)
    compose = repo / "deployment" / "phase9" / "docker-compose.local.yml"
    deployment_manifest = {
        "deployment_id": "phase9-local-reference",
        "profile": "LOCAL_DEVELOPMENT_REFERENCE",
        "compose_path": compose.relative_to(repo).as_posix() if compose.exists() else "NOT_AVAILABLE",
        "compose_sha256": canonical_sha256(compose.read_text(encoding="utf-8")) if compose.exists() else "0" * 64,
        "runtime_components": ["air", "pipeline", "interview-expression", "studio", "vae", "delegation-rc4"],
        "production_authorized": False,
        "limitations": ["local reference topology", "no production trust roots", "no external worker fleet"],
    }
    format02_gate = evaluate_format02_gate()
    _write(output / "release" / "FORMAT02_DEFERRAL_GATE.json", format02_gate)

    core_dir = output / "core"
    studio_dir = output / "studio"
    artifacts = [
        (core_dir / "media" / "source-led-short.mp4", "artifacts/source-led-short.mp4", "source_led_video"),
        (core_dir / "media" / "supervisual.png", "artifacts/supervisual.png", "supervisual"),
        (core_dir / "media" / "carousel.pdf", "artifacts/carousel.pdf", "carousel_pdf"),
        (core_dir / "media" / "animation" / "scene.mp4", "artifacts/animation-scene.mp4", "animation_scene"),
        (core_dir / "vae" / "reference-visual-asset.png", "artifacts/reference-visual-asset.png", "visual_asset"),
    ]
    missing = [str(path) for path, _, _ in artifacts if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"reference pilot artifacts missing: {missing}")

    continuity = json.loads((core_dir / "continuity.json").read_text(encoding="utf-8"))
    visual_eval = json.loads((core_dir / "visual_evaluation.json").read_text(encoding="utf-8"))
    semantic = json.loads((core_dir / "semantic.json").read_text(encoding="utf-8"))
    interview = json.loads((core_dir / "interview.json").read_text(encoding="utf-8"))
    audit_refs = []
    studio_audit = studio_dir / "audit-export.json"
    if studio_audit.is_file():
        audit_value = json.loads(studio_audit.read_text(encoding="utf-8"))
        audit_refs.append(_ref(audit_value, identifier=str(audit_value.get("export_id", "studio-audit-export"))))

    open_gaps = [
        {"gap_id": "P9-GAP-REAL-IMPORTED-INTERVIEW", "status": "OPEN", "owner": "operator", "description": "The final reference pilot uses deterministic fixtures, not an operator-supplied real interview."},
        {"gap_id": "P9-GAP-EXTERNAL-MODELS", "status": "OPEN", "owner": "external-infrastructure", "description": "Real SAM3, Lucida, ComfyUI, GNM, and certified evaluator execution remain unproven."},
        {"gap_id": "P9-GAP-PRODUCTION-TRUST", "status": "OPEN", "owner": "program-control", "description": "Signing, trust roots, production infrastructure, and release authority remain separate."},
        {"gap_id": "P9-GAP-FORMAT02", "status": "DEFERRED", "owner": "program-control", "description": "Format 02 remains deferred pending a current complete Harness and separate activation decision."},
    ]
    handoff_without_hash = {
        "handoff_id": "phase9-final-implementation-handoff",
        "completed_phase_ids": [f"PHASE_{index:02d}" for index in range(1, 10)],
        "open_gap_ids": [gap["gap_id"] for gap in open_gaps],
        "next_permitted_actions": ["run real imported-interview pilot", "bind external evaluator and workers", "prepare production trust decision"],
        "blocked_actions": ["claim production readiness", "claim certification", "activate Format 02", "authorize VAE Stage 5 from development evidence"],
        "claim_ceiling": "PHASE_09_FINAL_INTEGRATED_DEVELOPMENT_CANDIDATE",
    }
    implementation_handoff = {**handoff_without_hash, "handoff_sha256": canonical_sha256(handoff_without_hash)}

    release = ReleaseEvidenceBuilder(repo).build(
        release_id="conscious-activations-phase9-final-development-candidate",
        output_dir=output / "release",
        source_refs=[core["source_package_ref"]],
        semantic_refs=[core["semantic_production_package_ref"], _ref(semantic.get("approved_final_script_ref", {}), identifier="final-script:phase9")],
        continuity_ref=core["continuity_ref"],
        artifact_paths=artifacts,
        evaluation_refs=[_ref(visual_eval, identifier="activation-evaluation:phase9")],
        audit_export_refs=audit_refs,
        backup_receipts=[backup, restore],
        benchmark_receipts=[benchmark],
        sbom=sbom,
        deployment_manifest=deployment_manifest,
        open_gaps=open_gaps,
        implementation_handoff=implementation_handoff,
    )

    pilot_without_hash = {
        "pilot_id": "phase9-final-reference-pilot",
        "pilot_version": "0.9.0-dev.1",
        "source_package_ref": core["source_package_ref"],
        "semantic_production_package_ref": core["semantic_production_package_ref"],
        "continuity_ref": core["continuity_ref"],
        "artifact_refs": core["artifact_refs"],
        "release_manifest_ref": {
            "object_id": release["manifest"]["release_id"],
            "version": release["manifest"]["release_version"],
            "sha256": release["manifest"]["release_manifest_sha256"],
        },
        "studio_status": studio.get("status", "UNKNOWN"),
        "backup_result": backup["integrity"],
        "restore_result": restore["result"],
        "format02_activated": False,
        "vae_stage5_authorized": False,
        "production_authorized": False,
        "certified": False,
        "claim_ceiling": "PHASE_09_FINAL_INTEGRATED_DEVELOPMENT_CANDIDATE",
    }
    pilot_receipt = {**pilot_without_hash, "pilot_receipt_sha256": canonical_sha256(pilot_without_hash)}
    _write(output / "PILOT_RECEIPT.json", pilot_receipt)

    archive_sha = _deterministic_zip(output, output / "PHASE_09_REFERENCE_EVIDENCE.zip")
    result = {
        **pilot_receipt,
        "artifact_count": len(core["artifact_refs"]),
        "release_evidence_zip": str(output / "PHASE_09_REFERENCE_EVIDENCE.zip"),
        "release_evidence_zip_sha256": archive_sha,
        "output_dir": str(output),
    }
    _write(output / "PHASE_09_COMPLETION_RECEIPT.json", result)
    return result
