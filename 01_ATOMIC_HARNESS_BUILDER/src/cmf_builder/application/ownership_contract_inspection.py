"""Ownership, module, and contract inspection for OD-AM-004 / ST-10.06."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any


def sha256_of(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


class OwnershipInspectionError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class OwnershipObjectClass(str, Enum):
    PRODUCT = "PRODUCT"
    MODULE = "MODULE"
    PORT = "PORT"
    ADAPTER = "ADAPTER"
    DOMAIN_CONTRACT = "DOMAIN_CONTRACT"
    APPLICATION_CONTRACT = "APPLICATION_CONTRACT"
    EXTERNAL_CONTRACT = "EXTERNAL_CONTRACT"
    SHARED_CONTRACT = "SHARED_CONTRACT"
    STORY = "STORY"
    OBLIGATION = "OBLIGATION"
    AUTHORITY_OWNER = "AUTHORITY_OWNER"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise OwnershipInspectionError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class OwnershipRecord:
    identity: str
    object_class: OwnershipObjectClass
    owning_product: str
    owning_module: str
    responsibility: str
    allowed_dependencies: tuple[str, ...]
    prohibited_dependencies: tuple[str, ...]
    inbound_ports: tuple[str, ...]
    outbound_ports: tuple[str, ...]
    adapters: tuple[str, ...]
    contract_version: str
    compatibility: str
    implementation_paths: tuple[str, ...]
    story_ownership: str
    obligation_ownership: str
    external_ownership: str
    authority_basis: str
    source_evidence: tuple[str, ...]
    validity: str
    supersession: str
    limitations: tuple[str, ...]
    primary_obligation_owner: bool = False
    claims_human_authority: bool = False

    def __post_init__(self) -> None:
        for value, name in (
            (self.identity, "identity"), (self.owning_product, "owning_product"), (self.owning_module, "owning_module"),
            (self.responsibility, "responsibility"), (self.contract_version, "contract_version"), (self.compatibility, "compatibility"),
            (self.story_ownership, "story_ownership"), (self.obligation_ownership, "obligation_ownership"),
            (self.external_ownership, "external_ownership"), (self.authority_basis, "authority_basis"), (self.validity, "validity"),
        ):
            _text(value, name)
        if self.owning_product == "Atomic Harness Builder" and self.external_ownership in {"VAE", "Delegation"}:
            raise OwnershipInspectionError("EXTERNAL_PRODUCT_OWNERSHIP_CLAIMED_BY_BUILDER", "Builder cannot own external product behavior")
        if self.object_class is OwnershipObjectClass.ADAPTER and self.claims_human_authority:
            raise OwnershipInspectionError("ADAPTER_PRESENTED_AS_AUTHORITY", "adapters cannot be domain or human authority")

    def as_dict(self) -> dict[str, Any]:
        return {
            "identity": self.identity,
            "object_class": self.object_class.value,
            "owning_product": self.owning_product,
            "owning_module": self.owning_module,
            "responsibility": self.responsibility,
            "allowed_dependencies": list(self.allowed_dependencies),
            "prohibited_dependencies": list(self.prohibited_dependencies),
            "inbound_ports": list(self.inbound_ports),
            "outbound_ports": list(self.outbound_ports),
            "adapters": list(self.adapters),
            "contract_version": self.contract_version,
            "compatibility": self.compatibility,
            "implementation_paths": list(self.implementation_paths),
            "story_ownership": self.story_ownership,
            "obligation_ownership": self.obligation_ownership,
            "external_ownership": self.external_ownership,
            "authority_basis": self.authority_basis,
            "source_evidence": list(self.source_evidence),
            "validity": self.validity,
            "supersession": self.supersession,
            "limitations": list(self.limitations),
            "primary_obligation_owner": self.primary_obligation_owner,
            "claims_human_authority": self.claims_human_authority,
        }

    @property
    def record_identity(self) -> str:
        return sha256_of(self.as_dict())


def validate_ownership_records(records: tuple[OwnershipRecord, ...], registered_sources: set[str]) -> None:
    primary: dict[str, str] = {}
    module_owners = {record.owning_module for record in records if record.object_class is OwnershipObjectClass.MODULE}
    for record in records:
        for path in record.implementation_paths:
            if path not in registered_sources:
                raise OwnershipInspectionError("SOURCE_OUTSIDE_GOVERNED_REGISTRY", "source path not registered", path=path)
        if record.object_class is OwnershipObjectClass.MODULE and not record.owning_product:
            raise OwnershipInspectionError("UNOWNED_MODULE", "module must have product owner")
        if record.primary_obligation_owner:
            previous = primary.setdefault(record.obligation_ownership, record.identity)
            if previous != record.identity:
                raise OwnershipInspectionError("DUPLICATE_PRIMARY_OBLIGATION_OWNER", "obligation has multiple primary owners")
        if record.owning_module and record.owning_module not in module_owners and record.object_class is not OwnershipObjectClass.MODULE:
            raise OwnershipInspectionError("UNOWNED_MODULE", "record references unowned module")
        if any(dep in record.prohibited_dependencies for dep in record.allowed_dependencies):
            raise OwnershipInspectionError("PROHIBITED_DEPENDENCY_ALLOWED", "dependency cannot be both allowed and prohibited")


def inspect_ownership(records: tuple[OwnershipRecord, ...], **filters: str) -> tuple[OwnershipRecord, ...]:
    supported = {"source_path", "module", "contract", "story", "obligation", "product", "port", "adapter", "external_boundary"}
    unknown = set(filters) - supported
    if unknown:
        raise OwnershipInspectionError("UNSUPPORTED_OWNERSHIP_FILTER", "unsupported filter", filters=sorted(unknown))
    result = []
    for record in records:
        if "source_path" in filters and filters["source_path"] not in record.implementation_paths:
            continue
        if "module" in filters and filters["module"] != record.owning_module:
            continue
        if "contract" in filters and filters["contract"] not in record.identity:
            continue
        if "story" in filters and filters["story"] != record.story_ownership:
            continue
        if "obligation" in filters and filters["obligation"] != record.obligation_ownership:
            continue
        if "product" in filters and filters["product"] != record.owning_product:
            continue
        if "port" in filters and filters["port"] not in record.inbound_ports + record.outbound_ports:
            continue
        if "adapter" in filters and filters["adapter"] not in record.adapters:
            continue
        if "external_boundary" in filters and filters["external_boundary"] != record.external_ownership:
            continue
        result.append(record)
    return tuple(sorted(result, key=lambda item: item.identity))
