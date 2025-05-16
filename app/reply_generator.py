import requests
from dotenv import load_dotenv
import os

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large"

def analyze_tone(post_text: str) -> str:
    """
    Analyze the tone of the post (simplified heuristic-based approach).
    
    Args:
        post_text: Content of the social media post
        
    Returns:
        Tone description (e.g., "excited", "professional", "casual")
    """
    if any(word in post_text.lower() for word in ["excited", "thrilled", "🎉"]):
        return "excited"
    elif any(word in post_text.lower() for word in ["congratulations", "proud", "achievement"]):
        return "professional"
    return "casual"

def generate_reply(platform: str, post_text: str) -> str:
    """
    Generate a human-like reply using Hugging Face's BART model.
    
    Args:
        platform: Social media platform (Twitter, LinkedIn, Instagram)
        post_text: Content of the social media post
        
    Returns:
        Generated reply text
    """
    tone = analyze_tone(post_text)
    
    # Platform-specific prompt templates
    prompt_templates = {
        "Twitter": f"You are a witty, friendly Twitter user. Generate a reply to the following post that is concise (< 280 characters), matches the {tone} tone, includes 1-2 emojis, and references the post's content. Use casual language and 1 hashtag. Avoid generic phrases.\n\nPost: {post_text}\n\nReply:",
        "LinkedIn": f"You are a supportive, professional LinkedIn user. Generate a reply to the following post that is polite, matches the {tone} tone, and encourages networking. Avoid generic phrases.\n\nPost: {post_text}\n\nReply:",
        "Instagram": f"You are a friendly, casual Instagram user. Generate a reply to the following post that is conversational, matches the {tone} tone, and includes 1-2 emojis. Avoid generic phrases.\n\nPost: {post_text}\n\nReply:"
    }
    
    prompt = prompt_templates[platform]
    
    # Call Hugging Face API
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 100, "num_return_sequences": 1}
    }
    
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Hugging Face API error: {response.text}")
    
    reply = response.json()[0]["generated_text"].split("Reply:")[-1].strip()
    
    # Post-process reply for platform constraints
    if platform == "Twitter" and len(reply) > 280:
        reply = reply[:277] + "..."
    
    return reply