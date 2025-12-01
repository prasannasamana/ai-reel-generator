"""
Async processor for handling concurrent requests.
Uses threading to process video generation without blocking Django.
"""
import threading
from ..models import ReelJob
from .video_generation_runpod import generate_video_with_runpod_service
from django.conf import settings


def process_video_async(reel_job: ReelJob):
    """
    Process video generation in background thread.
    Assumes script is already approved.
    This allows Django to return immediately while video generation happens in background.
    """
    def _process():
        try:
            generate_video_with_runpod_service(reel_job)
        except Exception as e:
            # Error already saved in reel_job by service
            pass
    
    # Start processing in background thread
    thread = threading.Thread(target=_process, daemon=True)
    thread.start()

