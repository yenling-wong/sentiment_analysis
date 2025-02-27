import pytest
from fastapi.testclient import TestClient
from main import app 
from unittest.mock import patch
from models import AnalysisResult, Sentiment
from exception import ProcessingFailedError

client = TestClient(app)

# Mock the analyze function
@pytest.fixture
def mock_analyze():
    with patch('main.analyze') as mock: 
        yield mock

def test_analyze_sentiment_success(mock_analyze):
    mock_analyze.return_value = AnalysisResult(label=Sentiment.positive, score=0.8)
    
    response = client.post("/analyze_sentiment", json={
        "review_id": "123",
        "review_text": "This is a great product!"
    })
    
    assert response.status_code == 200
    assert response.json() == {
        "review_id": "123",
        "details": {
            "label": "POSITIVE",
            "score": 0.8
        }
    }

def test_analyze_sentiment_missing_field():
    response = client.post("/analyze_sentiment", json={
        "review_id": "123"
    })
    
    assert response.status_code == 400
    assert "review_text" in response.json()["detail"]

def test_analyze_sentiment_empty_field():
    response = client.post("/analyze_sentiment", json={
        "review_id": "123",
        "review_text": ""
    })
    
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

def test_analyze_sentiment_processing_error(mock_analyze):
    mock_analyze.side_effect = ProcessingFailedError("Processing failed")
    
    response = client.post("/analyze_sentiment", json={
        "review_id": "123",
        "review_text": "This is a test."
    })
    
    assert response.status_code == 500
    assert "Processing failed" in response.json()["detail"]

def test_analyze_sentiment_invalid_json():
    response = client.post("/analyze_sentiment", data="invalid json")
    
    assert response.status_code == 422
