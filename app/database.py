from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "productdb")

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def get_database():
    if db.client is None:
        db.client = AsyncIOMotorClient(MONGODB_URL)
        db.db = db.client[MONGODB_DB]
    return db.db

async def close_database():
    if db.client is not None:
        db.client.close()
        db.client = None

async def get_db():
    database = await get_database()
    try:
        yield database
    finally:
        pass  # Connection is managed by FastAPI lifecycle
