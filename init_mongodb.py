from motor.motor_asyncio import AsyncIOMotorClient
from app.auth import get_password_hash
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "productdb")

async def init_mongodb():
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[MONGODB_DB]
    
    # Create indexes
    await db.categories.create_index("name", unique=True)
    await db.users.create_index("email", unique=True)
    await db.products.create_index("name")
    await db.products.create_index("category_id")
    
    # Create default user if not exists
    default_user = {
        "email": "admin@example.com",
        "hashed_password": get_password_hash("testpass123"),
        "is_active": 1
    }
    
    try:
        await db.users.insert_one(default_user)
        print("Default user created successfully!")
    except Exception as e:
        if "duplicate key error" in str(e):
            print("Default user already exists")
        else:
            print(f"Error creating default user: {str(e)}")
    
    # Create some sample categories
    categories = [
        {"name": "Electronics", "description": "Electronic devices and accessories"},
        {"name": "Books", "description": "Physical and digital books"},
        {"name": "Clothing", "description": "Apparel and accessories"},
        {"name": "Home & Garden", "description": "Home improvement and garden supplies"},
        {"name": "Sports", "description": "Sports equipment and accessories"}
    ]
    
    for category in categories:
        try:
            await db.categories.insert_one(category)
            print(f"Created category: {category['name']}")
        except Exception as e:
            if "duplicate key error" in str(e):
                print(f"Category {category['name']} already exists")
            else:
                print(f"Error creating category {category['name']}: {str(e)}")
    
    # Close the connection
    client.close()
    print("\nMongoDB initialization completed!")

if __name__ == "__main__":
    asyncio.run(init_mongodb())