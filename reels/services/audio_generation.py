"""
Audio generation service - generates TTS audio when script is approved.
"""
from ..models import ReelJob
from .openai_tts import generate_tts_audio, OpenAITTSError


def generate_audio_for_approved_script(reel_job: ReelJob) -> ReelJob:
    """
    Generate TTS audio for an approved script.
    This is called when script is approved (either manually or auto-approved).
    
    Args:
        reel_job: The ReelJob instance with approved final_script
    
    Returns:
        The updated ReelJob instance
    
    Raises:
        OpenAITTSError: If audio generation fails
    """
    # Check script is approved
    if not reel_job.script_approved or not reel_job.final_script:
        raise Exception("Script must be approved before generating audio")
    
    # Generate audio if not already generated
    if not reel_job.audio_file:
        try:
            generate_tts_audio(reel_job.final_script, reel_job)
            reel_job.refresh_from_db()  # Refresh to get updated audio_file
        except OpenAITTSError as e:
            raise OpenAITTSError(f"Failed to generate audio: {str(e)}")
    
    return reel_job

