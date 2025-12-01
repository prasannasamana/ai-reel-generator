# Architecture Update: TTS in Django, Video on Runpod 🎯

## ✅ Updated Architecture

### **Before (Inefficient):**
- Django: Script rewriting
- Runpod: TTS + Video generation

### **After (Optimized):**
- **Django:** Script rewriting + TTS audio generation (no GPU needed)
- **Runpod:** Video generation only (SadTalker - GPU required)

---

## 🔄 New Workflow

```
1. User creates reel → Django rewrites script
2. User approves script → Django generates TTS audio (OpenAI API)
3. Django sends image + audio to Runpod
4. Runpod runs SadTalker (image + audio → video)
5. Runpod returns video to Django
6. Django saves video file
```

---

## 📋 What Changed

### 1. **Django (`reels/services/video_generation_runpod.py`)**
- Now generates TTS audio **before** calling Runpod
- Uses `generate_tts_audio()` from `openai_tts.py`
- Sends **image + audio** to Runpod (not script)

### 2. **Runpod Client (`reels/services/runpod_client.py`)**
- `generate_video_with_runpod()` now takes:
  - `image_path` (image file)
  - `audio_path` (audio file - already generated)
- No longer sends script to Runpod

### 3. **Runpod Handler (`runpod_handler.py`)**
- Removed TTS generation code
- Now only handles video generation (SadTalker)
- Receives: `image` + `audio` (both base64)
- Returns: `video_base64`

---

## 🎯 Benefits

✅ **Cost Effective:** TTS doesn't need GPU, saves Runpod costs  
✅ **Faster:** TTS is instant in Django, no need to wait for Runpod  
✅ **Better UX:** User can preview audio before expensive video generation  
✅ **Cleaner Separation:** Only GPU-intensive tasks on Runpod  
✅ **More Control:** Audio generation happens in Django, easier to debug  

---

## 📝 SadTalker Inputs

**SadTalker requires:**
- `--driven_audio` (audio file path)
- `--source_image` (image file path)
- `--result_dir` (output directory)

**That's it!** No script needed - audio is already generated.

---

## 🔧 API Flow

### Step 1: Create Reel
```
POST /api/reels/
→ Django rewrites script
→ Status: script_pending_approval
```

### Step 2: Approve Script
```
POST /api/reels/<id>/approve-script/
→ Django generates TTS audio (OpenAI API)
→ Django sends image + audio to Runpod
→ Runpod generates video (SadTalker)
→ Status: processing → done
```

### Step 3: Get Result
```
GET /api/reels/<id>/
→ Returns video_url, audio_url
```

---

## 💡 Key Points

1. **TTS in Django:** Uses OpenAI TTS API (fast, no GPU)
2. **Video on Runpod:** Only GPU-intensive task
3. **Audio Preview:** User can listen to audio before video generation
4. **Cost Optimization:** Only pay Runpod for video generation

---

## 🚀 Migration Notes

- No database changes needed
- Existing reels will work (audio will be generated on approval)
- Runpod handler needs to be redeployed with new code
- Django code updated automatically

---

This architecture is much more efficient! 🎉

