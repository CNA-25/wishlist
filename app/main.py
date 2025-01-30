from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import os 
from dotenv import load_dotenv

load_dotenv()

# FastAPI app
app = FastAPI()

# Database connection setup
SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')

# Create the database engine and sessionmaker
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Define the Item database model
class Item(Base):
    __tablename__ = "wishlist"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    product_id = Column(Integer)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Pydantic model to validate the incoming request body
class ItemCreate(BaseModel):
    user_id: int
    product_id: int

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST endpoint to create an item
@app.post("/wishlist/")
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(item_id=item.user_id, product_id=item.product_id)
    db.add(db_item)
    try:
        db.commit()
        db.refresh(db_item)
        return {"listing id": db_item.id, "user id": db_item.user_id, "product id": db_item.product_id}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
