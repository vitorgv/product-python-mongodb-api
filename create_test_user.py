from motor.motor_asyncio import AsyncIOMotorClient
from app.auth import get_password_hash
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

# Create test user with known credentials
user_email = "admin@example.com"
user_password = "testpass123"
hashed_password = get_password_hash(user_password)

print(f"Test user email: {user_email}")
print(f"Test user password: {user_password}")
print(f"Hashed password: {hashed_password}")

async def create_test_user():
    # Connect to MongoDB
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB = os.getenv("MONGODB_DB", "productdb")
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[MONGODB_DB]
    
    # Create the user
    test_user = {
        "email": user_email,
        "hashed_password": hashed_password,
        "is_active": 1
    }
    
    try:
        await db.users.insert_one(test_user)
        print("\nTest user created successfully!")
    except Exception as e:
        if "duplicate key error" in str(e):
            print("\nUser already exists!")
        else:
            print(f"\nError creating user: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_test_user())
