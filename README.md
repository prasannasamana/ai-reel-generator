# AI Reel Generator

A Django-based web application for generating AI-powered talking-head video reels using SadTalker and OpenAI.

## Features

- **REST API Only**: Clean RESTful API for programmatic access (no frontend UI)
- **Script Rewriting**: Optionally rewrite scripts using OpenAI GPT to match different tones (neutral, friendly, formal, energetic, dramatic)
- **Text-to-Speech**: Convert scripts to natural-sounding speech using OpenAI's TTS API
- **Talking Head Video**: Generate realistic talking-head videos using SadTalker
- **Full CRUD Operations**: Create, read, list, and delete reels via API

## Tech Stack

- Django 5.0+
- Django REST Framework 3.14+ (for API endpoints)
- Python 3.10+
- OpenAI API (for script rewriting and TTS)
- SadTalker (for video generation)
- PostgreSQL/SQLite (SQLite by default)
- Docker (for deployment)

## Project Structure

```
AI_ReelMaker/
├── reel_platform/          # Django project
│   ├── settings.py         # Configuration
│   ├── urls.py            # URL routing
│   └── ...
├── reels/                  # Django app
│   ├── models.py          # ReelJob model
│   ├── views.py           # Web views and API
│   ├── forms.py           # Forms
│   ├── services/          # Business logic
│   │   ├── openai_rewrite.py
│   │   ├── openai_tts.py
│   │   ├── sadtalker_runner.py
│   │   └── reel_pipeline.py
│   └── templates/         # HTML templates
├── manage.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## Quick Start (Windows)

**Fastest way to get started:**

```powershell
# 1. Navigate to project
cd AI_ReelMaker

# 2. Run automated setup
.\setup_windows.bat

# 3. Edit .env file (add your OPENAI_API_KEY)
# (The script will open it automatically)

# 4. Start the server
.\start_server.bat
```

Then open http://localhost:8000 in your browser!

## Setup

### Local Development (Windows Command Line)

Open **PowerShell** or **Command Prompt** and run these commands:

#### Step 1: Navigate to Project Directory
```powershell
cd "C:\Users\prasa\Desktop\Yellas Tech Work\Madhu_sir_works\AI_ReelMaker"
```

#### Step 2: Create Virtual Environment
```powershell
python -m venv venv
```

#### Step 3: Activate Virtual Environment
```powershell
# PowerShell:
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# OR use Command Prompt (CMD):
venv\Scripts\activate.bat
```

#### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

#### Step 5: Set Up Environment Variables
```powershell
# Copy example env file
copy env.example .env

# Edit .env file (use notepad or your editor)
notepad .env
```

**In the `.env` file, add your OpenAI API key:**
```
OPENAI_API_KEY=sk-your-actual-api-key-here
BACKEND_BASE_URL=http://localhost:8000
```

**Note about SadTalker:**
- **For Runpod deployment**: You DON'T need to clone SadTalker locally. The Dockerfile automatically clones it during the Docker build process.
- **For local testing**: You can skip SadTalker setup if you only want to test the API endpoints (script rewriting and TTS will work, but video generation will fail). If you want to test full video generation locally, then clone SadTalker and set `SADTALKER_ROOT` in `.env`.

#### Step 6: Run Database Migrations
```powershell
python manage.py migrate
```

#### Step 7: (Optional) Create Admin User
```powershell
python manage.py createsuperuser
```

#### Step 8: Start the Development Server
```powershell
python manage.py runserver
```

#### Step 9: Access the API
- API Info: http://localhost:8000/api/
- Create Reel: POST http://localhost:8000/api/reels/
- List Reels: GET http://localhost:8000/api/reels/
- Admin panel: http://localhost:8000/admin (for database management)

#### Quick Setup (Using Batch Script)

For faster setup on Windows, use the provided batch script:

```powershell
# Run setup script (does everything automatically)
.\setup_windows.bat

