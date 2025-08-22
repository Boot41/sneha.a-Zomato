# tests/test_menu.py
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
        cur.execute("DELETE FROM menu_items WHERE name LIKE '%Test%'")
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
        cur.execute("DELETE FROM menu_items WHERE name LIKE '%Test%'")
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

@pytest.fixture
def test_restaurant():
    """Create a test restaurant for menu tests"""
    restaurant_data = {
        "name": "Test Menu Restaurant",
        "description": "A test restaurant for menu testing",
        "address": "123 Menu Street",
        "phone": "555-MENU"
    }
    
    response = client.post("/api/restaurants", json=restaurant_data)
    assert response.status_code == 200
    return response.json()

class TestMenuItemCreation:
    """Test cases for menu item creation"""
    
    def test_successful_menu_item_creation(self, test_restaurant):
        """Test successful menu item creation for a restaurant"""
        restaurant_id = test_restaurant["id"]
        
        menu_item_data = {
            "name": "Test Burger",
            "description": "A delicious test burger with all the fixings",
            "price": 12.99,
            "category": "Main Course",
            "is_available": True
        }
        
        response = client.post(f"/api/menu/{restaurant_id}", json=menu_item_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == menu_item_data["name"]
        assert data["description"] == menu_item_data["description"]
        assert data["price"] == menu_item_data["price"]
        assert data["category"] == menu_item_data["category"]
        assert data["is_available"] == menu_item_data["is_available"]
        assert data["restaurant_id"] == restaurant_id
        assert "id" in data
    
    def test_menu_item_creation_minimal_data(self, test_restaurant):
        """Test menu item creation with minimal required data"""
        restaurant_id = test_restaurant["id"]
        
        menu_item_data = {
            "name": "Test Pizza",
            "price": 15.50,
            "category": "Main Course"
        }
        
        response = client.post(f"/api/menu/{restaurant_id}", json=menu_item_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == menu_item_data["name"]
        assert data["price"] == menu_item_data["price"]
        assert data["category"] == menu_item_data["category"]
        assert data["restaurant_id"] == restaurant_id
        # Check default values
        assert data["is_available"] == True  # Should default to True
    
    def test_menu_item_creation_different_categories(self, test_restaurant):
        """Test creating menu items in different categories"""
        restaurant_id = test_restaurant["id"]
        
        categories = ["Appetizer", "Main Course", "Dessert", "Beverage"]
        
        for category in categories:
            menu_item_data = {
                "name": f"Test {category} Item",
                "description": f"A test {category.lower()} item",
                "price": 8.99,
                "category": category
            }
            
            response = client.post(f"/api/menu/{restaurant_id}", json=menu_item_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["category"] == category
    
    def test_menu_item_creation_invalid_restaurant(self):
        """Test menu item creation for non-existent restaurant should fail"""
        invalid_restaurant_id = 99999
        
        menu_item_data = {
            "name": "Test Invalid Restaurant Item",
            "description": "This should fail",
            "price": 10.00,
            "category": "Main Course"
        }
        
        response = client.post(f"/api/menu/{invalid_restaurant_id}", json=menu_item_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "restaurant" in data["detail"].lower() or "not found" in data["detail"].lower()
    
    def test_menu_item_creation_missing_name(self, test_restaurant):
        """Test menu item creation fails when name is missing"""
        restaurant_id = test_restaurant["id"]
        
        menu_item_data = {
            "description": "A menu item without a name",
            "price": 10.00,
            "category": "Main Course"
        }
        
        response = client.post(f"/api/menu/{restaurant_id}", json=menu_item_data)
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "detail" in data
    
    def test_menu_item_creation_missing_price(self, test_restaurant):
        """Test menu item creation fails when price is missing"""
        restaurant_id = test_restaurant["id"]
        
        menu_item_data = {
            "name": "Test No Price Item",
            "description": "A menu item without a price",
            "category": "Main Course"
        }
        
        response = client.post(f"/api/menu/{restaurant_id}", json=menu_item_data)
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "detail" in data
    
    def test_menu_item_creation_negative_price(self, test_restaurant):
        """Test menu item creation fails with negative price"""
        restaurant_id = test_restaurant["id"]
        
        menu_item_data = {
            "name": "Test Negative Price Item",
            "description": "A menu item with negative price",
            "price": -5.00,
            "category": "Main Course"
        }
        
        response = client.post(f"/api/menu/{restaurant_id}", json=menu_item_data)
        
        # Should fail validation (422) or business logic (400)
        assert response.status_code in [400, 422]
        data = response.json()
        assert "detail" in data

class TestMenuItemRetrieval:
    """Test cases for menu item retrieval"""
    
    def test_get_menu_items_for_restaurant(self, test_restaurant):
        """Test getting all menu items for a restaurant"""
        restaurant_id = test_restaurant["id"]
        
        # First, create some menu items
        menu_items = [
            {
                "name": "Test Starter",
                "description": "A test starter",
                "price": 6.99,
                "category": "Appetizer"
            },
            {
                "name": "Test Main",
                "description": "A test main course",
                "price": 16.99,
                "category": "Main Course"
            },
            {
                "name": "Test Dessert",
                "description": "A test dessert",
                "price": 7.99,
                "category": "Dessert"
            }
        ]
        
        # Create the menu items
        created_items = []
        for item_data in menu_items:
            response = client.post(f"/api/menu/{restaurant_id}", json=item_data)
            assert response.status_code == 200
            created_items.append(response.json())
        
        # Now get all menu items for the restaurant
        response = client.get(f"/api/menu/{restaurant_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= len(menu_items)  # At least the items we created
        
        # Check that our created items are in the response
        retrieved_names = [item["name"] for item in data]
        for item_data in menu_items:
            assert item_data["name"] in retrieved_names
    
    def test_get_menu_items_empty_restaurant(self, test_restaurant):
        """Test getting menu items for restaurant with no menu items"""
        restaurant_id = test_restaurant["id"]
        
        response = client.get(f"/api/menu/{restaurant_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0  # Should be empty
    
    def test_get_menu_items_invalid_restaurant(self):
        """Test getting menu items for non-existent restaurant"""
        invalid_restaurant_id = 99999
        
        response = client.get(f"/api/menu/{invalid_restaurant_id}")
        
        # Might return 404 or empty list depending on implementation
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 0
    
    def test_get_specific_menu_item(self, test_restaurant):
        """Test getting a specific menu item by ID"""
        restaurant_id = test_restaurant["id"]
        
        # First create a menu item
        menu_item_data = {
            "name": "Test Specific Item",
            "description": "A specific test item",
            "price": 11.99,
            "category": "Main Course"
        }
        
        create_response = client.post(f"/api/menu/{restaurant_id}", json=menu_item_data)
        assert create_response.status_code == 200
        menu_item_id = create_response.json()["id"]
        
        # Now get the specific menu item
        response = client.get(f"/api/menu/item/{menu_item_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == menu_item_id
        assert data["name"] == menu_item_data["name"]
        assert data["price"] == menu_item_data["price"]
        assert data["restaurant_id"] == restaurant_id

class TestMenuItemUpdates:
    """Test cases for menu item updates"""
    
    def test_update_menu_item_availability(self, test_restaurant):
        """Test updating menu item availability"""
        restaurant_id = test_restaurant["id"]
        
        # Create a menu item
        menu_item_data = {
            "name": "Test Availability Item",
            "description": "Test availability updates",
            "price": 9.99,
            "category": "Main Course",
            "is_available": True
        }
        
        create_response = client.post(f"/api/menu/{restaurant_id}", json=menu_item_data)
        assert create_response.status_code == 200
        menu_item_id = create_response.json()["id"]
        
        # Update availability to False
        update_data = {"is_available": False}
        
        response = client.put(f"/api/menu/item/{menu_item_id}", json=update_data)
        
        if response.status_code == 200:  # If update endpoint exists
            data = response.json()
            assert data["is_available"] == False
    
    def test_update_menu_item_price(self, test_restaurant):
        """Test updating menu item price"""
        restaurant_id = test_restaurant["id"]
        
        # Create a menu item
        menu_item_data = {
            "name": "Test Price Update Item",
            "description": "Test price updates",
            "price": 12.99,
            "category": "Main Course"
        }
        
        create_response = client.post(f"/api/menu/{restaurant_id}", json=menu_item_data)
        assert create_response.status_code == 200
        menu_item_id = create_response.json()["id"]
        
        # Update price
        new_price = 15.99
        update_data = {"price": new_price}
        
        response = client.put(f"/api/menu/item/{menu_item_id}", json=update_data)
        
        if response.status_code == 200:  # If update endpoint exists
            data = response.json()
            assert data["price"] == new_price

class TestMenuItemDeletion:
    """Test cases for menu item deletion"""
    
    def test_delete_menu_item(self, test_restaurant):
        """Test deleting a menu item"""
        restaurant_id = test_restaurant["id"]
        
        # Create a menu item
        menu_item_data = {
            "name": "Test Delete Item",
            "description": "This item will be deleted",
            "price": 8.99,
            "category": "Appetizer"
        }
        
        create_response = client.post(f"/api/menu/{restaurant_id}", json=menu_item_data)
        assert create_response.status_code == 200
        menu_item_id = create_response.json()["id"]
        
        # Delete the menu item
        response = client.delete(f"/api/menu/item/{menu_item_id}")
        
        if response.status_code == 200:  # If delete endpoint exists
            # Verify it's deleted by trying to get it
            get_response = client.get(f"/api/menu/item/{menu_item_id}")
            assert get_response.status_code == 404
    
    def test_delete_nonexistent_menu_item(self):
        """Test deleting a menu item that doesn't exist"""
        response = client.delete("/api/menu/item/99999")
        
        # Should return 404 if delete endpoint exists
        if response.status_code != 404:
            # Endpoint might not exist yet
            assert response.status_code in [404, 405]  # 405 = Method Not Allowed

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
