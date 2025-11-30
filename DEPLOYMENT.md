# Runpod Deployment Guide

## Quick Deployment Checklist

### Before You Start:
- [ ] Have a Runpod account (sign up at runpod.io)
- [ ] Have your OpenAI API key ready
- [ ] Your project code is ready (all files committed if using Git)

---

## Step-by-Step Deployment

### 1. Create Runpod Pod

1. Go to [runpod.io](https://www.runpod.io) and login
2. Click **"Pods"** → **"Create New Pod"**
3. **Select Template**: Choose "PyTorch 2.0.1" or "CUDA 11.8.0"
4. **Select GPU**: RTX 3090, RTX 4090, or A100 (recommended)
5. **Container Disk**: Set to **at least 50GB** (SadTalker models are large)
6. **Region**: Choose closest to you
7. Click **"Create"** and wait for pod to initialize

### 2. Connect to Runpod

1. Open your pod from dashboard
2. Click **"Connect"** → Choose **"HTTP Service"** (Jupyter interface)
3. This opens a browser-based terminal

### 3. Upload Your Project

**Option A: Using Git (Recommended)**
```bash
cd /workspace
git clone <your-repo-url>
cd AI_ReelMaker
```

**Option B: Upload via Runpod File Browser**
1. In Runpod interface, use file browser
2. Navigate to `/workspace`
3. Upload your `AI_ReelMaker` folder (or zip and extract)

**Option C: Using SCP (from your local machine)**
```bash
# Zip your project first
cd "C:\Users\prasa\Desktop\Yellas Tech Work\Madhu_sir_works"
tar -czf AI_ReelMaker.tar.gz AI_ReelMaker

# Upload to Runpod (replace with your Runpod IP and port)
scp -P <port> AI_ReelMaker.tar.gz root@<runpod-ip>:/workspace/

# Then on Runpod, extract:
# tar -xzf AI_ReelMaker.tar.gz
```

### 4. Create .env File

```bash
cd /workspace/AI_ReelMaker
nano .env
```

**Add this content:**
```env
SECRET_KEY=your-secret-key-generate-random-string-here
DEBUG=False
ALLOWED_HOSTS=*
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
SADTALKER_ROOT=/workspace/SadTalker
BACKEND_BASE_URL=http://localhost:8000
```

**Save**: Press `Ctrl+X`, then `Y`, then `Enter`

**Generate SECRET_KEY** (optional, run this on Runpod):
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Build Docker Image

```bash
cd /workspace/AI_ReelMaker
docker build -t ai-reel-generator .
```

**⏱️ This will take 15-20 minutes** because it:
- Installs all dependencies
- Clones SadTalker automatically
- Downloads SadTalker models (~10GB)

**Watch for**: The build should complete without errors. If model download fails, you may need to download manually later.

### 6. Run Docker Container

```bash
docker run -d \
  --name ai-reel-app \
  --gpus all \
  -p 8000:8000 \
  --env-file .env \
  -v /workspace/AI_ReelMaker/media:/app/media \
  -v /workspace/SadTalker:/workspace/SadTalker \
  ai-reel-generator
```

### 7. Check Container Status

```bash
# Check if running
docker ps

# View logs
docker logs ai-reel-app

# If you see "Starting development server at http://0.0.0.0:8000/", it's working!
```

### 8. Configure Port Forwarding

1. In Runpod dashboard, go to your Pod
2. Find **"Ports"** or **"Network"** section
3. Add port mapping: **8000** → **8000**
4. Set visibility to **Public**
5. Copy the public URL (e.g., `https://xxxxx.runpod.net`)

### 9. Test Your API

Open in browser:
- API Info: `http://<your-runpod-url>:8000/api/`
- Create Reel: `POST http://<your-runpod-url>:8000/api/reels/`

**Test with curl:**
```bash
curl http://<your-runpod-url>:8000/api/
```

---

## Troubleshooting

### Container won't start
```bash
docker logs ai-reel-app
docker ps -a  # Check all containers
```

### GPU not detected
```bash
nvidia-smi  # Should show GPU info
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### Models not downloaded
```bash
# Enter container
docker exec -it ai-reel-app bash

# Manually download models
cd /workspace/SadTalker
bash scripts/download_models.sh
```

### Update your code
```bash
# Stop container
docker stop ai-reel-app
docker rm ai-reel-app

# Update code (git pull or re-upload)

# Rebuild (if code changed)
docker build -t ai-reel-generator .

# Run again
docker run -d --name ai-reel-app --gpus all -p 8000:8000 --env-file .env -v /workspace/AI_ReelMaker/media:/app/media -v /workspace/SadTalker:/workspace/SadTalker ai-reel-generator
```

---

## Important Notes

- **Cost**: Runpod charges per hour - stop your pod when not in use!
- **Data Persistence**: Files in `/workspace` persist between pod restarts
- **Media Files**: Mounted volume ensures videos persist
- **First Build**: Takes 15-20 minutes (downloading models)
- **Subsequent Builds**: Faster if you cache layers

---

## Quick Commands Reference

```bash
# Build image
docker build -t ai-reel-generator .

# Run container
docker run -d --name ai-reel-app --gpus all -p 8000:8000 --env-file .env -v /workspace/AI_ReelMaker/media:/app/media -v /workspace/SadTalker:/workspace/SadTalker ai-reel-generator

# View logs
docker logs ai-reel-app

# Stop container
docker stop ai-reel-app

# Start container
docker start ai-reel-app

# Remove container
docker rm ai-reel-app

# Enter container shell
docker exec -it ai-reel-app bash
```

