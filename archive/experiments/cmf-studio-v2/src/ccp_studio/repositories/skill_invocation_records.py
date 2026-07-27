"""Skill invocation repositories for TS-CMF-015."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.skills import (
    AntiDraftCalibrationReport,
    CompilerCandidateSet,
    ContrastivePromptLayer,
    DSPyProgramSpec,
    JITSkillCompiler,
    SkillInvocationReceipt,
)


@dataclass
class InMemorySkillInvocationRepository:
    dspy_program_specs: dict[UUID, DSPyProgramSpec] = field(default_factory=dict)
    compilers: dict[str, JITSkillCompiler] = field(default_factory=dict)
    contrastive_layers: dict[UUID, ContrastivePromptLayer] = field(default_factory=dict)
    candidate_sets: dict[UUID, CompilerCandidateSet] = field(default_factory=dict)
    calibration_reports: dict[UUID, AntiDraftCalibrationReport] = field(default_factory=dict)
    invocation_receipts: dict[UUID, SkillInvocationReceipt] = field(default_factory=dict)

    def put_program_spec(self, spec: DSPyProgramSpec) -> DSPyProgramSpec:
        self.dspy_program_specs[spec.dspy_program_spec_id] = spec
        return spec

    def put_compiler(self, compiler: JITSkillCompiler) -> JITSkillCompiler:
        self.compilers[compiler.skill_key] = compiler
        return compiler

    def put_contrastive_layer(self, layer: ContrastivePromptLayer) -> ContrastivePromptLayer:
        self.contrastive_layers[layer.contrastive_prompt_layer_id] = layer
        return layer

    def put_candidate_set(self, candidate_set: CompilerCandidateSet) -> CompilerCandidateSet:
        self.candidate_sets[candidate_set.compiler_candidate_set_id] = candidate_set
        return candidate_set

    def put_calibration_report(self, report: AntiDraftCalibrationReport) -> AntiDraftCalibrationReport:
        self.calibration_reports[report.anti_draft_calibration_report_id] = report
        return report

    def put_invocation_receipt(self, receipt: SkillInvocationReceipt) -> SkillInvocationReceipt:
        self.invocation_receipts[receipt.skill_invocation_receipt_id] = receipt
        return receipt
