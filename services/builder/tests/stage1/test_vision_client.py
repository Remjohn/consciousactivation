import pytest
import os
import json
from unittest.mock import patch, MagicMock
from cmf_builder.stage1.vision_client import VisionClient
from cmf_builder.stage1.zip_extractor import ExtractedFrame

def test_resolve_api_key_env():
    with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_key_from_env"}):
        client = VisionClient(model_name="test_model", base_url="http://test")
        assert client.api_key == "test_key_from_env"

def test_resolve_api_key_explicit():
    client = VisionClient(model_name="test_model", base_url="http://test", api_key="explicit_key")
    assert client.api_key == "explicit_key"

def test_strip_markdown():
    client = VisionClient(model_name="test_model", base_url="http://test", api_key="explicit_key")
    dirty_json = "```json\n{\"test\": 123}\n```"
    clean_json = client._strip_markdown_fences(dirty_json)
    assert clean_json == '{"test": 123}'

@patch("urllib.request.urlopen")
def test_analyze_frame(mock_urlopen):
    # Mocking response
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "choices": [
            {
                "message": {
                    "content": "```json\n{\"observations\": [{\"prop\": 1}], \"entries\": [{\"prop\": 2}]}\n```"
                }
            }
        ]
    }).encode('utf-8')
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response

    client = VisionClient(model_name="test_model", base_url="http://test", api_key="test")
    frame = ExtractedFrame(frame_index=0, filename="test.jpg", image_bytes=b"fake", mime_type="image/jpeg")
    
    result = client.analyze_frame(frame)
    
    assert "observations" in result
    assert len(result["observations"]) == 1
    assert result["observations"][0]["prop"] == 1
    assert "entries" in result
    assert len(result["entries"]) == 1
    assert result["entries"][0]["prop"] == 2
