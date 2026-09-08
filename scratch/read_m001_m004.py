import os, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

for b in ['CA-M001_BUNDLE', 'CA-M004_BUNDLE']:
    bpath = os.path.join('Mandates implementation/epoch_01', b)
    handoffs = glob.glob(os.path.join(bpath, '**', 'AGENT_HANDOFF*.md'), recursive=True)
    if handoffs:
        print('====================================================')
        print('HANDOFF FOR:', b)
        print('====================================================')
        lines = open(handoffs[0], encoding='utf-8').readlines()
        print(''.join(lines[:45]))
