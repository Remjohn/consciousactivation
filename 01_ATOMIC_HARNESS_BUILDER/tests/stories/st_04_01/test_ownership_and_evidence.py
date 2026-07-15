from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.domain.capability_ownership import (
    CapabilityAuthorityInvalid,
    CapabilityCoverageInvalid,
    CapabilityOwnerKind,
    CapabilityOwnershipDecision,
    CapabilityOwnershipInputInvalid,
)
from tests.stories.st_04_01 import build_context, compile_command


def decision(
    owner_kind: CapabilityOwnerKind,
    *,
    owner_id: str | None = None,
    participants: tuple[str, ...] = (),
    handoff: str | None = None,
) -> CapabilityOwnershipDecision:
    resolved_owner = owner_id or (
        "cmf_builder.test" if owner_kind is CapabilityOwnerKind.CODE else "owner-1"
    )
    return CapabilityOwnershipDecision(
        capability_id="test_capability",
        owner_kind=owner_kind,
        owner_id=resolved_owner,
        reliability_evidence=("attributable_receipt", "deterministic_evidence"),
        cost_evidence=("bounded_local_cost", "no_external_provider"),
        authority_boundary="explicit_authority_boundary",
        handoff_responsibility=handoff,
        ordered_participants=participants,
    )


class OwnershipAndEvidenceTests(unittest.TestCase):
    def test_ac_04_owner_kind_vocabulary_is_exact(self) -> None:
        self.assertEqual(
            tuple(item.value for item in CapabilityOwnerKind),
            ("CODE", "AGENT", "HUMAN", "EXTERNAL", "HYBRID"),
        )

    def test_ac_04_07_every_owner_kind_has_a_valid_explicit_contract(self) -> None:
        self.assertIs(decision(CapabilityOwnerKind.CODE).owner_kind, CapabilityOwnerKind.CODE)
        for kind in (
            CapabilityOwnerKind.AGENT,
            CapabilityOwnerKind.HUMAN,
            CapabilityOwnerKind.EXTERNAL,
        ):
            value = decision(
                kind,
                participants=("owner-1",),
                handoff="owner_reports_result_to_governing_builder_boundary",
            )
            value.validate()
        hybrid = decision(
            CapabilityOwnerKind.HYBRID,
            participants=("owner-1", "owner-2"),
            handoff="owner-1_to_owner-2_then_governed_return",
        )
        hybrid.validate()

    def test_ac_07_non_code_without_participants_or_handoff_fails_closed(self) -> None:
        for kind in (
            CapabilityOwnerKind.AGENT,
            CapabilityOwnerKind.HUMAN,
            CapabilityOwnerKind.EXTERNAL,
            CapabilityOwnerKind.HYBRID,
        ):
            with self.subTest(kind=kind.value), self.assertRaises(
                CapabilityAuthorityInvalid
            ):
                decision(kind)

    def test_ac_07_hybrid_requires_two_ordered_attributable_participants(self) -> None:
        with self.assertRaises(CapabilityAuthorityInvalid):
            decision(
                CapabilityOwnerKind.HYBRID,
                participants=("owner-1",),
                handoff="incomplete_handoff",
            )
        with self.assertRaises(CapabilityAuthorityInvalid):
            decision(
                CapabilityOwnerKind.HYBRID,
                participants=("owner-2", "owner-3"),
                handoff="owner-2_to_owner-3",
            )

    def test_ac_04_code_owner_cannot_silently_absorb_a_handoff(self) -> None:
        with self.assertRaises(CapabilityAuthorityInvalid):
            decision(
                CapabilityOwnerKind.CODE,
                participants=("cmf_builder.test",),
                handoff="unauthorized_handoff",
            )

    def test_ac_05_06_empty_or_duplicate_evidence_fails_closed(self) -> None:
        valid = decision(CapabilityOwnerKind.CODE)
        cases = (
            {"reliability_evidence": ()},
            {"cost_evidence": ()},
            {"reliability_evidence": ("same", "same")},
            {"cost_evidence": ("same", "same")},
        )
        for change in cases:
            with self.subTest(change=change), self.assertRaises(
                CapabilityOwnershipInputInvalid
            ):
                replace(valid, **change)

    def test_ac_02_missing_extra_duplicate_or_renamed_coverage_is_rejected(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        graph = repository.get_capability_ownership_graph(receipt.graph_id)
        assert graph is not None
        renamed = replace(graph.decisions[0], capability_id="renamed_capability")
        extra = replace(graph.decisions[0], capability_id="extra_capability")
        cases = (
            graph.decisions[:-1],
            (*graph.decisions, extra),
            (*graph.decisions, graph.decisions[0]),
            (renamed, *graph.decisions[1:]),
        )
        for changed in cases:
            with self.subTest(changed=tuple(item.capability_id for item in changed)):
                altered = replace(graph, decisions=tuple(changed))
                with self.assertRaises(CapabilityCoverageInvalid):
                    altered.validate()

    def test_ac_05_06_fixture_evidence_makes_no_production_economic_claim(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        graph = repository.get_capability_ownership_graph(receipt.graph_id)
        assert graph is not None
        evidence = " ".join(
            item
            for decision_value in graph.decisions
            for item in (
                *decision_value.reliability_evidence,
                *decision_value.cost_evidence,
            )
        ).lower()
        for invented in ("gpu_price", "provider_benchmark", "production_sla"):
            self.assertNotIn(invented, evidence)


if __name__ == "__main__":
    unittest.main()
