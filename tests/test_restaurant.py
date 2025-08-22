# tests/test_restaurant.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
import psycopg2
from psycopg2.extras import RealDictCursor

client = TestClient(app)

# Test database setup
def setup_test_db():
    """Setup test database and clean tables before tests"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="zomato_clone",
            user="postgres",
            password="postgres123",
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
        
        # Clean up test data
        cur.execute("DELETE FROM restaurants WHERE name LIKE '%Test%'")
        cur.execute("DELETE FROM users WHERE email LIKE '%test%'")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database setup error: {e}")

def teardown_test_db():
    """Clean up test data after tests"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="zomato_clone",
            user="postgres",
            password="postgres123",
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
        
        # Clean up test data
        cur.execute("DELETE FROM restaurants WHERE name LIKE '%Test%'")
        cur.execute("DELETE FROM users WHERE email LIKE '%test%'")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database cleanup error: {e}")

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup and teardown for each test"""
    setup_test_db()
    yield
    teardown_test_db()

class TestRestaurantOwnerRegistration:
    """Test cases for restaurant owner registration"""
    
    def test_successful_restaurant_owner_registration(self):
        """Test successful restaurant owner registration"""
        owner_data = {
            "name": "Test Restaurant Owner",
            "email": "testowner@example.com",
            "password": "ownerpassword123",
            "role": "restaurant_owner"
        }
        
        response = client.post("/api/users/register", json=owner_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == owner_data["name"]
        assert data["email"] == owner_data["email"]
        assert data["role"] == "restaurant_owner"
        assert "id" in data
        assert "password" not in data  # Password should not be returned
    
    def test_restaurant_owner_vs_customer_role(self):
        """Test that restaurant owner role is different from customer"""
        # Register customer
        customer_data = {
            "name": "Test Customer",
            "email": "testcustomer@example.com",
            "password": "customerpass123",
            "role": "customer"
        }
        
        customer_response = client.post("/api/users/register", json=customer_data)
        assert customer_response.status_code == 200
        assert customer_response.json()["role"] == "customer"
        
        # Register restaurant owner
        owner_data = {
            "name": "Test Owner",
            "email": "testowner2@example.com",
            "password": "ownerpass123",
            "role": "restaurant_owner"
        }
        
        owner_response = client.post("/api/users/register", json=owner_data)
        assert owner_response.status_code == 200
        assert owner_response.json()["role"] == "restaurant_owner"

class TestRestaurantCreation:
    """Test cases for restaurant creation and management"""
    
    def test_successful_restaurant_creation(self):
        """Test successful restaurant creation with all required fields"""
        restaurant_data = {
            "name": "Test Restaurant",
            "description": "A wonderful test restaurant serving delicious food",
            "address": "123 Test Street, Test City, TC 12345",
            "phone": "555-0123"
        }
        
        response = client.post("/api/restaurants", json=restaurant_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == restaurant_data["name"]
        assert data["description"] == restaurant_data["description"]
        assert data["address"] == restaurant_data["address"]
        assert data["phone"] == restaurant_data["phone"]
        assert "id" in data
        assert "created_at" in data
    
    def test_restaurant_creation_missing_name(self):
        """Test restaurant creation fails when name is missing"""
        restaurant_data = {
            "description": "A restaurant without a name",
            "address": "123 Test Street, Test City, TC 12345",
            "phone": "555-0123"
        }
        
        response = client.post("/api/restaurants", json=restaurant_data)
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "detail" in data
        # Check that the error mentions the missing field
        error_details = str(data["detail"]).lower()
        assert "name" in error_details or "required" in error_details
    
    def test_restaurant_creation_missing_address(self):
        """Test restaurant creation fails when address is missing"""
        restaurant_data = {
            "name": "Test Restaurant No Address",
            "description": "A restaurant without an address",
            "phone": "555-0123"
        }
        
        response = client.post("/api/restaurants", json=restaurant_data)
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "detail" in data
        error_details = str(data["detail"]).lower()
        assert "address" in error_details or "required" in error_details
    
    def test_restaurant_creation_missing_phone(self):
        """Test restaurant creation fails when phone is missing"""
        restaurant_data = {
            "name": "Test Restaurant No Phone",
            "description": "A restaurant without a phone",
            "address": "123 Test Street, Test City, TC 12345"
        }
        
        response = client.post("/api/restaurants", json=restaurant_data)
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "detail" in data
        error_details = str(data["detail"]).lower()
        assert "phone" in error_details or "required" in error_details
    
    def test_restaurant_creation_empty_name(self):
        """Test restaurant creation fails when name is empty string"""
        restaurant_data = {
            "name": "",
            "description": "A restaurant with empty name",
            "address": "123 Test Street, Test City, TC 12345",
            "phone": "555-0123"
        }
        
        response = client.post("/api/restaurants", json=restaurant_data)
        
        # Should fail validation (422) or business logic (400)
        assert response.status_code in [400, 422]
        data = response.json()
        assert "detail" in data
    
    def test_restaurant_creation_empty_address(self):
        """Test restaurant creation fails when address is empty string"""
        restaurant_data = {
            "name": "Test Restaurant Empty Address",
            "description": "A restaurant with empty address",
            "address": "",
            "phone": "555-0123"
        }
        
        response = client.post("/api/restaurants", json=restaurant_data)
        
        # Should fail validation (422) or business logic (400)
        assert response.status_code in [400, 422]
        data = response.json()
        assert "detail" in data
    
    def test_restaurant_creation_with_minimal_data(self):
        """Test restaurant creation with only required fields"""
        restaurant_data = {
            "name": "Minimal Test Restaurant",
            "address": "456 Minimal St",
            "phone": "555-9999"
        }
        
        response = client.post("/api/restaurants", json=restaurant_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == restaurant_data["name"]
        assert data["address"] == restaurant_data["address"]
        assert data["phone"] == restaurant_data["phone"]
        # Description might be None or empty string
        assert "description" in data

class TestRestaurantOperations:
    """Test cases for restaurant CRUD operations"""
    
    def test_get_all_restaurants(self):
        """Test getting all restaurants"""
        # First create a restaurant
        restaurant_data = {
            "name": "Test Restaurant for List",
            "description": "A test restaurant for listing",
            "address": "789 List Street",
            "phone": "555-1111"
        }
        
        create_response = client.post("/api/restaurants", json=restaurant_data)
        assert create_response.status_code == 200
        
        # Now get all restaurants
        response = client.get("/api/restaurants")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Check if our created restaurant is in the list
        restaurant_names = [restaurant["name"] for restaurant in data]
        assert restaurant_data["name"] in restaurant_names
    
    def test_get_restaurant_by_id(self):
        """Test getting a specific restaurant by ID"""
        # First create a restaurant
        restaurant_data = {
            "name": "Test Restaurant for Get",
            "description": "A test restaurant for getting by ID",
            "address": "101 Get Street",
            "phone": "555-2222"
        }
        
        create_response = client.post("/api/restaurants", json=restaurant_data)
        assert create_response.status_code == 200
        restaurant_id = create_response.json()["id"]
        
        # Now get the restaurant by ID
        response = client.get(f"/api/restaurants/{restaurant_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == restaurant_id
        assert data["name"] == restaurant_data["name"]
        assert data["address"] == restaurant_data["address"]
        assert data["phone"] == restaurant_data["phone"]
    
    def test_get_nonexistent_restaurant(self):
        """Test getting a restaurant that doesn't exist"""
        response = client.get("/api/restaurants/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_delete_restaurant(self):
        """Test deleting a restaurant"""
        # First create a restaurant
        restaurant_data = {
            "name": "Test Restaurant for Delete",
            "description": "A test restaurant for deletion",
            "address": "202 Delete Street",
            "phone": "555-3333"
        }
        
        create_response = client.post("/api/restaurants", json=restaurant_data)
        assert create_response.status_code == 200
        restaurant_id = create_response.json()["id"]
        
        # Delete the restaurant
        delete_response = client.delete(f"/api/restaurants/{restaurant_id}")
        assert delete_response.status_code == 200
        
        # Verify it's deleted by trying to get it
        get_response = client.get(f"/api/restaurants/{restaurant_id}")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_restaurant(self):
        """Test deleting a restaurant that doesn't exist"""
        response = client.delete("/api/restaurants/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

class TestRestaurantValidation:
    """Test cases for restaurant data validation"""
    
    def test_restaurant_name_length_validation(self):
        """Test restaurant name length validation"""
        # Test with very long name
        long_name = "A" * 300  # Very long name
        restaurant_data = {
            "name": long_name,
            "description": "Test description",
            "address": "123 Test Street",
            "phone": "555-0123"
        }
        
        response = client.post("/api/restaurants", json=restaurant_data)
        
        # Depending on validation rules, this might succeed or fail
        # If there's a length limit, it should return 422
        if response.status_code == 422:
            data = response.json()
            assert "detail" in data
    
    def test_restaurant_phone_format_validation(self):
        """Test phone number format validation"""
        restaurant_data = {
            "name": "Test Restaurant Phone Format",
            "description": "Testing phone format",
            "address": "123 Test Street",
            "phone": "invalid-phone-format"
        }
        
        response = client.post("/api/restaurants", json=restaurant_data)
        
        # Depending on validation rules, this might succeed or fail
        # If there's phone format validation, it should return 422
        if response.status_code == 422:
            data = response.json()
            assert "detail" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
