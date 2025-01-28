# Wishlist Service

# Features

- Add a product to the wishlist
- Remove a product from the wishlist
- Retrieve a user's wishlist
- Prevent duplicate wishlist entries

# Tech Stack
- Backend: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy

# Installation & Setup

# Clone the Repository

- git clone https://github.com/your-repo/wishlist-service.git

# Install Dependencies

- pip install -r requirements.txt

# Configure Database
- Update .env with your PostgreSQL credentials:
- DATABASE_URL=postgresql://user:password@localhost:5432/wishlist_db

# Start the FastAPI Server
- uvicorn main:app --reload

#  API Endpoints
- Add Product to Wishlist
- POST /wishlist/
- Request Body:

{
    "user_id": "123",
    "product_id": "456"
}
Response:
{
    "message": "Product added to wishlist"
}

# Get User's Wishlist
- GET /wishlist/{user_id}
Response:

[
    {"product_id": "456", "name": "Product Name", "price": 59.99}
]

# Remove Product from Wishlist
- DELETE /wishlist/
Request Body:

{
    "user_id": "123",
    "product_id": "456"
}
Response:
{
    "message": "Product removed from wishlist"
}

# Database Schema

CREATE TABLE wishlist (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    product_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_product UNIQUE (user_id, product_id)
);