# Then start the server
.\start_server.bat
```

**Note**: The setup script will:
- Create virtual environment
- Install all dependencies
- Create `.env` file from `env.example`
- Run database migrations
- Open `.env` file for you to add your API key

---

### Local Development (Linux/Mac)

1. **Navigate to project directory**:
   ```bash
   cd AI_ReelMaker
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env and add your OPENAI_API_KEY
   nano .env  # or use your preferred editor
   ```

5. **SadTalker Setup** (OPTIONAL - only for local video generation testing):
   
   **⚠️ IMPORTANT**: You DON'T need to clone SadTalker locally if you're deploying to Runpod!
   - The Dockerfile automatically clones SadTalker during the Docker build process
   - For Runpod deployment, SadTalker will be set up automatically
   
   **Only clone SadTalker locally if** you want to test video generation on your local machine:
   ```bash
   # Clone SadTalker to a local directory
   git clone https://github.com/OpenTalker/SadTalker.git
   cd SadTalker
   pip install -r requirements.txt
   # Download models (requires ~10GB+ disk space and GPU)
   bash scripts/download_models.sh  # On Windows, use Git Bash or WSL
   ```
   
   Then set `SADTALKER_ROOT` in your `.env` file:
   ```
   SADTALKER_ROOT=C:\path\to\SadTalker
   ```
   
   **For local API testing without video generation**: You can skip SadTalker setup entirely. The API will work for script rewriting and TTS, but video generation will fail (which is fine for testing the API endpoints).

6. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

9. **Access the API**:
   - API Info: http://localhost:8000/api/
   - Create Reel: POST http://localhost:8000/api/reels/
   - Admin: http://localhost:8000/admin (for database management)

### Docker Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t ai-reel-generator .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     -p 8000:8000 \
     -e OPENAI_API_KEY=your-api-key \
     -e SADTALKER_ROOT=/workspace/SadTalker \
     -e BACKEND_BASE_URL=http://localhost:8000 \
     -v $(pwd)/media:/app/media \
     ai-reel-generator
   ```

### Runpod GPU Deployment

Follow these step-by-step instructions to deploy on Runpod:

#### Step 1: Create a Runpod Account and Pod

