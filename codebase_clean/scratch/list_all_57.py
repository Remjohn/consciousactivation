import json

data = json.load(open('scratch/detailed_mandates.json', encoding='utf-8'))
print(f'Total mandates in files: {len(data)}')
for idx, m in enumerate(data):
    print(f"{idx+1:02d}. [{m['id']}] Wave {m['wave']:02d} | Q: {m['q']} | {m['title']}")
