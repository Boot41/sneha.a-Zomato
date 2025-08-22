# Specification

## User Features
- Signup/Login (email + password)
- Browse restaurants
- Search/filter by name or cuisine
- View restaurant menu
- Add to cart & place order (COD)
- View order history

## Restaurant Features
- Register/Login
- Add & manage menu items
- View incoming orders

## Admin Features (optional)
- Approve/reject restaurants
- View all users & restaurants

## API Endpoints (high-level)
- POST /auth/signup
- POST /auth/login
- GET /restaurants
- GET /restaurants/{id}/menu
- POST /orders
- GET /orders
- POST /restaurants/menu
- GET /restaurants/orders
