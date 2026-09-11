from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..domain.validation import require_string, require_string_list, semantic_identity
from ..workflow.infrastructure.repository import PipelineRepository


class BindingInvalidationProjector:
    def __init__(self, repository: PipelineRepository):
        self.repository = repository

    def plan(self, root_id: str, reason: str, *, idempotency_key: str) -> dict[str, Any]:
        root = require_string(root_id, "root_id")
        reason = require_string(reason, "reason")
        descendants = self.repository.descendants([root])
        core = {
            "root_id": root,
            "reason": reason,
            "affected_descendants": descendants,
            "historical_objects_preserved": True,
            "global_invalidation": False,
        }
        plan = {"plan_id": semantic_identity("binding-invalidation", core), **core}
        return self.repository.store_object(
            "binding_invalidation_plan",
            plan,
            idempotency_key=idempotency_key,
            object_id=plan["plan_id"],
            lifecycle_state="PROPOSED",
        )
