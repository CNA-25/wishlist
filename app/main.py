from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
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

class Wishlist(Base):
    __tablename__ = 'wishlist'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    sku = Column(String, index=True, unique=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

class WishlistItem(BaseModel):
    user_id: int
    sku: str
    name: str
    price: float
    description: str

@app.post("/wishlist/")
async def add_to_wishlist(item: WishlistItem, db: AsyncSession = Depends(get_db)):
    try:
        new_item = Wishlist(
            user_id=item.user_id,
            sku=item.sku,
            name=item.name,
            price=item.price,
            description=item.description,
        )
        db.add(new_item)
        await db.commit()
        return {"message": "Product added to wishlist successfully."}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Item already exists in the wishlist.")
    except Exception as e:
        await db.rollback()
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
