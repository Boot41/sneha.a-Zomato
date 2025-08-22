# tests/test_root.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestRootEndpoint:
    """Test cases for the root endpoint"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns 200 and welcome message"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check that response contains a welcome message
        assert "message" in data
        welcome_text = data["message"].lower()
        assert "welcome" in welcome_text and "zomato" in welcome_text and "api" in welcome_text
    
    def test_root_endpoint_response_structure(self):
        """Test the root endpoint returns proper JSON structure"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Ensure it's a dictionary with at least a message field
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)
        assert len(data["message"]) > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
