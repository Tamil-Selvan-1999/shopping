import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app import auth

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("MONGO_DB", "shopping_poc")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")


async def create_admin():
    if not ADMIN_EMAIL:
        print("Please set ADMIN_EMAIL environment variable before running this script.")
        return
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    existing = await db["users"].find_one({"email": ADMIN_EMAIL})
    if existing:
        print(f"Admin user already exists: {ADMIN_EMAIL}")
        user_id = existing.get("_id")
    else:
        hashed = auth.hash_password(ADMIN_PASSWORD)
        res = await db["users"].insert_one(
            {"email": ADMIN_EMAIL, "passwordHash": hashed}
        )
        user_id = res.inserted_id
        print(f"Created admin user: {ADMIN_EMAIL}")
    token = auth.create_access_token(str(user_id))
    print("Use this token for admin requests (set JWT_SECRET if changed):")
    print(token)


if __name__ == "__main__":
    asyncio.run(create_admin())