1. **Sign up/Login** at [runpod.io](https://www.runpod.io)
2. **Navigate to Pods** → **Create New Pod**
3. **Select GPU Template**:
   - Choose a GPU template (e.g., "PyTorch 2.0.1" or "CUDA 11.8.0")
   - Recommended GPUs: RTX 3090, RTX 4090, or A100 (for faster processing)
4. **Configure Pod**:
   - Select your preferred GPU
   - Set container disk to at least **50GB** (SadTalker models are large)
   - Choose your region
5. **Create the Pod** and wait for it to initialize

#### Step 2: Connect to Your Runpod Instance

1. **Open the Pod** from your Runpod dashboard
2. **Click "Connect"** → Choose "HTTP Service" or "SSH"
3. **For HTTP Service** (recommended):
   - This opens a Jupyter-like interface in your browser
   - You can use the terminal from there
4. **For SSH** (alternative):
   - Copy the SSH command shown
   - Connect from your local terminal: `ssh root@<runpod-ip> -p <port>`

#### Step 3: Upload Your Project to Runpod

**Option A: Using Git (Recommended)**
```bash
# In Runpod terminal
cd /workspace
git clone <your-repository-url>
cd AI_ReelMaker
```

**Option B: Using Runpod's File Upload**
1. In Runpod's web interface, use the file browser
2. Navigate to `/workspace`
3. Upload your project files (or zip and extract)

**Option C: Using SCP from Local Machine**
```bash
# From your local machine
scp -P <port> -r AI_ReelMaker root@<runpod-ip>:/workspace/
```

#### Step 4: Set Up Environment Variables

1. **Create `.env` file** in the project directory:
   ```bash
   cd /workspace/AI_ReelMaker
   nano .env
   ```

2. **Add your configuration**:
   ```env
   SECRET_KEY=your-secret-key-change-this
   DEBUG=False
   ALLOWED_HOSTS=*
   OPENAI_API_KEY=sk-your-openai-api-key-here
   SADTALKER_ROOT=/workspace/SadTalker
   BACKEND_BASE_URL=http://localhost:8000
   ```

3. **Save and exit** (Ctrl+X, then Y, then Enter)

#### Step 5: Build the Docker Image

```bash
cd /workspace/AI_ReelMaker

# Build the Docker image (this will take 10-20 minutes)
# It will clone SadTalker and download models automatically
docker build -t ai-reel-generator .
```

**✅ Important**: You DON'T need to clone SadTalker manually! The Dockerfile automatically:
- Clones SadTalker repository from GitHub
- Installs SadTalker dependencies
- Downloads SadTalker models (this is the longest step, ~10-15 minutes)
- Sets up everything needed for video generation

**Note**: The build process will:
- Install all Python dependencies
- Clone SadTalker repository automatically
- Install SadTalker dependencies
- Download SadTalker models (this is the longest step)

#### Step 6: Run the Docker Container

```bash
# Run the container with GPU support
docker run -d \
  --name ai-reel-app \
  --gpus all \
  -p 8000:8000 \
  --env-file .env \
  -v /workspace/AI_ReelMaker/media:/app/media \
  -v /workspace/SadTalker:/workspace/SadTalker \
  ai-reel-generator
```

**Explanation of flags**:
- `-d`: Run in detached mode (background)
- `--name`: Give container a name for easy management
- `--gpus all`: Enable GPU access
- `-p 8000:8000`: Map port 8000
- `--env-file .env`: Load environment variables from `.env` file
- `-v`: Mount volumes for persistent storage

#### Step 7: Configure Port Forwarding

1. **In Runpod Dashboard**:
   - Go to your Pod details
   - Find "Ports" or "Network" section
   - Add port mapping: **8000** → **8000**
   - Set visibility to **Public** (or Private if you prefer)

2. **Get your public URL**:
   - Runpod will provide a URL like: `https://<random-id>.runpod.net`
   - Or use: `http://<your-pod-ip>:8000`

#### Step 8: Verify the Application is Running

```bash
# Check if container is running
docker ps

# View logs
docker logs ai-reel-app

# If you see "Starting development server at http://0.0.0.0:8000/", it's working!
```

#### Step 9: Access Your API

1. **API Info**: `http://<your-runpod-url>:8000/api/` - Get API documentation
2. **Create Reel**: `POST http://<your-runpod-url>:8000/api/reels/`
3. **List Reels**: `GET http://<your-runpod-url>:8000/api/reels/`
4. **Admin Panel**: `http://<your-runpod-url>:8000/admin` (create superuser first, for database management only)

**Test the API**:
```bash
# Get API info
curl http://<your-runpod-url>:8000/api/

# Create a reel
curl -X POST http://<your-runpod-url>:8000/api/reels/ \
  -F "image=@face.jpg" \
  -F "script=Hello world" \
  -F "tone=friendly"
```

#### Step 10: Create Admin User (Optional)

```bash
# Enter the running container
docker exec -it ai-reel-app bash

# Create superuser
python manage.py createsuperuser

# Exit container
exit
```

#### Troubleshooting

**Container won't start:**
```bash
# Check logs
docker logs ai-reel-app

# Check if port is already in use
docker ps -a
```

**GPU not detected:**
```bash
# Verify GPU is available
nvidia-smi

# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

**Models not downloading:**
```bash
# Enter container and manually download
docker exec -it ai-reel-app bash
cd /workspace/SadTalker
bash scripts/download_models.sh
```

**Update your application:**
```bash
# Stop and remove old container
docker stop ai-reel-app
docker rm ai-reel-app

# Rebuild (if code changed)
docker build -t ai-reel-generator .

# Run again with same command as Step 6
```

#### Important Notes

- **Disk Space**: Ensure you have at least 50GB free for models
- **GPU Memory**: Video generation requires significant VRAM (8GB+ recommended)
- **Processing Time**: First video generation may take 5-10 minutes
- **Cost**: Runpod charges per hour - stop your pod when not in use!
- **Data Persistence**: Files in `/workspace` persist, but `/app/media` should be mounted as volume

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `SADTALKER_ROOT`: Path to SadTalker installation (default: `/workspace/SadTalker`)
- `BACKEND_BASE_URL`: Base URL for constructing video URLs (default: `http://localhost:8000`)
- `SECRET_KEY`: Django secret key (change in production)
- `DEBUG`: Debug mode (set to `False` in production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## API Usage

This is a **REST API only** application. All endpoints return JSON responses.

### Base URL
- Local: `http://localhost:8000`
- Production: `http://your-domain.com`

### API Information

**GET** `/api/` - Get API information and documentation
```bash
curl http://localhost:8000/api/
```

### Create a Reel

**POST** `/api/reels/` - Create a new reel

**Request** (multipart/form-data):
```bash
curl -X POST http://localhost:8000/api/reels/ \
  -F "image=@/path/to/face_image.jpg" \
  -F "script=Hello, this is my script for the reel" \
  -F "tone=friendly" \
  -F "use_rewrite=true" \
  -F "max_seconds=30"
```

**Parameters**:
- `image` (required): Face image file (JPEG, PNG)
- `script` (required): Script text
- `tone` (optional): `neutral`, `friendly`, `formal`, `energetic`, `dramatic` (default: `neutral`)
- `use_rewrite` (optional): `true` or `false` (default: `true`)
- `max_seconds` (optional): Target length in seconds (integer)

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "done",
  "tone": "friendly",
  "original_script": "Hello, this is my script",
  "final_script": "Hey there! Welcome to this amazing reel...",
  "video_url": "http://localhost:8000/media/reels/550e8400.../video.mp4",
  "audio_url": "http://localhost:8000/media/reels/550e8400.../audio.mp3",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z",
  "error_message": null
}
```

**Status Codes**:
- `201`: Reel created successfully
- `400`: Bad request (missing required fields)
- `500`: Processing error (check `error_message`)

### List Reels

**GET** `/api/reels/` - List all reels with pagination

**Query Parameters**:
- `status` (optional): Filter by status (`pending`, `processing`, `done`, `error`)
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20)

**Example**:
```bash
# Get all reels
curl http://localhost:8000/api/reels/

# Get only completed reels
curl http://localhost:8000/api/reels/?status=done

# Get page 2 with 10 items per page
curl http://localhost:8000/api/reels/?page=2&page_size=10
```

**Response** (200 OK):
```json
{
  "count": 50,
  "page": 1,
  "total_pages": 3,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "done",
      "tone": "friendly",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:35:00Z",
      "video_url": "http://localhost:8000/media/reels/550e8400.../video.mp4"
    }
  ]
}
```

### Get Reel Details

**GET** `/api/reels/<id>/` - Get detailed information about a specific reel

**Example**:
```bash
curl http://localhost:8000/api/reels/550e8400-e29b-41d4-a716-446655440000/
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "done",
  "tone": "friendly",
  "original_script": "Hello, this is my script",
  "final_script": "Hey there! Welcome to this amazing reel...",
  "image_url": "http://localhost:8000/media/reels/550e8400.../images/face.jpg",
  "audio_url": "http://localhost:8000/media/reels/550e8400.../audio.mp3",
  "video_url": "http://localhost:8000/media/reels/550e8400.../video.mp4",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z",
  "error_message": null
}
```

**Status Codes**:
- `200`: Success
- `404`: Reel not found

### Delete a Reel

**DELETE** `/api/reels/<id>/` - Delete a reel

**Example**:
```bash
curl -X DELETE http://localhost:8000/api/reels/550e8400-e29b-41d4-a716-446655440000/
```

**Response** (200 OK):
```json
{
  "message": "Reel deleted successfully"
}
```

### Status Values

- `pending`: Reel job created but not started
- `processing`: Currently being processed
- `done`: Successfully completed
- `error`: Processing failed (check `error_message`)

### Python Example

```python
import requests

