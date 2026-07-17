from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import re
from typing import Mapping


PACKAGE_SCHEMA_VERSION = "cmf-builder-portable-skill-package/v1"
RECEIPT_SCHEMA_VERSION = "cmf-builder-portable-skill-package-receipt/v1"
SKILL_ID = "activative_intelligence_pack_compiler"
SKILL_VERSION = "1.0.0"
AUTHORITY_LANE = "Analyst"
MATURITY = "development_uncertified"
MATURITY_CEILING = "development_validated"

REQUIRED_MEMBER_PATHS = (
    "SKILL.md",
    "compatibility.json",
    "contracts/input.schema.json",
    "contracts/output.schema.json",
    "execution/execution-instructions.md",
    "execution/system-instructions.md",
    "references/authority-boundaries.md",
    "references/behavioral-anchors.md",
    "references/context-requirements.md",
    "references/failure-taxonomy.md",
    "references/observability.md",
    "references/wrong-reading-locks.md",
)

MANIFEST_PATH = "manifest.json"
RECEIPT_PATH = "PACKAGE_RECEIPT.json"

_WINDOWS_ABSOLUTE = re.compile(r"(?i)(?:^|[\s\"'=])(?:[a-z]:[\\/])")
_POSIX_ABSOLUTE = re.compile(
    r"(?:^|[\s\"'=])/(?:Users|home|var|tmp|etc|opt|srv|mnt|workspace|root)/"
)
_UNSUPPORTED_TRUE_CLAIM = re.compile(
    r"(?i)\b(?:production_ready|production_eligible|production_certified|certified)"
    r"\s*[:=]\s*(?:true|yes|1)\b"
)
_UNSUPPORTED_MATURITY = re.compile(
    r"(?i)\b(?:maturity|status)\s*[:=]\s*(?:shadow_ready|certified|stable|production)\b"
)
_PROVIDER_REFERENCE = re.compile(
    r"(?i)\b(?:openai|anthropic|claude|gemini|vertex[ -]?ai|bedrock|gpt-[0-9])\b"
)


class PortablePackageErrorCode(str, Enum):
    INVALID_MANIFEST = "INVALID_MANIFEST"
    MISSING_MEMBER = "MISSING_MEMBER"
    ALTERED_MEMBER = "ALTERED_MEMBER"
    UNSAFE_PATH = "UNSAFE_PATH"
    UNSUPPORTED_CLAIM = "UNSUPPORTED_CLAIM"
    PROVIDER_COUPLING = "PROVIDER_COUPLING"
    RECEIPT_MISMATCH = "RECEIPT_MISMATCH"
    NON_CANONICAL = "NON_CANONICAL"


