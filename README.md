# Zomato Clone - Food Ordering Platform

## 📋 Project Overview

This is a comprehensive food ordering platform built as a Zomato clone using **FastAPI** and **PostgreSQL**. The application provides a complete ecosystem for food delivery services with separate dashboards for restaurant owners and customers.

### Key Components:
- **Restaurant Dashboard**: Restaurant owners can register, add their restaurants, create menus, and track orders with revenue analytics
- **Customer Dashboard**: Users can register, browse restaurants, view menus, place orders, and track their order history
- **Admin Features**: Complete order management and user management system

## 🎥 Demo Videos

Watch the application in action:

1. **Restaurant Owner Dashboard Demo**: [View Demo](https://www.loom.com/share/7243d3147aa84e81bf34ef25c9161a97?sid=dcc7cf39-5f71-480f-ab76-aa91bf2cbbe5)
   - Restaurant registration and management
   - Menu creation and item management
   - Order tracking and revenue analytics

2. **Customer Dashboard Demo**: [View Demo](https://www.loom.com/share/2c9bc5660ced4100abdac8b5f4bc8310?sid=3d9fbacc-1b4d-4e08-b136-eae8fb954fc5)
   - User registration and login
   - Restaurant browsing and menu viewing
   - Order placement and tracking

## ✨ Features

###  Authentication & User Management
- ✅ User Registration & Login (Customers & Restaurant Owners)
- ✅ Role-based access control (Customer/Restaurant Owner)
- ✅ Secure password hashing and JWT token authentication

### Restaurant Owner Dashboard
- ✅ Restaurant Owner Registration & Profile Management
- ✅ Add & Manage Restaurant Details (name, address, contact info)
- ✅ Create & Update Menu Items with categories and pricing
- ✅ View and Track Orders in real-time
-

###  Customer Dashboard
- ✅ Customer Registration & Profile Management
- ✅ Browse All Available Restaurants
- ✅ View Restaurant Menus & Item Details
- ✅ Place Orders with Multiple Items
-

### 📊 Order Management
- ✅ Real-time Order Processing
- ✅ Order Total Calculation with Item Quantities
- ✅ Revenue Tracking per Restaurant

## 🏗️ Project Structure

```
zomato_clone/
├── app/                          # Backend API Application
│   ├── main.py                   # FastAPI app entry point
│   ├── database.py               # PostgreSQL connection setup
│   ├── models/                   # Database interaction layer
│   │   ├── users.py              # User CRUD operations
│   │   ├── resturants.py         # Restaurant CRUD operations
│   │   ├── menu_item.py          # Menu item operations
│   │   └── orders.py             # Order management operations
│   ├── routes/                   # API endpoint definitions
│   │   ├── users.py              # User authentication endpoints
│   │   ├── resturants.py         # Restaurant management endpoints
│   │   ├── menu.py               # Menu item endpoints
│   │   ├── orders.py             # Order processing endpoints
│   │   └── upload.py             # File upload endpoints
│   ├── schemas/                  # Pydantic validation models
│   │   ├── user.py               # User data validation
│   │   ├── restaurant.py         # Restaurant data validation
│   │   ├── menu_item.py          # Menu item validation
│   │   └── order.py              # Order data validation
│   └── utils/                    # Utility functions
│       └── auth.py               # JWT token handling
├── frontend/                     # React Frontend Application
│   ├── src/
│   │   ├── pages/                # React components/pages
│   │   └── assets/               # Static assets
│   └── package.json              # Frontend dependencies
├── tests/                        # Test Suite
│   ├── test_auth.py              # Authentication tests
│   ├── test_restaurant.py        # Restaurant management tests
│   ├── test_menu.py              # Menu operations tests
│   └── test_root.py              # API health check tests
├── migrations/                   # Database migrations
│   └── initial.sql               # Initial database schema
├── uploads/                      # User uploaded files
├── venv/                         # Python virtual environment
├── pyproject.toml                # Python dependencies
└── README.md                     # Project documentation
```



### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Node.js 16+ (for frontend)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd zomato_clone
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup PostgreSQL database**
   ```bash
   # Create database
   createdb zomato_clone
   
   # Run migrations
   psql -d zomato_clone -f migrations/initial.sql
   ```

5. **Configure environment variables**
   ```bash
   # Create .env file with:
   DATABASE_URL=postgresql://username:password@localhost/zomato_clone
   SECRET_KEY=your-secret-key-here
   ```

6. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test files
pytest tests/test_auth.py -v
pytest tests/test_restaurant.py -v
pytest tests/test_menu.py -v
pytest tests/test_root.py -v

# Setup test database
./setup_test_db.sh
```

## 📡 API Endpoints

### Authentication
- `POST /api/users/register` - User registration
- `POST /api/users/login` - User login
- `GET /api/users/{user_id}` - Get user profile

### Restaurants
- `GET /api/restaurants` - List all restaurants
- `POST /api/restaurants` - Create restaurant (owner only)
- `GET /api/restaurants/{restaurant_id}` - Get restaurant details
- `DELETE /api/restaurants/{restaurant_id}` - Delete restaurant

### Menu Management
- `GET /api/menu/{restaurant_id}` - Get restaurant menu
- `POST /api/menu/{restaurant_id}` - Add menu item
- `PUT /api/menu/item/{item_id}` - Update menu item
- `DELETE /api/menu/item/{item_id}` - Delete menu item

### Orders
- `POST /api/orders` - Place new order
- `GET /api/orders/user/{user_id}` - Get user orders
- `GET /api/orders/restaurant/{restaurant_id}` - Get restaurant orders
- `PUT /api/orders/{order_id}/status` - Update order status

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **Pytest** - Testing framework

### Frontend
- **React** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool
- **CSS3** - Styling

##Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the GitHub repository.
