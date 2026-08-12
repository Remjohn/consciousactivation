import pytest
import zipfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from cmf_builder.stage1.runner import Stage1Runner, RunConfig

@pytest.fixture
def temp_zip(tmp_path):
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.writestr("image_00.jpg", b"fake_image_data")
    return zip_path

@patch('cmf_builder.stage1.vision_client.VisionClient.analyze_frame')
def test_end_to_end_vision(mock_analyze, temp_zip, tmp_path):
    mock_analyze.return_value = {
        "observations": [
            {
                "bbox_2d": [0,0,10,10],
                "confidence": 0.9,
                "label": "button"
            }
        ],
        "entries": [
            {
                "slide_role": "single_frame",
                "container_zones": ["full_bleed"],
                "primitives": [{"primitive_type": "text_block"}],
                "anchor_elements": []
            }
        ]
    }
    
    # Let's just compute the real hash so input_receipt passes
    from cmf_builder.stage1.input_receipt import compute_file_sha256
    real_hash = compute_file_sha256(temp_zip)
    
    config = RunConfig(
        harness_id="test_harness",
        source_zip_path=temp_zip,
        recorded_sha256=real_hash,
        vision_model="mock-model",
        base_url="http://mock-url",
        selected_by="tester",
        output_dir=tmp_path / "output"
    )
    
    runner = Stage1Runner(config)
    result = runner.run()

    # The run should pass through all vision steps
    assert '02_observation' in result.checkpoints_completed
    assert '03_taxonomy_resolution' in result.checkpoints_completed
    assert '04_visual_syntax' in result.checkpoints_completed
    assert '05_deduplication' in result.checkpoints_completed
        
    # Checking checkpoint outputs
    obs_data = runner.state['02_observation']
    assert len(obs_data['observations']) == 1
    assert obs_data['observations'][0]['object_id'] == 'frame0_obj1'
    
    tax_data = runner.state['03_taxonomy_resolution']
    assert len(tax_data['resolutions']) == 1
    assert tax_data['resolutions'][0]['slide_role']['status'] == 'CANONICAL'
    
    syn_data = runner.state['04_visual_syntax']
    assert len(syn_data['entries']) == 1
    assert syn_data['entries'][0]['evidence_refs'] == ['frame0_obj1']
    
    dedup_data = runner.state['05_deduplication']
    assert 'single_frame' in [u['slide_role'] for u in dedup_data['deduplication_summary']['unique_slide_roles']]
