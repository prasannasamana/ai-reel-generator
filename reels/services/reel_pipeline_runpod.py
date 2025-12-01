"""
Orchestration service using Runpod Serverless for video generation.
Django handles API and database, Runpod handles GPU processing.
"""
from ..models import ReelJob
from .runpod_client import process_reel_with_runpod, save_base64_to_file, RunpodClientError
from django.conf import settings
from pathlib import Path


def process_reel_job_with_runpod(
    reel_job: ReelJob,
    use_rewrite: bool,
    tone: str = "neutral",
    max_seconds: int = None
) -> ReelJob:
    """
    Process reel using Runpod Serverless.
    Django sends request to Runpod, Runpod does all processing, returns video.
    
    Args:
        reel_job: The ReelJob instance to process
        use_rewrite: Whether to rewrite the script using OpenAI
        tone: The tone to use for rewriting (if use_rewrite is True)
        max_seconds: Optional target length in seconds for rewriting
    
    Returns:
        The updated ReelJob instance
    """
    try:
        # Set status to processing
        reel_job.status = 'processing'
        reel_job.save()
        
        # Get image path
        if not reel_job.image:
            raise Exception("ReelJob must have an image")
        
        image_path = Path(reel_job.image.path)
        if not image_path.exists():
            raise Exception(f"Image file not found: {image_path}")
        
        # Call Runpod Serverless
        result = process_reel_with_runpod(
            image_path=str(image_path),
            script=reel_job.original_script,
            tone=tone,
            use_rewrite=use_rewrite,
            max_seconds=max_seconds
        )
        
        # Check for errors
        if result.get('error'):
            raise RunpodClientError(result['error'])
        
        # Update final script
        reel_job.final_script = result.get('final_script', reel_job.original_script)
        reel_job.tone = tone
        reel_job.save()
        
        # Create job-specific directory
        job_dir = settings.MEDIA_ROOT / 'reels' / str(reel_job.id)
        job_dir.mkdir(parents=True, exist_ok=True)
        
        # Save audio file
        if result.get('audio_base64'):
            audio_path = job_dir / 'audio.mp3'
            save_base64_to_file(result['audio_base64'], str(audio_path))
            reel_job.audio_file.name = f'reels/{reel_job.id}/audio.mp3'
        
        # Save video file
        if result.get('video_base64'):
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

