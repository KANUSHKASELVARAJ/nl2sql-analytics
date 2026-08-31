import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "nl_nosql")

client = MongoClient(MONGO_URI)

db = client[MONGO_DB]


def test_connection():
    try:
        client.admin.command("ping")
        print("MongoDB connected successfully!")
        return True
    except Exception as e:
        print("MongoDB connection failed:", e)
        return False


def get_collection(name):
    return db[name]