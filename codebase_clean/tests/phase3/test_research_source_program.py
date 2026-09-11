"""
Phase 3 Mandate M28 Acceptance Test Suite:
Research Source Ingestion + Identity Program Coordinator.

Governed by:
- 03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M28_research_source_ingestion_identity.md
- 00_CONTROL/20_PHASE3_CANONICALIZATION_MODEL.md
- 00_CONTROL/21_PHASE3_KNOWLEDGE_RUNTIME_CONTRACT.md
- 00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md
- Object Constitution CA-CAN-01B_EVIDENCE_SOURCE.yaml
"""

from __future__ import annotations

from . import _support

from datetime import datetime, timezone
import hashlib
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from ca_contracts import canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane, AuthorityLaneMismatchError
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateLifecycle,
    ProgramStateMachineDefinition,
    ProgramTransitionBlockedError,
    UniversalProgramStateRuntime,
    get_canonical_research_source_state_machine,
)
from ca_runtime.research_source_program import (
    DuplicateSourceInflationViolationError,
    InvalidSourceReingestionError,
    ResearchSourceProgramCoordinator,
    ResearchSourceProgramError,
    ResearchSourceRecord,
    ResearchSourceSnapshot,
    SourceHashMismatchError,
    SourceImmutabilityViolationError,
    SourceProvenanceIntegrityError,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenantContext,
    tenant_scope,
)
from cae_world_intelligence.adapters.fixture_adapter import FixtureResearchAdapter
from cae_world_intelligence.domain import RawObservation


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
        workspace_id=UUID(test_workspace_id) if isinstance(test_workspace_id, str) else test_workspace_id,
        actor_id="usr_hunter_lead",
        role="MEMBER",
    )


@pytest.fixture
def foreign_tenant_ctx(foreign_workspace_id: str) -> TenantContext:
    return TenantContext(
        workspace_id=UUID(foreign_workspace_id) if isinstance(foreign_workspace_id, str) else foreign_workspace_id,
        actor_id="usr_foreign_agent",
        role="MEMBER",
    )


@pytest.fixture
def runtime() -> UniversalProgramStateRuntime:
    rt = UniversalProgramStateRuntime()
    return rt


@pytest.fixture
def coordinator(runtime: UniversalProgramStateRuntime) -> ResearchSourceProgramCoordinator:
    return ResearchSourceProgramCoordinator(runtime=runtime)


@pytest.fixture
def aggregate_id(runtime: UniversalProgramStateRuntime, test_workspace_id: str, tenant_ctx: TenantContext) -> str:
    with tenant_scope(tenant_ctx):
        agg = runtime.initialize_program_state(
            program_id="research_source_ingestion_program",
            workspace_id=test_workspace_id,
            actor_id="usr_hunter_lead",
        )
        return agg.aggregate_id


# ----------------------------------------------------------------------------
# 1. Full Lifecycle Acceptance Test
# ----------------------------------------------------------------------------

def test_research_source_full_lifecycle_acceptance(
    coordinator: ResearchSourceProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
    aggregate_id: str,
):
    """Verifies complete progression: INITIAL -> ADMITTED -> VERIFIED -> REGISTERED -> ACTIVE."""
    with tenant_scope(tenant_ctx):
        raw_snippet = "Latent space geometry across transformer models demonstrates isomorphic alignment under orthogonal transformation."
        origin_url = "https://arxiv.org/abs/2501.04321"

        # Step 1: Admit Source (Hunter)
        rec, admit_receipt = coordinator.admit_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_hunter_lead",
            origin_url=origin_url,
            raw_text_snippet=raw_snippet,
            source_platform="arxiv",
            source_type="ACADEMIC_PAPER",
            author_outlet="Cornell AI Lab",
            rights_metadata={"license": "CC-BY-4.0", "access_tier": "PUBLIC"},
        )

        assert rec.status == "ADMITTED"
        assert rec.version == 1
        assert rec.supersedes_source_id is None
        assert rec.content_sha256 == hashlib.sha256(raw_snippet.encode("utf-8")).hexdigest()
        assert rec.root_domain == "arxiv.org"
        assert admit_receipt["authority_lane"] == "HUNTER"
        assert admit_receipt["receipt_type"] == "cae_execution_receipt"
        assert admit_receipt["idempotent_replay"] is False

        # Step 2: Verify Source (Analyst)
        verified_rec, verify_receipt = coordinator.verify_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_analyst_lead",
            source_id=rec.source_id,
        )

        assert verified_rec.status == "VERIFIED"
        assert verified_rec.verified_at is not None
        assert verify_receipt["authority_lane"] == "ANALYST"
        assert verified_rec.source_multiplicity["independent_source_count"] == 1

        # Step 3: Register Source (Composer)
        registered_rec, reg_receipt = coordinator.register_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_composer_lead",
            source_id=verified_rec.source_id,
        )

        assert registered_rec.status == "REGISTERED"
        assert reg_receipt["authority_lane"] == "COMPOSER"

        # Step 4: Approve Source (Commander)
        active_rec, approve_receipt = coordinator.approve_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_commander_lead",
            source_id=registered_rec.source_id,
        )

        assert active_rec.status == "ACTIVE"
        assert approve_receipt["authority_lane"] == "COMMANDER"

        # Verify Snapshot
        snapshot = coordinator.get_snapshot(aggregate_id)
        assert snapshot.current_state == "SOURCE_ACTIVE"
        assert snapshot.active_source_id == rec.source_id
        assert snapshot.active_source_version == 1
        assert snapshot.total_versions == 1


