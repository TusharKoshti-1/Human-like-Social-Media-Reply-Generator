from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB setup
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing in .env file")
if not (MONGODB_URI.startswith("mongodb://") or MONGODB_URI.startswith("mongodb+srv://")):
    raise ValueError(f"Invalid MONGODB_URI: '{MONGODB_URI}'. Must start with 'mongodb://' or 'mongodb+srv://'")

try:
    client = MongoClient(MONGODB_URI)
    client.server_info()  # Test connection
    db = client["social_media_replies"]
    collection = db["replies"]
except Exception as e:
    raise Exception(f"Failed to connect to MongoDB: {str(e)}")

def insert_post_reply(data: dict):
    """
    Insert a post-reply pair into MongoDB.
    
    Args:
        data: Dictionary containing platform, post_text, generated_reply, timestamp
    """
    try:
        collection.insert_one(data)
    except Exception as e:
        raise Exception(f"Database insertion failed: {str(e)}")