class PortablePackageError(ValueError):
    def __init__(
        self,
        code: PortablePackageErrorCode,
        message: str,
        *,
        member_path: str | None = None,
        context: Mapping[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.member_path = member_path
        self.context = dict(context or {})


@dataclass(frozen=True, slots=True)
class PackageMember:
    path: str
    sha256: str
    size_bytes: int

    def canonical_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
        }


@dataclass(frozen=True, slots=True)
class PackageReceipt:
    receipt_id: str
    skill_id: str
    version: str
    manifest_hash: str
    package_hash: str
    member_set_hash: str
    member_count: int
    maturity: str
    maturity_ceiling: str
    production_eligible: bool
    certified: bool
    outcome: str
    receipt_hash: str

    def identity_payload(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "skill_id": self.skill_id,
            "version": self.version,
            "manifest_hash": self.manifest_hash,
            "package_hash": self.package_hash,
            "member_set_hash": self.member_set_hash,
            "member_count": self.member_count,
            "maturity": self.maturity,
            "maturity_ceiling": self.maturity_ceiling,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
            "outcome": self.outcome,
        }


@dataclass(frozen=True, slots=True)
class PortableSkillPackage:
    root: Path
    skill_id: str
    version: str
    authority_lane: str
    maturity: str
    maturity_ceiling: str
    members: tuple[PackageMember, ...]
    member_set_hash: str
    manifest_bytes: bytes
    manifest_hash: str
    package_hash: str
    receipt: PackageReceipt

    @classmethod
    def load(cls, package_root: Path) -> "PortableSkillPackage":
        root = package_root.resolve()
        manifest_path = root / MANIFEST_PATH
        receipt_path = root / RECEIPT_PATH
        if not manifest_path.is_file():
            raise PortablePackageError(
                PortablePackageErrorCode.MISSING_MEMBER,
                "Portable package manifest is missing.",
                member_path=MANIFEST_PATH,
            )
        if not receipt_path.is_file():
            raise PortablePackageError(
                PortablePackageErrorCode.MISSING_MEMBER,
                "Portable package receipt is missing.",
                member_path=RECEIPT_PATH,
            )
        manifest_bytes = manifest_path.read_bytes()
        manifest = _load_canonical_json(manifest_bytes, MANIFEST_PATH)
        _validate_manifest_contract(manifest)
        manifest_members = _parse_members(manifest["members"])
        _verify_member_set(root, manifest_members)
        observed_members = tuple(
            _read_member(root, expected) for expected in manifest_members
        )
        member_set_hash = _member_set_hash(observed_members)
        if manifest["member_set_hash"] != member_set_hash:
            raise PortablePackageError(
                PortablePackageErrorCode.ALTERED_MEMBER,
                "Member-set hash does not match the immutable package contents.",
                member_path=MANIFEST_PATH,
            )
        manifest_hash = f"sha256:{sha256(manifest_bytes).hexdigest()}"
        package_hash = _package_hash(manifest_hash, observed_members)
        receipt_bytes = receipt_path.read_bytes()
        receipt_data = _load_canonical_json(receipt_bytes, RECEIPT_PATH)
        receipt = _parse_and_verify_receipt(
            receipt_data,
            manifest_hash=manifest_hash,
            package_hash=package_hash,
            member_set_hash=member_set_hash,
            member_count=len(observed_members),
        )
        result = cls(
            root=root,
            skill_id=str(manifest["skill_id"]),
            version=str(manifest["version"]),
            authority_lane=str(manifest["authority_lane"]),
            maturity=str(manifest["maturity"]),
            maturity_ceiling=str(manifest["maturity_ceiling"]),
            members=observed_members,
            member_set_hash=member_set_hash,
            manifest_bytes=manifest_bytes,
            manifest_hash=manifest_hash,
            package_hash=package_hash,
            receipt=receipt,
        )
        result.verify()
        return result

    def verify(self) -> None:
        if (
            self.skill_id != SKILL_ID
            or self.version != SKILL_VERSION
            or self.authority_lane != AUTHORITY_LANE
            or self.maturity != MATURITY
            or self.maturity_ceiling != MATURITY_CEILING
            or self.receipt.skill_id != self.skill_id
            or self.receipt.version != self.version
            or self.receipt.outcome != "PASS"
            or self.receipt.production_eligible
            or self.receipt.certified
        ):
            raise PortablePackageError(
                PortablePackageErrorCode.UNSUPPORTED_CLAIM,
                "Portable package identity, authority, or maturity boundary is invalid.",
            )

    def member(self, relative_path: str) -> bytes:
        for item in self.members:
            if item.path == relative_path:
                return (self.root / PurePosixPath(relative_path)).read_bytes()
        raise KeyError(relative_path)


def validate_portable_member(relative_path: str, content: bytes) -> None:
    """Validate one prospective package member before immutable assembly."""
    _validate_relative_path(relative_path)
    _validate_portable_content(relative_path, content)


def _load_canonical_json(content: bytes, member_path: str) -> dict[str, object]:
    try:
        decoded = content.decode("utf-8")
        value = json.loads(decoded)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PortablePackageError(
            PortablePackageErrorCode.INVALID_MANIFEST,
            "Package metadata must be valid UTF-8 JSON.",
            member_path=member_path,
        ) from error
    if not isinstance(value, dict):
        raise PortablePackageError(
            PortablePackageErrorCode.INVALID_MANIFEST,
            "Package metadata root must be a JSON object.",
            member_path=member_path,
        )
    if content != _canonical_json(value):
        raise PortablePackageError(
            PortablePackageErrorCode.NON_CANONICAL,
            "Package metadata bytes are not canonical.",
            member_path=member_path,
        )
    return value


def _validate_manifest_contract(manifest: Mapping[str, object]) -> None:
    expected_fields = {
        "schema_version",
        "skill_id",
        "version",
        "authority_lane",
        "maturity",
        "maturity_ceiling",
        "production_eligible",
        "certified",
        "provider_neutral",
        "capability_id",
        "entrypoint",
        "input_contract",
        "output_contract",
        "compatibility",
        "evaluation_assets",
        "members",
        "member_set_hash",
    }
    if set(manifest) != expected_fields:
        raise PortablePackageError(
            PortablePackageErrorCode.INVALID_MANIFEST,
            "Manifest fields do not match the frozen package contract.",
            member_path=MANIFEST_PATH,
        )
    if (
        manifest["schema_version"] != PACKAGE_SCHEMA_VERSION
        or manifest["skill_id"] != SKILL_ID
        or manifest["version"] != SKILL_VERSION
        or manifest["authority_lane"] != AUTHORITY_LANE
        or manifest["maturity"] != MATURITY
        or manifest["maturity_ceiling"] != MATURITY_CEILING
        or manifest["production_eligible"] is not False
        or manifest["certified"] is not False
        or manifest["provider_neutral"] is not True
        or manifest["capability_id"] != "compile_activative_intelligence_pack"
        or manifest["entrypoint"] != "SKILL.md"
        or manifest["input_contract"] != "contracts/input.schema.json"
        or manifest["output_contract"] != "contracts/output.schema.json"
    ):
        raise PortablePackageError(
            PortablePackageErrorCode.UNSUPPORTED_CLAIM,
            "Manifest identity or readiness declaration exceeds the authorized scope.",
            member_path=MANIFEST_PATH,
        )
    compatibility = manifest["compatibility"]
    if not isinstance(compatibility, dict) or compatibility != {
        "builder_prd": "1.2",
        "constitution": "1.1.0",
        "external_provider": None,
        "package_contract": "1.0.0",
    }:
        raise PortablePackageError(
            PortablePackageErrorCode.INVALID_MANIFEST,
            "Compatibility declaration is incomplete or provider-coupled.",
            member_path=MANIFEST_PATH,
        )
    evaluation_assets = manifest["evaluation_assets"]
    expected_evaluation_paths = {
        "corpus_manifest": "evaluation/skills/activative_intelligence_pack_compiler/CORPUS_MANIFEST.yaml",
        "rubric": "evaluation/skills/activative_intelligence_pack_compiler/RUBRIC.yaml",
        "evaluator": "evaluation/skills/activative_intelligence_pack_compiler/evaluator.py",
    }
    if not isinstance(evaluation_assets, dict) or set(evaluation_assets) != set(expected_evaluation_paths):
        raise PortablePackageError(
            PortablePackageErrorCode.INVALID_MANIFEST,
            "The development evaluation asset set is incomplete.",
            member_path=MANIFEST_PATH,
        )
    for name, expected_path in expected_evaluation_paths.items():
        asset = evaluation_assets[name]
        if (
            not isinstance(asset, dict)
            or set(asset) != {"path", "sha256"}
            or asset.get("path") != expected_path
            or not _is_sha256(asset.get("sha256"))
        ):
            raise PortablePackageError(
                PortablePackageErrorCode.INVALID_MANIFEST,
                "A development evaluation asset is not exactly path/hash pinned.",
                member_path=MANIFEST_PATH,
            )
    member_set_hash = manifest["member_set_hash"]
    if not _is_sha256(member_set_hash):
        raise PortablePackageError(
            PortablePackageErrorCode.INVALID_MANIFEST,
            "Manifest member-set hash is invalid.",
            member_path=MANIFEST_PATH,
        )


def _parse_members(value: object) -> tuple[PackageMember, ...]:
    if not isinstance(value, list):
        raise PortablePackageError(
            PortablePackageErrorCode.INVALID_MANIFEST,
            "Manifest members must be a list.",
            member_path=MANIFEST_PATH,
        )
    members: list[PackageMember] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict) or set(item) != {"path", "sha256", "size_bytes"}:
            raise PortablePackageError(
                PortablePackageErrorCode.INVALID_MANIFEST,
                "Manifest member entry is invalid.",
                member_path=f"members[{index}]",
            )
        path = item["path"]
        digest = item["sha256"]
        size = item["size_bytes"]
        if not isinstance(path, str):
            raise PortablePackageError(
                PortablePackageErrorCode.INVALID_MANIFEST,
                "Manifest member path must be a string.",
                member_path=f"members[{index}].path",
            )
        _validate_relative_path(path)
        if not _is_sha256(digest) or not isinstance(size, int) or isinstance(size, bool) or size < 1:
            raise PortablePackageError(
                PortablePackageErrorCode.INVALID_MANIFEST,
                "Manifest member hash or size is invalid.",
                member_path=path,
            )
        members.append(PackageMember(path=path, sha256=str(digest), size_bytes=size))
    result = tuple(members)
    if tuple(item.path for item in result) != REQUIRED_MEMBER_PATHS:
        raise PortablePackageError(
            PortablePackageErrorCode.MISSING_MEMBER,
            "Manifest does not contain the exact required canonical member set.",
            member_path=MANIFEST_PATH,
        )
    return result


