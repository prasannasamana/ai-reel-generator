# Runpod Serverless Setup - Using GitHub (Easier!) 🚀

## ✅ You Already Have:
- ✅ GitHub account
- ✅ Code pushed to GitHub: `https://github.com/prasanna7189/ai-reel-generator`
- ✅ Runpod account

**No Docker Hub needed!** Runpod will build from your GitHub repo directly.

---

## 🎯 Step 1: Get Runpod API Key

1. **Go to:** https://www.runpod.io/
2. **Login** to your account
3. **Click** on your profile (top right)
4. **Go to:** Settings → API Keys
5. **Click** "Create API Key"
6. **Copy the API key** (starts with `RUNPOD_API_KEY=...`)
7. **Save it** - you'll need it for Django `.env` file!

---

## 🚀 Step 2: Create Runpod Serverless Endpoint from GitHub

### 2.1: Go to Serverless Dashboard

1. **Go to:** https://www.runpod.io/serverless
2. **Click** "New Endpoint" or "Create Endpoint"

### 2.2: Configure Endpoint - Use GitHub

**Fill in these fields:**

1. **Endpoint Name:**
   ```
   ai-reel-generator
   ```

2. **Source:** Select **"GitHub"** (not Docker Hub)

3. **Repository URL:**
   ```
   https://github.com/prasanna7189/ai-reel-generator
   ```
   (Your GitHub repo URL)

4. **Branch:**
   ```
   main
   ```
   (Or `master` if that's your default branch)

5. **Dockerfile Path:**
   ```
   runpod_Dockerfile
   ```
   (The Dockerfile name in your repo)

6. **Container Disk:** 
   ```
   20 GB
   ```
   (Minimum required for SadTalker models)

7. **GPU Type:**
   ```
   RTX 3090
   ```
   (Or any GPU - RTX 3090 is good balance of cost/speed)

8. **Max Workers:**
   ```
   1
   ```
   (Start with 1, can increase later)

9. **Idle Timeout:**
   ```
   5 seconds
   ```
   (Shuts down quickly when idle to save costs)

10. **FlashBoot:**
    ```
    Enabled
    ```
    (Faster startup)

### 2.3: Environment Variables

**Add these environment variables:**

| Key | Value |
|-----|-------|
| `SADTALKER_ROOT` | `/workspace/SadTalker` |
| `PYTHONPATH` | `/workspace` |

**Note:** We don't need `OPENAI_API_KEY` here because TTS is done in Django!

### 2.4: Handler Configuration

**Handler Path:**
```
handler.handler
```

**This tells Runpod to call the `handler()` function in `handler.py`**

**Note:** Make sure `runpod_handler.py` is in the root of your GitHub repo!

### 2.5: Create Endpoint

1. **Click** "Create Endpoint"
2. **Runpod will:**
   - Clone your GitHub repo
   - Build the Docker image using `runpod_Dockerfile`
   - Set up the endpoint
3. **Wait** 10-20 minutes (first build takes time - downloads SadTalker, models, etc.)
4. **Copy the Endpoint ID** (looks like: `abc123def456`)

---

## 🔗 Step 3: Get Endpoint URL

After the endpoint is created, you'll see:

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

## ⚙️ Step 4: Update Django .env File

**On your local computer:**

1. **Open** `.env` file:
   ```powershell
   cd "C:\Users\prasa\Desktop\Yellas Tech Work\Madhu_sir_works\AI_ReelMaker"
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
   - `YOUR_ENDPOINT_ID` with your actual endpoint ID from Step 3
   - `your-runpod-api-key-here` with your actual Runpod API key from Step 1

4. **Example:**
   ```env
   USE_RUNPOD=true
   RUNPOD_ENDPOINT_URL=https://api.runpod.ai/v2/abc123def456/run
   RUNPOD_API_KEY=RUNPOD_API_KEY=abc123def456789...
   ```

5. **Save** and close

---

## ✅ Step 5: Verify Files in GitHub

**Make sure these files are in your GitHub repo:**

- ✅ `runpod_Dockerfile` (in root)
- ✅ `runpod_handler.py` (in root)
- ✅ `requirements.txt` (in root)

**Check your repo:** https://github.com/prasanna7189/ai-reel-generator

If `runpod_handler.py` is missing, push it:
```powershell
git add runpod_handler.py
git commit -m "Add Runpod handler"
git push
```

---

## ✅ Step 6: Test the Setup

### 6.1: Restart Django Server

```powershell
# Stop current server (Ctrl+C if running)
# Then restart:
cd "C:\Users\prasa\Desktop\Yellas Tech Work\Madhu_sir_works\AI_ReelMaker"
python manage.py runserver
```

### 6.2: Test Video Generation

**In Postman:**

1. **POST** `http://localhost:8000/api/reels/961a8a6e-6e4b-4b4b-8cf3-44f962e7ee38/generate-video/`
   (Use your existing reel ID that has audio)

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

## 🔄 Updating Your Code

**When you update code:**

1. **Push to GitHub:**
   ```powershell
   git add .
   git commit -m "Update code"
   git push
   ```

2. **Rebuild Endpoint in Runpod:**
   - Go to Serverless dashboard
   - Click on your endpoint
   - Click "Rebuild" or "Update"
   - Wait for rebuild to complete

**Or:** Runpod can auto-rebuild on push (check Runpod settings)

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
**Solution:** 
- Check `runpod_handler.py` is in root of GitHub repo
- Check handler path is `handler.handler` in Runpod config
- Make sure file is pushed to GitHub

### Issue: "Dockerfile not found"
**Solution:** 
- Check `runpod_Dockerfile` is in root of GitHub repo
- Check Dockerfile path in Runpod config is `runpod_Dockerfile`
- Make sure file is pushed to GitHub

### Issue: Build fails in Runpod
**Solution:** 
1. Check Runpod build logs
2. Go to Serverless dashboard → Your endpoint → Logs
3. See error messages
4. Common issues:
   - Missing files in GitHub
   - Wrong Dockerfile path
   - GitHub repo is private (make it public or add Runpod as collaborator)

### Issue: Video generation fails
**Solution:** Check Runpod logs:
1. Go to Serverless dashboard
2. Click on your endpoint
3. Click "Logs" tab
4. See error messages

---

## 📝 Quick Reference

**GitHub Repo:**
```
https://github.com/prasanna7189/ai-reel-generator
```

**Dockerfile Path (in Runpod):**
```
runpod_Dockerfile
```

**Handler Path:**
```
handler.handler
```

**Runpod Endpoint URL Format:**
```
https://api.runpod.ai/v2/ENDPOINT_ID/run
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

**Begin with Step 1: Get Runpod API Key**

Then go to Step 2 and create the endpoint using your GitHub repo!

**Much simpler than Docker Hub!** 🎉

