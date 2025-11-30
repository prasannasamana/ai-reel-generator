# Runpod Serverless Deployment Guide - Complete Step-by-Step

## 📋 Overview

This guide shows you **exactly** what to do on your **local computer** vs what to do on **Runpod**.

**You have:**
- ✅ Docker installed locally
- ✅ GitHub account
- ✅ Runpod Serverless account (just signed up)

---

## 🎯 What is Serverless?

**Serverless** = Pay only when your API is processing requests. When idle, you pay $0.

**Cost Example:**
- Regular Pod: ~$7/day (even when idle)
- Serverless: ~$0.50/day (only when processing)

---

## 📍 Part 1: LOCAL - Prepare Your Code

### Step 1.1: LOCAL - Verify Your Project

**On your local computer**, make sure you're in the project folder:

```bash
cd "C:\Users\prasa\Desktop\Yellas Tech Work\Madhu_sir_works\AI_ReelMaker"
```

**Check these files exist:**
- ✅ `Dockerfile`
- ✅ `requirements.txt`
- ✅ `manage.py`
- ✅ `handler.py`
- ✅ `reel_platform/` folder
- ✅ `reels/` folder

### Step 1.2: LOCAL - Create .env File (if not exists)

**On your local computer:**

1. **Check if .env exists:**
   ```bash
   dir .env
   ```

2. **If it doesn't exist, create it:**
   ```bash
   copy env.example .env
   ```

3. **Edit .env file** (open with Notepad):
   ```bash
   notepad .env
   ```

4. **Add your OpenAI API key:**
   ```
   SECRET_KEY=django-insecure-local-dev-key-change-in-production
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here
   SADTALKER_ROOT=/workspace/SadTalker
   BACKEND_BASE_URL=http://localhost:8000
   ```

5. **Save and close** Notepad

### Step 1.3: LOCAL - Push Code to GitHub

**On your local computer:**

1. **Open Command Prompt or PowerShell** in your project folder

2. **Initialize Git** (if not already done):
   ```bash
   git init
   ```

3. **Add all files:**
   ```bash
   git add .
   ```

4. **Commit:**
   ```bash
   git commit -m "Initial commit - AI Reel Generator"
   ```

5. **Connect to GitHub** (replace `YOUR_USERNAME` with your GitHub username):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ai-reel-generator.git
   ```

   **If you haven't created the repo on GitHub yet:**
   - Go to github.com
   - Click "+" → "New repository"
   - Name: `ai-reel-generator`
   - Click "Create repository"
   - Copy the repository URL

6. **Push to GitHub:**
   ```bash
   git branch -M main
   git push -u origin main
   ```

   **If asked for credentials**, use your GitHub username and a Personal Access Token (not password)

---

## 📍 Part 2: RUNPOD - Create Pod for Building Docker Image

### Step 2.1: RUNPOD - Create a Pod

**On Runpod website (runpod.io):**

1. **Login** to your Runpod account

2. **Click "Pods"** in the left sidebar

3. **Click "New Pod"** button (or "Create Pod")

4. **Select Template:**
   - Choose **"PyTorch 2.0.1"** or **"CUDA 11.8.0"**
   - Click it

5. **Select GPU:**
   - Choose **RTX 3090** (cheapest option, ~$0.29/hour)
   - Or RTX 4090 if available

6. **Set Container Disk:**
   - Set to **50GB** (important! SadTalker models are large)
   - Use the slider or type `50`

7. **Select Region:**
   - Choose closest to you (e.g., US East, EU West)

8. **Click "Continue"** or **"Deploy"**

9. **Wait 2-3 minutes** for pod to start (you'll see "Running" status)

### Step 2.2: RUNPOD - Connect to Pod

**On Runpod website:**

1. **Click on your pod** in the list

2. **Click "Connect"** button (top right)

3. **Choose "HTTP Service"** (Jupyter interface)

4. **Click "Start"** or **"Connect"**

5. **A new browser tab opens** with Jupyter interface

6. **Click "Terminal"** or **"New" → "Terminal"** to open command line

---

## 📍 Part 3: RUNPOD - Upload Your Code

### Step 3.1: RUNPOD - Clone from GitHub

**In the Runpod terminal (Jupyter interface):**

1. **Navigate to workspace:**
   ```bash
   cd /workspace
   ```

2. **Clone your GitHub repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-reel-generator.git
   ```
   (Replace `YOUR_USERNAME` with your actual GitHub username)

