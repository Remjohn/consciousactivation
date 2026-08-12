import zipfile
import mimetypes
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ExtractedFrame:
    frame_index: int
    filename: str
    image_bytes: bytes
    mime_type: str

def extract_frames(zip_path: Path, max_samples: int = 20) -> list[ExtractedFrame]:
    valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    
    with zipfile.ZipFile(zip_path, 'r') as z:
        # Get list of files
        files = [f for f in z.namelist() if not f.endswith('/')]
        
        # Filter for valid images
        image_files = []
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in valid_extensions:
                image_files.append(f)
                
        # Sort to maintain sequence
        image_files.sort()
        
        if not image_files:
            raise ValueError(f"No valid image files found in {zip_path}")
            
        # Sample if needed
        if len(image_files) > max_samples:
            step = len(image_files) / max_samples
            sampled_files = [image_files[int(i * step)] for i in range(max_samples)]
        else:
            sampled_files = image_files
            
        extracted = []
        for i, filename in enumerate(sampled_files):
            ext = Path(filename).suffix.lower()
            mime_type = mimetypes.types_map.get(ext, 'image/jpeg')
            
            with z.open(filename) as f:
                image_bytes = f.read()
                
            extracted.append(ExtractedFrame(
                frame_index=i,
                filename=filename,
                image_bytes=image_bytes,
                mime_type=mime_type
            ))
            
        return extracted
