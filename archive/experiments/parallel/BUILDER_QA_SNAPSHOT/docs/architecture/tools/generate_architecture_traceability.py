"""Generate FR/NFR to architecture component and ADR traceability."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TECH = ROOT / "docs/tech-specs"
OUT = ROOT / "docs/architecture/ARCHITECTURE_TRACEABILITY_MATRIX.csv"

OWNERS = {
    "IMPLEMENTATION_BASELINE": ("C18", "External Contract Ports", "ADR-015"),
    "TS-01": ("C01", "Run Governance", "ADR-001;ADR-003;ADR-005"),
    "TS-02": ("C02", "Evidence Workspace", "ADR-003;ADR-007;ADR-012"),
    "TS-03": ("C03", "Visual Understanding", "ADR-008;ADR-012"),
    "TS-04": ("C04", "Atomicity", "ADR-005;ADR-008;ADR-014"),
    "TS-05": ("C05", "Genesis", "ADR-003;ADR-005"),
    "TS-06": ("C06", "Harness IR And Compilers", "ADR-002;ADR-003;ADR-004"),
    "TS-07": ("C07", "Architecture Graphs", "ADR-001;ADR-002;ADR-004;ADR-005"),
    "TS-08": ("C08", "Skill Ecology", "ADR-009;ADR-010"),
    "TS-09": ("C09", "JIT Capsule Compiler", "ADR-004;ADR-009"),
    "TS-10": ("C10", "Evaluation", "ADR-003;ADR-010"),
    "TS-11": ("C11", "Category And Target Compilers", "ADR-013;ADR-014;ADR-018"),
    "TS-12": ("C12", "Control Tower", "ADR-003;ADR-011;ADR-016"),
    "TS-13": ("C13", "Repair, Authorization, Handoff", "ADR-003;ADR-004;ADR-005;ADR-010"),
    "TS-14": ("C14", "Workflow Runtime", "ADR-002;ADR-006;ADR-012;ADR-016;ADR-017"),
    "TS-15": ("C15", "Format 02 Reference Slice", "ADR-014;ADR-018"),
}

MECHANISMS = {
    "TS-01": "event-sourced Run aggregate, target profiles, guarded state machine, authority receipts, checkpoints",
    "TS-02": "source profiles, immutable Source Lock, reaction/expression consent and evidence spans, safe adapters, saturation contract",
    "TS-03": "Visual Syntax First development parsing, Activation First runtime guard, provider port, typed visual/conversational evidence",
    "TS-04": "candidate-boundary graph, typed atomicity assessment, Draft Harness Model, human ratification",
    "TS-05": "dependency-ready decision graph, rich Activative lineage, human-owned Identity DNA proposals, transactional IR patch",
    "TS-06": "canonical Harness IR, rich semantic refs, conversational receipts, visual handoffs, canonical JSON, migrations, drift guard",
    "TS-07": "typed ownership/module/phase/context/contract/reference/loading/repair graphs and impact analysis",
    "TS-08": "capability registry, necessity decision, immutable skill packages, maturity and redundancy controls",
    "TS-09": "typed recipes/bindings, authority and precedence resolver, deterministic context/capsule compiler",
    "TS-10": "isolated visual and conversational corpora, constitutional dimensions, independent evaluators, scorecards, maturity receipts",
    "TS-11": "five category constitutions, four conversational profiles, three target compilers, activation-first external handoffs",
    "TS-12": "event projections for semantic lineage, reaction/expression, HG-015, command/query API, accessible Control Tower",
    "TS-13": "failure/root-cause/repair graph, HG-001 through HG-015 evaluator, constitutional readiness and authorization receipts",
    "TS-14": "canonical Workflow IR, conversational recompile routes, activation-first visual handoff, bounded executors and incidents",
    "TS-15": "Format 02 non-regression, enriched stub asset-demand lineage, reference benchmark and downstream evidence",
    "IMPLEMENTATION_BASELINE": "explicit no-local-V2.1 disposition with repository-evidence invalidation trigger",
}

VERIFICATION = {
    "TS-01": "unit;state-machine;authority;concurrency;replay;resume;boundary",
    "TS-02": "unit;contract;archive-security;consent;withdrawal;property;scale;resume;invalidation",
    "TS-03": "golden;dual-order;lineage;contract;provider;adversarial;privacy;calibration;benchmark",
    "TS-04": "unit;authority;adversarial;empirical;invalidation;category",
    "TS-05": "unit;graph-property;transaction;concurrency;replay;authority",
    "TS-06": "unit;golden;property;contract;cross-artifact;migration;drift;sandbox",
    "TS-07": "unit;graph-property;contract;scale;security;impact;invalidation",
    "TS-08": "unit;contract;behavioral;maturity;dependency;security;revocation",
    "TS-09": "unit;golden;contract;context-budget;security;replay;revocation",
    "TS-10": "unit;statistical;identity;conversational;isolation;leakage;resume;hard-gate;behavioral",
    "TS-11": "schema;five-category;three-target;contract;sequence;semantic-non-mutation;boundary;golden",
    "TS-12": "api-contract;projection-replay;lineage;redaction;accessibility;performance",
    "TS-13": "unit;graph;false-readiness;HG-015;revocation;trace;capsule;boundary",
    "TS-14": "unit;conversational-route;visual-handoff;workflow;fault;security;replay;resume;rollback",
    "TS-15": "end-to-end;non-regression;stub-lineage;workflow;fault;security;benchmark;handoff;downstream",
    "IMPLEMENTATION_BASELINE": "repository-inventory;authority-review;classification-invalidation",
}


def main() -> None:
    requirements = json.loads((ROOT / "governance/REQUIREMENTS_REGISTRY.json").read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in requirements["functional_requirements"] + requirements["non_functional_requirements"]}
    coverage = list(csv.DictReader((TECH / "REQUIREMENT_COVERAGE_MATRIX.csv").open(encoding="utf-8")))
    rows = []
    for item in coverage:
        source = by_id[item["id"]]
        component_id, component, adrs = OWNERS[item["primary_spec"]]
        rows.append({
            "id": item["id"],
            "type": item["type"],
            "title": item["title"],
            "classification": item["classification"],
            "release_scope": item["release_scope"],
            "tech_spec": item["primary_spec"],
            "component_id": component_id,
            "architecture_component": component,
            "adr_ids": adrs,
            "locked_decisions": ";".join(source.get("decisions", [])),
            "architecture_mechanism": MECHANISMS[item["primary_spec"]],
            "verification_strategy": VERIFICATION[item["primary_spec"]],
            "blocking_decisions": item["blocking_decisions"],
            "requirement_source": source["source_file"],
        })
    assert len(rows) == 263 and len({row["id"] for row in rows}) == 263
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
