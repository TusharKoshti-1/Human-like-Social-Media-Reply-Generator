import os
import requests

def analyze_tone(post_text: str) -> str:
    """
    Analyze the tone of the post (simple heuristic).
    """
    if any(word in post_text.lower() for word in ["excited", "thrilled", "🎉"]):
        return "excited"
    elif any(word in post_text.lower() for word in ["congratulations", "proud", "achievement"]):
        return "professional"
    return "casual"

def generate_reply(platform: str, post_text: str) -> str:
    """
    Generate a reply using Groq's LLaMA 3.
    """
    tone = analyze_tone(post_text)

    # Define prompt templates
    prompt_templates = {
        "Twitter": f"Generate a witty, friendly Twitter reply to the following post. Keep it concise (<280 characters), match the {tone} tone, include 1-2 emojis, reference the post's content, use casual language, and add 1 hashtag. Avoid generic phrases.\n\nPost: {post_text}\n\nReply:",
        "LinkedIn": f"Generate a supportive, professional LinkedIn reply to the following post. Be polite, match the {tone} tone, encourage networking, and avoid generic phrases. Use professional language.\n\nPost: {post_text}\n\nReply:",
        "Instagram": f"Generate a friendly, casual Instagram reply to the following post. Be conversational, match the {tone} tone, include 1-2 emojis, and avoid generic phrases. Keep it fun and real.\n\nPost: {post_text}\n\nReply:",
        "Facebook": f"Generate a warm, community-style Facebook comment for the following post. Match the {tone} tone, use a few emojis if suitable, and respond in a friendly tone. Reference the content of the post directly.\n\nPost: {post_text}\n\nReply:",
        "Reddit": f"Generate a thoughtful, concise Reddit comment for this post. Match the {tone} tone and be relevant to the subreddit culture. Avoid fluff. Include subtle humor if applicable.\n\nPost: {post_text}\n\nComment:",
        "YouTube": f"Write a short YouTube comment matching the {tone} tone. Be engaging and relevant to the video's content. Add a light emoji if suitable. Avoid spammy vibes.\n\nPost: {post_text}\n\nComment:",
        "Threads": f"Generate a conversational Threads (Meta) reply to the following post. Match the {tone} tone, use casual and trendy language, include 1 emoji, and avoid clichés.\n\nPost: {post_text}\n\nReply:",
        "TikTok": f"Write a fun and relatable TikTok comment. Match the {tone} tone. Keep it short, casual, and engaging with 1-2 emojis or slang. Avoid generic praise.\n\nPost: {post_text}\n\nComment:"
    }

    prompt = prompt_templates.get(platform)
    if not prompt:
        raise ValueError(f"Unsupported platform: {platform}")

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful social media assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 120
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"].strip()

        if platform == "Twitter" and len(reply) > 280:
            reply = reply[:277] + "..."

        return reply

    except Exception as e:
        raise Exception(f"Failed to generate reply: {str(e)}")
