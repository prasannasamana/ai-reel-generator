"""
Service to call Runpod Serverless API for video generation.
"""
import requests
import base64
import os
from django.conf import settings
from pathlib import Path
import tempfile


class RunpodClientError(Exception):
    """Exception for Runpod client errors."""
    pass


def process_reel_with_runpod(
    image_path: str,
    script: str,
    tone: str = "neutral",
    use_rewrite: bool = True,
    max_seconds: int = None
) -> dict:
    """
    Call Runpod Serverless to process a reel.
    
    Args:
        image_path: Path to the image file
        script: Script text
        tone: Tone for rewriting
        use_rewrite: Whether to rewrite script
        max_seconds: Optional max seconds
    
    Returns:
        Dictionary with:
        - final_script: Rewritten script
        - audio_base64: Base64 encoded audio
        - video_base64: Base64 encoded video
        - error: Error message if any
    """
    runpod_endpoint = settings.RUNPOD_ENDPOINT_URL
    runpod_api_key = settings.RUNPOD_API_KEY
    
    if not runpod_endpoint:
        raise RunpodClientError("RUNPOD_ENDPOINT_URL not configured in settings")
    
    # Read and encode image
    with open(image_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    # Prepare payload
    payload = {
        "input": {
            "image": image_base64,
            "script": script,
            "tone": tone,
            "use_rewrite": use_rewrite,
            "max_seconds": max_seconds
        }
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    if runpod_api_key:
        headers["Authorization"] = f"Bearer {runpod_api_key}"
    
    try:
        # Call Runpod Serverless
        response = requests.post(
            runpod_endpoint,
            json=payload,
            headers=headers,
            timeout=600  # 10 minutes timeout
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Check for errors in response
        if result.get('error'):
            raise RunpodClientError(result['error'])
        
        return result.get('output', {})
    
    except requests.exceptions.RequestException as e:
        raise RunpodClientError(f"Runpod API call failed: {str(e)}")
    except Exception as e:
        raise RunpodClientError(f"Unexpected error: {str(e)}")


def generate_video_with_runpod(
    image_path: str,
    audio_path: str
) -> dict:
    """
    Call Runpod Serverless to generate video ONLY.
    TTS audio is generated in Django, Runpod only does video generation (SadTalker).
    
    SadTalker inputs:
    - image: Face image
    - audio: Audio file (already generated in Django)
    
    Args:
        image_path: Path to the image file
        audio_path: Path to the audio file (already generated in Django)
    
    Returns:
        Dictionary with:
        - video_base64: Base64 encoded video
        - error: Error message if any
    """
    runpod_endpoint = settings.RUNPOD_ENDPOINT_URL
    runpod_api_key = settings.RUNPOD_API_KEY
    
    if not runpod_endpoint:
        raise RunpodClientError("RUNPOD_ENDPOINT_URL not configured in settings")
    
    # Read and encode image
    with open(image_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    # Read and encode audio
    with open(audio_path, 'rb') as f:
        audio_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    # Prepare payload (only video generation - SadTalker needs image + audio)
    payload = {
        "input": {
            "image": image_base64,
            "audio": audio_base64  # Audio already generated in Django
        }
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    if runpod_api_key:
        headers["Authorization"] = f"Bearer {runpod_api_key}"
    
    try:
        # Call Runpod Serverless
        response = requests.post(
            runpod_endpoint,
            json=payload,
            headers=headers,
            timeout=600  # 10 minutes timeout
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Check for errors in response
        if result.get('error'):
            raise RunpodClientError(result['error'])
        
        return result.get('output', {})
    
    except requests.exceptions.RequestException as e:
        raise RunpodClientError(f"Runpod API call failed: {str(e)}")
    except Exception as e:
        raise RunpodClientError(f"Unexpected error: {str(e)}")


def save_base64_to_file(base64_data: str, output_path: str) -> str:
    """Save base64 encoded data to file."""
    file_data = base64.b64decode(base64_data)
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path_obj, 'wb') as f:
        f.write(file_data)
    
    return str(output_path_obj.absolute())

