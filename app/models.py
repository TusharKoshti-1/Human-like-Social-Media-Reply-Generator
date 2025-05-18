from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class PostRequest(BaseModel):
    platform: Literal[
        "Twitter",
        "LinkedIn",
        "Instagram",
        "Facebook",
        "Reddit",
        "YouTube",
        "Threads",
        "TikTok"
    ] = Field(..., description="Social media platform to generate a reply for.")
    post_text: str = Field(..., min_length=1, max_length=1000, description="Content of the social media post.")

class PostResponse(BaseModel):
    platform: str
    post_text: str
    generated_reply: str
    timestamp: datetime