# ----------------------------------------------------------------------------
# 2. Idempotent Deduplication Test (Zero Duplicate Canonical Identity)
# ----------------------------------------------------------------------------

def test_research_source_idempotent_deduplication(
    coordinator: ResearchSourceProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
    aggregate_id: str,
):
    """Re-ingesting the exact same content for an origin URL yields an idempotent replay."""
    with tenant_scope(tenant_ctx):
        raw_snippet = "Quantum topological data analysis accelerates molecular discovery manifolds."
        origin_url = "https://nature.com/articles/s41586-026-0001"

        # Initial admission
        rec1, receipt1 = coordinator.admit_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_hunter_lead",
            origin_url=origin_url,
            raw_text_snippet=raw_snippet,
            source_platform="nature",
        )
        assert receipt1["idempotent_replay"] is False

        # Duplicate admission attempt with identical payload
        rec2, receipt2 = coordinator.admit_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_hunter_lead",
            origin_url=origin_url,
            raw_text_snippet=raw_snippet,
            source_platform="nature",
        )

        # Invariants: Exact same source_id, no duplicate canonical source created, replay flagged
        assert rec1.source_id == rec2.source_id
        assert rec1.content_sha256 == rec2.content_sha256
        assert rec2.version == 1
        assert receipt2["idempotent_replay"] is True


# ----------------------------------------------------------------------------
# 3. Versioned Re-ingestion with Immutable Lineage
# ----------------------------------------------------------------------------

def test_research_source_versioned_reingestion_lineage(
    coordinator: ResearchSourceProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
    aggregate_id: str,
):
    """Re-ingesting modified content produces version 2 with lineage to version 1."""
    with tenant_scope(tenant_ctx):
        url = "https://techcrunch.com/2026/08/30/ai-agent-governance-breakthrough"
        content_v1 = "Initial announcement: Framework ensures 4-lane authority separation for autonomous agent execution."

        # Ingest Version 1 through to ACTIVE
        rec_v1, _ = coordinator.admit_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_hunter_lead",
            origin_url=url,
            raw_text_snippet=content_v1,
        )
        coordinator.verify_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_analyst_lead",
            source_id=rec_v1.source_id,
        )
        coordinator.register_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_composer_lead",
            source_id=rec_v1.source_id,
        )
        active_v1, _ = coordinator.approve_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_commander_lead",
            source_id=rec_v1.source_id,
        )

        # Later snapshot: Content updated at same URL
        content_v2 = "Updated announcement: Framework adds strict PostgreSQL RLS staging authority and cryptographic execution receipts."

        rec_v2, reingest_receipt = coordinator.reingest_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_hunter_lead",
            prior_source_id=rec_v1.source_id,
            new_raw_text_snippet=content_v2,
        )

        # Validate Version 2
        assert rec_v2.version == 2
        assert rec_v2.supersedes_source_id == rec_v1.source_id
        assert rec_v2.ancestor_version_hashes == (rec_v1.content_sha256,)
        assert rec_v2.source_id != rec_v1.source_id
        assert rec_v2.status == "VERSIONED"
        assert reingest_receipt["authority_lane"] == "HUNTER"

        # Validate Version 1 remains completely immutable and accessible
        stored_v1 = coordinator.get_source_record(rec_v1.source_id)
        assert stored_v1 is not None
        assert stored_v1.version == 1
        assert stored_v1.content_sha256 == rec_v1.content_sha256
        assert stored_v1.raw_content_excerpt == content_v1

        # Check origin version list
        versions = coordinator.get_versions_for_origin(test_workspace_id, url)
        assert len(versions) == 2
        assert [v.version for v in versions] == [1, 2]


# ----------------------------------------------------------------------------
# 4. Authority Lane Boundary Enforcement (Negative Tests)
# ----------------------------------------------------------------------------

