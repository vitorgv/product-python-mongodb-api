from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, List, Annotated
from datetime import datetime
from bson import ObjectId

# Custom type for ObjectId fields
PyObjectId = Annotated[str, BeforeValidator(lambda x: str(ObjectId(x)) if x else None)]

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: str = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category_id: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str = Field(alias="_id")
    is_active: bool

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
