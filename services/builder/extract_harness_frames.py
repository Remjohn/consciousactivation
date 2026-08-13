import sys
import zipfile
from pathlib import Path

BASE_DIR = Path(r"d:\Work\consciousactivation")
CAROUSELS_ZIP_DIR = BASE_DIR / "atomic_harnesses_visual_syntax" / "carousels"
SUPERVISUALS_ZIP_DIR = BASE_DIR / "atomic_harnesses_visual_syntax" / "supervisuals"
TEMP_DIR = BASE_DIR / "temp_frames"

def extract_harness(harness_id: str):
    if harness_id.startswith("CAR-"):
        zip_path = CAROUSELS_ZIP_DIR / f"{harness_id}.zip"
    else:
        zip_path = SUPERVISUALS_ZIP_DIR / f"{harness_id}.zip"

    if not zip_path.exists():
        print(f"Zip file not found: {zip_path}")
        return []

    out_dir = TEMP_DIR / harness_id
    out_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(out_dir)

    images = sorted([
        str(p) for p in out_dir.rglob("*")
        if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp')
    ])
    
    print(f"Extracted {len(images)} frame images for {harness_id}:")
    for img in images:
        print(f"  {img}")
    return images

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_harness(sys.argv[1])
    else:
        print("Usage: python extract_harness_frames.py <harness_id>")
