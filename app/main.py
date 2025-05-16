from fastapi import FastAPI, HTTPException
from app.models import PostRequest, PostResponse
from app.reply_generator import generate_reply
from app.database import insert_post_reply
from datetime import datetime

app = FastAPI(title="Social Media Reply Generator")

@app.post("/reply", response_model=PostResponse)
async def create_reply(post: PostRequest):
    """
    Generate a human-like reply to a social media post and store it in the database.
    
    Args:
        post: JSON containing platform and post_text
        
    Returns:
        JSON with platform, post_text, generated_reply, and timestamp
        
    Raises:
        HTTPException: If platform is invalid or generation fails
    """
    valid_platforms = {"Twitter", "LinkedIn", "Instagram"}
    if post.platform not in valid_platforms:
        raise HTTPException(status_code=400, detail=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}")
    
    try:
        # Generate reply
        reply = generate_reply(post.platform, post.post_text)
        
        # Prepare response
        timestamp = datetime.utcnow()
        response = PostResponse(
            platform=post.platform,
            post_text=post.post_text,
            generated_reply=reply,
            timestamp=timestamp
        )
        
        # Store in database
        await insert_post_reply({
            "platform": post.platform,
            "post_text": post.post_text,
            "generated_reply": reply,
            "timestamp": timestamp
        })
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate reply: {str(e)}")