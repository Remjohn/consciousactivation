"""
Stage 2 Runner for Visual Syntax Composition Compiler.
Orchestrates Stage 2 execution for single harnesses or batch processing.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict, Any, List
import json

from .input_adapter import build_compiler_input
from .composition_compiler import CompositionCompiler, SpecificationValidationError


@dataclass
class Stage2Config:
    harness_id: str
    stage1_report_path: Path
    output_dir: Path
    skill_ref: str = "visual_syntax_composition_compiler@1.0.0"


@dataclass
class Stage2RunResult:
    harness_id: str
    status: str
    spec_path: Optional[Path]
    report_path: Path
    deduplication_hash: Optional[str]
    stage2_complete: bool
    findings: List[Dict[str, Any]]


class Stage2Runner:
    def __init__(self, config: Stage2Config):
        self.config = config
        self.output_dir = self.config.output_dir
        self.specs_dir = self.output_dir / "specs"
        self.reports_dir = self.output_dir / "reports"
        
        self.specs_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> Stage2RunResult:
        harness_id = self.config.harness_id
        report_path = self.reports_dir / f"{harness_id}_STAGE2_REPORT.json"
        
        if not self.config.stage1_report_path.exists():
            findings = [{
                "rule": "STAGE1_REPORT_MISSING",
                "severity": "ERROR",
                "message": f"Stage 1 report not found at {self.config.stage1_report_path}"
            }]
            result = Stage2RunResult(
                harness_id=harness_id,
                status="FAIL",
                spec_path=None,
                report_path=report_path,
                deduplication_hash=None,
                stage2_complete=False,
                findings=findings
            )
            self._write_report(result)
            return result

        try:
            with open(self.config.stage1_report_path, "r", encoding="utf-8") as f:
                stage1_data = json.load(f)

            # Build compiler input payload
            compiler_input = build_compiler_input(stage1_data)

            # Execute composition compiler
            compiler = CompositionCompiler(skill_ref=self.config.skill_ref)
            composition_spec = compiler.compile(compiler_input)

            # Write spec output
            spec_path = self.specs_dir / f"{harness_id}_STAGE2_SPEC.json"
            with open(spec_path, "w", encoding="utf-8") as f:
                json.dump(composition_spec, f, indent=2)

            dedup_hash = composition_spec.get("deduplication_hash")
            
            result = Stage2RunResult(
                harness_id=harness_id,
                status="PASS",
                spec_path=spec_path,
                report_path=report_path,
                deduplication_hash=dedup_hash,
                stage2_complete=True,
                findings=[]
            )
            self._write_report(result)
            return result

        except SpecificationValidationError as e:
            findings = getattr(e, "findings", None)
            if not findings:
                findings = [{
                    "rule": "COMPILATION_VALIDATION_ERROR",
                    "severity": "ERROR",
                    "message": str(e)
                }]
            result = Stage2RunResult(
                harness_id=harness_id,
                status="FAIL",
                spec_path=None,
                report_path=report_path,
                deduplication_hash=None,
                stage2_complete=False,
                findings=findings
            )
            self._write_report(result)
            return result

        except Exception as e:
            findings = [{
                "rule": "UNHANDLED_RUNNER_ERROR",
                "severity": "ERROR",
                "message": str(e)
            }]
            result = Stage2RunResult(
                harness_id=harness_id,
                status="FAIL",
                spec_path=None,
                report_path=report_path,
                deduplication_hash=None,
                stage2_complete=False,
                findings=findings
            )
            self._write_report(result)
            return result

    def _write_report(self, result: Stage2RunResult):
        report_data = {
            "harness_id": result.harness_id,
            "technical_status": result.status,
            "stage2_complete": result.stage2_complete,
            "deduplication_hash": result.deduplication_hash,
            "spec_path": str(result.spec_path) if result.spec_path else None,
            "findings": result.findings,
            "operator_review": {
                "disposition": "APPROVE" if result.stage2_complete else "REJECT",
                "reviewed_by": "stage2_runner",
                "reviewed_at": "2026-08-12"
            }
        }
        with open(result.report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
