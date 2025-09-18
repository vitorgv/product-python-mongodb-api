from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import json
import csv
from io import StringIO
from fastapi.responses import StreamingResponse
from datetime import timedelta, datetime
from bson import ObjectId
from . import models, schemas, auth
from .database import get_db

app = FastAPI(
    title="Product Management System API",
    description="A RESTful API for managing products and categories with token-based authentication",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "authentication",
            "description": "Operations related to authentication"
        },
        {
            "name": "categories",
            "description": "CRUD operations for product categories"
        },
        {
            "name": "products",
            "description": "CRUD operations for products"
        },
        {
            "name": "export",
            "description": "Data export operations"
        }
    ]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication endpoints
@app.post("/token", response_model=schemas.Token, tags=["authentication"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Authenticate user and return JWT token
    
    - **username**: Email address of the user
    - **password**: User's password
    """
    user = await db.users.find_one({"email": form_data.username})
    if not user or not auth.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Category endpoints
@app.post("/categories/", response_model=schemas.CategoryResponse)
async def create_category(
    category: schemas.CategoryCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    category_dict = category.dict()
    result = await db.categories.insert_one(category_dict)
    created_category = await db.categories.find_one({"_id": result.inserted_id})
    return created_category

@app.get("/categories/", response_model=List[schemas.CategoryResponse])
async def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    categories = await db.categories.find().skip(skip).limit(limit).to_list(None)
    return categories

@app.get("/categories/{category_id}", response_model=schemas.CategoryResponse)
async def read_category(
    category_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        category = await db.categories.find_one({"_id": ObjectId(category_id)})
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    except:
        raise HTTPException(status_code=400, detail="Invalid category ID")

# Product endpoints
@app.post("/products/", response_model=schemas.ProductResponse)
async def create_product(
    product: schemas.ProductCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    product_dict = product.dict()
    product_dict["category_id"] = ObjectId(product_dict["category_id"])
    product_dict["created_at"] = datetime.utcnow()
    product_dict["updated_at"] = datetime.utcnow()
    result = await db.products.insert_one(product_dict)
    created_product = await db.products.find_one({"_id": result.inserted_id})
    return created_product

@app.get("/products/", response_model=List[schemas.ProductResponse])
async def read_products(
    skip: int = 0,
    limit: int = 100,
    category_id: str = None,
    name: str = None,
    db: AsyncIOMotorDatabase = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    query = {}
    if category_id:
        try:
            query["category_id"] = ObjectId(category_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid category ID")
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    
    products = await db.products.find(query).skip(skip).limit(limit).to_list(None)
    return products

@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
async def read_product(
    product_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        product = await db.products.find_one({"_id": ObjectId(product_id)})
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except:
        raise HTTPException(status_code=400, detail="Invalid product ID")

@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
async def update_product(
    product_id: str,
    product: schemas.ProductCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        product_dict = product.dict()
        product_dict["category_id"] = ObjectId(product_dict["category_id"])
        product_dict["updated_at"] = datetime.utcnow()
        
        result = await db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product_dict}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
            
        updated_product = await db.products.find_one({"_id": ObjectId(product_id)})
        return updated_product
    except:
        raise HTTPException(status_code=400, detail="Invalid product ID")

@app.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        result = await db.products.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}
    except:
        raise HTTPException(status_code=400, detail="Invalid product ID")

# Export endpoints
@app.get("/export/products/json")
async def export_products_json(
    db: AsyncIOMotorDatabase = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    products = await db.products.find().to_list(None)
    products_list = []
    for product in products:
        product["id"] = str(product["_id"])
        product["category_id"] = str(product["category_id"])
        del product["_id"]
        products_list.append(product)
    return products_list

@app.get("/export/products/csv")
async def export_products_csv(
    db: AsyncIOMotorDatabase = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    products = await db.products.find().to_list(None)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "description", "price", "quantity", "category_id", "created_at", "updated_at"])
    
    for product in products:
        writer.writerow([
            str(product["_id"]),
            product["name"],
            product["description"],
            product["price"],
            product["quantity"],
            str(product["category_id"]),
            product["created_at"].isoformat() if "created_at" in product else "",
            product["updated_at"].isoformat() if "updated_at" in product else ""
        ])
    
    response = StreamingResponse(iter([output.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=products.csv"
    return response
