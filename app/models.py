from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Product(BaseModel):
    id: str
    name: str
    sku: str
    price: float
    category_id: Optional[str] = None
    created_at: datetime

class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float
    category_id: Optional[str] = None

class Category(BaseModel):
    id: str
    name: str
    description: str = ""

class CategoryCreate(BaseModel):
    name: str
    description: str = ""

class StockMovement(BaseModel):
    id: str
    product_id: str
    quantity: int  # positive = in, negative = out
    reason: str
    timestamp: datetime

class StockAdjust(BaseModel):
    quantity: int
    reason: str

