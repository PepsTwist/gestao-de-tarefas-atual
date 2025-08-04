#!/usr/bin/env python3

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def test_user():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Find the user
    user = await db.users.find_one({"email": "r.cortezzz7@gmail.com"})
    if user:
        print("User found:")
        print(f"Email: {user.get('email')}")
        print(f"Available fields: {list(user.keys())}")
        print(f"Has password_hash: {'password_hash' in user}")
        print(f"Has hashed_password: {'hashed_password' in user}")
        if 'hashed_password' in user:
            print(f"Hashed password: {user['hashed_password'][:20]}...")
    else:
        print("User not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(test_user())