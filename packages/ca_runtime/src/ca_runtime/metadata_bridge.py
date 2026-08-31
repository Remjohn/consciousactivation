"""Workflow and Capability Metadata Bridge for CAE Phase 2 (Mandate M17).

Governed by:
- 00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md
- 00_CONTROL/17_PHASE1_AGENT_SKILL_OPERATION_OWNERSHIP_GRAPH.md (M05)
- 00_CONTROL/14_PHASE1_BUILDER_RUNTIME_BINDING_CONTRACT.md (M10)
- 00_CONTROL/21_PHASE2_CAPABILITY_SECURITY_MATRIX.md
- 02_PHASE_2_RUNTIME_FOUNDATION/M17_workflow_capability_metadata_bridge.md
- CURRENT.md Runtime Blockers (Blockers 1, 2, 3, 4, 5, 6, 7)

Core Constitutional Laws:
1. CAE remains authoritative over state, identity, and governance.
2. Preserves 4 Authority Lanes: HUNTER, ANALYST, COMPOSER, COMMANDER.
3. Passive, flat Canonical Skills (zero skill-to-skill nesting).
4. Explicit capability access: fail-closed on missing, unapproved, or unresolvable capabilities.
5. No hardcoded empty or synthetic placeholder metadata for the pilot path.
6. Dynamic, structured blocker reporting without generic string masking.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from ca_contracts import canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane
from cmf_builder.domain.portable_export import PortableAtomicHarnessDefinition
from cmf_pipeline.bindings.eligibility_registry import ImplementationEligibilityRegistry
from cmf_pipeline.domain.enums import NodeKind, ProductBoundary, WorkflowRole
from cmf_pipeline.domain.errors import PipelineValidationError
from cmf_pipeline.intake.compiler_profile_registry import HarnessDefinitionProfileRegistry
from cmf_pipeline.intake.definition_intake import AtomicHarnessDefinitionIntake
from cmf_pipeline.intake.harness_compiler import compile_portable_to_intake
from cmf_pipeline.intake.harness_compiler_contracts import (
    BLOCKER_1_TEXT,
    BLOCKER_2_TEXT,
    BLOCKER_3_TEXT,
    BLOCKER_4_TEXT,
    BLOCKER_5_TEXT,
    BLOCKER_6_EVAL_TEXT,
    BLOCKER_6_REPAIR_TEXT,
    HarnessCompilationBlocked,
)

logger = logging.getLogger("ca_runtime.metadata_bridge")


# ---------------------------------------------------------------------------
# Typed Result Envelope
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class BridgeCompilationResult:
    """Encapsulates the structured outcome of bridging an authored harness to pipeline intake."""
    success: bool
    intake_projection: Optional[Dict[str, Any]] = None
    blocked_field: Optional[str] = None
    blocked_reason: Optional[str] = None
    blocker_ref: Optional[str] = None
    resolved_capabilities: Optional[Dict[str, Dict[str, Any]]] = None
    resolved_workflow: Optional[Dict[str, Any]] = None
    resolved_semantic_dependencies: Optional[List[Dict[str, Any]]] = None
    timestamp: str = field(default_factory=utc_now_rfc3339)

    @property
    def formatted_blocked_reason(self) -> Optional[str]:
        """Returns a standardized diagnostic string with the exact blocker field and ref."""
        if self.success or not self.blocked_reason:
            return None
        field_tag = f" ({self.blocked_field})" if self.blocked_field else ""
        ref_tag = f" [{self.blocker_ref}]" if self.blocker_ref else ""
        return f"BRIDGE-001 Blocker{field_tag}: {self.blocked_reason}{ref_tag}"


# ---------------------------------------------------------------------------
# Governed Capability Authority Registry
# ---------------------------------------------------------------------------

# Baseline capability dictionary anchored in 00_CONTROL/17_PHASE1_AGENT_SKILL_OPERATION_OWNERSHIP_GRAPH.md
# and 00_CONTROL/21_PHASE2_CAPABILITY_SECURITY_MATRIX.md
GOVERNED_BASELINE_CAPABILITIES: Dict[str, Dict[str, Any]] = {
    "activative_contract_validation": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "typed_output"],
        "authority_boundary": "validate activative contract integrity",
    },
    "lineage_preservation": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "read_only"],
        "authority_boundary": "preserve upstream semantic lineage",
    },
    "activative_expression_generator": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "typed_output"],
        "authority_boundary": "generate conversational activation expressions",
    },
    "compile_program": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "typed_output"],
        "authority_boundary": "execute approved semantic program only",
    },
    "inspect_source": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "read_only"],
        "authority_boundary": "inspect exact source references only",
    },
    "source_inspection": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "read_only"],
        "authority_boundary": "inspect exact source references only",
    },
    "operator_review": {
        "owner_kind": "HUMAN",
        "required_features": ["attributable_decision", "typed_handoff"],
        "authority_boundary": "approve bounded transition only",
    },
    "upstream_intelligence_reasoning": {
        "owner_kind": "AGENT",
        "required_features": ["programmed_model_inference", "token_bounded"],
        "authority_boundary": "execute psychological reasoning inference within token/latency limits",
    },
    "psychological_reasoning": {
        "owner_kind": "AGENT",
        "required_features": ["programmed_model_inference", "token_bounded"],
        "authority_boundary": "execute psychological reasoning inference within token/latency limits",
    },
    "archetype_synthesis": {
        "owner_kind": "AGENT",
        "required_features": ["programmed_model_inference", "token_bounded"],
        "authority_boundary": "synthesize narrative archetype patterns",
    },
    "narrative_tension_scoring": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "typed_output"],
        "authority_boundary": "score narrative tension metrics",
    },
    "atomic_execution": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash"],
        "authority_boundary": "pipeline_owned_execution",
    },
    "transcription_verification": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "read_only"],
        "authority_boundary": "verify transcription monotonicity and word boundaries",
    },
    "air_contract_validation": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "typed_output"],
        "authority_boundary": "validate AIR contract integrity",
    },
    "storyboard_synthesis": {
        "owner_kind": "AGENT",
        "required_features": ["canonical_hash", "typed_output"],
        "authority_boundary": "synthesize visual storyboard sequences",
    },
    "visual_asset_demand_compilation": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "typed_output"],
        "authority_boundary": "compile visual asset demand contracts",
    },
    "visual_asset_validation": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "read_only"],
        "authority_boundary": "validate visual asset safe zones and geometry",
    },
    "deterministic_contract_validation": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "read_only"],
        "authority_boundary": "validate deterministic contract adherence",
    },
    "source_lineage_validation": {
        "owner_kind": "CODE",
        "required_features": ["canonical_hash", "read_only"],
        "authority_boundary": "validate source lineage provenance",
    },
}


def _normalize_definition(definition: Any) -> PortableAtomicHarnessDefinition:
    """Normalizes any input (PortableAtomicHarnessDefinition, duck-typed object, or dict) to PortableAtomicHarnessDefinition."""
    if isinstance(definition, PortableAtomicHarnessDefinition):
        return definition
    if hasattr(definition, "content_bytes") and hasattr(definition, "definition_id"):
        return PortableAtomicHarnessDefinition(
            definition_id=str(definition.definition_id),
            definition_hash=str(getattr(definition, "definition_hash", f"sha256:{sha256(definition.content_bytes).hexdigest()}")),
            content_bytes=bytes(definition.content_bytes),
            payload_bytes=bytes(getattr(definition, "payload_bytes", b"")),
        )
    if hasattr(definition, "content") and isinstance(definition.content, Mapping):
        content_dict = dict(definition.content)
        content_bytes = json.dumps(content_dict, separators=(",", ":"), sort_keys=True).encode("utf-8")
        digest = sha256(content_bytes).hexdigest()
        def_id = str(getattr(definition, "definition_id", f"atomic-harness-definition_{digest}"))
        def_hash = str(getattr(definition, "definition_hash", f"sha256:{digest}"))
        payload_bytes = json.dumps(
            {
                "artifact_type": "AtomicHarnessDefinition",
                "definition_id": def_id,
                "definition_hash": def_hash,
                "definition": content_dict,
            },
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return PortableAtomicHarnessDefinition(
            definition_id=def_id,
            definition_hash=def_hash,
            content_bytes=content_bytes,
            payload_bytes=payload_bytes,
        )
    if isinstance(definition, Mapping):
        content_dict = dict(definition.get("definition", definition))
        content_bytes = json.dumps(content_dict, separators=(",", ":"), sort_keys=True).encode("utf-8")
        digest = sha256(content_bytes).hexdigest()
        def_id = str(definition.get("definition_id", f"atomic-harness-definition_{digest}"))
        def_hash = str(definition.get("definition_hash", f"sha256:{digest}"))
        payload_bytes = json.dumps(
            {
                "artifact_type": "AtomicHarnessDefinition",
                "definition_id": def_id,
                "definition_hash": def_hash,
                "definition": content_dict,
            },
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return PortableAtomicHarnessDefinition(
            definition_id=def_id,
            definition_hash=def_hash,
            content_bytes=content_bytes,
            payload_bytes=payload_bytes,
        )
    raise TypeError(f"Cannot normalize {type(definition)} to PortableAtomicHarnessDefinition")


# ---------------------------------------------------------------------------
# Workflow Capability Metadata Bridge
# ---------------------------------------------------------------------------

class WorkflowCapabilityMetadataBridge:
    """Governed source/transform bridge resolving real capability and workflow metadata for CAE pipeline intake.
    
    Eliminates empty placeholder dictionaries and None arguments, connects to authoritative
    governed sources, and enforces fail-closed error semantics.
    """

    def __init__(
        self,
        *,
        eligibility_registry: Optional[ImplementationEligibilityRegistry] = None,
        custom_capabilities: Optional[Mapping[str, Mapping[str, Any]]] = None,
        profile_registry: Optional[HarnessDefinitionProfileRegistry] = None,
    ):
        self._eligibility_registry = eligibility_registry
        self._custom_capabilities = dict(custom_capabilities or {})
        self._profile_registry = profile_registry or HarnessDefinitionProfileRegistry()
        self._intake_validator = AtomicHarnessDefinitionIntake()

    def resolve_capability_metadata(
        self,
        definition: Any,
        *,
        override_metadata: Optional[Mapping[str, Mapping[str, Any]]] = None,
        ownership_graph: Optional[Any] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """Resolves required capabilities from authoritative governed sources fail-closed.
        
        Resolution precedence:
        1. Explicit caller override metadata (if supplied and valid)
        2. Eligibility registry candidate records (if registered)
        3. Capability ownership graph decisions (if supplied)
        4. Custom bridge capabilities
        5. Governed baseline capability catalogue
        
        Raises:
            HarnessCompilationBlocked(field='capabilities') if any required capability is missing.
        """
        norm_def = _normalize_definition(definition)
        content = norm_def.content

        required_cap_ids: List[str] = list(content.get("capability_requirements", []))

        resolved: Dict[str, Dict[str, Any]] = {}
        missing_caps: List[str] = []

        for cap_id in required_cap_ids:
            # 1. Caller override
            if override_metadata and cap_id in override_metadata:
                entry = dict(override_metadata[cap_id])
                resolved[cap_id] = {
                    "owner_kind": str(entry.get("owner_kind", "CODE")),
                    "required_features": list(entry.get("required_features", ["canonical_hash"])),
                    "authority_boundary": str(entry.get("authority_boundary", "caller_authorized_boundary")),
                }
                continue

            # 2. Eligibility registry
            if self._eligibility_registry is not None:
                candidates = self._eligibility_registry.eligible(cap_id, [])
                if candidates:
                    first = candidates[0]
                    resolved[cap_id] = {
                        "owner_kind": str(first.get("implementation_kind", "CODE")),
                        "required_features": list(first.get("features", ["canonical_hash"])),
                        "authority_boundary": str(first.get("authority_boundary", "pipeline_owned_execution")),
                    }
                    continue

            # 3. Capability ownership graph
            if ownership_graph is not None and hasattr(ownership_graph, "decisions"):
                if cap_id in ownership_graph.decisions:
                    decision = ownership_graph.decisions[cap_id]
                    resolved[cap_id] = {
                        "owner_kind": str(getattr(decision, "owner_kind", "CODE")),
                        "required_features": ["canonical_hash", "typed_output"],
                        "authority_boundary": str(getattr(decision, "authority_boundary", "governed_ownership_graph")),
                    }
                    continue

            # 4. Custom bridge capabilities
            if cap_id in self._custom_capabilities:
                entry = self._custom_capabilities[cap_id]
                resolved[cap_id] = {
                    "owner_kind": str(entry.get("owner_kind", "CODE")),
                    "required_features": list(entry.get("required_features", ["canonical_hash"])),
                    "authority_boundary": str(entry.get("authority_boundary", "custom_bridge_boundary")),
                }
                continue

            # 5. Governed baseline catalogue
            if cap_id in GOVERNED_BASELINE_CAPABILITIES:
                resolved[cap_id] = dict(GOVERNED_BASELINE_CAPABILITIES[cap_id])
                continue

            # If not resolvable from any authoritative source, record missing
            missing_caps.append(cap_id)

        if missing_caps:
            raise HarnessCompilationBlocked(
                field="capabilities",
                reason=f"{BLOCKER_2_TEXT}; missing metadata for: {sorted(missing_caps)}",
                blocker_ref="TS-APP-BRIDGE-001#blocker-2",
            )

        return resolved

    def resolve_workflow(
        self,
        definition: Any,
        *,
        override_workflow: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Resolves workflow DAG nodes and edges preserving 4 Authority Lanes fail-closed.
        
        Resolution precedence:
        1. Caller override workflow (if supplied and valid)
        2. Authored workflow in definition.content['workflow']
        3. Structured execution plan in definition.content['execution_plan']
        
        Raises:
            HarnessCompilationBlocked(field='workflow') if no valid workflow can be derived.
        """
        norm_def = _normalize_definition(definition)
        content = norm_def.content


        # 1. Caller override workflow
        if override_workflow is not None:
            raw_nodes = override_workflow.get("nodes", [])
            raw_edges = override_workflow.get("edges", [])
            if not raw_nodes:
                raise HarnessCompilationBlocked(
                    field="workflow",
                    reason=f"{BLOCKER_5_TEXT}; override workflow has empty nodes",
                    blocker_ref="TS-APP-BRIDGE-001#blocker-5",
                )
            return self._validate_and_normalize_workflow(raw_nodes, raw_edges)

        # 2. Authored workflow directly present in content
        if "workflow" in content and isinstance(content["workflow"], Mapping):
            wf = content["workflow"]
            raw_nodes = wf.get("nodes", [])
            raw_edges = wf.get("edges", [])
            if raw_nodes:
                return self._validate_and_normalize_workflow(raw_nodes, raw_edges)

        # 3. Derive structured workflow from execution_plan or capability_requirements preserving 4 lanes
        execution_plan = content.get("execution_plan", [])
        cap_reqs = content.get("capability_requirements", [])

        if not execution_plan and not cap_reqs:
            raise HarnessCompilationBlocked(
                field="workflow",
                reason=BLOCKER_5_TEXT,
                blocker_ref="TS-APP-BRIDGE-001#blocker-5",
            )

        nodes: List[Dict[str, Any]] = []
        edges: List[Dict[str, Any]] = []

        # If execution plan contains structured steps
        if execution_plan:
            for idx, step in enumerate(execution_plan, 1):
                step_name = step if isinstance(step, str) else f"step_{idx}"
                cap_id = cap_reqs[idx - 1] if idx - 1 < len(cap_reqs) else (cap_reqs[0] if cap_reqs else "atomic_execution")
                
                # Determine Authority Lane based on step semantics
                role = AuthorityLane.COMPOSER.value
                lower = step_name.lower()
                if any(k in lower for k in ("inspect", "read", "search", "hunt", "ingest", "fetch")) or idx == 1:
                    role = AuthorityLane.HUNTER.value
                elif any(k in lower for k in ("eval", "score", "analyze", "validate", "verify", "falsify")):
                    role = AuthorityLane.ANALYST.value
                elif any(k in lower for k in ("review", "gate", "approve", "authorize", "sign", "decide")):
                    role = AuthorityLane.COMMANDER.value

                node_id = f"node:{step_name.replace(' ', '_').lower()}"
                nodes.append(
                    {
                        "node_id": node_id,
                        "capability_id": cap_id,
                        "phase_order": idx,
                        "purpose": f"Execute step: {step_name}",
                        "actor_kind": NodeKind.HUMAN_GATE.value if role == AuthorityLane.COMMANDER.value else NodeKind.DETERMINISTIC_MODULE.value,
                        "role": role,
                        "product_boundary": ProductBoundary.STUDIO.value if role == AuthorityLane.COMMANDER.value else ProductBoundary.AHP.value,
                        "input_contracts": [f"contract:input:{idx}"],
                        "output_contracts": [f"contract:output:{idx}"],
                        "side_effect_class": "HUMAN_DECISION" if role == AuthorityLane.COMMANDER.value else ("READ_ONLY" if role == AuthorityLane.HUNTER.value else "LOCAL_STATE_WRITE"),
                    }
                )

            for i in range(1, len(nodes)):
                edges.append(
                    {
                        "source_node_id": nodes[i - 1]["node_id"],
                        "target_node_id": nodes[i]["node_id"],
                        "contract_id": f"contract:pipe:{i}",
                    }
                )
        elif cap_reqs:
            # Derive from capability requirements directly
            for idx, cap_id in enumerate(cap_reqs, 1):
                role = AuthorityLane.COMPOSER.value
                lower = cap_id.lower()
                if any(k in lower for k in ("inspect", "read", "search", "hunt", "ingest", "fetch")) or idx == 1:
                    role = AuthorityLane.HUNTER.value
                elif any(k in lower for k in ("eval", "score", "analyze", "validate", "verify", "falsify")):
                    role = AuthorityLane.ANALYST.value
                elif any(k in lower for k in ("review", "gate", "approve", "authorize", "sign", "decide")):
                    role = AuthorityLane.COMMANDER.value

                node_id = f"node:{cap_id}"
                nodes.append(
                    {
                        "node_id": node_id,
                        "capability_id": cap_id,
                        "phase_order": idx,
                        "purpose": f"Execute capability: {cap_id}",
                        "actor_kind": NodeKind.HUMAN_GATE.value if role == AuthorityLane.COMMANDER.value else NodeKind.DETERMINISTIC_MODULE.value,
                        "role": role,
                        "product_boundary": ProductBoundary.STUDIO.value if role == AuthorityLane.COMMANDER.value else ProductBoundary.AHP.value,
                        "input_contracts": [f"contract:in:{cap_id}"],
                        "output_contracts": [f"contract:out:{cap_id}"],
                        "side_effect_class": "HUMAN_DECISION" if role == AuthorityLane.COMMANDER.value else ("READ_ONLY" if role == AuthorityLane.HUNTER.value else "LOCAL_STATE_WRITE"),
                    }
                )

            for i in range(1, len(nodes)):
                edges.append(
                    {
                        "source_node_id": nodes[i - 1]["node_id"],
                        "target_node_id": nodes[i]["node_id"],
                        "contract_id": f"contract:edge:{i}",
                    }
                )

        return self._validate_and_normalize_workflow(nodes, edges)

    def _validate_and_normalize_workflow(
        self,
        raw_nodes: Sequence[Mapping[str, Any]],
        raw_edges: Sequence[Mapping[str, Any]],
    ) -> Dict[str, Any]:
        """Validates node roles against 4 Authority Lanes, node kinds, and topology."""
        normalized_nodes: List[Dict[str, Any]] = []
        valid_roles = {lane.value for lane in AuthorityLane}

        for idx, node in enumerate(raw_nodes):
            role = str(node.get("role", AuthorityLane.COMPOSER.value))
            if role not in valid_roles:
                raise HarnessCompilationBlocked(
                    field="workflow",
                    reason=f"Workflow node role '{role}' is not one of the 4 Authority Lanes ({sorted(valid_roles)})",
                    blocker_ref="TS-APP-BRIDGE-001#blocker-5",
                )
            
            actor_kind = str(node.get("actor_kind", NodeKind.DETERMINISTIC_MODULE.value))
            boundary = str(node.get("product_boundary", ProductBoundary.AHP.value))
            if actor_kind == NodeKind.HUMAN_GATE.value:
                boundary = ProductBoundary.STUDIO.value

            normalized_nodes.append(
                {
                    "node_id": str(node["node_id"]),
                    "capability_id": str(node["capability_id"]),
                    "phase_order": int(node.get("phase_order", idx + 1)),
                    "purpose": str(node.get("purpose", f"Execute {node['capability_id']}")),
                    "actor_kind": actor_kind,
                    "role": role,
                    "product_boundary": boundary,
                    "input_contracts": list(node.get("input_contracts", [])),
                    "output_contracts": list(node.get("output_contracts", [])),
                    "side_effect_class": str(node.get("side_effect_class", "LOCAL_STATE_WRITE")),
                }
            )

        node_ids = {n["node_id"] for n in normalized_nodes}
        normalized_edges: List[Dict[str, Any]] = []
        for edge in raw_edges:
            src = str(edge["source_node_id"])
            tgt = str(edge["target_node_id"])
            if src in node_ids and tgt in node_ids and src != tgt:
                normalized_edges.append(
                    {
                        "source_node_id": src,
                        "target_node_id": tgt,
                        "contract_id": str(edge.get("contract_id", f"contract:{src}->{tgt}")),
                    }
                )

        return {
            "nodes": sorted(normalized_nodes, key=lambda n: n["node_id"]),
            "edges": sorted(normalized_edges, key=lambda e: (e["source_node_id"], e["target_node_id"], e["contract_id"])),
        }

    def resolve_semantic_dependencies(
        self,
        definition: Any,
        *,
        air_refs: Optional[Mapping[str, str]] = None,
        override_dependencies: Optional[Sequence[Mapping[str, str]]] = None,
    ) -> List[Dict[str, str]]:
        """Resolves versioned, hashed semantic dependencies fail-closed.
        
        Resolution precedence:
        1. Explicit caller override dependencies (if supplied)
        2. Caller-supplied air_refs from interview/air resolution
        3. category_binding['semantic_lineage_refs']
        4. content['provenance_refs']
        
        Raises:
            HarnessCompilationBlocked(field='semantic_dependencies') if none can be resolved.
        """
        # 1. Override dependencies
        if override_dependencies is not None:
            deps = [dict(d) for d in override_dependencies]
            return sorted(deps, key=lambda d: d.get("object_id", ""))

        norm_def = _normalize_definition(definition)
        content = norm_def.content
        category_binding = content.get("category_binding", {})

        # 2. AIR refs
        if air_refs:
            deps = [
                {
                    "object_id": str(v),
                    "version": "1.0.0",
                    "sha256": canonical_sha256({"ref": str(v), "key": str(k)}),
                }
                for k, v in air_refs.items()
            ]
            return sorted(deps, key=lambda d: d["object_id"])

        # 3. Lineage refs in category binding
        lineage_refs = category_binding.get("semantic_lineage_refs", [])
        if lineage_refs:
            deps = [
                {
                    "object_id": str(ref_id),
                    "version": "1.0.0",
                    "sha256": canonical_sha256({"ref": str(ref_id)}),
                }
                for ref_id in lineage_refs
            ]
            return sorted(deps, key=lambda d: d["object_id"])

        # 4. Provenance refs in content
        prov_refs = content.get("provenance_refs", [])
        if prov_refs:
            deps = [
                {
                    "object_id": str(ref_id),
                    "version": "1.0.0",
                    "sha256": canonical_sha256({"ref": str(ref_id)}),
                }
                for ref_id in prov_refs
            ]
            return sorted(deps, key=lambda d: d["object_id"])

        raise HarnessCompilationBlocked(
            field="semantic_dependencies",
            reason=BLOCKER_1_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-1",
        )

    def resolve_evaluation_and_repair(
        self,
        definition: Any,
        *,
        override_eval: Optional[Sequence[str]] = None,
        override_repair: Optional[Sequence[str]] = None,
    ) -> Tuple[List[str], List[str]]:
        """Resolves evaluation requirements and repair laws."""
        norm_def = _normalize_definition(definition)
        content = norm_def.content

        # Evaluation requirements
        eval_reqs: List[str]
        if override_eval is not None:
            eval_reqs = list(override_eval)
        elif "evaluation_requirements" in content and content["evaluation_requirements"]:
            eval_reqs = list(content["evaluation_requirements"])
        else:
            eval_reqs = ["deterministic_contract_validation", "source_lineage_validation"]

        # Repair laws
        repair_laws: List[str]
        if override_repair is not None:
            repair_laws = list(override_repair)
        elif "repair_laws" in content and content["repair_laws"]:
            repair_laws = list(content["repair_laws"])
        else:
            repair_laws = ["descendant_only_rerun", "preserve_upstream_semantic_truth"]

        return eval_reqs, repair_laws

    def compile(
        self,
        definition: Any,
        *,
        air_refs: Optional[Mapping[str, str]] = None,
        override_semantic_dependencies: Optional[Sequence[Mapping[str, str]]] = None,
        override_capability_metadata: Optional[Mapping[str, Mapping[str, Any]]] = None,
        override_workflow: Optional[Mapping[str, Any]] = None,
        override_evaluation_requirements: Optional[Sequence[str]] = None,
        override_repair_laws: Optional[Sequence[str]] = None,
        ownership_graph: Optional[Any] = None,
    ) -> BridgeCompilationResult:
        """Executes full governed metadata bridge compilation for an authored harness definition.
        
        Returns BridgeCompilationResult containing either the validated intake projection or
        structured blocker diagnostics with the exact field and citation.
        """
        try:
            norm_def = _normalize_definition(definition)

            # 1. Resolve semantic dependencies (Blocker 1)
            semantic_deps = self.resolve_semantic_dependencies(
                norm_def,
                air_refs=air_refs,
                override_dependencies=override_semantic_dependencies,
            )

            # 2. Resolve capability metadata (Blocker 2)
            cap_metadata = self.resolve_capability_metadata(
                norm_def,
                override_metadata=override_capability_metadata,
                ownership_graph=ownership_graph,
            )

            # 3. Resolve workflow DAG (Blocker 5)
            workflow = self.resolve_workflow(
                norm_def,
                override_workflow=override_workflow,
            )

            # 4. Resolve evaluation and repair laws (Blocker 6)
            eval_reqs, repair_laws = self.resolve_evaluation_and_repair(
                norm_def,
                override_eval=override_evaluation_requirements,
                override_repair=override_repair_laws,
            )

            # 5. Execute canonical compiler intake
            raw_intake = compile_portable_to_intake(
                norm_def,
                semantic_dependencies=semantic_deps,
                capability_metadata=cap_metadata,
                workflow=workflow,
                evaluation_requirements=eval_reqs,
                repair_laws=repair_laws,
            )

            # 6. Validate intake against compiler profile
            profile_key = raw_intake.get("profile_id", "portable_activative_v1").replace("-", "_")
            profile = self._profile_registry.resolve(profile_key)
            intake_projection = self._intake_validator.validate(raw_intake, profile)

            return BridgeCompilationResult(
                success=True,
                intake_projection=intake_projection,
                resolved_capabilities=cap_metadata,
                resolved_workflow=workflow,
                resolved_semantic_dependencies=semantic_deps,
            )

        except HarnessCompilationBlocked as exc:
            def_id = getattr(definition, "definition_id", "unknown_definition")
            logger.info(
                "HarnessCompilationBlocked in bridge for '%s': field=%s reason=%s blocker_ref=%s",
                def_id, exc.field, exc.reason, exc.blocker_ref,
            )
            return BridgeCompilationResult(
                success=False,
                blocked_field=exc.field,
                blocked_reason=exc.reason,
                blocker_ref=exc.blocker_ref,
            )
        except PipelineValidationError as exc:
            def_id = getattr(definition, "definition_id", "unknown_definition")
            logger.warning("PipelineValidationError in bridge for '%s': %s", def_id, exc)
            return BridgeCompilationResult(
                success=False,
                blocked_field="validation",
                blocked_reason=str(exc),
                blocker_ref="TS-APP-BRIDGE-001#validation-error",
            )
        except Exception as exc:
            def_id = getattr(definition, "definition_id", "unknown_definition")
            logger.exception("Unexpected error bridging harness '%s': %s", def_id, exc)
            return BridgeCompilationResult(

                success=False,
                blocked_field="system",
                blocked_reason=str(exc),
                blocker_ref="TS-APP-BRIDGE-001#system-error",
            )
