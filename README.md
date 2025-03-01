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
https://wishlist-git-wishlist.2.rahtiapp.fi/wishlist/

- Add Product to JWT token ID Wishlist
POST /wishlist/{sku}

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
      "sku": "123-ABC"
    }
]

# Remove Product from JWT token ID Wishlist
- DELETE /wishlist/{sku}

Response:
{
    "message": "Product removed from wishlist"
}

# Database Schema

CREATE TABLE wishlist (
id SERIAL PRIMARY KEY,
user_id INT NOT NULL,
sku VARCHAR(50) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
>>>>>>> 171655fa63cd125d5706fd7c45083e278f64d499

