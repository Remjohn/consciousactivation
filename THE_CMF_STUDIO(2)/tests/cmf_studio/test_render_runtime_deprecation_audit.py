from pathlib import Path


def test_render_runtime_deprecation_report_records_migration_without_deletion():
    report = Path("docs/architecture/render-runtime-deprecation/RENDER_RUNTIME_DEPRECATION_AUDIT.md")
    migration = Path("docs/architecture/render-runtime-deprecation/RENDER_RUNTIME_MIGRATION_REPORT.md")

    assert report.exists()
    assert migration.exists()

    report_text = report.read_text(encoding="utf-8")
    migration_text = migration.read_text(encoding="utf-8")

    assert "Remotion Node.js + `@remotion/skia`" in report_text
    assert "No fields, validators, route behavior, or service behavior were changed." in report_text
    assert "Do not delete legacy contracts until these pass" in migration_text
    assert "Local Render Worker owns queue, lease, heartbeat, and result lifecycle." in migration_text


def test_legacy_skia_runtime_contracts_are_marked_deprecated():
    contracts = Path("src/ccp_studio/contracts/asset_program_compilers.py").read_text(encoding="utf-8")

    assert "LEGACY_SKIA_RUNTIME_DEPRECATION_NOTE" in contracts
    assert "Deprecated legacy queue contract" in contracts
    assert "Deprecated Skia sidecar-era binding" in contracts
    assert "Remotion Node.js + @remotion/skia" in contracts


def test_no_active_python_skia_sidecar_imports_or_shell_sidecar_calls():
    source_files = [
        path
        for path in Path("src/ccp_studio").rglob("*.py")
        if "__pycache__" not in path.parts
    ]
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in source_files)

    assert "import skia" not in combined
    assert "from skia" not in combined
    assert "skia-python" not in combined
    assert "src/ccp/sidecars/skia-renderer" not in combined
    assert "shell=true" not in combined
