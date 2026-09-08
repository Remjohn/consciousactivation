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

test_files = [
    'tests/cae/test_ca_m006_activative_elicitation_link.py',
    'tests/phase6/test_ca_m011_preproduction_pack.py',
    'tests/phase6/test_ca_m014_cross_window_chunking.py',
    'tests/phase4/test_ca_m016_collision_matrix.py',
    'tests/phase4/test_ca_m021_anchor_coordinates.py',
    'tests/cae/test_ca_m035_workflow_dispatch.py',
    'tests/cae/test_ca_m037_agent_host_runner.py',
]

results = {}
for tf in test_files:
    print('\n' + '='*70)
    print('RUNNING:', tf)
    print('='*70)
    code = pytest.main(['-v', tf])
    results[tf] = code
    print('EXIT CODE:', code)

print('\n' + '='*70)
print('SUMMARY:')
print('='*70)
all_passed = True
for tf, code in results.items():
    status = 'PASSED' if code == 0 else f'FAILED (code {code})'
    if code != 0:
        all_passed = False
    print(f'{tf}: {status}')

if not all_passed:
    sys.exit(1)
else:
    print('\nALL EPOCH 03 TESTS PASSED!')
