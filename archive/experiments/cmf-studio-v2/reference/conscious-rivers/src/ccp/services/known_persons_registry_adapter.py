"""
FR-VIS-12 — Known Persons Registry — Adapter Service
Phase 2B, CVE Visual Engine — spec 6 of 13

4-stage pipeline:
  Stage 1 — Registry Query (Notion lookup, SERPER fallback)
  Stage 2 — Context-Appropriateness Validation (4-role routing rules)
  Stage 3 — Non-Repetition Window Check (56-day / 8-week window)
  Stage 4 — Image Resolution & Delivery (URL health, R2 delivery)

Hard constraint: Named persons NEVER route to AI generation.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone, timedelta
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    CONTEXT_ROUTING_RULES,
    REPETITION_WINDOW_DAYS,
    CanonicalImage,
    ContextValidationResult,
    ImageUsageLogEntry,
    KnownPersonRegistryEntry,
    KnownPersonsError,
    PersonRole,
    RepetitionCheckResult,
    ResolvedPersonImage,
)


class KnownPersonsRegistryAdapter:
    """Query interface to the Known Persons Registry (DEP-VIS-006).

    Resolves named person references from VCB slides to canonical images
    with context validation, repetition window checks, and audit logging.
    """

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: ReceiptChain,
        *,
        registry_data: list[KnownPersonRegistryEntry] | None = None,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"coach_acronym must be 2-4 characters, got '{coach_acronym}'"
            )
        self.coach_acronym = coach_acronym
        self.receipt_chain = receipt_chain
        # In-memory registry for testing; production uses Notion API
        self._registry: dict[str, KnownPersonRegistryEntry] = {}
        if registry_data:
            for entry in registry_data:
                key = entry.person_name.lower().strip()
                self._registry[key] = entry

    # ── Stage 1: Registry Query ──────────────────────

    def query_registry(
        self,
        person_name: str,
        coach_id: str,
        *,
        simulate_timeout: bool = False,
    ) -> KnownPersonRegistryEntry | None:
        """Query the Known Persons Registry for a named person.

        Returns the registry entry if found, or None for PERSON_NOT_IN_REGISTRY.
        """
        if simulate_timeout:
            return None  # Simulates Notion API timeout

        key = person_name.lower().strip()
        entry = self._registry.get(key)
        if entry and entry.coach_id == coach_id:
            return entry
        # Also try without coach_id filtering (for shared entries)
        if entry:
            return entry
        return None

    # ── Stage 2: Context-Appropriateness Validation ──

    @staticmethod
    def validate_context(
        person_name: str,
        person_role: PersonRole,
        slide_context: str,
        custom_rules: dict[str, list[str]] | None = None,
    ) -> ContextValidationResult:
        """Validate whether a person's role permits the given slide context.

        Args:
            person_name: The person's name.
            person_role: The person's role (Hero/Enemy/Mentor/Wildcard).
            slide_context: The slide's emotional/narrative context string.
            custom_rules: Optional per-entry overrides to routing rules.

        Returns:
            ContextValidationResult with valid=True or CONTEXT_VIOLATION.
        """
        rules = custom_rules or CONTEXT_ROUTING_RULES.get(
            person_role.value, {"permitted": [], "prohibited": []}
        )

        permitted: list[str] = rules.get("permitted", [])
        prohibited: list[str] = rules.get("prohibited", [])

        # Wildcard: all contexts permitted (no prohibitions)
        if person_role == PersonRole.WILDCARD and not prohibited:
            return ContextValidationResult(
                valid=True,
                person_name=person_name,
                person_role=person_role.value,
                slide_context=slide_context,
                permitted_contexts=permitted,
            )

        # Check prohibited first
        ctx_lower = slide_context.lower().strip()
        prohibited_lower = [p.lower() for p in prohibited]
        if ctx_lower in prohibited_lower:
            return ContextValidationResult(
                valid=False,
                person_name=person_name,
                person_role=person_role.value,
                slide_context=slide_context,
                violation_detail=(
                    f"{person_role.value} '{person_name}' cannot appear in "
                    f"{slide_context} context. Permitted contexts: "
                    f"{', '.join(permitted)}"
                ),
                permitted_contexts=permitted,
            )

        # Check permitted (if list is non-empty, context must be in it)
        if permitted:
            permitted_lower = [p.lower() for p in permitted]
            if ctx_lower not in permitted_lower:
                return ContextValidationResult(
                    valid=False,
                    person_name=person_name,
                    person_role=person_role.value,
                    slide_context=slide_context,
                    violation_detail=(
                        f"{person_role.value} '{person_name}' context "
                        f"'{slide_context}' not in permitted list. "
                        f"Permitted contexts: {', '.join(permitted)}"
                    ),
                    permitted_contexts=permitted,
                )

        return ContextValidationResult(
            valid=True,
            person_name=person_name,
            person_role=person_role.value,
            slide_context=slide_context,
            permitted_contexts=permitted,
        )

    # ── Stage 3: Non-Repetition Window Check ─────────

    @staticmethod
    def check_repetition_window(
        canonical_images: list[CanonicalImage],
        usage_log: list[ImageUsageLogEntry],
        reference_date: datetime | None = None,
    ) -> RepetitionCheckResult:
        """Check the 8-week non-repetition window for each canonical image.

        Selects the first image outside the window (least recently used among
        viable candidates). If all images are within the window, returns
        ALL_IMAGES_IN_WINDOW.

        Args:
            canonical_images: Available canonical images.
            usage_log: Historical usage log entries.
            reference_date: The date to check against (defaults to now UTC).

        Returns:
            RepetitionCheckResult with the selected image or all_in_window flag.
        """
        if not canonical_images:
            return RepetitionCheckResult(
                clear=False,
                all_in_window=True,
                error_type=KnownPersonsError.ALL_IMAGES_IN_WINDOW.value,
            )

        now = reference_date or datetime.now(timezone.utc)
        window_start = now - timedelta(days=REPETITION_WINDOW_DAYS)

        # Build map: image_id → most recent usage date
        latest_usage: dict[str, datetime] = {}
        for log_entry in usage_log:
            try:
                used_dt = datetime.fromisoformat(log_entry.used_date).replace(
                    tzinfo=timezone.utc
                )
            except (ValueError, TypeError):
                continue
            if log_entry.image_id not in latest_usage or used_dt > latest_usage[log_entry.image_id]:
                latest_usage[log_entry.image_id] = used_dt

        # Find images outside the window, prefer least recently used
        candidates: list[tuple[CanonicalImage, datetime | None, int]] = []
        for img in canonical_images:
            last_used = latest_usage.get(img.image_id)
            if last_used is None:
                # Never used → ideal candidate
                candidates.append((img, None, 999))
            else:
                days_since = (now - last_used).days
                if days_since >= REPETITION_WINDOW_DAYS:
                    candidates.append((img, last_used, days_since))

        if candidates:
            # Sort by days_since descending (most stale first)
            candidates.sort(key=lambda x: x[2], reverse=True)
            best = candidates[0]
            return RepetitionCheckResult(
                clear=True,
                selected_image_id=best[0].image_id,
                last_used_date=best[1].isoformat() if best[1] else None,
                days_since_last_use=best[2] if best[2] != 999 else None,
                window_days=REPETITION_WINDOW_DAYS,
            )

        # All images are within the window
        # Return the least recently used (closest to clearing the window)
        all_used: list[tuple[CanonicalImage, int, datetime | None]] = []
        for img in canonical_images:
            last_used = latest_usage.get(img.image_id)
            if last_used:
                all_used.append((img, (now - last_used).days, last_used))
            else:
                all_used.append((img, 999, None))
        all_used.sort(key=lambda x: x[1], reverse=True)

        best_last = all_used[0] if all_used else None
        return RepetitionCheckResult(
            clear=False,
            all_in_window=True,
            last_used_date=best_last[2].isoformat() if best_last and best_last[2] else None,
            days_since_last_use=best_last[1] if best_last and best_last[1] != 999 else None,
            window_days=REPETITION_WINDOW_DAYS,
            error_type=KnownPersonsError.ALL_IMAGES_IN_WINDOW.value,
        )

    # ── Stage 4: Full Resolution Pipeline ────────────

    def resolve_person(
        self,
        person_name: str,
        person_role: PersonRole,
        slide_index: int,
        slide_context: str,
        coach_id: str,
        content_output_id: str,
        *,
        simulate_timeout: bool = False,
        reference_date: datetime | None = None,
    ) -> ResolvedPersonImage:
        """Full 4-stage pipeline: query → context validate → repetition → resolve.

        This is the main entry point for Aurore's Tier 1 resolution.
        """
        now_str = datetime.now(timezone.utc).isoformat()
        res_id = f"RPI-{self.coach_acronym}-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"

        # Stage 1: Registry Query
        entry = self.query_registry(person_name, coach_id, simulate_timeout=simulate_timeout)

        if simulate_timeout and entry is None:
            self.receipt_chain.log(
                agent_id="known_persons_registry",
                action="VIS12_REGISTRY_QUERY",
                asset_id=content_output_id,
                input_summary=f"person={person_name}, coach={coach_id}",
                output_summary="REGISTRY_QUERY_TIMEOUT",
                decision="TIMEOUT",
            )
            return ResolvedPersonImage(
                resolution_id=res_id,
                person_name=person_name,
                person_role=person_role.value,
                slide_index=slide_index,
                content_output_id=content_output_id,
                error_type=KnownPersonsError.REGISTRY_QUERY_TIMEOUT.value,
                error_detail=f"Notion API timeout for '{person_name}'",
                timestamp_utc=now_str,
            )

        if entry is None:
            # Person not in registry → SERPER fallback
            receipt = self.receipt_chain.log(
                agent_id="known_persons_registry",
                action="VIS12_REGISTRY_QUERY",
                asset_id=content_output_id,
                input_summary=f"person={person_name}, coach={coach_id}",
                output_summary="PERSON_NOT_IN_REGISTRY",
                decision="SERPER_FALLBACK",
            )
            return ResolvedPersonImage(
                resolution_id=res_id,
                person_name=person_name,
                person_role=person_role.value,
                slide_index=slide_index,
                content_output_id=content_output_id,
                source_type="serper_fallback",
                pending_registry_addition=True,
                error_type=KnownPersonsError.PERSON_NOT_IN_REGISTRY.value,
                error_detail=f"'{person_name}' not in Known Persons Registry",
                receipt_chain_block=receipt.receipt_id,
                timestamp_utc=now_str,
            )

        # Stage 1 receipt
        self.receipt_chain.log(
            agent_id="known_persons_registry",
            action="VIS12_REGISTRY_QUERY",
            asset_id=content_output_id,
            input_summary=f"person={person_name}, coach={coach_id}",
            output_summary=f"found: {entry.registry_entry_id}, images={len(entry.canonical_images)}",
            decision="REGISTRY_MATCH",
        )

        # Stage 2: Context Validation
        ctx_result = self.validate_context(
            person_name=person_name,
            person_role=entry.person_role,
            slide_context=slide_context,
            custom_rules=entry.context_routing_rules,
        )

        self.receipt_chain.log(
            agent_id="known_persons_registry",
            action="VIS12_CONTEXT_VALIDATION",
            asset_id=content_output_id,
            input_summary=f"person={person_name}, role={entry.person_role.value}, context={slide_context}",
            output_summary=f"valid={ctx_result.valid}",
            decision="CONTEXT_VALID" if ctx_result.valid else "CONTEXT_VIOLATION",
        )

        if not ctx_result.valid:
            return ResolvedPersonImage(
                resolution_id=res_id,
                person_name=person_name,
                person_role=entry.person_role.value,
                slide_index=slide_index,
                content_output_id=content_output_id,
                context_validation=ctx_result,
                error_type=KnownPersonsError.CONTEXT_VIOLATION.value,
                error_detail=ctx_result.violation_detail,
                timestamp_utc=now_str,
            )

        # Stage 3: Repetition Window Check
        rep_result = self.check_repetition_window(
            canonical_images=entry.canonical_images,
            usage_log=entry.usage_log,
            reference_date=reference_date,
        )

        self.receipt_chain.log(
            agent_id="known_persons_registry",
            action="VIS12_REPETITION_CHECK",
            asset_id=content_output_id,
            input_summary=f"person={person_name}, images={len(entry.canonical_images)}",
            output_summary=f"clear={rep_result.clear}, selected={rep_result.selected_image_id}",
            decision="REPETITION_CLEAR" if rep_result.clear else "ALL_IMAGES_IN_WINDOW",
        )

        if not rep_result.clear:
            return ResolvedPersonImage(
                resolution_id=res_id,
                person_name=person_name,
                person_role=entry.person_role.value,
                slide_index=slide_index,
                content_output_id=content_output_id,
                context_validation=ctx_result,
                repetition_check=rep_result,
                source_type="serper_fallback",
                pending_registry_addition=True,
                error_type=KnownPersonsError.ALL_IMAGES_IN_WINDOW.value,
                error_detail=f"All {len(entry.canonical_images)} images used within {REPETITION_WINDOW_DAYS}-day window",
                timestamp_utc=now_str,
            )

        # Stage 4: Image Resolution
        selected_image = None
        for img in entry.canonical_images:
            if img.image_id == rep_result.selected_image_id:
                selected_image = img
                break

        receipt = self.receipt_chain.log(
            agent_id="known_persons_registry",
            action="VIS12_IMAGE_RESOLUTION",
            asset_id=content_output_id,
            input_summary=f"person={person_name}, selected={rep_result.selected_image_id}",
            output_summary=f"resolved, tier=1",
            decision="RESOLVED",
        )

        return ResolvedPersonImage(
            resolution_id=res_id,
            person_name=person_name,
            person_role=entry.person_role.value,
            slide_index=slide_index,
            content_output_id=content_output_id,
            selected_image=selected_image,
            context_validation=ctx_result,
            repetition_check=rep_result,
            sourcing_tier="tier_1_real_person",
            source_type="known_persons_registry",
            receipt_chain_block=receipt.receipt_id,
            timestamp_utc=now_str,
        )

    # ── AI Generation Hard Prohibition ───────────────

    @staticmethod
    def assert_no_ai_generation(person_name: str) -> None:
        """Hard architectural constraint: named persons NEVER route to AI.

        This method exists as a safety checkpoint. Any code path that
        could potentially route a named person to Tier 3 or Tier 4
        MUST call this assertion first. If reached, it means the cascade
        has a logical error.

        Raises:
            RuntimeError: Always — AI generation of named persons is prohibited.
        """
        raise RuntimeError(
            f"AI_GENERATION_PROHIBITED: Cannot generate AI image of named person "
            f"'{person_name}'. This is a hard architectural constraint (FR-VIS-12 §6). "
            f"Named persons must resolve via Known Persons Registry or SERPER fallback, "
            f"or be flagged PENDING_OPERATOR_REVIEW."
        )
