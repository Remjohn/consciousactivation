import json

data = json.load(open('scratch/detailed_mandates.json', encoding='utf-8'))

file_map = {m['file']: m for m in data}

epochs = {
    'Epoch 1: Foundations & Upstream Context': [
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_01/02_CA_MANDATE_001.md', # Q01: Audience Context 3 Layers
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_01/05_CA_MANDATE_004.md', # Q04: Pipeline Ordering
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_02/02_CA_MANDATE_010.md', # Q10: Structured Research Briefs
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_02/04_CA_MANDATE_012.md', # Q12: Sovereign Media Byte Supremacy
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_04/04_CA_MANDATE_027.md', # Q26: Declarative Policy Rule Packages
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/03_CA_MANDATE_033.md', # Q33: Canonical FR Test Contract
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/08_CA_MANDATE_038.md', # Q38: Multi-Provider Routing
    ],
    'Epoch 2: Ingestion, Elicitation & Parameter Prep': [
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_01/03_CA_MANDATE_002.md', # Q02: Dual-Context Convergence Gate
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_01/06_CA_MANDATE_005.md', # Q05: Format Matchmaking Gate
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_02/01_CA_MANDATE_009.md', # Q09: Parameter Prep Room
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_02/05_CA_MANDATE_013.md', # Q13: Temporal Evidence Anchoring
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_02/07_CA_MANDATE_015.md', # Q15: Verbatim Whisper Capture
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/04_CA_MANDATE_034.md', # Q34: Program Execution Dispatch
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/06_CA_MANDATE_036.md', # Q36: State-Local Context Projection
    ],
    'Epoch 3: Anchoring, Workflows & Sealing': [
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_01/07_CA_MANDATE_006.md', # Q06: Activative to Elicitation Linking
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_02/03_CA_MANDATE_011.md', # Q11: Sealed Pre-Production Pack
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_02/06_CA_MANDATE_014.md', # Q14: Cross-Window Chunking Protection
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_02/08_CA_MANDATE_016.md', # Q16: Grounded Collision Tension Matrix
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_03/06_CA_MANDATE_021.md', # Q21: Anchor Hits Exact Coordinates
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/05_CA_MANDATE_035.md', # Q35: Workflow Dispatcher
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/07_CA_MANDATE_037.md', # Q37: Agent Invocation Host Runner
    ],
    'Epoch 4: Evidence Admission, Lineage & Gate Halting': [
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_01/08_CA_MANDATE_007.md', # Q07: Activative Strategic Execution Object
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_03/02_CA_MANDATE_017.md', # Q17: Multi-Dimensional Evidence Admission
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_03/03_CA_MANDATE_018.md', # Q18: Hierarchical Context Lineage
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_03/04_CA_MANDATE_019.md', # Q19: Expression Moments Semantic Bridge
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/09_CA_MANDATE_039.md', # Q39: Deterministic Output Contract & Self-Repair
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/10_CA_MANDATE_040.md', # Q40: Gate Milestone Suspension Contract
    ],
    'Epoch 5: Gate Resumption, Receipts & Policy Binding': [
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_01/04_CA_MANDATE_003.md', # Q03: Subject Constitution Lifecycle
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_03/05_CA_MANDATE_020.md', # Q20: Reaction Receipts First-Class Evidence
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_03/07_CA_MANDATE_022.md', # Q22: Adaptive Elicitation Remediation
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_04/02_CA_MANDATE_025.md', # Q24: Campaign Auth Policy (Production)
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_04/05_CA_MANDATE_028.md', # Q27: Policy Revisions Execution Binding
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/11_CA_MANDATE_041.md', # Q40: Reactive Gate Resumption & Receipts
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_06/08_CA_MANDATE_048.md', # Q47: Path Traversal & Tool Sandbox
    ],
    'Epoch 6: Memory Write-Back, CAS Concurrency & Registry': [
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_01/09_CA_MANDATE_008.md', # Q08: Frozen Content Portfolio
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_03/08_CA_MANDATE_023.md', # Q23: Deterministic Portfolio Yield Gating
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_03/09_CA_MANDATE_024.md', # Q24: Preliminary Auth Policy
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_04/03_CA_MANDATE_026.md', # Q25: Durable Auth Decision Receipts
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/02_CA_MANDATE_032.md', # Q32: Governed Memory Write-Back
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_06/02_CA_MANDATE_042.md', # Q41: Atomic CAS SQLite Transitions
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_06/09_CA_MANDATE_049.md', # Q48: Program Registry Immutability
    ],
    'Epoch 7: Merkle Receipts, Composition & Isolation': [
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_04/06_CA_MANDATE_029.md', # Q28: No-Unanchored-Invention Invariant
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_04/07_CA_MANDATE_030.md', # Q29: Immutable Release Manifest
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_06/03_CA_MANDATE_043.md', # Q42: Merkle Receipt Chaining
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_06/07_CA_MANDATE_047.md', # Q46: Multi-Tenant Workspace Isolation
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/03_CA_MANDATE_051.md', # Q50: Model Economics & Quotas
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/04_CA_MANDATE_052.md', # Q51: Subject Constitution Voice DNA
    ],
    'Epoch 8: Distribution, Replay, Preemption & DAG': [
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_04/08_CA_MANDATE_031.md', # Q30: External Distribution Delivery
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_04/09_CA_MANDATE_032.md', # Q31: Outcome Measurement Attribution
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_06/04_CA_MANDATE_044.md', # Q43: Persisted Replay Verification Engine
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_06/05_CA_MANDATE_045.md', # Q44: Worker Restart & Zombie Lease Reconcile
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_06/06_CA_MANDATE_046.md', # Q45: Real Operator Control & Preemption
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/02_CA_MANDATE_050.md', # Q49: Cryptographic Evidence DAG
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/06_CA_MANDATE_054.md', # Q53: Unified Telemetry Flywheel
    ],
    'Epoch 9: Autonomous Collisions, Benchmarking & Live Proof': [
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/05_CA_MANDATE_053.md', # Q52: CSEB Golden Benchmark Certification
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/07_CA_MANDATE_055.md', # Q54: Autonomous Collision Approval Gate
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/08_CA_MANDATE_056.md', # Q55: SQLite WAL Concurrency & Tuning
        'docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/09_CA_MANDATE_057.md', # Q56: Live End-to-End Proof Harness
    ]
}

all_scheduled = []
for ep_name, f_list in epochs.items():
    all_scheduled.extend(f_list)

print(f"Total scheduled: {len(all_scheduled)}")
print(f"Unique scheduled: {len(set(all_scheduled))}")
missing = set(file_map.keys()) - set(all_scheduled)
extra = set(all_scheduled) - set(file_map.keys())
print(f"Missing count: {len(missing)}")
print(f"Extra count: {len(extra)}")
