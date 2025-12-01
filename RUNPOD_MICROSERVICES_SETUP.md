# Runpod Microservices Architecture Setup

## 🎯 Architecture Overview

**Django (Lightweight)** → Runs separately (local/server)
- Handles API requests
- Stores data in database
- Manages file uploads/downloads

**Runpod Serverless (GPU Processing)** → Runs on Runpod
- Script rewriting (OpenAI)
- TTS generation (OpenAI)
- Video generation (SadTalker + GPU)
- Returns processed files to Django

---

## 📋 Setup Steps

### Part 1: Deploy Runpod Serverless Handler

#### Step 1.1: Create Standalone Runpod Handler

**File: `runpod_handler.py`** ✅ Already created!

This handler:
- Receives image + script from Django
- Does script rewrite (OpenAI)
- Generates TTS audio (OpenAI)
- Generates video (SadTalker + GPU)
- Returns base64 encoded audio + video

#### Step 1.2: Build Docker Image for Runpod

**Use: `runpod_Dockerfile`** (simpler, no Django)

**On Runpod pod:**
```bash
cd /workspace
git clone https://github.com/prasannasamana/ai-reel-generator.git
cd ai-reel-generator

# Build image
docker build -f runpod_Dockerfile -t runpod-reel-processor .
```

#### Step 1.3: Push to Docker Hub

```bash
docker tag runpod-reel-processor YOUR_DOCKERHUB_USERNAME/runpod-reel-processor:latest
docker push YOUR_DOCKERHUB_USERNAME/runpod-reel-processor:latest
```

#### Step 1.4: Create Runpod Serverless Endpoint

1. **Go to Runpod** → **Serverless** → **New Endpoint**
2. **Container Image:** `YOUR_DOCKERHUB_USERNAME/runpod-reel-processor:latest`
3. **Handler:** `handler.handler` (points to `runpod_handler.py`)
4. **GPU:** RTX 3090 or better
5. **Container Disk:** 50GB
6. **Environment Variables:**
   ```
   OPENAI_API_KEY=sk-your-openai-key
   SADTALKER_ROOT=/workspace/SadTalker
   ```
7. **Timeout:** 600 seconds (10 minutes)
8. **Create Endpoint**

#### Step 1.5: Get Endpoint URL

After creation, copy the endpoint URL:
```
https://api.runpod.ai/v2/xxxxx-xxxxx-xxxxx/run
```

---

### Part 2: Configure Django to Use Runpod

#### Step 2.1: Update Django Settings

**Add to your `.env` file (on Django server):**

```env
# Runpod Configuration
USE_RUNPOD=true
RUNPOD_ENDPOINT_URL=https://api.runpod.ai/v2/xxxxx-xxxxx-xxxxx/run
RUNPOD_API_KEY=your-runpod-api-key  # Optional, if endpoint requires auth
```

#### Step 2.2: Update Django Settings File

**Add to `reel_platform/settings.py`:**

```python
# Runpod Serverless configuration
USE_RUNPOD = os.getenv('USE_RUNPOD', 'false').lower() == 'true'
RUNPOD_ENDPOINT_URL = os.getenv('RUNPOD_ENDPOINT_URL', '')
RUNPOD_API_KEY = os.getenv('RUNPOD_API_KEY', '')
```

#### Step 2.3: Install Requests (if not already)

**Add to `requirements.txt`:**
```
requests>=2.31.0
```

---

### Part 3: Test the Setup

#### Step 3.1: Test Runpod Handler Directly

**Create test script:**

```python
import requests
import base64

# Read image
with open('face.jpg', 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

# Call Runpod
payload = {
    "input": {
        "image": image_base64,
        "script": "Hello, this is a test!",
        "tone": "friendly",
        "use_rewrite": True
    }
}

response = requests.post(
    "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run",
    json=payload
)

result = response.json()
print(result)
```

#### Step 3.2: Test Django API

**Django will automatically use Runpod if `USE_RUNPOD=true`:**

```bash
curl -X POST http://localhost:8000/api/reels/ \
  -F "image=@face.jpg" \
  -F "script=Hello world" \
  -F "tone=friendly"
```

---

## 🔄 How It Works

### Flow:

1. **Client** → POST to Django `/api/reels/`
2. **Django** → Saves image, creates ReelJob
3. **Django** → Calls Runpod Serverless API
   - Sends: image (base64), script, tone, etc.
4. **Runpod** → Processes:
   - Script rewrite (OpenAI)
   - TTS generation (OpenAI)
   - Video generation (SadTalker + GPU)
5. **Runpod** → Returns: final_script, audio_base64, video_base64
6. **Django** → Saves audio/video files
7. **Django** → Returns response to client

---

## 💰 Cost Benefits

**Django Server:**
- Can run on cheap VPS ($5-10/month)
- No GPU needed
- Handles API, database, file storage

**Runpod Serverless:**
- Pay only when processing (~$0.50/day for occasional use)
- GPU only when needed
- Auto-scales

**Total:** Much cheaper than running GPU 24/7!

---

## 📝 Environment Variables

### Django Server (.env):
```env
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=your-domain.com
OPENAI_API_KEY=sk-...  # Not needed if Runpod handles it
USE_RUNPOD=true
RUNPOD_ENDPOINT_URL=https://api.runpod.ai/v2/xxxxx/run
RUNPOD_API_KEY=optional-runpod-api-key
```

### Runpod Serverless (in Runpod dashboard):
```env
OPENAI_API_KEY=sk-...
SADTALKER_ROOT=/workspace/SadTalker
```

---

## ✅ Advantages

1. **Cost Effective:** Django on cheap server, GPU only when needed
2. **Scalable:** Runpod auto-scales
3. **Separation:** API logic separate from GPU processing
4. **Flexible:** Can switch between local/runpod easily

---

## 🔧 Switching Between Local and Runpod

**Use Runpod (recommended):**
```env
USE_RUNPOD=true
RUNPOD_ENDPOINT_URL=https://...
```

**Use Local Processing (requires GPU):**
```env
USE_RUNPOD=false
```

Django automatically chooses the right pipeline!

---

## 🚀 Next Steps

1. Deploy Runpod handler (Part 1)
2. Configure Django (Part 2)
3. Test end-to-end (Part 3)
4. Deploy Django to production server

Your Django app can run anywhere - local, VPS, Heroku, etc.!

