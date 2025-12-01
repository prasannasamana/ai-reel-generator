# Human-in-the-Loop Workflow Guide

## 🎯 New Architecture

**Script Rewriting:** Django (with user approval)  
**TTS + Video Generation:** Runpod Serverless (GPU processing)

---

## 📋 Complete Workflow

### Step 1: Create Reel
**POST** `/api/reels/`

**Request:**
```json
{
  "image": "<file>",
  "script": "Hello, this is my original script",
  "tone": "friendly",
  "use_rewrite": true,
  "max_seconds": 30
}
```

**Response:**
```json
{
  "id": "uuid",
  "status": "script_pending_approval",
  "original_script": "Hello, this is my original script",
  "final_script": "Hey there! Welcome to this amazing reel...",
  "script_approved": false,
  ...
}
```

**What happens:**
- Django saves image and script
- If `use_rewrite=true`, Django rewrites script using OpenAI
- Status set to `script_pending_approval`
- User can review the rewritten script

---

### Step 2: Review & Regenerate (Optional)

**If user wants to regenerate:**

**POST** `/api/reels/<id>/regenerate-script/`

**Request (optional):**
```json
{
  "tone": "energetic",  // Optional: change tone
  "max_seconds": 45     // Optional: change length
}
```

**Response:**
```json
{
  "id": "uuid",
  "status": "script_pending_approval",
  "final_script": "New rewritten version...",
  "script_approved": false,
  "message": "Script regenerated. Review and approve when ready."
}
```

**User can call this multiple times** until satisfied!

---

### Step 3: Approve Script & Generate Video

**POST** `/api/reels/<id>/approve-script/`

**Request (optional):**
```json
{
  "async": true  // Optional: process in background
}
```

**Response:**
```json
{
  "id": "uuid",
  "status": "processing",
  "script_approved": true,
  "message": "Script approved. Video generation started..."
}
```

**What happens:**
- Django marks script as approved
- Django calls Runpod Serverless
- Runpod generates TTS audio + video (GPU)
- Runpod returns video to Django
- Django saves video file
- Status changes to `done`

---

### Step 4: Check Status

**GET** `/api/reels/<id>/`

**Response (when done):**
```json
{
  "id": "uuid",
  "status": "done",
  "final_script": "Approved script...",
  "script_approved": true,
  "video_url": "http://.../video.mp4",
  "audio_url": "http://.../audio.mp3",
  ...
}
```

---

## 🔄 Complete Flow Diagram

```
User → POST /api/reels/
  ↓
Django → Saves image + script
  ↓
Django → Rewrites script (OpenAI) [if use_rewrite=true]
  ↓
Django → Returns rewritten script
  ↓
User → Reviews script
  ↓
[Optional] User → POST /regenerate-script/ (can repeat)
  ↓
User → POST /approve-script/
  ↓
Django → Calls Runpod Serverless
  ↓
Runpod → Generates TTS (OpenAI)
  ↓
Runpod → Generates Video (SadTalker + GPU)
  ↓
Runpod → Returns audio + video (base64)
  ↓
Django → Saves files, updates status
  ↓
User → GET /api/reels/<id>/ → Gets video URL
```

---

## 📝 API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/reels/` | POST | Create reel, rewrite script |
| `/api/reels/<id>/` | GET | Get reel details |
| `/api/reels/<id>/rewrite-script/` | POST | Rewrite script manually |
| `/api/reels/<id>/regenerate-script/` | POST | Regenerate script (user not satisfied) |
| `/api/reels/<id>/approve-script/` | POST | Approve script & generate video |
| `/api/reels/<id>/generate-video/` | POST | Generate video (if script already approved) |
| `/api/reels/<id>/` | DELETE | Delete reel |

---

## 💡 Example Usage

### Python Example:

```python
import requests

# Step 1: Create reel
files = {'image': open('face.jpg', 'rb')}
data = {
    'script': 'Hello world',
    'tone': 'friendly',
    'use_rewrite': 'true'
}
response = requests.post('http://localhost:8000/api/reels/', files=files, data=data)
reel = response.json()
reel_id = reel['id']

print(f"Rewritten script: {reel['final_script']}")

# Step 2: User reviews, decides to regenerate
response = requests.post(
    f'http://localhost:8000/api/reels/{reel_id}/regenerate-script/',
    json={'tone': 'energetic'}
)
reel = response.json()
print(f"New script: {reel['final_script']}")

# Step 3: User approves and generates video
response = requests.post(f'http://localhost:8000/api/reels/{reel_id}/approve-script/')
reel = response.json()
print(f"Status: {reel['status']}")

# Step 4: Poll for completion
import time
while True:
    response = requests.get(f'http://localhost:8000/api/reels/{reel_id}/')
    reel = response.json()
    if reel['status'] == 'done':
        print(f"Video ready: {reel['video_url']}")
        break
    elif reel['status'] == 'error':
        print(f"Error: {reel['error_message']}")
        break
    time.sleep(5)  # Poll every 5 seconds
```

---

## ✅ Benefits

1. **User Control:** User approves script before expensive video generation
2. **Cost Effective:** Only generate video after approval (saves Runpod costs)
3. **Flexible:** User can regenerate script multiple times
4. **Separation:** Script rewriting in Django, GPU work on Runpod

---

## 🔧 Configuration

**Django Settings:**
```env
OPENAI_API_KEY=sk-...  # For script rewriting
USE_RUNPOD=true
RUNPOD_ENDPOINT_URL=https://api.runpod.ai/v2/xxxxx/run
ASYNC_PROCESSING=true  # Optional: process video in background
```

**Runpod Handler:** Only needs TTS + Video generation (no script rewrite)

---

## 📊 Status Flow

```
pending → script_pending_approval → script_approved → processing → done
                                    ↓
                              (user regenerates)
                                    ↓
                            script_pending_approval
```

---

This workflow gives users full control over script approval before expensive video generation!

