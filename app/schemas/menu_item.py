# app/schemas/menu_item.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MenuItemCreate(BaseModel):
    name: str
    price: float
    category: Optional[str] = None
    image: Optional[str] = None

class MenuItemResponse(BaseModel):
    id: int
    name: str
    price: float
    category: Optional[str]
    image: Optional[str]
    created_at: Optional[datetime] = None
