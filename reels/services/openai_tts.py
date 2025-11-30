"""
OpenAI Text-to-Speech service.
"""
import os
from pathlib import Path
from django.conf import settings
from openai import OpenAI
from ..models import ReelJob


class OpenAITTSError(Exception):
    """Custom exception for OpenAI TTS errors."""
    pass


def generate_tts_audio(script: str, reel_job: ReelJob) -> str:
    """
    Generate speech audio for the given script using OpenAI TTS API.
    Save it under the reel's folder, update the ReelJob.audio_file, and return the absolute path.
    
    Args:
        script: The script text to convert to speech
        reel_job: The ReelJob instance to associate the audio with
    
    Returns:
        Absolute path to the saved audio file
    
    Raises:
        OpenAITTSError: If the TTS generation fails
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        raise OpenAITTSError("OPENAI_API_KEY not configured in settings")
    
    client = OpenAI(api_key=api_key)
    
    # Create job-specific directory
    job_dir = settings.MEDIA_ROOT / 'reels' / str(reel_job.id)
    job_dir.mkdir(parents=True, exist_ok=True)
    
    audio_path = job_dir / 'audio.mp3'
    
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
            input=script,
        )
        
        # Save the audio file
        with open(audio_path, 'wb') as f:
            for chunk in response.iter_bytes():
                f.write(chunk)
        
        # Update the ReelJob model
        relative_audio_path = f'reels/{reel_job.id}/audio.mp3'
        reel_job.audio_file.name = relative_audio_path
        reel_job.save()
        
        return str(audio_path.absolute())
    
    except Exception as e:
        raise OpenAITTSError(f"Failed to generate TTS audio: {str(e)}") from e