def _verify_member_set(root: Path, expected: tuple[PackageMember, ...]) -> None:
    observed = tuple(
        sorted(
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file() and path.name not in {MANIFEST_PATH, RECEIPT_PATH}
        )
    )
    expected_paths = tuple(item.path for item in expected)
    if observed != expected_paths:
        missing = sorted(set(expected_paths) - set(observed))
        unexpected = sorted(set(observed) - set(expected_paths))
        raise PortablePackageError(
            PortablePackageErrorCode.MISSING_MEMBER,
            "On-disk package members differ from the immutable manifest.",
            context={"missing": missing, "unexpected": unexpected},
        )


def _read_member(root: Path, expected: PackageMember) -> PackageMember:
    path = root / PurePosixPath(expected.path)
    if not path.is_file():
        raise PortablePackageError(
            PortablePackageErrorCode.MISSING_MEMBER,
            "Required package member is missing.",
            member_path=expected.path,
        )
    content = path.read_bytes()
    observed = PackageMember(
        path=expected.path,
        sha256=f"sha256:{sha256(content).hexdigest()}",
        size_bytes=len(content),
    )
    if observed != expected:
        raise PortablePackageError(
            PortablePackageErrorCode.ALTERED_MEMBER,
            "Package member bytes do not match the immutable manifest.",
            member_path=expected.path,
            context={"expected": expected.canonical_dict(), "observed": observed.canonical_dict()},
        )
    _validate_portable_content(expected.path, content)
    return observed


