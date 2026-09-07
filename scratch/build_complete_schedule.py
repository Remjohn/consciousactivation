import json

data = json.load(open('scratch/detailed_mandates.json', encoding='utf-8'))

# We want an exhaustive mapping of all 58 mandate files into clean parallel epochs
# Let's map each mandate by unique identifier (file basename or ID)
# Let's see all unique files:
print(f"Total files: {len(data)}")

# Let's inspect the exact list of mandate files:
all_files = [m['file'] for m in data]
print(f"Unique files: {len(set(all_files))}")
