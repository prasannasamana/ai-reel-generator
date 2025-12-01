# Next Steps After Migrations ✅

## 🎯 Current Status
- ✅ Django project created
- ✅ Models defined
- ✅ Migrations applied
- ✅ Human-in-the-loop workflow implemented

---

## 📋 Step-by-Step Next Actions

### Step 1: Test API Locally (Script Rewriting)

**Start Django Server:**
```bash
# Make sure venv is activated
python manage.py runserver
```

**Test API Endpoints:**

1. **Check API Info:**
   ```bash
   curl http://localhost:8000/api/
   ```
   Or open in browser: http://localhost:8000/api/

2. **Create a Reel (Script Rewriting):**
   ```bash
   # Using curl (PowerShell)
   curl -X POST http://localhost:8000/api/reels/ `
     -F "image=@path/to/your/image.jpg" `
     -F "script=Hello, this is my original script" `
     -F "tone=friendly" `
     -F "use_rewrite=true"
   ```

   **Or use the test script:**
   ```bash
   python test_api.py path/to/image.jpg "Your script here"
   ```

3. **Check the Response:**
   - You should get a `reel_id` and `final_script` (rewritten version)
   - Status should be `script_pending_approval`

4. **Review & Regenerate Script (if needed):**
   ```bash
   curl -X POST http://localhost:8000/api/reels/<reel_id>/regenerate-script/ `
     -H "Content-Type: application/json" `
     -d '{"tone": "energetic"}'
   ```

5. **Approve Script:**
   ```bash
   curl -X POST http://localhost:8000/api/reels/<reel_id>/approve-script/
   ```

**Note:** Video generation will fail locally (no GPU), but script rewriting should work!

---

### Step 2: Set Up Runpod Serverless (For Video Generation)

Since you don't have a local GPU, you need to deploy the Runpod handler for video generation.

#### 2.1: Update `.env` File

Add Runpod configuration to your `.env`:

```env
# Runpod Serverless Configuration
USE_RUNPOD=true
RUNPOD_ENDPOINT_URL=https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run
RUNPOD_API_KEY=your-runpod-api-key-here
```

**You'll get these values after deploying to Runpod Serverless.**

#### 2.2: Deploy Runpod Handler

Follow the detailed guide: **`SERVERLESS_DEPLOYMENT.md`**

**Quick Summary:**
1. Build Docker image from `runpod_Dockerfile`
2. Push to Docker Hub
3. Create Runpod Serverless endpoint
4. Configure handler
5. Get endpoint URL and API key
6. Update `.env` with those values

---

### Step 3: Test Complete Workflow

Once Runpod is set up:

1. **Create Reel:**
   ```bash
   POST /api/reels/
   ```

2. **Review Script:**
   ```bash
   GET /api/reels/<id>/
   ```

3. **Regenerate (if needed):**
   ```bash
   POST /api/reels/<id>/regenerate-script/
   ```

4. **Approve & Generate Video:**
   ```bash
   POST /api/reels/<id>/approve-script/
   ```

5. **Check Status:**
   ```bash
   GET /api/reels/<id>/
   ```
   - Status will be `processing` → `done`
   - Video URL will be available when done

---

## 🔧 Configuration Checklist

### Required in `.env`:
- [x] `SECRET_KEY` - Django secret key
- [x] `DEBUG=True` - For development
- [x] `OPENAI_API_KEY` - For script rewriting & TTS
- [ ] `USE_RUNPOD=true` - Enable Runpod integration
- [ ] `RUNPOD_ENDPOINT_URL` - From Runpod dashboard
- [ ] `RUNPOD_API_KEY` - From Runpod dashboard

### Optional:
- [ ] `SADTALKER_ROOT` - Only if using local GPU
- [ ] `BACKEND_BASE_URL` - For production deployment
- [ ] `ASYNC_PROCESSING=true` - Process videos in background

---

## 📚 Documentation Files

- **`HUMAN_IN_LOOP_WORKFLOW.md`** - Complete API workflow guide
- **`SERVERLESS_DEPLOYMENT.md`** - Runpod Serverless setup
- **`CHANGES_SUMMARY.md`** - What changed in the architecture
- **`test_api.py`** - Test script for API endpoints

---

## 🚀 Quick Test Commands

**Test API Info:**
```bash
python -c "import requests; print(requests.get('http://localhost:8000/api/').json())"
```

**Create Reel (PowerShell):**
```powershell
$image = Get-Item "path\to\image.jpg"
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/reels/" `
  -Method Post `
  -Form @{
    image = $image
    script = "Hello world"
    tone = "friendly"
    use_rewrite = "true"
  }
$response | ConvertTo-Json
```

---

## ⚠️ Important Notes

1. **Script Rewriting Works Locally** - You can test the full approval workflow without GPU
2. **Video Generation Requires Runpod** - Set up Runpod Serverless for actual video generation
3. **Cost Optimization** - Only generate video after user approval (saves Runpod costs)
4. **Async Processing** - Set `ASYNC_PROCESSING=true` for background video generation

---

## 🎯 Your Next Action

**Right Now:**
1. Start server: `python manage.py runserver`
2. Test script rewriting: Create a reel and see the rewritten script
3. Test approval workflow: Regenerate and approve scripts

**Then:**
4. Deploy Runpod Serverless (follow `SERVERLESS_DEPLOYMENT.md`)
5. Test complete workflow with video generation

---

## 💡 Tips

- Use Postman or Insomnia for easier API testing
- Check Django logs: `python manage.py runserver --verbosity 2`
- Monitor Runpod costs in Runpod dashboard
- Use async processing for better user experience

Good luck! 🚀

