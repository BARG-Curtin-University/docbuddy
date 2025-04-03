"""Tests for web interface."""
import pytest
from unittest.mock import patch, MagicMock
from starlette.testclient import TestClient

from atari_assist.web.app import app
from atari_assist.core import ask_question, preview_matches
from atari_assist.web.handlers import Question

@pytest.fixture
def client():
    """Create a test client for the web app."""
    return TestClient(app)

def test_index_route(client):
    """Test the index route returns a 200 status code."""
    response = client.get("/")
    assert response.status_code == 200
    content = response.text.lower()
    
    # Check that the page contains the expected elements
    assert "atari assist" in content
    assert "question" in content
    assert "model" in content
    assert "ask" in content

@patch('atari_assist.web.handlers.ask_question')
def test_ask_question_route(mock_ask, client):
    """Test the ask question route."""
    # Setup mock
    mock_ask.return_value = "This is a test answer."
    
    # Make the request
    response = client.post(
        "/ask",
        data={"query": "How does WSYNC work?", "model": "openai"}
    )
    
    # Verify
    assert response.status_code == 200
    assert "This is a test answer." in response.text
    assert "How does WSYNC work?" in response.text
    mock_ask.assert_called_once_with("How does WSYNC work?", "openai")

@patch('atari_assist.web.handlers.preview_matches')
def test_preview_route(mock_preview, client):
    """Test the preview route."""
    # Setup mock
    mock_preview.return_value = [
        ("file1.txt", "This is sample content from file 1."),
        ("file2.txt", "This is sample content from file 2.")
    ]
    
    # Make the request
    response = client.post(
        "/preview",
        data={"query": "How does WSYNC work?", "model": "openai"}
    )
    
    # Verify
    assert response.status_code == 200
    assert "Top Matching Documents" in response.text
    assert "file1.txt" in response.text
    assert "file2.txt" in response.text
    assert "This is sample content from file 1." in response.text
    mock_preview.assert_called_once_with("How does WSYNC work?")

def test_model_info_route(client):
    """Test the model info route."""
    # Make the request
    response = client.get("/model-info")
    
    # Verify
    assert response.status_code == 200
    assert "Available Models" in response.text
    assert "OpenAI" in response.text
    assert "Ollama" in response.text
    assert "Claude" in response.text
    assert "Gemini" in response.text
    assert "Groq" in response.text