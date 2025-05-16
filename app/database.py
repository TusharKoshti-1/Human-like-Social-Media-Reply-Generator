from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB setup
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["social_media_replies"]
collection = db["replies"]

async def insert_post_reply(data: dict):
    """
    Insert a post-reply pair into MongoDB.
    
    Args:
        data: Dictionary containing platform, post_text, generated_reply, timestamp
    """
    try:
        await collection.insert_one(data)
    except Exception as e:
        raise Exception(f"Database insertion failed: {str(e)}")