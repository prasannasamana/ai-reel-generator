# Runpod Serverless Setup - Step by Step 🚀

## 📋 Prerequisites Checklist

- [x] Docker installed locally
- [x] GitHub account (code already pushed)
- [x] Runpod account (just signed up)
- [ ] Docker Hub account (we'll create this)
- [ ] Runpod API key (we'll get this)

---

## 🎯 Step 1: Create Docker Hub Account

1. **Go to:** https://hub.docker.com/
2. **Sign up** for a free account
3. **Verify your email**
4. **Note your username** (e.g., `yourusername`)

---

## 🐳 Step 2: Build Docker Image Locally

**On your local computer (PowerShell):**

```powershell
# Navigate to project folder
cd "C:\Users\prasa\Desktop\Yellas Tech Work\Madhu_sir_works\AI_ReelMaker"

# Login to Docker Hub (will prompt for username/password)
docker login

# Build the image (replace YOUR_USERNAME with your Docker Hub username)
docker build -f runpod_Dockerfile -t YOUR_USERNAME/ai-reel-runpod:latest .

# Example:
# docker build -f runpod_Dockerfile -t prasanna7189/ai-reel-runpod:latest .
```

**This will take 10-20 minutes** (clones SadTalker, downloads models, etc.)

**Expected output:**
```
Successfully built abc123def456
Successfully tagged YOUR_USERNAME/ai-reel-runpod:latest
```

---

## 📤 Step 3: Push Image to Docker Hub

```powershell
# Push the image to Docker Hub
docker push YOUR_USERNAME/ai-reel-runpod:latest

# Example:
# docker push prasanna7189/ai-reel-runpod:latest
```

**This will take 5-10 minutes** (uploading ~5-10GB image)

**Expected output:**
```
The push refers to repository [docker.io/YOUR_USERNAME/ai-reel-runpod]
latest: digest: sha256:abc123... size: 12345
```

**✅ Verify:** Go to https://hub.docker.com/r/YOUR_USERNAME/ai-reel-runpod and see your image!

---

## 🔑 Step 4: Get Runpod API Key

1. **Go to:** https://www.runpod.io/
2. **Login** to your account
3. **Click** on your profile (top right)
4. **Go to:** Settings → API Keys
5. **Click** "Create API Key"
6. **Copy the API key** (starts with `RUNPOD_API_KEY=...`)
7. **Save it** - you'll need it later!

---

## 🚀 Step 5: Create Runpod Serverless Endpoint

### 5.1: Go to Serverless Dashboard

1. **Go to:** https://www.runpod.io/serverless
2. **Click** "New Endpoint" or "Create Endpoint"

### 5.2: Configure Endpoint

**Fill in these fields:**

1. **Endpoint Name:**
   ```
   ai-reel-generator
   ```

2. **Container Image:**
   ```
   YOUR_USERNAME/ai-reel-runpod:latest
   ```
   (Replace `YOUR_USERNAME` with your Docker Hub username)

3. **Container Disk:** 
   ```
   20 GB
   ```
   (Minimum required for SadTalker models)

4. **GPU Type:**
   ```
   RTX 3090
   ```
   (Or any GPU - RTX 3090 is good balance of cost/speed)

5. **Max Workers:**
   ```
   1
   ```
   (Start with 1, can increase later)

6. **Idle Timeout:**
   ```
   5 seconds
   ```
   (Shuts down quickly when idle to save costs)

7. **FlashBoot:**
   ```
   Enabled
   ```
   (Faster startup)

### 5.3: Environment Variables

**Add these environment variables:**

| Key | Value |
|-----|-------|
| `SADTALKER_ROOT` | `/workspace/SadTalker` |
| `PYTHONPATH` | `/workspace` |

**Note:** We don't need `OPENAI_API_KEY` here because TTS is done in Django!

### 5.4: Handler Configuration

**Handler Path:**
```
handler.handler
```

**This tells Runpod to call the `handler()` function in `handler.py`**

### 5.5: Create Endpoint

1. **Click** "Create Endpoint"
2. **Wait** for endpoint to be created (1-2 minutes)
3. **Copy the Endpoint ID** (looks like: `abc123def456`)

---

## 🔗 Step 6: Get Endpoint URL

After creating the endpoint, you'll see:

**Endpoint URL:**
```
https://api.runpod.ai/v2/abc123def456/run
```

**Copy this URL** - you'll need it for Django!

**Or find it later:**
1. Go to Serverless dashboard
2. Click on your endpoint
3. Copy the "Endpoint URL"

---

## ⚙️ Step 7: Update Django .env File

**On your local computer:**

1. **Open** `.env` file:
   ```powershell
   notepad .env
   ```

2. **Add these lines:**
   ```env
   # Runpod Serverless Configuration
   USE_RUNPOD=true
   RUNPOD_ENDPOINT_URL=https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run
   RUNPOD_API_KEY=your-runpod-api-key-here
   ```

3. **Replace:**
   - `YOUR_ENDPOINT_ID` with your actual endpoint ID
   - `your-runpod-api-key-here` with your actual Runpod API key

4. **Example:**
   ```env
   USE_RUNPOD=true
   RUNPOD_ENDPOINT_URL=https://api.runpod.ai/v2/abc123def456/run
   RUNPOD_API_KEY=RUNPOD_API_KEY=abc123def456789...
   ```

5. **Save** and close

---

## ✅ Step 8: Test the Setup

### 8.1: Restart Django Server

```powershell
# Stop current server (Ctrl+C if running)
# Then restart:
python manage.py runserver
```

### 8.2: Test Video Generation

**In Postman:**

1. **POST** `http://localhost:8000/api/reels/961a8a6e-6e4b-4b4b-8cf3-44f962e7ee38/generate-video/`
   (Use your existing reel ID)

2. **Expected Response:**
   ```json
   {
     "id": "...",
     "status": "processing",
     ...
   }
   ```

3. **Wait 1-2 minutes** (video generation takes time)

4. **Check Status:**
   ```
   GET http://localhost:8000/api/reels/961a8a6e-6e4b-4b4b-8cf3-44f962e7ee38/
   ```

5. **When done:**
   ```json
   {
     "status": "done",
     "video_url": "http://localhost:8000/media/reels/.../video.mp4"
   }
   ```

---

## 🎉 Success!

If you see `video_url` in the response, **everything is working!** 🎊

---

## 💰 Cost Monitoring

**Check costs:**
1. Go to Runpod dashboard
2. Click "Billing" or "Usage"
3. Monitor your spending

**Tips to save costs:**
- Set `Idle Timeout` to 5 seconds (already done)
- Use `Max Workers: 1` (already done)
- Only process when needed

---

## 🐛 Troubleshooting

### Issue: "RUNPOD_ENDPOINT_URL not configured"
**Solution:** Check `.env` file has `RUNPOD_ENDPOINT_URL` set correctly

### Issue: "401 Unauthorized"
**Solution:** Check `RUNPOD_API_KEY` in `.env` is correct

### Issue: "Endpoint not found"
**Solution:** Verify endpoint ID in `RUNPOD_ENDPOINT_URL` is correct

### Issue: "Handler not found"
**Solution:** Make sure handler path is `handler.handler` in Runpod config

### Issue: "SadTalker not found"
**Solution:** Check Docker image was built correctly with SadTalker

### Issue: Video generation fails
**Solution:** Check Runpod logs:
1. Go to Serverless dashboard
2. Click on your endpoint
3. Click "Logs" tab
4. See error messages

---

## 📝 Quick Reference

**Docker Hub Image:**
```
YOUR_USERNAME/ai-reel-runpod:latest
```

**Runpod Endpoint URL Format:**
```
https://api.runpod.ai/v2/ENDPOINT_ID/run
```

**Handler Path:**
```
handler.handler
```

**Environment Variables (Runpod):**
- `SADTALKER_ROOT=/workspace/SadTalker`
- `PYTHONPATH=/workspace`

**Django .env:**
```env
USE_RUNPOD=true
RUNPOD_ENDPOINT_URL=https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run
RUNPOD_API_KEY=your-api-key-here
```

---

## 🚀 Let's Start!

Begin with **Step 1: Create Docker Hub Account** and work through each step.

If you get stuck at any step, let me know! 💪

