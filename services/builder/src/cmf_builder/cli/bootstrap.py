from __future__ import annotations

from pathlib import Path
from typing import Sequence

from cmf_builder.adapters.sqlite_productization_repository import (
    SQLiteProductizationRepository,
)
from cmf_builder.application.export_service import (
    DeterministicPortableExportService,
    PortableAtomicHarnessCompiler,
)
from cmf_builder.application.productization_service import BuilderProductizationService
from cmf_builder.cli.commands import run_cli


def build_local_service(database_path: Path) -> BuilderProductizationService:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    repository = SQLiteProductizationRepository(database_path)
    return BuilderProductizationService(
        repository=repository,
        compiler=PortableAtomicHarnessCompiler(),
        exporter=DeterministicPortableExportService(repository),
    )


def local_main(
    argv: Sequence[str] | None = None,
    *,
    database_path: Path = Path(".cmf-builder/builder.sqlite3"),
) -> int:
    import sys

    return run_cli(
        build_local_service(database_path),
        tuple(sys.argv[1:] if argv is None else argv),
    )