# Create a reel
url = "http://localhost:8000/api/reels/"
files = {'image': open('face.jpg', 'rb')}
data = {
    'script': 'Hello, welcome to my reel!',
    'tone': 'friendly',
    'use_rewrite': 'true',
    'max_seconds': '30'
}
response = requests.post(url, files=files, data=data)
reel_data = response.json()
print(f"Reel ID: {reel_data['id']}")
print(f"Status: {reel_data['status']}")
print(f"Video URL: {reel_data['video_url']}")
```

### JavaScript/Node.js Example

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('image', fs.createReadStream('face.jpg'));
form.append('script', 'Hello, welcome to my reel!');
form.append('tone', 'friendly');
form.append('use_rewrite', 'true');
form.append('max_seconds', '30');

axios.post('http://localhost:8000/api/reels/', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log('Reel ID:', response.data.id);
  console.log('Status:', response.data.status);
  console.log('Video URL:', response.data.video_url);
})
.catch(error => console.error('Error:', error));
```

### Testing the API

A simple test script is included (`test_api.py`) to verify the API is working:

```bash
# Install requests if not already installed
pip install requests

# Test API endpoints
python test_api.py

# Test with an image file
python test_api.py path/to/face_image.jpg "Your script text here"
```

## Architecture

The application follows a clean architecture with separate layers:

- **Models**: Database models (`reels/models.py`)
- **Services**: Business logic (`reels/services/`)
  - `openai_rewrite.py`: Script rewriting
  - `openai_tts.py`: Text-to-speech
  - `sadtalker_runner.py`: Video generation
  - `reel_pipeline.py`: Orchestration
- **Views**: REST API endpoints (`reels/views.py`)

## Notes

- Video generation can take several minutes depending on GPU and video length
- Ensure sufficient disk space for media files
- For production, consider:
  - Using Celery for async job processing
  - Setting up proper file storage (S3, etc.)
  - Implementing rate limiting
  - Adding authentication/authorization
  - Using a production WSGI server (Gunicorn, uWSGI)

## Troubleshooting

- **SadTalker not found**: Ensure `SADTALKER_ROOT` points to the correct directory
- **OpenAI API errors**: Check your API key and quota
- **Video generation fails**: Check GPU availability and SadTalker model files
- **Media files not accessible**: Ensure `MEDIA_URL` and `MEDIA_ROOT` are configured correctly

## License

[Your License Here]

