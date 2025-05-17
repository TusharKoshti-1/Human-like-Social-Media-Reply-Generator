from fastapi import FastAPI, HTTPException
from app.models import PostRequest
from app.reply_generator import generate_reply
from app.database import insert_post_reply
from datetime import datetime

app = FastAPI()

@app.post("/reply")
async def generate_reply_endpoint(post: PostRequest):
    try:
        # Generate reply
        reply = generate_reply(post.platform, post.post_text)
        
        # Prepare data for storage
        data = {
            "platform": post.platform,
            "post_text": post.post_text,
            "generated_reply": reply,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Insert into MongoDB (synchronous call, no await)
        insert_post_reply(data)
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate reply: {str(e)}")