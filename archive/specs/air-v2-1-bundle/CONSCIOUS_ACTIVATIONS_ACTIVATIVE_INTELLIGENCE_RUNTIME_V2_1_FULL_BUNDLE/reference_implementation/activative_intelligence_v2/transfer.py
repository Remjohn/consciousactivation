from __future__ import annotations

from dataclasses import dataclass

from .models import ActivationTransferContract


@dataclass(frozen=True, slots=True)
class TransferEvidence:
    source_meaning_fidelity: float
    edge_preservation: float
    role_preservation: float
    generator_preservation: float
    wrong_reading_control: float
    format_execution: float

    def score(self) -> float:
        weights = (0.22, 0.18, 0.18, 0.18, 0.14, 0.10)
        values = (
            self.source_meaning_fidelity,
            self.edge_preservation,
            self.role_preservation,
            self.generator_preservation,
            self.wrong_reading_control,
            self.format_execution,
        )
        return sum(v * w for v, w in zip(values, weights))


def validate_transfer_contract(contract: ActivationTransferContract) -> None:
    if not contract.original_activation_generator:
        raise ValueError("original activation generator is required")
    if not contract.must_remain_true:
        raise ValueError("must_remain_true invariants are required")
    overlap = set(contract.permitted_compression) & set(contract.prohibited_collapses)
    if overlap:
        raise ValueError(f"compression/collapse conflict: {sorted(overlap)}")
