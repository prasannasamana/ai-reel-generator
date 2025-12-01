# Handling Concurrent Requests - Architecture Guide

## 🔍 Current Behavior

### What Happens Now (Synchronous):

**Request 1 comes in:**
1. Django creates ReelJob
2. Django calls Runpod (waits 5-10 minutes)
3. Django saves result
4. Returns response

**Request 2 comes in (while Request 1 is processing):**
1. Django creates ReelJob
2. Django calls Runpod (waits 5-10 minutes)
3. Django saves result
4. Returns response

**Problem:** Each request blocks Django for 5-10 minutes!

---

## ✅ How Runpod Serverless Handles Concurrent Requests

### Runpod Serverless Configuration:

**Max Workers:** Set in Runpod dashboard (e.g., 1, 2, 3, 5)

- **Max Workers = 1:** Only 1 request at a time (others queue)
- **Max Workers = 3:** Can process 3 requests simultaneously
- **Max Workers = 5:** Can process 5 requests simultaneously

**What happens:**
- Request 1 → Worker 1 processes
- Request 2 → Worker 2 processes (if Max Workers > 1)
- Request 3 → Worker 3 processes (if Max Workers > 2)
- Request 4 → Queues until a worker is free

---

## ⚠️ Current Issue: Django Blocks

**Current code is synchronous:**
- Django waits for Runpod to finish before returning
- If 2 requests come, Django handles them sequentially
- Each request takes 5-10 minutes
- User waits for response

---

## 🚀 Solution: Make It Async (Non-Blocking)

### Option 1: Async Response (Recommended)

**Django returns immediately, processes in background:**

```python
# User gets response immediately with job ID
# Django processes in background
# User polls for status
```

### Option 2: Celery (Production Ready)

**Use Celery for background tasks:**
- Django returns immediately
- Celery worker processes Runpod calls
- User polls for status

### Option 3: Keep Synchronous (Simple)

**Current approach works but:**
- User waits 5-10 minutes
- Django blocks during processing
- Runpod can handle concurrent requests (if Max Workers > 1)

---

## 📊 Concurrent Request Scenarios

### Scenario 1: Max Workers = 1

**2 requests come simultaneously:**

```
Time 0:00 - Request 1 → Runpod Worker 1 (starts processing)
Time 0:00 - Request 2 → Queued (waits)
Time 5:00 - Request 1 → Done, Worker 1 free
Time 5:00 - Request 2 → Runpod Worker 1 (starts processing)
Time 10:00 - Request 2 → Done
```

**Total time:** 10 minutes (sequential)

### Scenario 2: Max Workers = 3

**3 requests come simultaneously:**

```
Time 0:00 - Request 1 → Worker 1 (processing)
Time 0:00 - Request 2 → Worker 2 (processing)
Time 0:00 - Request 3 → Worker 3 (processing)
Time 5:00 - All 3 done simultaneously
```

**Total time:** 5 minutes (parallel)

---

## 🔧 Solution Implemented: Async Processing

I've updated the code to support **both sync and async modes**.

### How It Works Now:

**Synchronous Mode (Default):**
```bash
POST /api/reels/
# Waits 5-10 minutes, returns complete result
```

**Async Mode (Non-Blocking):**
```bash
POST /api/reels/?async=true
# Returns immediately with job ID
# Process continues in background
# Poll GET /api/reels/<id>/ for status
```

---

## 📊 Concurrent Request Handling

### With Async Mode Enabled:

**2 requests come simultaneously:**

```
Time 0:00 - Request 1 → Django creates job, starts background thread, returns immediately
Time 0:00 - Request 2 → Django creates job, starts background thread, returns immediately
Time 0:01 - Both users have job IDs, can poll for status

Background:
Time 0:00 - Request 1 thread → Calls Runpod Worker 1
Time 0:00 - Request 2 thread → Calls Runpod Worker 2 (if Max Workers > 1)
Time 5:00 - Both complete, status updates in database
```

