"""
cae_asset_intelligence
----------------------
The Multimodal Asset Intelligence and E/D-Roll package for CAE.
"""

from .domain import (
    SourceType,
    MediaType,
    EditorialInsertRole,
    RightsStatus,
    RightsMetadata,
    AssetAnnotation,
    AssetCatalog,
)
from .errors import (
    AssetIntelligenceError,
    AssetByteHashMismatchError,
    MissingRightsEvidenceError,
    InsertRoleContextMismatchError,
    GenericCaptionRejectedError,
    DurationConstraintViolationError,
)
from .annotator import AssetAnnotator
from .verifier import AssetIntelligenceVerifier

__all__ = [
    "SourceType",
    "MediaType",
    "EditorialInsertRole",
    "RightsStatus",
    "RightsMetadata",
    "AssetAnnotation",
    "AssetCatalog",
    "AssetIntelligenceError",
    "AssetByteHashMismatchError",
    "MissingRightsEvidenceError",
    "InsertRoleContextMismatchError",
    "GenericCaptionRejectedError",
    "DurationConstraintViolationError",
    "AssetAnnotator",
    "AssetIntelligenceVerifier",
]

from .demand_contract import (
    AssetDemandResolutionContract,
    AssetDemandResolver,
    AssetDemandValidationError,
    AssetDurationConstraint,
    AssetRef,
    AssetResolutionError,
    AssetResolutionOutcome,
    AssetResolutionState,
    AssetRightsConstraint,
    AssetSemanticObligation,
    PhysicalMediaRequirement,
    ProductionAssetDemand,
    compile_production_asset_demand,
)

__all__ += [
    "AssetDemandResolutionContract",
    "AssetDemandResolver",
    "AssetDemandValidationError",
    "AssetDurationConstraint",
    "AssetRef",
    "AssetResolutionError",
    "AssetResolutionOutcome",
    "AssetResolutionState",
    "AssetRightsConstraint",
    "AssetSemanticObligation",
    "PhysicalMediaRequirement",
    "ProductionAssetDemand",
    "compile_production_asset_demand",
]

from .corpus import (
    AuthorizationError,
    CorpusIngestionError,
    CorpusIntegrityError,
    CorpusState,
    CinematicCorpusEngine,
    IngestReceipt,
    MediaAuthorization,
    SceneBoundaryError,
    SceneIndex,
    SceneProposal,
    SceneRecord,
    TranscriptCue,
    stable_media_id,
    stable_scene_id,
)
from .corpus_store import SceneCorpusStore

__all__ += [
    "AuthorizationError",
    "CorpusIngestionError",
    "CorpusIntegrityError",
    "CorpusState",
    "CinematicCorpusEngine",
    "IngestReceipt",
    "MediaAuthorization",
    "SceneBoundaryError",
    "SceneIndex",
    "SceneProposal",
    "SceneRecord",
    "TranscriptCue",
    "SceneCorpusStore",
    "stable_media_id",
    "stable_scene_id",
]

from .retrieval import (
    DeterministicSemanticEncoder,
    EmbeddingModel,
    RetrievalCandidate,
    RetrievalError,
    RetrievalQuery,
    RetrievalReceipt,
    RetrievalState,
    RightsPolicy,
    SemanticCinematicRetriever,
)

__all__ += [
    "DeterministicSemanticEncoder",
    "EmbeddingModel",
    "RetrievalCandidate",
    "RetrievalError",
    "RetrievalQuery",
    "RetrievalReceipt",
    "RetrievalState",
    "RightsPolicy",
    "SemanticCinematicRetriever",
]

from .research_session import (
    AssetPromotionRequest,
    AssetResearchCandidate,
    AssetResearchError,
    AssetResearchMode,
    AssetResearchRequest,
    AssetResearchSession,
    AssetResearchSessionFactory,
    AssetResearchSessionState,
    CandidateSelectionError,
    CandidateSelectionReceipt,
    PlayPhraseTemporalAdapter,
    PlayablePreviewRef,
    RangeMode,
    ResearchSourceRef,
    SourceTimeRange,
    TranscriptExcerpt,
)

__all__ += [
    "AssetPromotionRequest",
    "AssetResearchCandidate",
    "AssetResearchError",
    "AssetResearchMode",
    "AssetResearchRequest",
    "AssetResearchSession",
    "AssetResearchSessionFactory",
    "AssetResearchSessionState",
    "CandidateSelectionError",
    "CandidateSelectionReceipt",
    "PlayPhraseTemporalAdapter",
    "PlayablePreviewRef",
    "RangeMode",
    "ResearchSourceRef",
    "SourceTimeRange",
    "TranscriptExcerpt",
]

from .candidate_preview import (
    AcceptancePolicyRegistry,
    AutoAcceptanceBlockedError,
    CandidateDecision,
    CandidateDecisionReceipt,
    CandidatePortfolio,
    CandidatePreviewCard,
    CandidatePreviewError,
    CandidatePreviewSession,
    CandidateSelectionError,
    CandidateSourceRef,
    CandidateStaleVersionError,
    NavigationDirection,
    build_portfolio,
    decide_session,
    navigate_session,
)

__all__ += [
    "AcceptancePolicyRegistry",
    "AutoAcceptanceBlockedError",
    "CandidateDecision",
    "CandidateDecisionReceipt",
    "CandidatePortfolio",
    "CandidatePreviewCard",
    "CandidatePreviewError",
    "CandidatePreviewSession",
    "CandidateSelectionError",
    "CandidateSourceRef",
    "CandidateStaleVersionError",
    "NavigationDirection",
    "build_portfolio",
    "decide_session",
    "navigate_session",
]
