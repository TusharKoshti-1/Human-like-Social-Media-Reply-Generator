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

    # Define prompt
    prompt_templates = {
        "Twitter": f"Generate a witty, friendly Twitter reply to the following post. Keep it concise (< 280 characters), match the {tone} tone, include 1-2 emojis, reference the post's content, use casual language, and add 1 hashtag. Avoid generic phrases.\n\nPost: {post_text}\n\nReply:",
        "LinkedIn": f"Generate a supportive, professional LinkedIn reply to the following post. Be polite, match the {tone} tone, encourage networking, and avoid generic phrases.\n\nPost: {post_text}\n\nReply:",
        "Instagram": f"Generate a friendly, casual Instagram reply to the following post. Be conversational, match the {tone} tone, include 1-2 emojis, and avoid generic phrases.\n\nPost: {post_text}\n\nReply:"
    }

    prompt = prompt_templates.get(platform)
    if not prompt:
        raise ValueError(f"Unsupported platform: {platform}")

    # Send request to Groq
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",  # Make sure this is set
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
