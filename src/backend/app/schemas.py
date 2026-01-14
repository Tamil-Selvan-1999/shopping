from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class ProductIn(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    imageUrl: Optional[str] = None
    available: Optional[bool] = True


class ProductOut(ProductIn):
    id: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OrderItem(BaseModel):
    productId: str
    quantity: int
    price: float


class OrderCreate(BaseModel):
    items: List[OrderItem]


class OrderOut(BaseModel):
    id: str
    userId: Optional[str]
    items: List[OrderItem]
    totalAmount: float
    createdAt: datetime
