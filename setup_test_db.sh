#!/bin/bash

# Set environment variables
export PGPASSWORD=postgres123

# Create test database if it doesn't exist
psql -h localhost -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'zomato_clone'" | grep -q 1 || \
    psql -h localhost -U postgres -c "CREATE DATABASE zomato_clone"

# Apply migrations
psql -h localhost -U postgres -d zomato_clone -f migrations/initial.sql

# Run tests
python3 -m pytest tests/ -v
