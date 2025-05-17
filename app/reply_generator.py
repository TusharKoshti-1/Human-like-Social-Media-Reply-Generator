# from dotenv import load_dotenv
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# load_dotenv()

# Load model and tokenizer
try:
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
    # Move model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
except Exception as e:
    raise Exception(f"Failed to load model or tokenizer: {str(e)}")

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
    Generate a human-like reply using the local facebook/bart-large-cnn model.
    
    Args:
        platform: Social media platform (Twitter, LinkedIn, Instagram)
        post_text: Content of the social media post
        
    Returns:
        Generated reply text
        
    Raises:
        Exception: If model processing fails
    """
    tone = analyze_tone(post_text)
    
    # Platform-specific prompt templates
    prompt_templates = {
        "Twitter": f"Generate a witty, friendly Twitter reply to the following post. Keep it concise (< 280 characters), match the {tone} tone, include 1-2 emojis, reference the post's content, use casual language, and add 1 hashtag. Avoid generic phrases.\n\nPost: {post_text}\n\nReply:",
        "LinkedIn": f"Generate a supportive, professional LinkedIn reply to the following post. Be polite, match the {tone} tone, encourage networking, and avoid generic phrases.\n\nPost: {post_text}\n\nReply:",
        "Instagram": f"Generate a friendly, casual Instagram reply to the following post. Be conversational, match the {tone} tone, include 1-2 emojis, and avoid generic phrases.\n\nPost: {post_text}\n\nReply:"
    }
    
    prompt = prompt_templates[platform]
    
    try:
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}  # Move to GPU/CPU
        
        # Generate reply
        outputs = model.generate(
            **inputs,
            max_length=100,
            num_return_sequences=1,
            do_sample=True,  # Add randomness for varied replies
            top_p=0.95,      # Nucleus sampling for natural text
            temperature=0.7  # Control creativity
        )
        
        # Decode generated text
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Debug: Log generated text
        print(f"Generated Text: {generated_text}")
        
        if not generated_text:
            return f"Sorry, I couldn't generate a reply. Let's connect on {platform}! 😊"
        
        # Extract reply after "Reply:" if present, otherwise use the full text
        reply_parts = generated_text.split("Reply:")
        reply = reply_parts[-1].strip() if len(reply_parts) > 1 else generated_text.strip()
        
        # Post-process reply for platform constraints
        if platform == "Twitter" and len(reply) > 280:
            reply = reply[:277] + "..."
        
        return reply
    
    except Exception as e:
        raise Exception(f"Failed to generate reply: {str(e)}")