import pytest
import zipfile
from pathlib import Path
from cmf_builder.stage1.zip_extractor import extract_frames

@pytest.fixture
def temp_zip(tmp_path):
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, 'w') as z:
        for i in range(30):
            z.writestr(f"image_{i:02d}.jpg", b"fake_image_data")
        z.writestr("not_an_image.txt", b"text data")
    return zip_path

@pytest.fixture
def empty_zip(tmp_path):
    zip_path = tmp_path / "empty.zip"
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.writestr("not_an_image.txt", b"text data")
    return zip_path

def test_extract_frames_basic(temp_zip):
    frames = extract_frames(temp_zip, max_samples=50)
    assert len(frames) == 30
    assert frames[0].filename == "image_00.jpg"
    assert frames[0].mime_type == "image/jpeg"
    assert frames[0].image_bytes == b"fake_image_data"

def test_extract_frames_sampling(temp_zip):
    frames = extract_frames(temp_zip, max_samples=10)
    assert len(frames) == 10
    # step is 30 / 10 = 3
    assert frames[0].filename == "image_00.jpg"
    assert frames[1].filename == "image_03.jpg"

def test_extract_frames_empty(empty_zip):
    with pytest.raises(ValueError, match="No valid image files found"):
        extract_frames(empty_zip)
