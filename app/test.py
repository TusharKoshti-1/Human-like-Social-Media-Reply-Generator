# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()
print(f"MONGODB_URI: {os.getenv('MONGODB_URI')}")