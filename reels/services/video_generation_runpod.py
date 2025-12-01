"""
Video generation service using Runpod Serverless.
TTS audio is generated in Django, Runpod only handles video generation (SadTalker).
"""
from ..models import ReelJob
from .runpod_client import generate_video_with_runpod, save_base64_to_file, RunpodClientError
from .openai_tts import generate_tts_audio, OpenAITTSError
from django.conf import settings
from pathlib import Path


def generate_video_with_runpod_service(
    reel_job: ReelJob
) -> ReelJob:
    """
    Generate video using Runpod Serverless.
    Flow:
    1. Generate TTS audio in Django (using OpenAI TTS API)
    2. Send image + audio to Runpod
    3. Runpod runs SadTalker to generate video
    4. Save video file
    
    Args:
        reel_job: The ReelJob instance with approved final_script
    
    Returns:
        The updated ReelJob instance
    """
    try:
        # Set status to processing
        reel_job.status = 'processing'
        reel_job.save()
        
        # Check script is approved
        if not reel_job.script_approved or not reel_job.final_script:
            raise Exception("Script must be approved before generating video")
        
        # Get image path
        if not reel_job.image:
            raise Exception("ReelJob must have an image")
        
        image_path = Path(reel_job.image.path)
        if not image_path.exists():
            raise Exception(f"Image file not found: {image_path}")
        
        # Step 1: Generate TTS audio in Django (no GPU needed!)
        if not reel_job.audio_file:
            try:
                audio_path = generate_tts_audio(reel_job.final_script, reel_job)
                reel_job.refresh_from_db()  # Refresh to get updated audio_file
            except OpenAITTSError as e:
                raise Exception(f"TTS generation failed: {str(e)}")
        
        # Get audio file path
        if not reel_job.audio_file:
            raise Exception("Audio file not generated")
        
        audio_path = Path(reel_job.audio_file.path)
        if not audio_path.exists():
            raise Exception(f"Audio file not found: {audio_path}")
        
        # Step 2: Call Runpod Serverless for video generation only
        # SadTalker needs: image + audio file
        result = generate_video_with_runpod(
            image_path=str(image_path),
            audio_path=str(audio_path)
        )
        
        # Check for errors
        if result.get('error'):
            raise RunpodClientError(result['error'])
        
        # Step 3: Save video file
        if result.get('video_base64'):
            job_dir = settings.MEDIA_ROOT / 'reels' / str(reel_job.id)
            job_dir.mkdir(parents=True, exist_ok=True)
            
            video_path = job_dir / 'video.mp4'
            save_base64_to_file(result['video_base64'], str(video_path))
            reel_job.video_file.name = f'reels/{reel_job.id}/video.mp4'
        
        # Mark as done
        reel_job.status = 'done'
        reel_job.save()
        
        return reel_job
    
    except Exception as e:
        # Set error status
        reel_job.status = 'error'
        reel_job.error_message = str(e)
        reel_job.save()
        raise

