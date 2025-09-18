from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "productdb")

async def check_users():
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[MONGODB_DB]
    
    # Get all users
    users = await db.users.find().to_list(None)
    print("\nCurrent users in database:")
    for user in users:
        print(f"ID: {user['_id']}")
        print(f"Email: {user['email']}")
        print(f"Password hash: {user['hashed_password']}")
        print(f"Active: {user.get('is_active', 1)}")
        print("-" * 50)
    
    # Close the connection
    client.close()

if __name__ == "__main__":
    asyncio.run(check_users())
