import json

data = json.load(open('scratch/detailed_mandates.json', encoding='utf-8'))

# Let's inspect each mandate's key identifier and title:
mandates_by_key = {}
for m in data:
    # Key: wave + file basename
    bn = m['file'].split('/')[-1]
    key = f\"W{m['wave']}_{bn}\"
    mandates_by_key[key] = m

print(f\"Loaded {len(mandates_by_key)} unique mandates.\")
