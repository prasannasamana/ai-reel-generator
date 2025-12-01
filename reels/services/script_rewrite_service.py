"""
Script rewriting service with human-in-the-loop support.
Handles script rewriting in Django, allows user approval before proceeding.
"""
from typing import Literal
from django.conf import settings
from openai import OpenAI

Tone = Literal["neutral", "friendly", "formal", "energetic", "dramatic"]


class ScriptRewriteError(Exception):
    """Custom exception for script rewrite errors."""
    pass


def rewrite_script(original_script: str, tone: Tone = "neutral", max_seconds: int | None = None) -> str:
    """
    Rewrite a script using OpenAI API to match the requested tone.
    This is called in Django, user can approve or regenerate.
    
    Args:
        original_script: The original script text
        tone: The desired tone (neutral, friendly, formal, energetic, dramatic)
        max_seconds: Optional target length in seconds (approximate)
    
    Returns:
        The rewritten script as a string
    
    Raises:
        ScriptRewriteError: If the API call fails
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        raise ScriptRewriteError("OPENAI_API_KEY not configured in settings")
    
    client = OpenAI(api_key=api_key)
    
    # Build the prompt
    tone_instructions = {
        "neutral": "Keep the tone neutral and professional.",
        "friendly": "Make the tone warm, approachable, and conversational.",
        "formal": "Use a formal, professional, and authoritative tone.",
        "energetic": "Make it energetic, enthusiastic, and exciting.",
        "dramatic": "Use a dramatic, impactful, and emotionally engaging tone.",
    }
    
    prompt = f"""Rewrite the following script to have a {tone} tone. {tone_instructions.get(tone, '')}
    
    Original script:
    {original_script}
    
    Rewritten script:"""
    
    if max_seconds:
        prompt += f"\n\nTarget length: approximately {max_seconds} seconds when spoken (roughly {max_seconds * 2.5} words)."
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional script writer. Rewrite scripts to match the requested tone while preserving the core message."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        rewritten_script = response.choices[0].message.content.strip()
        return rewritten_script
    
    except Exception as e:
        raise ScriptRewriteError(f"Failed to rewrite script: {str(e)}") from e

