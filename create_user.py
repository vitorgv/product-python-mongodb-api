from motor.motor_asyncio import AsyncIOMotorClient
from app.auth import get_password_hash
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def create_user():
    # Connect to MongoDB
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB = os.getenv("MONGODB_DB", "productdb")
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[MONGODB_DB]
    
    # Create test user
    test_user = {
        "email": "test@example.com",
        "hashed_password": get_password_hash("testpassword123"),
        "is_active": 1
    }
    
    try:
        await db.users.insert_one(test_user)
        print("Test user created successfully!")
    except Exception as e:
        if "duplicate key error" in str(e):
            print("User already exists!")
        else:
            print(f"Error creating user: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_user())
