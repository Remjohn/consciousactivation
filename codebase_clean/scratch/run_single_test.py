import sys, os, tomllib, pytest

with open('pyproject.toml', 'rb') as f:
    cfg = tomllib.load(f)
pp = cfg.get('tool', {}).get('pytest', {}).get('ini_options', {}).get('pythonpath', [])
for p in pp:
    abs_p = os.path.abspath(p)
    if abs_p not in sys.path:
        sys.path.insert(0, abs_p)

args = sys.argv[1:] if len(sys.argv) > 1 else ['tests/pipeline/test_audience_context_adapter.py']
print(f'Running: {args}')
ret = pytest.main(['-q', *args, '-p', 'no:asyncio'])
sys.exit(ret)