def _validate_relative_path(value: str) -> None:
    path = PurePosixPath(value)
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or ":" in value
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.as_posix() != value
    ):
        raise PortablePackageError(
            PortablePackageErrorCode.UNSAFE_PATH,
            "Package member paths must be canonical relative POSIX paths.",
            member_path=value,
        )


def _validate_portable_content(member_path: str, content: bytes) -> None:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PortablePackageError(
            PortablePackageErrorCode.NON_CANONICAL,
            "Portable package members must be UTF-8 text.",
            member_path=member_path,
        ) from error
    if _WINDOWS_ABSOLUTE.search(text) or _POSIX_ABSOLUTE.search(text) or "file://" in text.lower():
        raise PortablePackageError(
            PortablePackageErrorCode.UNSAFE_PATH,
            "Portable package member contains an absolute local path.",
            member_path=member_path,
        )
    if _UNSUPPORTED_TRUE_CLAIM.search(text) or _UNSUPPORTED_MATURITY.search(text):
        raise PortablePackageError(
            PortablePackageErrorCode.UNSUPPORTED_CLAIM,
            "Portable package member contains an unsupported readiness claim.",
            member_path=member_path,
        )
    if _PROVIDER_REFERENCE.search(text):
        raise PortablePackageError(
            PortablePackageErrorCode.PROVIDER_COUPLING,
            "Portable package member names a model or provider implementation.",
            member_path=member_path,
        )


