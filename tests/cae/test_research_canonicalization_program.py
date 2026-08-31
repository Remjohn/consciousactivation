"""
Phase 3 Mandate M29 Acceptance Test Suite:
Research Knowledge Extraction + Canonicalization + OKF Program Coordinator.

Governed by:
- 03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M29_research_knowledge_extraction_canonicalization_okf.md
- 00_CONTROL/20_PHASE3_CANONICALIZATION_MODEL.md
- 00_CONTROL/21_PHASE3_KNOWLEDGE_RUNTIME_CONTRACT.md
- 00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from ca_contracts import canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateMachineDefinition,
    UniversalProgramStateRuntime,
    get_canonical_research_canonicalization_state_machine,
)
from ca_runtime.research_canonicalization_program import (
    AdjudicationDecision,
    CanonicalKnowledgeNode,
    CanonicalRelationship,
    CanonicalRelationshipType,
    ContradictionAdjudicationRequiredError,
    FalseMergeViolationError,
    KnowledgeCandidate,
    NodeRetractedError,
    OKFDocument,
    OKFKnowledgeBundle,
    OKFValidationError,
    ResearchCanonicalizationProgramCoordinator,
    ResearchCanonicalizationProgramError,
    ResearchCanonicalizationSnapshot,
    SourceProvenanceMissingError,
    WorkspaceScopeViolationError,
)
from ca_runtime.tenancy import TenantContext, tenant_scope


# ----------------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------------

@pytest.fixture
def test_workspace_id() -> str:
    return str(uuid4())


@pytest.fixture
def foreign_workspace_id() -> str:
    return str(uuid4())


@pytest.fixture
def tenant_ctx(test_workspace_id: str) -> TenantContext:
    return TenantContext(
        workspace_id=UUID(test_workspace_id),
        actor_id="usr_lead_commander",
        role="MEMBER",
    )


@pytest.fixture
def foreign_tenant_ctx(foreign_workspace_id: str) -> TenantContext:
    return TenantContext(
        workspace_id=UUID(foreign_workspace_id),
        actor_id="usr_foreign_agent",
        role="MEMBER",
    )


@pytest.fixture
def runtime() -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime()


@pytest.fixture
def coordinator(runtime: UniversalProgramStateRuntime) -> ResearchCanonicalizationProgramCoordinator:
    return ResearchCanonicalizationProgramCoordinator(runtime=runtime)


@pytest.fixture
def sample_sources() -> list[dict]:
    s1_text = "Artificial General Intelligence (AGI) is the hypothetical ability of an intelligent agent to understand or learn any intellectual task that human beings can."
    s1_hash = hashlib.sha256(s1_text.encode("utf-8")).hexdigest()

    s2_text = "Strong AI refers to artificial intelligence that possesses human-like cognitive abilities and self-awareness."
    s2_hash = hashlib.sha256(s2_text.encode("utf-8")).hexdigest()

    s3_text = "Project Gemini was NASA's second human spaceflight program, operating between Mercury and Apollo."
    s3_hash = hashlib.sha256(s3_text.encode("utf-8")).hexdigest()

    return [
        {
            "source_id": "src_agi_overview_001",
            "topic": "Artificial General Intelligence",
            "evidence_excerpt": s1_text,
            "content_hash_sha256": s1_hash,
            "origin_url": "https://en.wikipedia.org/wiki/Artificial_general_intelligence",
        },
        {
            "source_id": "src_strong_ai_002",
            "topic": "Strong AI",
            "evidence_excerpt": s2_text,
            "content_hash_sha256": s2_hash,
            "origin_url": "https://plato.stanford.edu/entries/artificial-intelligence/",
        },
        {
            "source_id": "src_nasa_gemini_003",
            "topic": "Project Gemini",
            "evidence_excerpt": s3_text,
            "content_hash_sha256": s3_hash,
            "origin_url": "https://www.nasa.gov/specials/gemini/",
        },
    ]


# ----------------------------------------------------------------------------
# 1. Package Discovery & Manifest Tests
# ----------------------------------------------------------------------------

def test_program_package_discovery_and_manifest():
    """Verifies that the research_canonicalization_program package is discovered with valid manifest and skills."""
    registry = ProgramRegistry(discovery_roots=[Path("programs")])
    discovered = registry.discover()
    discovered_ids = [p.program_id for p in discovered]
    assert "research_canonicalization_program" in discovered_ids

    pkg = registry.get_program("research_canonicalization_program")
    assert pkg is not None
    assert pkg.manifest.id == "research_canonicalization_program"
    assert pkg.manifest.version == "1.0.0"
    assert pkg.manifest.status.value == "ACTIVE"
    assert pkg.manifest.state_machine == "RESEARCH_CANONICALIZATION_STATE_MACHINE_V1"

    # Verify Authority Lanes
    lanes = pkg.manifest.lanes
    assert "COMMANDER" in lanes
    assert "HUNTER" in lanes
    assert "ANALYST" in lanes
    assert "COMPOSER" in lanes

    # Verify Passive Flat Skills
    skill_names = [s.name for s in pkg.manifest.skills]
    assert "knowledge_candidate_extractor" in skill_names
    assert "canonical_relationship_classifier" in skill_names
    assert "okf_bundle_projector" in skill_names


# ----------------------------------------------------------------------------
# 2. State Machine Grammar & Transition Contracts
# ----------------------------------------------------------------------------

def test_state_machine_grammar_and_transitions():
    """Verifies the canonical state machine definition for research_canonicalization_program."""
    sm = get_canonical_research_canonicalization_state_machine()
    assert sm.machine_id == "RESEARCH_CANONICALIZATION_STATE_MACHINE_V1"
    assert sm.program_id == "research_canonicalization_program"
    assert sm.initial_state == "INITIAL"
    assert "KNOWLEDGE_COMMITTED" in sm.terminal_states

    # Verify transitions and authority lanes
    assert sm.transitions["attach_sources"].from_state == "INITIAL"
    assert sm.transitions["attach_sources"].to_state == "SOURCES_ATTACHED"
    assert sm.transitions["attach_sources"].required_lane == AuthorityLane.COMMANDER

    assert sm.transitions["extract_candidates"].from_state == "SOURCES_ATTACHED"
    assert sm.transitions["extract_candidates"].to_state == "CANDIDATES_EXTRACTED"
    assert sm.transitions["extract_candidates"].required_lane == AuthorityLane.HUNTER

    assert sm.transitions["canonicalize_candidates"].from_state == "CANDIDATES_EXTRACTED"
    assert sm.transitions["canonicalize_candidates"].to_state == "CANONICALIZED"
    assert sm.transitions["canonicalize_candidates"].required_lane == AuthorityLane.ANALYST

    assert sm.transitions["project_okf_bundle"].from_state == "CANONICALIZED"
    assert sm.transitions["project_okf_bundle"].to_state == "OKF_PROJECTED"
    assert sm.transitions["project_okf_bundle"].required_lane == AuthorityLane.COMPOSER

    assert sm.transitions["commit_canonical_knowledge"].from_state == "OKF_PROJECTED"
    assert sm.transitions["commit_canonical_knowledge"].to_state == "KNOWLEDGE_COMMITTED"
    assert sm.transitions["commit_canonical_knowledge"].required_lane == AuthorityLane.COMMANDER

    assert sm.repair_transitions["repair_canonicalization"].from_state == "REPAIRING"
    assert sm.repair_transitions["repair_canonicalization"].to_state == "SOURCES_ATTACHED"
    assert sm.repair_transitions["repair_canonicalization"].required_lane == AuthorityLane.COMMANDER


# ----------------------------------------------------------------------------
# 3. End-to-End Lifecycle Execution
# ----------------------------------------------------------------------------

def test_full_canonicalization_lifecycle_e2e(
    coordinator: ResearchCanonicalizationProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
    sample_sources: list[dict],
):
    """Proves the full state progression from INITIAL through KNOWLEDGE_COMMITTED."""
    with tenant_scope(tenant_ctx):
        agg_id = coordinator.initialize_program(
            workspace_id=test_workspace_id,
            actor_id=tenant_ctx.actor_id,
        )

        # 1. Attach sources (COMMANDER)
        res_attach = coordinator.attach_sources(
            aggregate_id=agg_id,
            sources=sample_sources,
            context=tenant_ctx,
        )
        assert res_attach.aggregate.current_state == "SOURCES_ATTACHED"

        # 2. Extract candidates (HUNTER)
        hunter_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_hunter", role="MEMBER")
        res_extract = coordinator.extract_candidates(
            aggregate_id=agg_id,
            context=hunter_ctx,
        )
        assert res_extract.aggregate.current_state == "CANDIDATES_EXTRACTED"

        # 3. Canonicalize candidates (ANALYST)
        analyst_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_analyst", role="MEMBER")
        res_canon = coordinator.canonicalize_candidates(
            aggregate_id=agg_id,
            context=analyst_ctx,
        )
        assert res_canon.aggregate.current_state == "CANONICALIZED"

        # 4. Project OKF bundle (COMPOSER)
        composer_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_composer", role="MEMBER")
        res_okf = coordinator.project_okf_bundle(
            aggregate_id=agg_id,
            context=composer_ctx,
        )
        assert res_okf.aggregate.current_state == "OKF_PROJECTED"

        # 5. Commit canonical knowledge (COMMANDER)
        res_commit = coordinator.commit_canonical_knowledge(
            aggregate_id=agg_id,
            context=tenant_ctx,
        )
        assert res_commit.aggregate.current_state == "KNOWLEDGE_COMMITTED"

        # Snapshot verification
        snap = coordinator.get_snapshot(agg_id)
        assert snap.state == "KNOWLEDGE_COMMITTED"
        assert len(snap.canonical_nodes) >= 2
        assert snap.okf_bundle is not None
        assert snap.okf_bundle.bundle_sha256 is not None
        assert len(snap.okf_bundle.documents) == len(snap.canonical_nodes)


# ----------------------------------------------------------------------------
# 4. Controlled Corpus: Alias & Duplicate Resolution
# ----------------------------------------------------------------------------

def test_controlled_corpus_alias_and_duplicate_resolution(
    coordinator: ResearchCanonicalizationProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
):
    """Proves that aliases ('Artificial General Intelligence', 'AGI', 'Strong AI') resolve to a single canonical node."""
    s1_text = "Artificial General Intelligence (AGI) is machine intelligence with human-level capability."
    s1_hash = hashlib.sha256(s1_text.encode("utf-8")).hexdigest()

    s2_text = "AGI refers to flexible autonomous intelligence across diverse cognitive domains."
    s2_hash = hashlib.sha256(s2_text.encode("utf-8")).hexdigest()

    sources = [
        {"source_id": "src_1", "topic": "Artificial General Intelligence", "evidence_excerpt": s1_text, "content_hash_sha256": s1_hash},
        {"source_id": "src_2", "topic": "AGI", "evidence_excerpt": s2_text, "content_hash_sha256": s2_hash},
    ]

    with tenant_scope(tenant_ctx):
        agg_id = coordinator.initialize_program(workspace_id=test_workspace_id, actor_id=tenant_ctx.actor_id)
        coordinator.attach_sources(agg_id, sources, context=tenant_ctx)

        hunter_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_hunter", role="MEMBER")
        coordinator.extract_candidates(agg_id, context=hunter_ctx)

        analyst_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_analyst", role="MEMBER")
        coordinator.canonicalize_candidates(agg_id, context=analyst_ctx)

        snap = coordinator.get_snapshot(agg_id)
        # Should merge into 1 canonical node with alias 'AGI'
        assert len(snap.canonical_nodes) == 1
        node = snap.canonical_nodes[0]
        assert node.canonical_label == "Artificial General Intelligence"
        assert "AGI" in node.aliases or "Artificial General Intelligence" in node.aliases
        # Both source refs should be present
        assert "src_1" in node.source_record_refs
        assert "src_2" in node.source_record_refs
        assert s1_hash in node.source_evidence_hashes
        assert s2_hash in node.source_evidence_hashes


# ----------------------------------------------------------------------------
# 5. False-Merge Rejection (Homonyms & Distinct Concepts)
# ----------------------------------------------------------------------------

def test_false_merge_rejection_homonyms(
    coordinator: ResearchCanonicalizationProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
):
    """Proves distinct homonyms (e.g. Gemini AI vs Project Gemini NASA) are kept DISTINCT."""
    s1_text = "Google Gemini is a family of multimodal large language models developed by Google DeepMind."
    s1_hash = hashlib.sha256(s1_text.encode("utf-8")).hexdigest()

    s2_text = "Project Gemini was NASA's spaceflight program conducting extravehicular activities in Earth orbit."
    s2_hash = hashlib.sha256(s2_text.encode("utf-8")).hexdigest()

    sources = [
        {"source_id": "src_gemini_ai", "topic": "Gemini AI", "evidence_excerpt": s1_text, "content_hash_sha256": s1_hash},
        {"source_id": "src_gemini_nasa", "topic": "Project Gemini", "evidence_excerpt": s2_text, "content_hash_sha256": s2_hash},
    ]

    with tenant_scope(tenant_ctx):
        agg_id = coordinator.initialize_program(workspace_id=test_workspace_id, actor_id=tenant_ctx.actor_id)
        coordinator.attach_sources(agg_id, sources, context=tenant_ctx)

        hunter_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_hunter", role="MEMBER")
        coordinator.extract_candidates(agg_id, context=hunter_ctx)

        analyst_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_analyst", role="MEMBER")
        # Explicit homonym blacklist to forbid false merge
        homonym_blacklist = {
            "gemini ai": {"project gemini", "gemini spaceflight"},
            "project gemini": {"gemini ai", "google gemini"},
        }
        coordinator.canonicalize_candidates(
            agg_id,
            homonym_blacklist=homonym_blacklist,
            context=analyst_ctx,
        )

        snap = coordinator.get_snapshot(agg_id)
        # Must produce exactly 2 distinct nodes, NOT merged
        assert len(snap.canonical_nodes) == 2
        labels = [n.canonical_label for n in snap.canonical_nodes]
        assert "Gemini AI" in labels
        assert "Project Gemini" in labels


# ----------------------------------------------------------------------------
# 6. Contradiction Detection & Commander Adjudication
# ----------------------------------------------------------------------------

def test_contradiction_detection_and_commander_adjudication(
    coordinator: ResearchCanonicalizationProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
):
    """Proves contradictory claims require Commander adjudication before commit."""
    s1_text = "Room-temperature superconductivity in LK-99 has been independently replicated with zero resistance."
    s1_hash = hashlib.sha256(s1_text.encode("utf-8")).hexdigest()

    s2_text = "Comprehensive independent testing refutes superconductivity claims in LK-99, showing ferromagnetic impurities."
    s2_hash = hashlib.sha256(s2_text.encode("utf-8")).hexdigest()

    sources = [
        {"source_id": "src_lk99_claim", "topic": "LK-99 Superconductivity Claim", "evidence_excerpt": s1_text, "content_hash_sha256": s1_hash},
        {"source_id": "src_lk99_refutation", "topic": "LK-99 Superconductivity Refutation", "evidence_excerpt": s2_text, "content_hash_sha256": s2_hash},
    ]

    with tenant_scope(tenant_ctx):
        agg_id = coordinator.initialize_program(workspace_id=test_workspace_id, actor_id=tenant_ctx.actor_id)
        coordinator.attach_sources(agg_id, sources, context=tenant_ctx)

        hunter_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_hunter", role="MEMBER")
        coordinator.extract_candidates(agg_id, context=hunter_ctx)

        analyst_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_analyst", role="MEMBER")
        # Add explicit contradiction relationship
        contradiction_rel = CanonicalRelationship(
            rel_id="rel_lk99_contra_01",
            source_id="kn_lk99-superconductivity-claim",
            target_id="kn_lk99-superconductivity-refutation",
            rel_type=CanonicalRelationshipType.CONTRADICTORY,
            rationale="Mutually exclusive empirical findings regarding zero resistance in LK-99",
            adjudicated=False,
        )
        coordinator.canonicalize_candidates(
            agg_id,
            custom_relationships=[contradiction_rel],
            context=analyst_ctx,
        )

        composer_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_composer", role="MEMBER")
        coordinator.project_okf_bundle(agg_id, context=composer_ctx)

        # Attempting commit without adjudication MUST fail closed
        with pytest.raises(ContradictionAdjudicationRequiredError) as exc_info:
            coordinator.commit_canonical_knowledge(agg_id, context=tenant_ctx)
        assert "rel_lk99_contra_01" in exc_info.value.contradiction_ids

        # Commander adjudicates contradiction
        decision = AdjudicationDecision(
            decision_id="dec_001",
            target_id="rel_lk99_contra_01",
            action="RESOLVE_CONTRADICTION",
            operator_actor_id=tenant_ctx.actor_id,
            rationale="Scientific consensus established LK-99 is an insulator; claim superseded by refutation.",
        )
        coordinator.adjudicate_contradiction(agg_id, decision, context=tenant_ctx)

        # Now commit succeeds
        res_commit = coordinator.commit_canonical_knowledge(agg_id, context=tenant_ctx)
        assert res_commit.aggregate.current_state == "KNOWLEDGE_COMMITTED"


# ----------------------------------------------------------------------------
# 7. OKF Bundle Generation & Directory Export
# ----------------------------------------------------------------------------

def test_okf_bundle_generation_and_export(
    coordinator: ResearchCanonicalizationProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
    sample_sources: list[dict],
):
    """Proves OKF Markdown rendering, frontmatter format, and filesystem export."""
    with tenant_scope(tenant_ctx):
        agg_id = coordinator.initialize_program(workspace_id=test_workspace_id, actor_id=tenant_ctx.actor_id)
        coordinator.attach_sources(agg_id, sample_sources, context=tenant_ctx)

        hunter_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_hunter", role="MEMBER")
        coordinator.extract_candidates(agg_id, context=hunter_ctx)

        analyst_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_analyst", role="MEMBER")
        coordinator.canonicalize_candidates(agg_id, context=analyst_ctx)

        composer_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_composer", role="MEMBER")
        coordinator.project_okf_bundle(agg_id, context=composer_ctx)

        with TemporaryDirectory() as tmpdir:
            out_path = coordinator.export_okf_bundle_to_directory(agg_id, tmpdir)
            assert out_path.exists()

            # Check index.md
            index_file = out_path / "index.md"
            assert index_file.exists()
            index_text = index_file.read_text(encoding="utf-8")
            assert "# Research Knowledge Catalog (OKF)" in index_text
            assert "cmf-okf-research-knowledge-1.0" in index_text

            # Check concept files
            concept_dir = out_path / "concepts"
            assert concept_dir.exists()
            md_files = list(concept_dir.glob("*.md"))
            assert len(md_files) >= 2

            # Verify YAML frontmatter and structure of a concept file
            sample_doc = md_files[0].read_text(encoding="utf-8")
            assert sample_doc.startswith("---")
            assert "okf_version:" in sample_doc
            assert "cmf_profile:" in sample_doc
            assert "lineage_sha256:" in sample_doc
            assert "## Definition" in sample_doc
            assert "## Provenance & Lineage" in sample_doc


# ----------------------------------------------------------------------------
# 8. Source Immutability & Lineage Preservation
# ----------------------------------------------------------------------------

def test_source_provenance_immutability_and_lineage(
    coordinator: ResearchCanonicalizationProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
):
    """Proves missing or unverified source hashes fail closed with SourceProvenanceMissingError."""
    # Attempting to extract candidate referencing non-existent source
    with tenant_scope(tenant_ctx):
        agg_id = coordinator.initialize_program(workspace_id=test_workspace_id, actor_id=tenant_ctx.actor_id)
        
        valid_src = [{
            "source_id": "src_valid",
            "topic": "Valid Topic",
            "evidence_excerpt": "Valid excerpt",
            "content_hash_sha256": hashlib.sha256(b"Valid excerpt").hexdigest(),
        }]
        coordinator.attach_sources(agg_id, valid_src, context=tenant_ctx)

        invalid_cand = KnowledgeCandidate(
            candidate_id="cand_bad",
            label="Fake Candidate",
            extracted_text="Fake text",
            source_id="src_NONEXISTENT",
            source_sha256="a" * 64,
        )

        hunter_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_hunter", role="MEMBER")
        with pytest.raises(SourceProvenanceMissingError):
            coordinator.extract_candidates(agg_id, custom_candidates=[invalid_cand], context=hunter_ctx)


# ----------------------------------------------------------------------------
# 9. Node Retraction & Re-expression Lifecycle
# ----------------------------------------------------------------------------

def test_node_retraction_and_reexpression_lifecycle(
    coordinator: ResearchCanonicalizationProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
    sample_sources: list[dict],
):
    """Proves retraction marks status and re-expression creates v2 with supersedes lineage."""
    with tenant_scope(tenant_ctx):
        agg_id = coordinator.initialize_program(workspace_id=test_workspace_id, actor_id=tenant_ctx.actor_id)
        coordinator.attach_sources(agg_id, sample_sources, context=tenant_ctx)

        hunter_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_hunter", role="MEMBER")
        coordinator.extract_candidates(agg_id, context=hunter_ctx)

        analyst_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_analyst", role="MEMBER")
        coordinator.canonicalize_candidates(agg_id, context=analyst_ctx)

        snap = coordinator.get_snapshot(agg_id)
        target_node = snap.canonical_nodes[0]
        node_id = target_node.node_id

        # 1. Re-express node -> creates version 2 with supersedes_node_id
        new_def = "Updated advanced definition for the canonical knowledge node."
        reexpressed_node = coordinator.reexpress_canonical_node(
            agg_id,
            node_id=node_id,
            new_definition=new_def,
            context=tenant_ctx,
        )
        assert reexpressed_node.version == 2
        assert reexpressed_node.supersedes_node_id == node_id
        assert reexpressed_node.definition == new_def
        assert "supersedes" in reexpressed_node.typed_edges

        # 2. Retract node
        retracted_node = coordinator.retract_canonical_node(
            agg_id,
            node_id=reexpressed_node.node_id,
            retraction_reason="Experimental findings superseded by updated empirical study.",
            context=tenant_ctx,
        )
        assert retracted_node.lifecycle_status == "retracted"
        assert retracted_node.retraction_reason is not None

        # Attempting to re-express retracted node MUST fail
        with pytest.raises(NodeRetractedError):
            coordinator.reexpress_canonical_node(
                agg_id,
                node_id=retracted_node.node_id,
                new_definition="Another definition",
                context=tenant_ctx,
            )


# ----------------------------------------------------------------------------
# 10. Cross-Workspace Isolation & Authority Lane Denial
# ----------------------------------------------------------------------------

def test_cross_workspace_and_authority_lane_denial(
    coordinator: ResearchCanonicalizationProgramCoordinator,
    test_workspace_id: str,
    foreign_workspace_id: str,
    tenant_ctx: TenantContext,
    foreign_tenant_ctx: TenantContext,
    sample_sources: list[dict],
):
    """Proves cross-workspace access fails with WorkspaceScopeViolationError and lane mismatches fail."""
    with tenant_scope(tenant_ctx):
        agg_id = coordinator.initialize_program(workspace_id=test_workspace_id, actor_id=tenant_ctx.actor_id)

    # Cross-workspace isolation denial
    with tenant_scope(foreign_tenant_ctx):
        with pytest.raises(WorkspaceScopeViolationError):
            coordinator.attach_sources(agg_id, sample_sources, context=foreign_tenant_ctx)

    # Authority lane mismatch denial (e.g. Hunter trying to attach sources)
    with tenant_scope(tenant_ctx):
        hunter_ctx = TenantContext(workspace_id=UUID(test_workspace_id), actor_id="usr_hunter", role="MEMBER")
        # In UniversalProgramStateRuntime, executing attach_sources with Hunter lane fails
        with pytest.raises(ProgramAuthorityLaneViolationError):
            coordinator.runtime.execute_transition(
                aggregate_id=agg_id,
                transition_name="attach_sources",
                actor_lane=AuthorityLane.HUNTER,  # Mismatch: requires COMMANDER
                actor_id=hunter_ctx.actor_id,
                context_claims=["workspace_active", "sources_verified"],
            )
