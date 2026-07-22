"""Revision repositories for TS-CMF-040."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.revision import (
    FinalApprovalBinding,
    ReconstructionAuditView,
    RevisionChain,
    RevisionReceipt,
    RevisionRequest,
    RevisionVersion,
)


@dataclass
class InMemoryRevisionRepository:
    revision_requests: dict[UUID, RevisionRequest] = field(default_factory=dict)
    revision_versions: dict[UUID, RevisionVersion] = field(default_factory=dict)
    revision_chains: dict[UUID, RevisionChain] = field(default_factory=dict)
    approval_bindings: dict[UUID, FinalApprovalBinding] = field(default_factory=dict)
    audit_views: dict[UUID, ReconstructionAuditView] = field(default_factory=dict)
    receipts: dict[UUID, RevisionReceipt] = field(default_factory=dict)

    def put_revision_request(self, request: RevisionRequest) -> RevisionRequest:
        self.revision_requests[request.revision_request_id] = request
        return request

    def put_revision_version(self, version: RevisionVersion) -> RevisionVersion:
        self.revision_versions[version.revision_version_id] = version
        return version

    def put_revision_chain(self, chain: RevisionChain) -> RevisionChain:
        self.revision_chains[chain.revision_chain_id] = chain
        return chain

    def put_approval_binding(self, binding: FinalApprovalBinding) -> FinalApprovalBinding:
        self.approval_bindings[binding.final_approval_binding_id] = binding
        return binding

    def put_audit_view(self, view: ReconstructionAuditView) -> ReconstructionAuditView:
        self.audit_views[view.complete_editing_session_id] = view
        return view

    def put_receipt(self, receipt: RevisionReceipt) -> RevisionReceipt:
        self.receipts[receipt.revision_receipt_id] = receipt
        return receipt
