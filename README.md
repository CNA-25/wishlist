<<<<<<< HEAD
=======
# Wishlist Service

# Features

- Add a product to the wishlist
- Remove a product from the wishlist
- Retrieve a user's wishlist
- Prevent duplicate wishlist entries

# Tech Stack
- Backend: FastAPI (Use /docs in endpoint for api documentation)
- Database: PostgreSQL
- ORM: SQLAlchemy

# Installation & Setup

# Clone the Repository

- git clone https://github.com/CNA-25/wishlist

# Install Dependencies

- pip install -r requirements.txt

# Configure Database
- Update .env with your PostgreSQL credentials:
- DATABASE_URL=postgresql://user:password@localhost:5432/wishlist_db

# Start the FastAPI Server
- uvicorn app.main:app --reload

#  API Endpoints
- Add Product to Wishlist
POST https://wishlist-git-wishlist.2.rahtiapp.fi/wishlist/
Content-Type: application/json

{
    "user_id": 2,
    "sku": "123-ABC",
    "name": "Lager", 
    "price": 55.99,
    "description": "En ljus och frisk lager med balanserad smak."
}
Response:
{
    "message": "Product added to wishlist"
}

# Get User's Wishlist
- GET /wishlist/{user_id}
Response:

[
    {
      "user_id": 2,
      "sku": "123-ABC",
      "name": "Lager",
      "price": 55.99,
      "description": "En ljus och frisk lager med balanserad smak."
    }
]

# Remove Product from Wishlist
- DELETE https://wishlist-git-wishlist.2.rahtiapp.fi/wishlist/{user_id}/{sku}

Response:
{
    "message": "Product removed from wishlist"
}

# Database Schema

CREATE TABLE wishlist (
id SERIAL PRIMARY KEY,
user_id INT NOT NULL,
sku VARCHAR(50) UNIQUE NOT NULL,
name TEXT NOT NULL,
price DECIMAL(10,2) NOT NULL,
description TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
>>>>>>> 171655fa63cd125d5706fd7c45083e278f64d499

