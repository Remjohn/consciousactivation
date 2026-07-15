from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from cmf_builder.domain.atomicity import (
    BoundaryInputHashMismatch,
    BoundaryInputInvalid,
    DeclaredBoundaryInput,
)


class FileDeclaredBoundaryRepository:
    """Read one hash-pinned repository-local declared boundary; never execute it."""

    def __init__(self, repository_root: Path) -> None:
        self._root = repository_root.resolve()

    def load(
        self, relative_path: str, expected_sha256: str
    ) -> DeclaredBoundaryInput:
        relative = Path(*relative_path.replace("\\", "/").split("/"))
        if relative.is_absolute() or ".." in relative.parts:
            raise BoundaryInputInvalid(
                "Declared boundary path must be repository-relative.",
                path=relative_path,
            )
        path = (self._root / relative).resolve()
        if self._root != path and self._root not in path.parents:
            raise BoundaryInputInvalid(
                "Declared boundary path escapes the repository root.",
                path=relative_path,
            )
        try:
            content = path.read_bytes()
        except OSError as error:
            raise BoundaryInputInvalid(
                "Declared boundary input is unavailable.", path=relative_path
            ) from error
        observed = sha256(content).hexdigest()
        if observed != expected_sha256:
            raise BoundaryInputHashMismatch(
                "Declared boundary bytes do not match the capsule hash.",
                path=relative_path,
                expected_sha256=expected_sha256,
                observed_sha256=observed,
            )
        return DeclaredBoundaryInput.from_json_bytes(
            content, observed_sha256=expected_sha256
        )
