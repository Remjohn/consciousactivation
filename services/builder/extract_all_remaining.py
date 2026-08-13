import subprocess
import sys

harnesses = [
    'CAR-LST-Planetdat-1-1-8', 'CAR-LST-Realconfid-4-5-4', 'CAR-LST-Relatives-4-5-7',
    'CAR-LST-Resentmnt-4-5-10', 'CAR-LST-Rightppl-4-5-3', 'CAR-LST-Ronaldo-4-5-6',
    'CAR-LST-Ronweasly-4-5-9', 'CAR-LST-Safespace-4-5-5', 'CAR-LST-Screenstr-4-5-8',
    'CAR-LST-Selflove-4-5-4', 'CAR-LST-Stayrare-4-5-4', 'CAR-LST-Stopsave-1-1-10',
    'CAR-LST-Upgrades-4-5-3', 'CAR-LST-Viralpost-3-4-8', 'CAR-LST-Weekgoals-4-5-2',
    'CAR-LST-Yurchance-4-5-5'
]

for h in harnesses:
    result = subprocess.run(
        [sys.executable, 'extract_harness_frames.py', h],
        capture_output=True, text=True
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print(f'ERROR: {result.stderr.strip()}')
