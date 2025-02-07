from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

load_dotenv("./code/.env")

DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app = FastAPI()
Base = declarative_base()

class Wishlist(Base):
    __tablename__ = "wishlist"
    user_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, primary_key=True, index=True)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

class WishlistItem(BaseModel):
    user_id: int
    product_id: int

@app.post("/wishlist/")
async def add_to_wishlist(item: WishlistItem, db: AsyncSession = Depends(get_db)):
    try:
        new_item = Wishlist(user_id=item.user_id, product_id=item.product_id)
        db.add(new_item)
        await db.commit()
        (f"Added item to wishlist: {item}")
        return {"message": "Product added to wishlist successfully."}
    except IntegrityError:
        await db.rollback() 
        (f"Error: Item already exists in wishlist. User ID: {item.user_id}, Product ID: {item.product_id}")
        raise HTTPException(status_code=400, detail="Item already exists in the wishlist.")
    except Exception as e:
        await db.rollback()
        (f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")

@app.get("/wishlist/{user_id}")
async def get_wishlist(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Wishlist).filter(Wishlist.user_id == user_id)
        result = await db.execute(stmt)
        wishlist_items = result.scalars().all()
        return {"wishlist": [{"user_id": item.user_id, "product_id": item.product_id} for item in wishlist_items]}
    except Exception as e:
        (f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    
@app.delete("/wishlist/{user_id}/{product_id}")
async def remove_from_wishlist(user_id: int, product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Wishlist).filter(Wishlist.user_id == user_id, Wishlist.product_id == product_id)
        result = await db.execute(stmt)
        wishlist_item = result.scalar_one_or_none()
        if not wishlist_item:
            raise HTTPException(status_code=404, detail="Item not found in wishlist.")
        await db.delete(wishlist_item)
        await db.commit()
        return {"message": "Product removed from wishlist successfully."}
    except Exception as e:
        await db.rollback()
        (f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")
