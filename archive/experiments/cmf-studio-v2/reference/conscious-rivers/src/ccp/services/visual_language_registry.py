"""
CCP FR6 — Visual Recognition Code & Language Registry (Phase B4) (Unit 5)
Insider/rejection/sacred visual codes + safe/sacred/outsider vocabulary.

Spec reference: FR6 Tech Spec §Phase B4
  Visual Recognition Codes:
    - INSIDER OBJECTS (≥5): objects/scenes tribe recognizes instantly as "us"
    - REJECTION TRIGGERS (≥3): visuals that signal "outsider" or "tourist"
    - SACRED OBJECTS (≥2): visuals the tribe considers precious

  In-Group Language Registry:
    - SAFE vocabulary (≥10 terms): can use freely in content
    - SACRED vocabulary: use only in specific emotional contexts
    - OUTSIDER vocabulary (≥5 terms): NEVER use — signals inauthenticity

Gate (Law 3): ≥10 safe terms, ≥5 outsider terms.
"""

from typing import Any

from src.ccp.models.tribe_profile_models import (
    LanguageRegistryEntry,
    LanguageRegisterType,
    VisualCodeType,
    VisualRecognitionCode,
)


class VisualLanguageRegistry:
    """FR6 Phase B4: Visual Recognition Code & In-Group Language Registry.

    Processes tribe profile data into classified visual codes and
    language registry entries.

    AC6: ≥5 insider objects, ≥3 rejection triggers.
    AC7: ≥10 safe terms with context, ≥5 outsider terms with alternatives.
    """

    # ── Visual Code Thresholds (AC6) ──
    MIN_INSIDER_OBJECTS = 5
    MIN_REJECTION_TRIGGERS = 3
    MIN_SACRED_OBJECTS = 2

    # ── Language Registry Thresholds (AC7 / Law 3) ──
    MIN_SAFE_TERMS = 10
    MIN_OUTSIDER_TERMS = 5

    # ──────────────────────────────────────────────────────────
    # Visual Recognition Codes
    # ──────────────────────────────────────────────────────────

    def classify_visual_code(
        self,
        description: str,
        tribe_significance: str = "",
        handling_notes: str = "",
    ) -> VisualCodeType:
        """Classify a visual code as insider/rejection/sacred.
        Uses significance and handling signals."""
        desc_lower = description.lower()
        sig_lower = tribe_significance.lower()

        # Sacred detection: handling notes present or sacred keywords
        sacred_signals = [
            "precious", "sacred", "honored", "ancestral",
            "heritage", "ritual", "ceremony", "memorial",
        ]
        if handling_notes or any(s in desc_lower or s in sig_lower for s in sacred_signals):
            return VisualCodeType.SACRED

        # Rejection detection
        rejection_signals = [
            "outsider", "tourist", "fake", "corporate",
            "stock photo", "generic", "inauthentic", "cringe",
            "reject", "hate", "avoid",
        ]
        if any(s in desc_lower or s in sig_lower for s in rejection_signals):
            return VisualCodeType.REJECTION

        # Default: insider
        return VisualCodeType.INSIDER

    def validate_visual_codes(
        self,
        codes: list[VisualRecognitionCode],
    ) -> dict[str, bool | int]:
        """AC6: Validate visual code quotas."""
        insider_count = sum(1 for c in codes if c.code_type == VisualCodeType.INSIDER)
        rejection_count = sum(1 for c in codes if c.code_type == VisualCodeType.REJECTION)
        sacred_count = sum(1 for c in codes if c.code_type == VisualCodeType.SACRED)

        return {
            "insider_objects_pass": insider_count >= self.MIN_INSIDER_OBJECTS,
            "rejection_triggers_pass": rejection_count >= self.MIN_REJECTION_TRIGGERS,
            "sacred_objects_pass": sacred_count >= self.MIN_SACRED_OBJECTS,
            "insider_count": insider_count,
            "rejection_count": rejection_count,
            "sacred_count": sacred_count,
            "all_pass": (
                insider_count >= self.MIN_INSIDER_OBJECTS
                and rejection_count >= self.MIN_REJECTION_TRIGGERS
            ),
        }

    # ──────────────────────────────────────────────────────────
    # In-Group Language Registry
    # ──────────────────────────────────────────────────────────

    def classify_language_register(
        self,
        term: str,
        context: str = "",
        why_rejected: str = "",
        misuse_risk: str = "",
    ) -> LanguageRegisterType:
        """Classify a term as safe/sacred/outsider."""
        # If explicitly rejected
        if why_rejected:
            return LanguageRegisterType.OUTSIDER

        # If misuse risk identified → sacred
        if misuse_risk:
            return LanguageRegisterType.SACRED

        # Context-based classification
        context_lower = context.lower()
        sacred_signals = [
            "only in", "careful", "specific context",
            "sacred", "ritual", "ceremony", "grief",
            "loss", "memorial",
        ]
        if any(s in context_lower for s in sacred_signals):
            return LanguageRegisterType.SACRED

        outsider_signals = [
            "never use", "cringe", "tourist", "outsider",
            "fake", "corporate", "inauthentic",
        ]
        if any(s in context_lower for s in outsider_signals):
            return LanguageRegisterType.OUTSIDER

        return LanguageRegisterType.SAFE

    def validate_language_registry(
        self,
        entries: list[LanguageRegistryEntry],
    ) -> dict[str, bool | int]:
        """AC7 / Law 3: Validate language registry quotas.
        ≥10 safe terms, ≥5 outsider terms."""
        safe_count = sum(
            1 for e in entries if e.register == LanguageRegisterType.SAFE
        )
        outsider_count = sum(
            1 for e in entries if e.register == LanguageRegisterType.OUTSIDER
        )

        # Check outsider terms have "use instead" alternatives
        outsider_with_alt = sum(
            1 for e in entries
            if e.register == LanguageRegisterType.OUTSIDER and e.use_instead
        )

        # Check safe terms have context examples
        safe_with_context = sum(
            1 for e in entries
            if e.register == LanguageRegisterType.SAFE and e.example_usage
        )

        return {
            "safe_terms_pass": safe_count >= self.MIN_SAFE_TERMS,
            "outsider_terms_pass": outsider_count >= self.MIN_OUTSIDER_TERMS,
            "outsider_with_alternatives": outsider_with_alt,
            "safe_with_context": safe_with_context,
            "safe_count": safe_count,
            "outsider_count": outsider_count,
            "all_pass": (
                safe_count >= self.MIN_SAFE_TERMS
                and outsider_count >= self.MIN_OUTSIDER_TERMS
            ),
        }

    # ──────────────────────────────────────────────────────────
    # Combined Validation (Law 2 + Law 3)
    # ──────────────────────────────────────────────────────────

    def validate_all(
        self,
        visual_codes: list[VisualRecognitionCode],
        language_entries: list[LanguageRegistryEntry],
    ) -> dict[str, Any]:
        """Combined validation for Phase B4 outputs."""
        visual_result = self.validate_visual_codes(visual_codes)
        language_result = self.validate_language_registry(language_entries)
        return {
            "visual": visual_result,
            "language": language_result,
            "all_pass": visual_result["all_pass"] and language_result["all_pass"],
        }
