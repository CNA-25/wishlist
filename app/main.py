from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from jose import jwt, ExpiredSignatureError, JWTError
from fastapi.middleware.cors import CORSMiddleware # for corss-origin
import os
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app = FastAPI()
Base = declarative_base()

# ALLOW CROSS ORIGIN
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now, you can limit it to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

#Auth

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")
#verify and decode JWT
def verify_jwt_token(authorization: str = Header(...)):
    try:
        if not authorization:
            raise HTTPException(status_code=403, detail="Authorization header missing.")
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except IndexError:
        raise HTTPException(status_code=403, detail="Invalid authorization header format.")
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

#
class Wishlist(Base):
    __tablename__ = 'wishlist'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    sku = Column(String, index=True)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

class WishlistItem(BaseModel):
    user_id: int
    sku: str

#add one item to the JWT users wishlist
#the only part of the JWT token we care about is the sub (user id)
@app.post("/wishlist/{sku}")
async def add_to_wishlist(sku: str, db: AsyncSession = Depends(get_db), user: dict = Depends(verify_jwt_token)):
    try:
        #user.get("sub") is the users id.
        new_item = Wishlist(
            user_id =int(user.get("sub")),
            sku=sku
        )
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)
        return {"message": "Product added to wishlist successfully."}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Item already exists in the wishlist.")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {e}")

#question: should you be able to browse other users wishlist? this code allows for that.
@app.get("/wishlist/{user_id}")
async def get_wishlist(user_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(verify_jwt_token)):
    try:
        stmt = select(Wishlist).filter(Wishlist.user_id == user_id)
        result = await db.execute(stmt)
        wishlist_items = result.scalars().all()
        return {
            "wishlist": [
                {
                    "user_id": item.user_id,
                    "sku": item.sku
                }
                for item in wishlist_items
            ]
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    

@app.get("/wishlist/")
async def get_wishlist(db: AsyncSession = Depends(get_db), user: dict = Depends(verify_jwt_token)):
    try:
        stmt = select(Wishlist).filter(Wishlist.user_id == int(user.get("sub")))
        result = await db.execute(stmt)
        wishlist_items = result.scalars().all()
        return {
            "wishlist": [
                {
                    "user_id": item.user_id,
                    "sku": item.sku
                }
                for item in wishlist_items
            ]
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")

#remove one product from the JWT logged users wishlist.
@app.delete("/wishlist/{sku}")
async def remove_from_wishlist(sku: str, db: AsyncSession = Depends(get_db), user: dict = Depends(verify_jwt_token)):
    try:
        #find the specific item in the list, that Also has a matching user id
        stmt = select(Wishlist).filter(Wishlist.user_id == int(user.get("sub")), Wishlist.sku == sku)
        result = await db.execute(stmt)
        wishlist_item = result.scalar_one_or_none()
        if not wishlist_item:
            raise HTTPException(status_code=404, detail="Item not found in wishlist.")
        await db.delete(wishlist_item)
        await db.commit()
        return {"message": "Product removed from wishlist successfully."}
    except Exception as e:
        await db.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")
