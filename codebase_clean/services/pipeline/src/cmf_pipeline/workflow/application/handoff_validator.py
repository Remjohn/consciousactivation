from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from ...domain.errors import PipelineValidationError
from ...domain.validation import require_ref, require_string, require_string_list, semantic_identity


class HandoffValidator:
    def validate(
        self,
        handoff: Mapping[str, Any],
        *,
        producer_node: Mapping[str, Any],
        consumer_node: Mapping[str, Any],
    ) -> dict[str, Any]:
        required = {
            "producer_node_id",
            "consumer_node_id",
            "output_ref",
            "contract_id",
            "validation_receipt_refs",
            "authority_refs",
            "lifecycle_state",
        }
        if set(handoff) != required:
            raise PipelineValidationError("handoff contains unknown or missing fields")
        if handoff["producer_node_id"] != producer_node["node_id"]:
            raise PipelineValidationError("handoff producer mismatch")
        if handoff["consumer_node_id"] != consumer_node["node_id"]:
            raise PipelineValidationError("handoff consumer mismatch")
        contract = require_string(handoff["contract_id"], "contract_id")
        if contract not in producer_node["output_contracts"] or contract not in consumer_node["input_contracts"]:
            raise PipelineValidationError("handoff contract is not bilateral")
        if handoff["lifecycle_state"] != "ACCEPTED":
            raise PipelineValidationError("handoff lifecycle state must be ACCEPTED")
        core = {
            "producer_node_id": producer_node["node_id"],
            "consumer_node_id": consumer_node["node_id"],
            "output_ref": require_ref(handoff["output_ref"], "output_ref"),
            "contract_id": contract,
            "validation_receipt_refs": require_string_list(handoff["validation_receipt_refs"], "validation_receipt_refs", non_empty=True),
            "authority_refs": require_string_list(handoff["authority_refs"], "authority_refs", non_empty=True),
            "lifecycle_state": "ACCEPTED",
        }
        return {"handoff_id": semantic_identity("handoff", core), **core, "handoff_sha256": canonical_sha256(core)}