3. **Navigate into project:**
   ```bash
   cd ai-reel-generator
   ```

4. **Verify files are there:**
   ```bash
   ls -la
   ```
   You should see: `Dockerfile`, `manage.py`, `requirements.txt`, etc.

### Step 3.2: RUNPOD - Create .env File for Production

**In Runpod terminal:**

1. **Create .env file:**
   ```bash
   nano .env
   ```

2. **Paste this content** (press `Ctrl+Shift+V` to paste in terminal):
   ```env
   SECRET_KEY=CHANGE-THIS-TO-RANDOM-STRING
   DEBUG=False
   ALLOWED_HOSTS=*
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here
   SADTALKER_ROOT=/workspace/SadTalker
   BACKEND_BASE_URL=https://api.runpod.ai
   ```

3. **Generate a secret key** (in terminal):
   ```bash
   python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Copy the output (long random string)

4. **Edit .env again:**
   ```bash
   nano .env
   ```
   Replace `CHANGE-THIS-TO-RANDOM-STRING` with the secret key you just generated

5. **Replace** `sk-your-actual-openai-api-key-here` with your real OpenAI API key

6. **Save:**
   - Press `Ctrl+X`
   - Press `Y` (yes)
   - Press `Enter`

---

## 📍 Part 4: RUNPOD - Build Docker Image

### Step 4.1: RUNPOD - Build the Image

**In Runpod terminal** (make sure you're in `/workspace/ai-reel-generator`):

1. **Check current directory:**
   ```bash
   pwd
   ```
   Should show: `/workspace/ai-reel-generator`

2. **Build Docker image** (this takes 15-20 minutes!):
   ```bash
   docker build -t ai-reel-generator .
   ```

   **What's happening:**
   - Installing Python dependencies
   - Cloning SadTalker from GitHub
   - Installing SadTalker dependencies
   - Downloading SadTalker models (~10GB) ← This is the longest part!

3. **Wait patiently** - You'll see lots of output. When done, you'll see:
   ```
   Successfully built abc123def456
   Successfully tagged ai-reel-generator:latest
   ```

### Step 4.2: RUNPOD - Test Image Locally (Optional)

**In Runpod terminal:**

Test that the image works:
```bash
docker run --rm ai-reel-generator python manage.py --version
```

Should show Django version.

---

## 📍 Part 5: RUNPOD - Push Image to Docker Hub

### Step 5.1: RUNPOD - Create Docker Hub Account (if needed)

**On Docker Hub website (hub.docker.com):**

1. **Go to hub.docker.com**
2. **Sign up** (if you don't have account) - It's FREE
3. **Verify email** if needed
4. **Note your username** (you'll need it)

### Step 5.2: RUNPOD - Login to Docker Hub

**In Runpod terminal:**

1. **Login to Docker Hub:**
   ```bash
   docker login
   ```

2. **Enter your credentials:**
   - Username: (your Docker Hub username)
   - Password: (your Docker Hub password or access token)

3. **You should see:** `Login Succeeded`

### Step 5.3: RUNPOD - Tag Your Image

**In Runpod terminal:**

1. **Tag your image** (replace `YOUR_DOCKERHUB_USERNAME`):
   ```bash
   docker tag ai-reel-generator YOUR_DOCKERHUB_USERNAME/ai-reel-generator:latest
   ```

   **Example:**
   ```bash
   docker tag ai-reel-generator johnsmith/ai-reel-generator:latest
   ```

### Step 5.4: RUNPOD - Push to Docker Hub

**In Runpod terminal:**

1. **Push the image** (this takes 5-10 minutes, ~10GB upload):
   ```bash
   docker push YOUR_DOCKERHUB_USERNAME/ai-reel-generator:latest
   ```

2. **Wait for upload to complete** - You'll see progress bars

3. **Verify on Docker Hub:**
   - Go to hub.docker.com
   - Login
   - Click on your repositories
   - You should see `ai-reel-generator`

4. **Note your image name:** `YOUR_DOCKERHUB_USERNAME/ai-reel-generator:latest`
   - You'll need this for the serverless endpoint!

---

## 📍 Part 6: RUNPOD - Create Serverless Endpoint

### Step 6.1: RUNPOD - Go to Serverless Section

**On Runpod website:**

1. **Click "Serverless"** in the left sidebar

2. **Click "New Endpoint"** or **"Create Endpoint"** button

### Step 6.2: RUNPOD - Configure Basic Settings

**In the Create Endpoint form:**

1. **Endpoint Name:**
   - Type: `ai-reel-generator`
   - (Or any name you like)

2. **Container Image:**
   - Type: `YOUR_DOCKERHUB_USERNAME/ai-reel-generator:latest`
   - **Example:** `johnsmith/ai-reel-generator:latest`
   - (Use the exact name from Step 5.4)

3. **GPU Type:**
   - Select: **RTX 3090** (or RTX 4090/A100)
   - This is what will process your videos

4. **Container Disk:**
   - Set to: **50GB**
   - (For SadTalker models)

### Step 6.3: RUNPOD - Configure Handler (IMPORTANT!)

**In the Create Endpoint form:**

**Option A: Use Handler Template** (for custom handler)

1. **Handler:**
   - Type: `handler.handler`
   - This tells Runpod to use the `handler` function in `handler.py`

2. **Docker Command:** (leave empty or use):
   ```
   python -c "import handler"
   ```

**Option B: Use HTTP Template** (EASIER - Recommended!)

1. **Look for "Template" or "Type" dropdown**
2. **Select "HTTP"** or **"HTTP Endpoint"**
3. **Port:** `8000` (Django runs on port 8000)
4. **Skip the Handler field** (not needed for HTTP template)

**👉 RECOMMENDATION: Use Option B (HTTP Template) - It's simpler!**

### Step 6.4: RUNPOD - Set Environment Variables

**In the Create Endpoint form, find "Environment Variables" section:**

Click **"Add Environment Variable"** for each of these:

1. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: (paste the secret key from your .env file)

2. **DEBUG**
   - Key: `DEBUG`
   - Value: `False`

3. **ALLOWED_HOSTS**
   - Key: `ALLOWED_HOSTS`
   - Value: `*`

4. **OPENAI_API_KEY**
   - Key: `OPENAI_API_KEY`
   - Value: (paste your OpenAI API key)

5. **SADTALKER_ROOT**
   - Key: `SADTALKER_ROOT`
   - Value: `/workspace/SadTalker`

6. **BACKEND_BASE_URL**
   - Key: `BACKEND_BASE_URL`
   - Value: `https://api.runpod.ai` (for handler template)
   - OR: `https://your-endpoint-id.runpod.net` (for HTTP template - you'll get this after creation)

### Step 6.5: RUNPOD - Advanced Settings

**In the Create Endpoint form:**

1. **Max Workers:**
   - Set to: `1` (start with 1, increase later if needed)

2. **Idle Timeout:**
   - Set to: `5` seconds (saves money - shuts down when idle)

3. **Flashboot:**
   - ✅ Enable this (faster cold starts)

4. **Timeout:**
   - Set to: `600` seconds (10 minutes - for video generation)

5. **Volume Mounts:** (Optional)
   - You can mount persistent storage here if needed

### Step 6.6: RUNPOD - Create the Endpoint

1. **Review all settings**

2. **Click "Create"** or **"Deploy"** button

3. **Wait 2-3 minutes** for endpoint to be created

4. **You'll see your endpoint** in the Serverless list

---

## 📍 Part 7: RUNPOD - Get Your Endpoint URL

### Step 7.1: RUNPOD - Copy Endpoint URL

**On Runpod website:**

1. **Click on your endpoint** in the Serverless list

2. **Find the endpoint URL** - It will be one of these formats:

   **For HTTP Template:**
   ```
   https://xxxxx-xxxxx.runpod.net
   ```

   **For Handler Template:**
   ```
   https://api.runpod.ai/v2/xxxxx-xxxxx-xxxxx/run
   ```

3. **Copy this URL** - You'll need it to test!

---

## 📍 Part 8: LOCAL or RUNPOD - Test Your Endpoint

### Step 8.1: Test API Info Endpoint

**On your local computer OR Runpod terminal:**

**If using HTTP Template** (easier):

```bash
curl https://xxxxx-xxxxx.runpod.net/api/
```

**If using Handler Template:**

```bash
curl -X POST https://api.runpod.ai/v2/xxxxx-xxxxx-xxxxx/run \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "method": "GET",
      "path": "/api/",
      "headers": {},
      "body": "",
      "query": {}
    }
  }'
```

**Expected Response:** JSON with API information

### Step 8.2: Test Create Reel Endpoint

**On your local computer** (create a test file):

1. **Create test file:**
   ```bash
   notepad test_serverless.py
   ```

2. **Paste this code** (for HTTP template):
   ```python
   import requests

   endpoint_url = "https://xxxxx-xxxxx.runpod.net"
   
   # Test API info
   response = requests.get(f"{endpoint_url}/api/")
   print("Status:", response.status_code)
   print("Response:", response.json())
   
   # Test create reel (with image file)
   files = {'image': open('face.jpg', 'rb')}
   data = {
       'script': 'Hello, welcome to my reel!',
       'tone': 'friendly',
       'use_rewrite': 'true'
   }
   
   response = requests.post(f"{endpoint_url}/api/reels/", files=files, data=data)
   print("\nCreate Reel Status:", response.status_code)
   print("Response:", response.json())
   ```

3. **Save and run:**
   ```bash
   python test_serverless.py
   ```

---

## 📍 Summary: What Runs Where

### ✅ LOCAL (Your Computer):
- ✅ Prepare code
- ✅ Push to GitHub
- ✅ Test API (optional)
- ✅ Create test scripts

### ✅ RUNPOD (Website + Terminal):
- ✅ Create pod
- ✅ Clone code from GitHub
- ✅ Build Docker image
- ✅ Push to Docker Hub
- ✅ Create serverless endpoint
- ✅ Configure settings
- ✅ Test endpoint

---

## 🔧 Troubleshooting

### Problem: "Image not found" when creating endpoint
**Solution:**
- Make sure image is pushed to Docker Hub
- Check image name is correct: `username/ai-reel-generator:latest`
- Make sure image is public (or you're logged in)

### Problem: "Handler not found"
**Solution:**
- Check handler path: `handler.handler`
- Make sure `handler.py` is in root of Docker image
- OR use HTTP template instead (easier!)

### Problem: "Timeout error"
**Solution:**
- Increase timeout in endpoint settings (600 seconds)
- Video generation takes 5-10 minutes

### Problem: "Cold start too slow"
**Solution:**
- Enable Flashboot in settings
- First request after idle takes 10-30 seconds (normal)

### Problem: "File upload not working"
**Solution:**
- Use HTTP template (simpler for file uploads)
- For handler template, need base64 encoding

---

## 💰 Cost Management

### Monitor Usage:
1. Go to Runpod Dashboard → **Billing**
2. Check **Serverless** usage
3. Set up alerts if available

### Cost Example:
- **10 requests/day** × **2 minutes each** = **20 minutes/day**
- **Cost:** ~$0.48/day (vs $7/day for regular pod)

---

## 📝 Quick Reference

### Docker Image Name:
```
YOUR_DOCKERHUB_USERNAME/ai-reel-generator:latest
```

### Environment Variables:
```
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=*
OPENAI_API_KEY=sk-...
SADTALKER_ROOT=/workspace/SadTalker
BACKEND_BASE_URL=https://api.runpod.ai
```

### Endpoint URLs:
- **HTTP Template:** `https://xxxxx.runpod.net`
- **Handler Template:** `https://api.runpod.ai/v2/xxxxx/run`

---

## ✅ Final Checklist

- [ ] Code pushed to GitHub
- [ ] Docker image built on Runpod
- [ ] Image pushed to Docker Hub
- [ ] Serverless endpoint created
- [ ] Environment variables set
- [ ] Endpoint tested
- [ ] API working correctly

---

## 🎉 You're Done!

Your serverless API is now live! You only pay when processing requests.

**Next Steps:**
1. Test all endpoints
2. Monitor costs
3. Optimize settings
4. Start using your API!

---

## 📞 Need Help?

If stuck:
1. Check Runpod logs (in endpoint details)
2. Check Docker build logs
3. Verify environment variables
4. Try HTTP template (simpler than handler)
