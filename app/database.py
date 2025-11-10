from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# ✅ Correct: use variable NAMES
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

# ✅ Debug print (optional)
print("DEBUG MONGO_URL =", MONGO_URL)
print("DEBUG DB_NAME =", DB_NAME)

# ✅ Basic validation
if not MONGO_URL:
    raise ValueError("MONGO_URL is missing from .env")

if not DB_NAME:
    raise ValueError("DB_NAME is missing from .env")

# ✅ Create MongoDB client
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
