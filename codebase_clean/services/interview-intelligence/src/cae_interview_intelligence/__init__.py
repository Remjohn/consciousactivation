"""
cae_interview_intelligence
--------------------------
The Interview Semantic Program and Human-First Elicitation package for CAE.
"""

from .domain import (
    QuestionStage,
    DesiredEvidenceClass,
    InterviewQuestion,
    AdaptiveFollowUpPolicy,
    MatrixOfEdgingConfig,
    InterviewBrief,
    InterviewTurnResponse,
    InterviewSessionResult,
)
from .errors import (
    InterviewIntelligenceError,
    ScriptedAnswerViolationError,
    GenericResponseFailureError,
    UnauthenticatedSessionError,
    EdgingBoundaryExceededError,
    PrematureContentError,
)
from .composer import InterviewBriefComposer
from .verifier import InterviewSessionVerifier
from .hypothesis_adapter import (
    CandidateState,
    SemanticRef,
    Provenance,
    SelectionDiagnostics,
    CoordinateBasis,
    HypothesisCandidate,
    CandidateCluster,
    PortfolioSelectionResult,
    HypothesisPortfolioAdapter,
)
from .question_resolver import (
    AnswerResolution,
    InformationCompleteness,
    InquiryStateTransition,
    EvidenceMode,
    TemporalOrientation,
    SocialReferenceFrame,
    MechanismDisposition,
    ProvisionalMechanism,
    APPROVED_PROVISIONAL_MECHANISMS,
    CompositionCompatibility,
    QuestionCandidate,
    AnswerRoutingProfile,
    QuestionProgramDerived,
    QuestionIntelligenceResolver,
)

from .brief_compiler import ActivativeInterviewBriefCompiler
from .operator_studio import (
    OperatorActionType,
    OperatorFeedback,
    CandidateReviewItem,
    StudioSession,
    OperatorStudioService,
)
from .adaptive_frontier import (
    AdaptiveAction,
    RequirementStatus,
    EvidenceRequirement,
    CoverageSpineItem,
    AnswerObservation,
    QuestionAttempt,
    FrontierState,
    AdaptiveQuestionFrontierEngine,
)
from .semantic_acquisition import (
    EvidenceLineageKind,
    AcquisitionEvidenceRecord,
    DiscrepancyRecord,
    SemanticAcquisitionObservation,
    SemanticAcquisitionObserver,
)

from .composition_compatibility import (
    ArchetypeSpec,
    FormatSpec,
    NarrativeRoleSpec,
    KNOWN_ARCHETYPES,
    KNOWN_FORMATS,
    KNOWN_NARRATIVE_ROLES,
    CompositionCompatibilityEvaluator,
)

from .evidence_handoff import (
    SourceReference,
    QuestionAttemptRef,
    AcceptedEvidenceRecord,
    DownstreamContentCandidate,
    AuthenticatedEvidencePackage,
    LineageTraceNode,
    AuthenticatedEvidenceHandoffEngine,
)

from .content_menu import (
    ContentCandidateMenuStatus,
    MenuCandidateDiagnostics,
    MenuCandidateItem,
    ContentMenuCluster,
    ContentCandidateMenu,
    ContentMenuReadinessEngine,
)

__all__ = [
    "QuestionStage",
    "DesiredEvidenceClass",
    "InterviewQuestion",
    "AdaptiveFollowUpPolicy",
    "MatrixOfEdgingConfig",
    "InterviewBrief",
    "InterviewTurnResponse",
    "InterviewSessionResult",
    "InterviewIntelligenceError",
    "ScriptedAnswerViolationError",
    "GenericResponseFailureError",
    "UnauthenticatedSessionError",
    "EdgingBoundaryExceededError",
    "PrematureContentError",
    "InterviewBriefComposer",
    "InterviewSessionVerifier",
    "CandidateState",
    "SemanticRef",
    "Provenance",
    "SelectionDiagnostics",
    "CoordinateBasis",
    "HypothesisCandidate",
    "CandidateCluster",
    "PortfolioSelectionResult",
    "HypothesisPortfolioAdapter",
    "AnswerResolution",
    "InformationCompleteness",
    "InquiryStateTransition",
    "EvidenceMode",
    "TemporalOrientation",
    "SocialReferenceFrame",
    "MechanismDisposition",
    "ProvisionalMechanism",
    "APPROVED_PROVISIONAL_MECHANISMS",
    "CompositionCompatibility",
    "QuestionCandidate",
    "AnswerRoutingProfile",
    "QuestionProgramDerived",
    "QuestionIntelligenceResolver",
    "ActivativeInterviewBriefCompiler",
    "OperatorActionType",
    "OperatorFeedback",
    "CandidateReviewItem",
    "StudioSession",
    "OperatorStudioService",
    "AdaptiveAction",
    "RequirementStatus",
    "EvidenceRequirement",
    "CoverageSpineItem",
    "AnswerObservation",
    "QuestionAttempt",
    "FrontierState",
    "AdaptiveQuestionFrontierEngine",
    "EvidenceLineageKind",
    "AcquisitionEvidenceRecord",
    "DiscrepancyRecord",
    "SemanticAcquisitionObservation",
    "SemanticAcquisitionObserver",
    "ArchetypeSpec",
    "FormatSpec",
    "NarrativeRoleSpec",
    "KNOWN_ARCHETYPES",
    "KNOWN_FORMATS",
    "KNOWN_NARRATIVE_ROLES",
    "CompositionCompatibilityEvaluator",
    "SourceReference",
    "QuestionAttemptRef",
    "AcceptedEvidenceRecord",
    "DownstreamContentCandidate",
    "AuthenticatedEvidencePackage",
    "LineageTraceNode",
    "AuthenticatedEvidenceHandoffEngine",
    "ContentCandidateMenuStatus",
    "MenuCandidateDiagnostics",
    "MenuCandidateItem",
    "ContentMenuCluster",
    "ContentCandidateMenu",
    "ContentMenuReadinessEngine",
]






