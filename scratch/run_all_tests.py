import sys, os, tomllib, pytest

# Load pythonpath from pyproject.toml
with open('pyproject.toml', 'rb') as f:
    cfg = tomllib.load(f)
pp = cfg.get('tool', {}).get('pytest', {}).get('ini_options', {}).get('pythonpath', [])
for p in pp:
    abs_p = os.path.abspath(p)
    if abs_p not in sys.path:
        sys.path.insert(0, abs_p)

print('sys.path configured with', len(pp), 'paths from pyproject.toml.')

# Run tests
test_files = [
    'tests/pipeline/test_audience_context_adapter.py',
    'tests/pipeline/test_causal_admission.py',
    'tests/pipeline/test_research_briefs.py',
    'tests/wave04/test_ca_m027_declarative_policy_packages.py',
    'tests/cae/test_m033_canonical_fr_test_contract_harness.py',
    'tests/cae/test_m38_resilient_multi_provider_routing.py',
    'tests/phase6/test_ca_m012_source_media.py',
]

for tf in test_files:
    print('\n' + '='*60)
    print('RUNNING:', tf)
    print('='*60)
    code = pytest.main(['-q', tf, '-p', 'no:asyncio'])
    print('EXIT CODE:', code)
