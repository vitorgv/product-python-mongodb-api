from motor.motor_asyncio import AsyncIOMotorClient
from app.auth import get_password_hash
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "productdb")

async def update_password():
    # Test user credentials
    test_password = "testpass123"
    hashed_password = get_password_hash(test_password)
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[MONGODB_DB]
    
    try:
        # Update user's password
        result = await db.users.update_one(
            {"email": "admin@example.com"},
            {"$set": {"hashed_password": hashed_password}}
        )
        
        if result.modified_count > 0:
            print("\nPassword updated successfully!")
            print(f"Email: admin@example.com")
            print(f"Password: {test_password}")
            print(f"New hash: {hashed_password}")
        else:
            print("\nUser not found!")
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(update_password())