def test_research_source_authority_lane_enforcement(
    runtime: UniversalProgramStateRuntime,
    coordinator: ResearchSourceProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
    aggregate_id: str,
):
    """Contrastive tests verifying lane violations are blocked fail-closed."""
    with tenant_scope(tenant_ctx):
        url = "https://example.org/research/lane-violation"
        snippet = "Verifiable data structures ensure provable state machine executions."

        # 1. Analyst attempting admit_source transition directly
        with pytest.raises(ProgramAuthorityLaneViolationError) as exc_info:
            runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="admit_source",
                actor_lane=AuthorityLane.ANALYST,  # Violates required HUNTER lane
                actor_id="usr_analyst_lead",
                context_claims=["workspace_active", "source_origin_valid"],
                state_updates={"origin_url": url},
            )
        assert "actor is in lane 'ANALYST', but contract requires 'HUNTER'" in str(exc_info.value)

        # 2. Legitimate Hunter admission
        rec, _ = coordinator.admit_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_hunter_lead",
            origin_url=url,
            raw_text_snippet=snippet,
        )

        # 3. Hunter attempting verify_source transition
        with pytest.raises(ProgramAuthorityLaneViolationError) as exc_info:
            runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="verify_source",
                actor_lane=AuthorityLane.HUNTER,  # Violates required ANALYST lane
                actor_id="usr_hunter_lead",
                context_claims=["workspace_active", "provenance_hash_verified", "multiplicity_checked"],
                state_updates={"status": "VERIFIED"},
            )
        assert "actor is in lane 'HUNTER', but contract requires 'ANALYST'" in str(exc_info.value)

        # 4. Legitimate Analyst verification
        coordinator.verify_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_analyst_lead",
            source_id=rec.source_id,
        )

        # 4.5. Legitimate Composer registration
        coordinator.register_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_composer_lead",
            source_id=rec.source_id,
        )

        # 5. Hunter attempting approve_source transition (now in SOURCE_REGISTERED state)
        with pytest.raises(ProgramAuthorityLaneViolationError) as exc_info:
            runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="approve_source",
                actor_lane=AuthorityLane.HUNTER,  # Violates required COMMANDER lane
                actor_id="usr_hunter_lead",
                context_claims=["workspace_active", "operator_authorized"],
                state_updates={"status": "ACTIVE"},
            )
        assert "actor is in lane 'HUNTER', but contract requires 'COMMANDER'" in str(exc_info.value)


# ----------------------------------------------------------------------------
# 5. Multi-Tenant Workspace Isolation (Negative Test)
# ----------------------------------------------------------------------------

def test_research_source_cross_workspace_isolation(
    coordinator: ResearchSourceProgramCoordinator,
    test_workspace_id: str,
    foreign_workspace_id: str,
    tenant_ctx: TenantContext,
    foreign_tenant_ctx: TenantContext,
    aggregate_id: str,
):
    """Validates that records cannot be read, verified, or updated across workspaces."""
    # Admit in test_workspace
    with tenant_scope(tenant_ctx):
        rec, _ = coordinator.admit_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_hunter_lead",
            origin_url="https://sec.gov/filings/0001",
            raw_text_snippet="Official SEC 10-K filing excerpt detailing revenue figures.",
        )

    # Attempt access from foreign_workspace
    with tenant_scope(foreign_tenant_ctx):
        with pytest.raises(CrossWorkspaceLeakError):
            coordinator.get_source_record(
                workspace_id=foreign_workspace_id,
                source_id=rec.source_id,
            )

        with pytest.raises(CrossWorkspaceLeakError):
            coordinator.verify_source(
                workspace_id=foreign_workspace_id,
                aggregate_id=aggregate_id,
                actor_id="usr_analyst_alt",
                source_id=rec.source_id,
            )


# ----------------------------------------------------------------------------
# 6. Duplicate-Source Anti-Inflation Syndication Check
# ----------------------------------------------------------------------------

def test_research_source_anti_inflation_and_syndication_detection(
    coordinator: ResearchSourceProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
    aggregate_id: str,
):
    """Validates that syndicated mirrors do not inflate independent source count."""
    with tenant_scope(tenant_ctx):
        syndicated_fixtures = FixtureResearchAdapter.get_syndicated_mirror_fixture()
        primary_wire = syndicated_fixtures[0]

        rec, _ = coordinator.admit_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_hunter_lead",
            origin_url=primary_wire.source_url,
            raw_text_snippet=primary_wire.raw_text_snippet,
            source_platform=primary_wire.source_platform,
            author_outlet=primary_wire.author_outlet,
        )

        # Verify with all 5 syndicated scraper observations
        verified_rec, _ = coordinator.verify_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_analyst_lead",
            source_id=rec.source_id,
            corroborating_observations=syndicated_fixtures[1:],
        )

        mult = verified_rec.source_multiplicity
        # 5 mentions across 5 domains, but identical wire text -> syndication detected
        assert mult["raw_mention_count"] == 5
        assert mult["unique_root_domain_count"] == 5
        assert mult["independent_source_count"] == 1  # Capped at 1 because all share identical wire text
        assert mult["syndication_ratio_bps"] > 0


