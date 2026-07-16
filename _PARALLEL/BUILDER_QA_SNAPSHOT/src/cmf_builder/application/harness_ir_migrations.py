from __future__ import annotations

from dataclasses import dataclass

from cmf_builder.domain.harness_ir import HARNESS_IR_SCHEMA_VERSION


class MissingHarnessIRMigration(Exception):
    code = "MissingHarnessIRMigration"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class HarnessIRVersionRegistry:
    write_version: str
    readable_versions: tuple[str, ...]
    migrations: tuple[str, ...]

    @classmethod
    def initial(cls) -> "HarnessIRVersionRegistry":
        return cls(
            write_version=HARNESS_IR_SCHEMA_VERSION,
            readable_versions=(HARNESS_IR_SCHEMA_VERSION,),
            migrations=(),
        )

    def require_readable(self, version: str) -> None:
        if version not in self.readable_versions:
            raise MissingHarnessIRMigration(
                "Harness IR version is not readable without an explicit migration.",
                version=version,
                readable_versions=self.readable_versions,
            )

    def require_migration(self, from_version: str, to_version: str) -> str:
        identity = f"{from_version}->{to_version}"
        if identity not in self.migrations:
            raise MissingHarnessIRMigration(
                "No explicit Harness IR migration and receipt are registered.",
                from_version=from_version,
                to_version=to_version,
            )
        return identity
