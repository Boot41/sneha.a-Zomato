# tests/test_auth.py
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

class TestUserRegistration:
    """Test cases for user registration"""
    
    def test_successful_user_registration(self):
        """Test successful user registration"""
        user_data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "role": "customer"
        }
        
        response = client.post("/api/users/register", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert data["role"] == user_data["role"]
        assert "id" in data
        assert "password" not in data  # Password should not be returned
    
    def test_register_duplicate_user(self):
        """Test registration with duplicate email should fail"""
        user_data = {
            "name": "Test User",
            "email": "duplicate@example.com",
            "password": "testpassword123",
            "role": "customer"
        }
        
        # First registration should succeed
        response1 = client.post("/api/users/register", json=user_data)
        assert response1.status_code == 200
        
        # Second registration with same email should fail
        response2 = client.post("/api/users/register", json=user_data)
        assert response2.status_code == 400
        data = response2.json()
        assert "detail" in data
        assert "already exists" in data["detail"].lower() or "duplicate" in data["detail"].lower()
    
    def test_register_with_invalid_email(self):
        """Test registration with invalid email format should fail"""
        user_data = {
            "name": "Test User",
            "email": "invalid-email-format",
            "password": "testpassword123",
            "role": "customer"
        }
        
        response = client.post("/api/users/register", json=user_data)
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "detail" in data
    
    def test_register_restaurant_owner(self):
        """Test successful restaurant owner registration"""
        user_data = {
            "name": "Restaurant Owner",
            "email": "owner@example.com",
            "password": "ownerpassword123",
            "role": "restaurant_owner"
        }
        
        response = client.post("/api/users/register", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "restaurant_owner"

class TestUserLogin:
    """Test cases for user login"""
    
    def test_successful_user_login(self):
        """Test successful user login"""
        # First register a user
        user_data = {
            "name": "Login Test User",
            "email": "logintest@example.com",
            "password": "loginpassword123",
            "role": "customer"
        }
        
        register_response = client.post("/api/users/register", json=user_data)
        assert register_response.status_code == 200
        
        # Now test login
        login_data = {
            "username": "logintest@example.com",  # FastAPI OAuth2 uses 'username' field
            "password": "loginpassword123"
        }
        
        response = client.post(
            "/api/users/login",
            data=login_data,  # Use data instead of json for form data
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data or "token" in data or "user" in data
    
    def test_login_with_wrong_password(self):
        """Test login with wrong password should fail"""
        # First register a user
        user_data = {
            "name": "Wrong Password Test",
            "email": "wrongpass@example.com",
            "password": "correctpassword123",
            "role": "customer"
        }
        
        register_response = client.post("/api/users/register", json=user_data)
        assert register_response.status_code == 200
        
        # Try login with wrong password
        login_data = {
            "username": "wrongpass@example.com",
            "password": "wrongpassword123"
        }
        
        response = client.post(
            "/api/users/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "incorrect" in data["detail"].lower() or "invalid" in data["detail"].lower()
    
    def test_login_with_nonexistent_user(self):
        """Test login with non-existent user should fail"""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "somepassword123"
        }
        
        response = client.post(
            "/api/users/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
    
    def test_login_with_invalid_email_format(self):
        """Test login with invalid email format should fail"""
        login_data = {
            "username": "invalid-email-format",
            "password": "somepassword123"
        }
        
        response = client.post(
            "/api/users/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # This might return 401 (user not found) or 422 (validation error)
        # depending on implementation
        assert response.status_code in [401, 422]
        data = response.json()
        assert "detail" in data

class TestUserProfile:
    """Test cases for user profile operations"""
    
    def test_get_user_profile(self):
        """Test getting user profile by ID"""
        # First register a user
        user_data = {
            "name": "Profile Test User",
            "email": "profile@example.com",
            "password": "profilepassword123",
            "role": "customer"
        }
        
        register_response = client.post("/api/users/register", json=user_data)
        assert register_response.status_code == 200
        user_id = register_response.json()["id"]
        
        # Get user profile
        response = client.get(f"/api/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert data["role"] == user_data["role"]
        assert "password" not in data  # Password should not be returned
    
    def test_get_nonexistent_user_profile(self):
        """Test getting profile of non-existent user should fail"""
        response = client.get("/api/users/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
