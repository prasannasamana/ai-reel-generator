"""
Standalone Runpod Serverless Handler
This runs on Runpod and handles ONLY video generation (SadTalker).
TTS audio is generated in Django, script rewriting is done in Django.
NO Django - just pure GPU processing
"""
import os
import base64
import tempfile
import subprocess
from pathlib import Path

# SadTalker path
SADTALKER_ROOT = os.getenv('SADTALKER_ROOT', '/workspace/SadTalker')


def generate_video(image_path: str, audio_path: str, output_dir: str) -> str:
    """Generate video using SadTalker."""
    sadtalker_root = Path(SADTALKER_ROOT)
    if not sadtalker_root.exists():
        raise Exception(f"SadTalker not found at {SADTALKER_ROOT}")
    
    inference_script = sadtalker_root / 'inference.py'
    if not inference_script.exists():
        raise Exception(f"SadTalker inference.py not found")
    
    cmd = [
        'python',
        str(inference_script),
        '--driven_audio', str(audio_path),
        '--source_image', str(image_path),
        '--result_dir', str(output_dir),
        '--enhancer', 'gfpgan',
        '--preprocess', 'full',
    ]
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(sadtalker_root),
            capture_output=True,
            text=True,
            check=True,
            timeout=600
        )
        
        # Find generated video
        video_files = list(Path(output_dir).rglob('*.mp4'))
        if not video_files:
            raise Exception("No video file generated")
        
        video_file = max(video_files, key=lambda p: p.stat().st_mtime)
        return str(video_file)
    except subprocess.TimeoutExpired:
        raise Exception("Video generation timed out")
    except subprocess.CalledProcessError as e:
        raise Exception(f"SadTalker failed: {e.stderr or e.stdout}")


def handler(event):
    """
    Runpod Serverless handler - Video Generation Only (SadTalker).
    TTS audio is generated in Django, this only handles video generation.
    
    SadTalker inputs:
    - image: Face image (base64)
    - audio: Audio file (base64) - already generated in Django
    
    Expected input:
    {
        "image": "base64_encoded_image",
        "audio": "base64_encoded_audio"  # Already generated in Django
    }
    
    Returns:
    {
        "video_base64": "base64_encoded_video",
        "error": null
    }
    """
    try:
        input_data = event.get('input', {})
        
        # Parse inputs
        image_base64 = input_data.get('image', '')
        audio_base64 = input_data.get('audio', '')
        
        if not image_base64 or not audio_base64:
            return {
                "error": "Missing required fields: image and audio"
            }
        
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Decode image
            image_data = base64.b64decode(image_base64)
            image_path = temp_path / 'input_image.jpg'
            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            # Decode audio (already generated in Django)
            audio_data = base64.b64decode(audio_base64)
            audio_path = temp_path / 'audio.mp3'
            with open(audio_path, 'wb') as f:
                f.write(audio_data)
            
            # Generate video using SadTalker (only GPU-intensive task)
            video_path = generate_video(
                str(image_path),
                str(audio_path),
                str(temp_path / 'output')
            )
            
            # Read and encode video
            with open(video_path, 'rb') as f:
                video_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            return {
                "video_base64": video_base64,
                "error": None
            }
    
    except Exception as e:
        import traceback
        return {
            "video_base64": "",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

