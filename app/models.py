from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator
from bson import ObjectId

# Custom type for ObjectId fields
PyObjectId = Annotated[str, BeforeValidator(lambda x: str(ObjectId(x)) if x else None)]

class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

class CategoryDB(MongoBaseModel):
    name: str
    description: Optional[str] = None

class ProductDB(MongoBaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserDB(MongoBaseModel):
    email: str
    hashed_password: str
    is_active: int = 1
