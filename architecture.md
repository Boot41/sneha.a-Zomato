# Architecture

## Overview
This project is a food ordering MVP built with FastAPI and PostgreSQL.
We use psycopg2 for database connectivity.

## Components
- FastAPI (backend framework)
- PostgreSQL (database)
- psycopg2 (database driver)
- Pydantic (data validation)
- JWT authentication (email + password login)

## Flow
1. User signs up (customer or restaurant owner).
2. Customers browse restaurants and menus.
3. Customers add items to cart and place orders.
4. Restaurants receive orders and update status.
5. (Optional) Admin can approve/reject restaurants.

## Database Design
- Users
- Restaurants
- Menu Items
- Orders
- Order Items
