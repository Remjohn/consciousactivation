"""Generate reproducible Stage 1 repository and requirement evidence tables.

This is audit tooling only. It reads the PRD package and the extracted V2.1
brownfield bundle; it does not modify the brownfield source repository.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

import yaml


DEFAULT_SOURCE_ROOT = Path(r"D:\Work\CCP_CMF_ATOMIC_HARNESS_SPEC_BUILDER_V2_1")
VERDICT_BLOCKER = (
    "UNRESOLVED_GOVERNANCE: the applicable AGENTS.md defines no Stage 1 "
    "requirement-coverage verdict vocabulary"
)


FEATURE_EVIDENCE: dict[str, dict[str, str]] = {
    "F01": {
        "code": "src/cmf_harness_spec_builder/{cli.py:35-312,module_registry.py:12-108,state.py:12-27,models.py:35-115}",
        "tests": "tests/test_spec_builder_v2.py:452-478",
        "gap": "Three modules and file-backed run state exist, but lifecycle transitions, authority checks, checkpoints, invalidation, waiver control, and an append-only ledger are not enforced.",
    },
    "F02": {
        "code": "src/cmf_harness_spec_builder/{source_index.py:47-257,saturation.py:72-148,cli.py:112-138}",
        "tests": "tests/test_spec_builder_v2.py:115-132",
        "gap": "Files and ZIPs are hashed and text is keyword-indexed; target-specific profiles, authoritative roles, stable specimen IDs, media normalization, conflicts, measurable saturation, and typed outcomes are absent.",
    },
    "F03": {
        "code": "src/cmf_harness_spec_builder/source_index.py:185-209",
        "tests": "No visual-syntax parser test found in tests/.",
        "gap": "Only image dimensions and file hashes are indexed. No frame/slide extraction, syntax primitives, temporal structure, motif clustering, grammar induction, confidence, provenance, or parser validation exists.",
    },
    "F04": {
        "code": "src/cmf_harness_spec_builder/{models.py:51-63,cli.py:140-148}",
        "tests": "No atomicity classification or ratification test found in tests/.",
        "gap": "Atomicity status can be assigned directly; no evidence-linked classifier, rationale packet, draft harness model, partition graph, contradiction handling, or human ratification gate exists.",
    },
    "F05": {
        "code": "src/cmf_harness_spec_builder/{decision_tree.py:188-316,grill_me.py:81-313,models.py:204-330}",
        "tests": "tests/test_spec_builder_v2.py:144-209,332-377",
        "gap": "Static dependency graphs and question packets exist, but no transactional Genesis checkpoint, descendant invalidation on reopen, source-linked answer compiler, or canonical IR commit exists.",
    },
    "F06": {
        "code": "src/cmf_harness_spec_builder/{models.py:1-972,spec_compiler.py:72-188}",
        "tests": "tests/test_spec_builder_v2.py:319-330,604-622",
        "gap": "Pydantic contracts and template compilation exist, but there is no canonical Harness IR root, identity/integrity model, schema migration system, deterministic serializer, or IR-to-target compiler boundary.",
    },
    "F07": {
        "code": "src/cmf_harness_spec_builder/{models.py:416-572,743-970,decision_tree.py:18-185}",
        "tests": "tests/test_spec_builder_v2.py:211-267,507-568",
        "gap": "Several typed contracts and decision ownership labels exist; complete capability/module/phase graphs, executable handoffs, ownership validation, and contract compilers do not.",
    },
    "F08": {
        "code": "src/cmf_harness_spec_builder/models.py:416-462",
        "tests": "tests/test_spec_builder_v2.py:211-222,558-568",
        "gap": "Context-plan fields are modeled, but no reference registry, SPR compiler, loading policy engine, precedence resolver, context manifest compiler, or budget enforcement exists.",
    },
    "F09": {
        "code": "src/cmf_harness_spec_builder/models.py:528-620",
        "tests": "tests/test_spec_builder_v2.py:224-237",
        "gap": "Skill references and JIT plans are data models only; no canonical registry, dependency resolver, maturity workflow, behavior evaluation, versioning, or promotion process exists.",
    },
    "F10": {
        "code": "src/cmf_harness_spec_builder/models.py:574-620",
        "tests": "tests/test_spec_builder_v2.py:224-237",
        "gap": "A static execution-plan model exists; there is no skill composition planner, recipe compiler, runtime capsule compiler, adapter, budget check, or execution test.",
    },
    "F11": {
        "code": "No benchmark, evaluator, corpus, scorecard, or receipt implementation found under src/.",
        "tests": "No protected-corpus, repeated-run, independent-evaluation, or scorecard test found in tests/.",
        "gap": "The behavioral evaluation subsystem is absent.",
    },
    "F12": {
        "code": "src/cmf_harness_spec_builder/cli.py:242-268",
        "tests": "No Control Tower API, projection, UI, accessibility, or event-stream test found in tests/.",
        "gap": "A CLI status printout exists; no event-derived read model, API, operator UI, evidence drill-down, intervention controls, or export surface exists.",
    },
    "F13": {
        "code": "src/cmf_harness_spec_builder/{readiness.py:14-143,models.py:99-113,401-414}",
        "tests": "tests/test_spec_builder_v2.py:319-330,604-622; fixtures at 108-111 and 445-448 are empty",
        "gap": "Readiness checks files, markers, and decision statuses. It does not validate evidence semantics, benchmarks, repair ownership, causal graphs, maturity receipts, hard gates, or implementation authorization, and tests can PASS with empty evidence indexes.",
    },
    "F14": {
        "code": "configs/*.yaml; src/cmf_harness_spec_builder/{module_registry.py:12-108,legacy_format01.py:44-103}",
        "tests": "tests/test_spec_builder_v2.py:379-397,452-478",
        "gap": "Module configuration and a legacy Format 01 donor guard exist; the four canonical category constitutions, category-local IR, sequencing compilers, isolation checks, and migration rules do not.",
    },
    "F15": {
        "code": "src/cmf_harness_spec_builder/{spec_compiler.py:72-188,target_scaffold.py:10-54}; schemas/harness_spec_artifact_manifest.schema.json",
        "tests": "tests/test_spec_builder_v2.py:269-287,571-602",
        "gap": "OpenSpec files and target pointers can be emitted, but no complete Development Capsule manifest compiler, executable story/fixture generation, trace closure, integrity signing, or handoff validation exists.",
    },
    "F16": {
        "code": "src/cmf_harness_spec_builder/{cli.py:270-283,legacy_format01.py:44-103,saturation.py:72-148}",
        "tests": "tests/test_spec_builder_v2.py:379-397",
        "gap": "Upgrade re-runs saturation and legacy donor detection; there is no source-to-IR migration, schema migration, dual compilation, equivalence report, deprecation ledger, rollback, or migration test suite.",
    },
    "F17": {
        "code": "src/cmf_harness_spec_builder/module_registry.py:12-108; openspec/schemas/{cmf-atomic-content-harness-spec-v2.1,cmf-atomic-vae-spec-v1,cmf-atomic-delegation-spec-v1}/",
        "tests": "tests/test_spec_builder_v2.py:452-478,604-622",
        "gap": "All three named modules compile against separate OpenSpec trees, but they do not compile from one canonical Harness IR and have no cross-target compatibility or target-local IR conformance suite.",
    },
    "F18": {
        "code": ".pi/skills/cmf-atomic-harness-spec-builder/{SKILL.md,steps/step-00-select-module.md..step-14-implementation-handoff.md}",
        "tests": "No Workflow IR, router, scheduler, sandbox, retry, promotion, rollback, telemetry, or fault-injection test found in tests/.",
        "gap": "A Markdown operator workflow exists, but no typed Builder Workflow IR, executable runtime, node contracts, routing, bounded parallelism, sandboxing, telemetry, promotion, rollback, or workflow conformance suite exists.",
    },
}


DECISION_FEATURES: dict[str, tuple[str, ...]] = {
    "D001": ("F01", "F06", "F18"), "D002": ("F01", "F05", "F18"),
    "D003": ("F01", "F11", "F13"), "D004": ("F17",), "D005": ("F02",),
    "D006": ("F01", "F18"), "D007": ("F03",), "D008": ("F04",),
    "D009": ("F05",), "D010": ("F05",), "D011": ("F06",),
    "D012": ("F07",), "D013": ("F07", "F08"), "D014": ("F07",),
    "D015": ("F07",), "D016": ("F08",), "D017": ("F09", "F10"),
    "D018": ("F10",), "D019": ("F08", "F10"), "D020": ("F08", "F10"),
    "D021": ("F09", "F11"), "D022": ("F11",), "D023": ("F11",),
    "D024": ("F11",), "D025": ("F12", "F18"), "D026": ("F13",),
    "D027": ("F01", "F13", "F18"), "D028": ("F16",), "D029": ("F15",),
    "D030": ("F14",), "D031": ("F14",), "D032": ("F16", "F17"),
    "D033": ("F01", "F03", "F06", "F09", "F13", "F14", "F18"),
}


NFR_FEATURES: dict[str, tuple[str, ...]] = {
    "REL": ("F01", "F06", "F18"), "PERF": ("F10", "F12", "F18"),
    "TRACE": ("F02", "F06", "F12", "F18"), "OBS": ("F12", "F18"),
    "SEC": ("F02", "F18"), "COMPAT": ("F06", "F16"),
    "PORT": ("F02", "F17", "F18"), "UX": ("F12",),
    "EVAL": ("F11", "F14"), "MAINT": ("F06", "F09", "F14"),
    "SCALE": ("F02", "F03"), "ARCH": ("F07", "F18"),
    "TEST": ("F11", "F18"), "CAT": ("F14",), "WORKFLOW": ("F18",),
}


ANTI_GOAL_FEATURES: dict[str, tuple[str, ...]] = {
    "AG-001": ("F01", "F15"), "AG-002": ("F17",), "AG-003": ("F04", "F14"),
    "AG-004": ("F14",), "AG-005": ("F14",), "AG-006": ("F03",),
    "AG-007": ("F02", "F06"), "AG-008": ("F09",), "AG-009": ("F09", "F10"),
    "AG-010": ("F09", "F11"), "AG-011": ("F18",), "AG-012": ("F08", "F18"),
    "AG-013": ("F08",), "AG-014": ("F13",), "AG-015": ("F13",),
    "AG-016": ("F12",), "AG-017": ("F11", "F13"), "AG-018": ("F06",),
    "AG-019": ("F18",), "AG-020": ("F18",), "AG-021": ("F18",),
    "AG-022": ("F01", "F05", "F13", "F18"),
}


HARD_GATE_FEATURES: dict[str, tuple[str, ...]] = {
    "HG-001": ("F05", "F06"), "HG-002": ("F02", "F13"),
    "HG-003": ("F04",), "HG-004": ("F07",), "HG-005": ("F07",),
    "HG-006": ("F09", "F11"), "HG-007": ("F07", "F09"),
    "HG-008": ("F11",), "HG-009": ("F13",), "HG-010": ("F13",),
    "HG-011": ("F18",), "HG-012": ("F18",), "HG-013": ("F18",),
    "HG-014": ("F11", "F18"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def classify(path: Path) -> str:
    value = path.as_posix().lower()
    if "/.pytest_cache/" in f"/{value}" or value.startswith(".pytest_cache/"):
        return "generated_test_cache"
    if value.startswith("src/") and path.suffix == ".py": return "production_python"
    if value.startswith("tests/"): return "test"
    if value.startswith("schemas/"): return "json_schema"
    if value.startswith("openspec/"): return "openspec_schema_or_template"
    if value.startswith(".pi/"): return "operator_workflow"
    if value.startswith("configs/"): return "configuration"
    if value.startswith("templates/"): return "template"
    if value.startswith("docs/") or value.startswith("references/") or path.suffix == ".md": return "documentation_or_reference"
    if value.startswith("scripts/"): return "utility_script"
    return "project_metadata_or_other"


def verify_file(path: Path) -> str:
    suffix = path.suffix.lower()
    try:
        if suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            return "python_ast_parsed"
        if suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
            return "json_parsed"
        if suffix in {".yaml", ".yml"}:
            yaml.safe_load(path.read_text(encoding="utf-8"))
            return "yaml_parsed"
        if suffix in {".md", ".txt", ".toml", ".gitignore", ""}:
            path.read_text(encoding="utf-8")
            return "utf8_read"
        path.read_bytes()
        return "binary_read"
    except Exception as exc:  # Evidence must retain parse failures, not hide them.
        return f"verification_error:{type(exc).__name__}:{exc}"


def write_repository_inventory(source_root: Path, output_dir: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    baseline_hash = hashlib.sha256()
    for path in sorted((p for p in source_root.rglob("*") if p.is_file()), key=lambda p: p.as_posix().lower()):
        relative = path.relative_to(source_root).as_posix()
        digest = sha256(path)
        asset_class = classify(Path(relative))
        verification = verify_file(path)
        rows.append({
            "path": relative,
            "size_bytes": path.stat().st_size,
            "sha256": digest,
            "asset_class": asset_class,
            "inspection_method": verification,
            "source_baseline": "no" if asset_class == "generated_test_cache" else "yes",
        })
        if asset_class != "generated_test_cache":
            baseline_hash.update(relative.encode("utf-8"))
            baseline_hash.update(digest.encode("ascii"))
            baseline_hash.update(str(path.stat().st_size).encode("ascii"))

    fieldnames = ["path", "size_bytes", "sha256", "asset_class", "inspection_method", "source_baseline"]
    with (output_dir / "REPOSITORY_FILE_INVENTORY.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    class_counts: dict[str, int] = {}
    errors = []
    for row in rows:
        class_counts[row["asset_class"]] = class_counts.get(row["asset_class"], 0) + 1
        if str(row["inspection_method"]).startswith("verification_error"):
            errors.append({"path": row["path"], "error": row["inspection_method"]})
    return {
        "source_root": str(source_root),
        "observed_file_count": len(rows),
        "baseline_file_count_excluding_generated_test_cache": sum(r["source_baseline"] == "yes" for r in rows),
        "baseline_size_bytes": sum(int(r["size_bytes"]) for r in rows if r["source_baseline"] == "yes"),
        "aggregate_evidence_sha256": baseline_hash.hexdigest(),
        "asset_class_counts": dict(sorted(class_counts.items())),
        "verification_errors": errors,
    }


def write_prd_package_inventory(prd_root: Path, output_dir: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    package_hash = hashlib.sha256()
    paths = sorted(
        (
            path for path in prd_root.rglob("*")
            if path.is_file() and "stage1" not in path.relative_to(prd_root).parts
        ),
        key=lambda path: path.as_posix().lower(),
    )
    for path in paths:
        relative = path.relative_to(prd_root).as_posix()
        digest = sha256(path)
        verification = verify_file(path)
        rows.append({
            "path": relative,
            "size_bytes": path.stat().st_size,
            "sha256": digest,
            "inspection_method": verification,
        })
        package_hash.update(relative.encode("utf-8"))
        package_hash.update(digest.encode("ascii"))
        package_hash.update(str(path.stat().st_size).encode("ascii"))

    with (output_dir / "PRD_PACKAGE_FILE_INVENTORY.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "size_bytes", "sha256", "inspection_method"])
        writer.writeheader()
        writer.writerows(rows)
    return {
        "file_count_including_manifest": len(rows),
        "size_bytes": sum(int(row["size_bytes"]) for row in rows),
        "aggregate_evidence_sha256": package_hash.hexdigest(),
        "verification_errors": [
            {"path": row["path"], "error": row["inspection_method"]}
            for row in rows if str(row["inspection_method"]).startswith("verification_error")
        ],
    }


def combine_features(feature_ids: Iterable[str]) -> tuple[str, str, str]:
    ids = tuple(dict.fromkeys(feature_ids))
    code = " | ".join(FEATURE_EVIDENCE[i]["code"] for i in ids)
    tests = " | ".join(FEATURE_EVIDENCE[i]["tests"] for i in ids)
    gaps = " | ".join(f"{i}: {FEATURE_EVIDENCE[i]['gap']}" for i in ids)
    return code, tests, gaps


def matrix_row(
    record_type: str,
    item_id: str,
    title: str,
    parent: str,
    status: str,
    text: str,
    source_file: str,
    feature_ids: Iterable[str],
) -> dict[str, str]:
    code, tests, gaps = combine_features(feature_ids)
    return {
        "record_type": record_type,
        "id": item_id,
        "title": title,
        "parent": parent,
        "status": status,
        "requirement_decision_or_gate": text,
        "applicability": "applicable",
        "code_evidence": code,
        "test_evidence": tests,
        "prd_or_schema_evidence": source_file,
        "verified_gap": gaps,
        "verdict": "",
        "verdict_blocker": VERDICT_BLOCKER,
    }


def write_requirement_matrix(prd_root: Path, output_dir: Path) -> dict[str, Any]:
    registry = json.loads((prd_root / "governance/REQUIREMENTS_REGISTRY.json").read_text(encoding="utf-8"))
    decisions = json.loads((prd_root / "governance/DECISION_REGISTER.json").read_text(encoding="utf-8"))["decisions"]
    anti_goals = json.loads((prd_root / "governance/ARCHITECTURAL_PROHIBITIONS.json").read_text(encoding="utf-8"))["anti_goals"]
    hard_gates = yaml.safe_load((prd_root / "governance/READINESS_HARD_GATES.yaml").read_text(encoding="utf-8"))["gates"]
    rows: list[dict[str, str]] = []

    for item in registry["functional_requirements"]:
        feature = item["feature_id"]
        rows.append(matrix_row(
            "functional_requirement", item["id"], item["title"],
            f"{feature} {item['feature_title']}", item["status"], item["requirement"],
            item["source_file"], (feature,),
        ))
    for item in registry["non_functional_requirements"]:
        domain = item["id"].split("-")[1]
        rows.append(matrix_row(
            "non_functional_requirement", item["id"], item["title"], domain,
            item["status"], item["requirement"], item["source_file"], NFR_FEATURES[domain],
        ))
    for item in decisions:
        rows.append(matrix_row(
            "locked_decision", item["id"], item["title"], "DECISION_REGISTER",
            item["status"], item["decision"], "governance/DECISION_REGISTER.json",
            DECISION_FEATURES[item["id"]],
        ))
    for item in anti_goals:
        rows.append(matrix_row(
            "binding_anti_goal", item["id"], item["title"], "ARCHITECTURAL_PROHIBITIONS",
            "binding", item["prohibition"], "governance/ARCHITECTURAL_PROHIBITIONS.json",
            ANTI_GOAL_FEATURES[item["id"]],
        ))
    for item in hard_gates:
        rows.append(matrix_row(
            "readiness_hard_gate", item["id"], item["name"], "READINESS_HARD_GATES",
            "binding", f"Required result: {item['result']}", "governance/READINESS_HARD_GATES.yaml",
            HARD_GATE_FEATURES[item["id"]],
        ))

    fieldnames = list(rows[0])
    with (output_dir / "REQUIREMENT_COVERAGE_MATRIX.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["record_type"]] = counts.get(row["record_type"], 0) + 1
    return {
        "row_count": len(rows),
        "counts_by_record_type": counts,
        "applicable_rows": sum(row["applicability"] == "applicable" for row in rows),
        "classified_verdict_rows": sum(bool(row["verdict"]) for row in rows),
        "unclassified_due_to_missing_taxonomy": sum(row["verdict_blocker"] == VERDICT_BLOCKER for row in rows),
        "verdict_blocker": VERDICT_BLOCKER,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prd-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    args = parser.parse_args()
    prd_root = args.prd_root.resolve()
    source_root = args.source_root.resolve()
    output_dir = Path(__file__).resolve().parent
    if not (source_root / "src/cmf_harness_spec_builder").is_dir():
        raise SystemExit(f"Brownfield source root is unavailable: {source_root}")

    evidence = {
        "generator": str(Path(__file__).resolve()),
        "prd_root": str(prd_root),
        "prd_package_inventory": write_prd_package_inventory(prd_root, output_dir),
        "repository_inventory": write_repository_inventory(source_root, output_dir),
        "requirement_matrix": write_requirement_matrix(prd_root, output_dir),
    }
    (output_dir / "STAGE1_EVIDENCE_SUMMARY.json").write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(evidence, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
