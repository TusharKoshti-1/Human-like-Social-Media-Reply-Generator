from fastapi import FastAPI, HTTPException
from app.models import PostRequest
from app.reply_generator import generate_reply
from app.database import insert_post_reply, collection
from datetime import datetime


app = FastAPI()

@app.post("/reply")
async def generate_reply_endpoint(post: PostRequest):
    try:
        reply = generate_reply(post.platform, post.post_text)
        data = {
            "platform": post.platform,
            "post_text": post.post_text,
            "generated_reply": reply,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        insert_post_reply(data.copy())
        
        # Query inserted document (example)
        inserted_doc = collection.find_one({
            "platform": data["platform"],
            "post_text": data["post_text"],
            "timestamp": data["timestamp"]
        })
        
        # Convert ObjectId to string
        if inserted_doc:
            inserted_doc["_id"] = str(inserted_doc["_id"])
        
        return inserted_doc or data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate reply: {str(e)}")
    