**User Experience:**
- Gets response in < 1 second
- Polls for status every few seconds
- Gets result when ready

### With Sync Mode (Current Default):

**2 requests come simultaneously:**

```
Time 0:00 - Request 1 → Django waits for Runpod (5-10 min)
Time 0:00 - Request 2 → Django waits (queued behind Request 1)
Time 5:00 - Request 1 → Returns
Time 5:00 - Request 2 → Starts processing
Time 10:00 - Request 2 → Returns
```

**User Experience:**
- Waits 5-10 minutes for response
- Gets complete result immediately

---

## ⚙️ Configuration

### Enable Async Mode by Default:

**In `reel_platform/settings.py`:**
```python
# Async processing (returns immediately, processes in background)
ASYNC_PROCESSING = os.getenv('ASYNC_PROCESSING', 'true').lower() == 'true'
```

**In `.env`:**
```env
ASYNC_PROCESSING=true
```

### Runpod Max Workers:

**In Runpod Serverless Dashboard:**
- Set **Max Workers** to 3-5 (depending on your needs)
- More workers = more concurrent processing
- Cost: You pay for each worker when processing

---

## 🎯 Recommended Setup

### For Production:

1. **Enable Async Mode:**
   ```env
   ASYNC_PROCESSING=true
   ```

2. **Set Runpod Max Workers:**
   - Start with 2-3 workers
   - Monitor usage and adjust

3. **Django WSGI Server:**
   - Use Gunicorn with multiple workers:
     ```bash
     gunicorn --workers 4 reel_platform.wsgi:application
     ```

### For Development:

- Use sync mode (simpler to test)
- Set Runpod Max Workers = 1

---

## 📈 Performance Comparison

### Sync Mode:
- **Concurrent Requests:** Handled sequentially
- **Response Time:** 5-10 minutes per request
- **Django Blocks:** Yes (waits for Runpod)
- **User Experience:** Waits for complete result

### Async Mode:
- **Concurrent Requests:** All handled immediately
- **Response Time:** < 1 second (returns job ID)
- **Django Blocks:** No (background processing)
- **User Experience:** Gets job ID, polls for status

---

## 🔄 Request Flow (Async Mode)

```
Client → POST /api/reels/?async=true
  ↓
Django → Creates ReelJob (status: "pending")
  ↓
Django → Starts background thread
  ↓
Django → Returns 202 Accepted with job ID (< 1 second)
  ↓
Background Thread → Calls Runpod Serverless
  ↓
Runpod → Processes (5-10 minutes)
  ↓
Background Thread → Updates ReelJob (status: "done")
  ↓
Client → Polls GET /api/reels/<id>/
  ↓
Django → Returns status and video URL
```

---

## 💡 Best Practices

1. **Use Async Mode** for production (better UX)
2. **Set Runpod Max Workers** based on expected load
3. **Monitor Runpod costs** (more workers = more cost)
4. **Implement polling** in your frontend/client
5. **Set reasonable timeouts** (10 minutes for video generation)

---

## 🚨 Important Notes

### Django Threading:
- Uses Python `threading` module
- Each request spawns a background thread
- Threads are daemon threads (die when Django stops)
- **For production:** Consider Celery instead

### Runpod Concurrency:
- Max Workers controls how many requests Runpod processes simultaneously
- More workers = faster processing of multiple requests
- But also = higher cost

### Database:
- Each ReelJob is independent
- No conflicts when processing concurrently
- Status field tracks progress

---

## ✅ Summary

**With current implementation:**

✅ **Sync Mode:** Works, but blocks Django  
✅ **Async Mode:** Returns immediately, processes in background  
✅ **Runpod:** Handles concurrent requests based on Max Workers  
✅ **Multiple Requests:** All handled, each gets own job ID

**Recommendation:** Use async mode + Runpod Max Workers = 3-5

