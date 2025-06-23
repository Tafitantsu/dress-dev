from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

# Environment Variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/content_db")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Model ---
class ContentItem(Base):
    __tablename__ = "content_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    body = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

Base.metadata.create_all(bind=engine) # This will create tables if they don't exist

# --- Pydantic Models ---
class ContentItemBase(BaseModel):
    title: str
    description: str | None = None
    body: str

class ContentItemCreate(ContentItemBase):
    pass

class ContentItemUpdate(ContentItemBase):
    title: str | None = None
    description: str | None = None
    body: str | None = None

class ContentItemInDB(ContentItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# FastAPI app instance
app = FastAPI(title="Content Service")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---
@app.post("/content/", response_model=ContentItemInDB, status_code=status.HTTP_201_CREATED)
def create_content_item(item: ContentItemCreate, db: Session = Depends(get_db)):
    db_item = ContentItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/content/{item_id}", response_model=ContentItemInDB)
def read_content_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ContentItem).filter(ContentItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Content item not found")
    return db_item

@app.get("/content/", response_model=List[ContentItemInDB])
def read_content_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(ContentItem).offset(skip).limit(limit).all()
    return items

@app.put("/content/{item_id}", response_model=ContentItemInDB)
def update_content_item(item_id: int, item: ContentItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(ContentItem).filter(ContentItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Content item not found")

    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/content/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ContentItem).filter(ContentItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Content item not found")
    db.delete(db_item)
    db.commit()
    return

@app.get("/")
def read_root():
    return {"message": "Content Service is running"}

# To run this service (for development):
# uvicorn services.content-service.main:app --reload --port 8002
# Remember to set up your DATABASE_URL environment variable.
# Example: DATABASE_URL="postgresql://youruser:yourpassword@localhost:5432/content_db"
# Store this in a .env file in the services/content-service directory.