# ----------------------------------------------------------------------------
# 7. Tampered Hash / Provenance Mismatch (Negative Test)
# ----------------------------------------------------------------------------

def test_research_source_tampered_hash_rejection(
    coordinator: ResearchSourceProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
    aggregate_id: str,
):
    """Detects tampered content hash during verification."""
    with tenant_scope(tenant_ctx):
        rec, _ = coordinator.admit_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_hunter_lead",
            origin_url="https://valid-domain.com/article",
            raw_text_snippet="Original unmodified source snippet content.",
        )

        # Inject tampering: mutate raw_content_excerpt in storage map directly
        tampered_record = ResearchSourceRecord(
            source_id=rec.source_id,
            workspace_id=rec.workspace_id,
            source_type=rec.source_type,
            origin_url=rec.origin_url,
            root_domain=rec.root_domain,
            platform=rec.platform,
            content_sha256=rec.content_sha256,
            raw_content_excerpt="TAMPERED content injected by adversary.",
            author_outlet=rec.author_outlet,
            rights_metadata=rec.rights_metadata,
            version=rec.version,
            supersedes_source_id=rec.supersedes_source_id,
            ancestor_version_hashes=rec.ancestor_version_hashes,
            provenance_record=rec.provenance_record,
            source_multiplicity=rec.source_multiplicity,
            admitted_at=rec.admitted_at,
            verified_at=rec.verified_at,
            status=rec.status,
            receipt_sha256=rec.receipt_sha256,
        )
        coordinator._source_records[rec.source_id] = tampered_record

        with pytest.raises(SourceHashMismatchError) as exc_info:
            coordinator.verify_source(
                workspace_id=test_workspace_id,
                aggregate_id=aggregate_id,
                actor_id="usr_analyst_lead",
                source_id=rec.source_id,
            )
        assert exc_info.value.reason_code == "SOURCE_HASH_MISMATCH"


# ----------------------------------------------------------------------------
# 8. Immutability Protection
# ----------------------------------------------------------------------------

def test_research_source_record_immutability(
    coordinator: ResearchSourceProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
    aggregate_id: str,
):
    """Validates that frozen dataclass fields cannot be modified in place."""
    with tenant_scope(tenant_ctx):
        rec, _ = coordinator.admit_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_hunter_lead",
            origin_url="https://immutable-source.org/paper",
            raw_text_snippet="Immutable record content protecting speaker semantic sovereignty.",
        )

        with pytest.raises((AttributeError, TypeError, ValidationError)):
            rec.raw_content_excerpt = "Silently mutated in place"

        with pytest.raises((AttributeError, TypeError, ValidationError)):
            rec.version = 99


# ----------------------------------------------------------------------------
# 9. Quarantine and Bounded Recovery / Repair Route
# ----------------------------------------------------------------------------

def test_research_source_quarantine_and_bounded_repair(
    runtime: UniversalProgramStateRuntime,
    coordinator: ResearchSourceProgramCoordinator,
    test_workspace_id: str,
    tenant_ctx: TenantContext,
    aggregate_id: str,
):
    """Validates quarantine transition and Commander bounded repair recovery."""
    with tenant_scope(tenant_ctx):
        rec, _ = coordinator.admit_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_hunter_lead",
            origin_url="https://dubious-outlet.net/unverified-rumor",
            raw_text_snippet="Unsubstantiated market rumor regarding regulatory action.",
        )

        # Quarantine source
        quarantined_rec, q_receipt = coordinator.quarantine_source(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_commander_lead",
            source_id=rec.source_id,
            quarantine_reason="Unverified provenance from known disinformation outlet",
        )

        assert quarantined_rec.status == "QUARANTINED"
        # Simulate fault injection into REPAIRING state
        repaired_agg = coordinator.recover_to_repairing(
            aggregate_id=aggregate_id,
            failure_reason="Corrupted external feed source provenance",
            context=tenant_ctx,
            actor_id="usr_commander_lead",
        )
        assert repaired_agg.current_state == "REPAIRING"
        assert repaired_agg.lifecycle == ProgramStateLifecycle.REPAIRING

        # Commander executes repair recovery
        repair_receipt = coordinator.repair_source_state(
            workspace_id=test_workspace_id,
            aggregate_id=aggregate_id,
            actor_id="usr_commander_lead",
            repair_reason="Provenance verified via authenticated cryptographic signature",
        )

        assert repair_receipt["authority_lane"] == "COMMANDER"
        assert runtime.get_aggregate(aggregate_id).current_state == "SOURCE_ADMITTED"
