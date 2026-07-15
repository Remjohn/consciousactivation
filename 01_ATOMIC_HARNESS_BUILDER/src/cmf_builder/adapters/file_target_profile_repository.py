from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import re

from cmf_builder.domain.target_profile import (
    AUTHORIZED_CANONICAL_PATH,
    AUTHORIZED_CATEGORY_ID,
    AUTHORIZED_PROFILE_ID,
    AUTHORIZED_TARGET_ID,
    GOVERNED_TARGET_IDS,
    RegistryIntegrityError,
    TargetProfile,
    UnsupportedTargetForAuthorizedSlice,
    validate_single_target,
)


class FileTargetProfileRepository:
    TARGET_REGISTRY = Path("governance/COMPILATION_TARGET_REGISTRY.yaml")
    COMPATIBILITY_REGISTRY = Path(
        "contracts/integration/CATEGORY_PROFILE_COMPATIBILITY.yaml"
    )
    TARGET_REGISTRY_SHA256 = (
        "0e9c82b6f87a9b7f5dff317578c0da18241fbfd66e29cc2226e161399d4da2ca"
    )
    COMPATIBILITY_REGISTRY_SHA256 = (
        "781a438ef1298c1bc71da6ab54298774f09c0be97becf513510913f98fc97a71"
    )

    def __init__(self, repository_root: Path) -> None:
        self._root = repository_root.resolve()

    def recognized_target_ids(self) -> frozenset[str]:
        text = self._read_verified(
            self.TARGET_REGISTRY, self.TARGET_REGISTRY_SHA256
        ).decode("utf-8-sig")
        observed = frozenset(
            match.group(1)
            for match in re.finditer(r"(?m)^\s*-\s*target_id:\s*([^\s#]+)\s*$", text)
        )
        if observed != GOVERNED_TARGET_IDS:
            raise RegistryIntegrityError(
                "Compilation target registry identities do not match the governed set.",
                expected_target_ids=tuple(sorted(GOVERNED_TARGET_IDS)),
                observed_target_ids=tuple(sorted(observed)),
            )
        return observed

    def load_authorized_profile(self) -> TargetProfile:
        self.recognized_target_ids()
        text = self._read_verified(
            self.COMPATIBILITY_REGISTRY, self.COMPATIBILITY_REGISTRY_SHA256
        ).decode("utf-8-sig")
        block_match = re.search(
            rf"(?ms)^\s{{2}}- profile_id:\s*{re.escape(AUTHORIZED_PROFILE_ID)}\s*$"
            r"(?P<body>.*?)(?=^\s{2}- profile_id:|\Z)",
            text,
        )
        if block_match is None:
            raise RegistryIntegrityError(
                "Authorized Format 02 profile is absent from compatibility registry."
            )
        block = block_match.group("body")
        category_id = self._field(block, "category_id")
        canonical_path = self._field(block, "canonical_path")
        compatibility_state = self._field(block, "strongest_current_state")
        production_certified = bool(
            re.search(r"production_certified:\s*true", block, flags=re.IGNORECASE)
        )
        if (
            category_id != AUTHORIZED_CATEGORY_ID
            or canonical_path != AUTHORIZED_CANONICAL_PATH
            or compatibility_state != "contract_compatible"
            or production_certified
        ):
            raise RegistryIntegrityError(
                "Format 02 compatibility fields do not match the bounded capsule.",
                category_id=category_id,
                canonical_path=canonical_path,
                compatibility_state=compatibility_state,
                production_certified=production_certified,
            )
        return TargetProfile(
            target_id=AUTHORIZED_TARGET_ID,
            category_id=category_id,
            profile_id=AUTHORIZED_PROFILE_ID,
            canonical_path=canonical_path,
            version=f"sha256:{self.COMPATIBILITY_REGISTRY_SHA256}",
            compiler_id="run-governance/format02/v1",
            compatibility_state=compatibility_state,
            production_certified=False,
            required_work=(
                "configure_evidence_workspace",
                "lock_target_specific_evidence",
            ),
            lifecycle_edges=(("CREATED", "SOURCE_DIAGNOSTIC"),),
            transition_prerequisites=(
                ("SOURCE_DIAGNOSTIC", ("target_profile_selected",)),
            ),
        )

    def resolve(
        self,
        target_ids: tuple[str, ...],
        category_id: str,
        profile_id: str,
    ) -> TargetProfile:
        target_id = validate_single_target(target_ids)
        self.recognized_target_ids()
        if (
            target_id != AUTHORIZED_TARGET_ID
            or category_id != AUTHORIZED_CATEGORY_ID
            or profile_id != AUTHORIZED_PROFILE_ID
        ):
            raise UnsupportedTargetForAuthorizedSlice(
                "The selected target/category/profile is structural or outside the bounded Format 02 slice.",
                target_id=target_id,
                category_id=category_id,
                profile_id=profile_id,
            )
        return self.load_authorized_profile()

    def _read_verified(self, relative: Path, expected_sha256: str) -> bytes:
        path = (self._root / relative).resolve()
        if self._root not in path.parents:
            raise RegistryIntegrityError("Registry path escapes repository root.")
        content = path.read_bytes()
        observed = sha256(content).hexdigest()
        if observed != expected_sha256:
            raise RegistryIntegrityError(
                "Governed registry hash does not match the Development Capsule.",
                path=relative.as_posix(),
                expected_sha256=expected_sha256,
                observed_sha256=observed,
            )
        return content

    @staticmethod
    def _field(block: str, field: str) -> str:
        match = re.search(rf"(?m)^\s+{re.escape(field)}:\s*([^\s#]+)\s*$", block)
        if match is None:
            raise RegistryIntegrityError(
                "Required compatibility field is absent.", field=field
            )
        return match.group(1)
