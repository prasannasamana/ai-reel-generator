"""
Orchestration service for the full reel generation pipeline.
"""
from typing import Literal
from ..models import ReelJob
from .openai_rewrite import rewrite_script, Tone
from .openai_tts import generate_tts_audio
from .sadtalker_runner import run_sadtalker_for_reel


def process_reel_job(
    reel_job: ReelJob,
    use_rewrite: bool,
    tone: str = "neutral",
    max_seconds: int | None = None
) -> ReelJob:
    """
    Orchestrate the full reel generation pipeline: optional rewrite -> TTS -> SadTalker.
    Update reel_job fields (final_script, status, audio_file, video_file).
    
    Args:
        reel_job: The ReelJob instance to process
        use_rewrite: Whether to rewrite the script using OpenAI
        tone: The tone to use for rewriting (if use_rewrite is True)
        max_seconds: Optional target length in seconds for rewriting
    
    Returns:
        The updated ReelJob instance
    
    Raises:
        Various exceptions from the service layers
    """
    try:
        # Set status to processing
        reel_job.status = 'processing'
        reel_job.save()
        
        # Step 1: Optional script rewriting
        if use_rewrite:
            final_script = rewrite_script(
                reel_job.original_script,
                tone=tone,  # type: ignore
                max_seconds=max_seconds
            )
            reel_job.final_script = final_script
        else:
            reel_job.final_script = reel_job.original_script
        
        reel_job.tone = tone
        reel_job.save()
        
        # Step 2: Generate TTS audio
        audio_path = generate_tts_audio(reel_job.final_script, reel_job)
        
        # Step 3: Generate video using SadTalker
        video_path = run_sadtalker_for_reel(reel_job)
        
        # Step 4: Mark as done
        reel_job.status = 'done'
        reel_job.save()
        
        return reel_job
    
    except Exception as e:
        # Set error status
        reel_job.status = 'error'
        reel_job.error_message = str(e)
        reel_job.save()
        raise