def _parse_and_verify_receipt(
    value: Mapping[str, object],
    *,
    manifest_hash: str,
    package_hash: str,
    member_set_hash: str,
    member_count: int,
) -> PackageReceipt:
    expected_fields = {
        "schema_version",
        "receipt_id",
        "skill_id",
        "version",
        "manifest_hash",
        "package_hash",
        "member_set_hash",
        "member_count",
        "maturity",
        "maturity_ceiling",
        "production_eligible",
        "certified",
        "outcome",
        "receipt_hash",
    }
    if set(value) != expected_fields or value.get("schema_version") != RECEIPT_SCHEMA_VERSION:
        raise PortablePackageError(
            PortablePackageErrorCode.RECEIPT_MISMATCH,
            "Package receipt fields do not match the frozen receipt contract.",
            member_path=RECEIPT_PATH,
        )
    receipt = PackageReceipt(
        receipt_id=str(value["receipt_id"]),
        skill_id=str(value["skill_id"]),
        version=str(value["version"]),
        manifest_hash=str(value["manifest_hash"]),
        package_hash=str(value["package_hash"]),
        member_set_hash=str(value["member_set_hash"]),
        member_count=int(value["member_count"]),
        maturity=str(value["maturity"]),
        maturity_ceiling=str(value["maturity_ceiling"]),
        production_eligible=value["production_eligible"] is True,
        certified=value["certified"] is True,
        outcome=str(value["outcome"]),
        receipt_hash=str(value["receipt_hash"]),
    )
    expected_id = f"portable-skill-package-receipt_{package_hash.removeprefix('sha256:')}"
    expected_receipt_hash = f"sha256:{sha256(_canonical_json(receipt.identity_payload())).hexdigest()}"
    if (
        receipt.receipt_id != expected_id
        or receipt.skill_id != SKILL_ID
        or receipt.version != SKILL_VERSION
        or receipt.manifest_hash != manifest_hash
        or receipt.package_hash != package_hash
        or receipt.member_set_hash != member_set_hash
        or receipt.member_count != member_count
        or receipt.maturity != MATURITY
        or receipt.maturity_ceiling != MATURITY_CEILING
        or receipt.production_eligible
        or receipt.certified
        or receipt.outcome != "PASS"
        or receipt.receipt_hash != expected_receipt_hash
    ):
        raise PortablePackageError(
            PortablePackageErrorCode.RECEIPT_MISMATCH,
            "Package receipt does not bind the exact immutable package.",
            member_path=RECEIPT_PATH,
        )
    return receipt


def _member_set_hash(members: tuple[PackageMember, ...]) -> str:
    return f"sha256:{sha256(_canonical_json([item.canonical_dict() for item in members])).hexdigest()}"


def _package_hash(manifest_hash: str, members: tuple[PackageMember, ...]) -> str:
    payload = {
        "manifest_hash": manifest_hash,
        "members": [item.canonical_dict() for item in members],
    }
    return f"sha256:{sha256(_canonical_json(payload)).hexdigest()}"


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 71
        and value.startswith("sha256:")
        and all(char in "0123456789abcdef" for char in value[7:])
    )


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
