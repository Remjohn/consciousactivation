"""Interview Asset Contract repositories for TS-CMF-027."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.interview_contracts import (
    ContractCompilationReceipt,
    DeckSessionBinding,
    InterviewAssetContract,
    InterviewDeck,
)


@dataclass
class InMemoryInterviewContractRepository:
    contracts: dict[UUID, InterviewAssetContract] = field(default_factory=dict)
    decks: dict[UUID, InterviewDeck] = field(default_factory=dict)
    receipts: dict[UUID, ContractCompilationReceipt] = field(default_factory=dict)
    bindings: dict[UUID, DeckSessionBinding] = field(default_factory=dict)

    def put_contract(self, contract: InterviewAssetContract) -> InterviewAssetContract:
        self.contracts[contract.contract_id] = contract
        return contract

    def put_deck(self, deck: InterviewDeck) -> InterviewDeck:
        self.decks[deck.interview_deck_id] = deck
        return deck

    def put_receipt(self, receipt: ContractCompilationReceipt) -> ContractCompilationReceipt:
        self.receipts[receipt.contract_compilation_receipt_id] = receipt
        return receipt

    def put_binding(self, binding: DeckSessionBinding) -> DeckSessionBinding:
        self.bindings[binding.deck_session_binding_id] = binding
        return binding
