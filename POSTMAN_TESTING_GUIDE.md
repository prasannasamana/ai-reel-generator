# Postman API Testing Guide 🚀

Complete guide for testing the AI Reel Generator API using Postman.

---

## 📋 Prerequisites

1. **Django Server Running:**
   ```bash
   python manage.py runserver
   ```
   Server should be running at: `http://localhost:8000`

2. **Postman Installed:** Download from [postman.com](https://www.postman.com/downloads/)

3. **Test Image:** Have a face image ready (`.jpg` or `.png`)

---

## 🔧 Postman Setup

### 1. Create a New Collection

1. Open Postman
2. Click **"New"** → **"Collection"**
3. Name it: **"AI Reel Generator API"**
4. Click **"Create"**

### 2. Set Collection Variables (Optional but Recommended)

1. Click on your collection
2. Go to **"Variables"** tab
3. Add these variables:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | `http://localhost:8000` | `http://localhost:8000` |
| `reel_id` | (leave empty) | (will be set automatically) |

**Usage:** Use `{{base_url}}` in requests instead of typing the full URL.

---

## 📝 API Endpoints

### 1. Get API Info

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/`
- **Headers:** None required

**Expected Response:**
```json
{
  "name": "AI Reel Generator API",
  "version": "1.0.0",
  "endpoints": {...},
  "workflow": {...}
}
```

**Postman Steps:**
1. Click **"New"** → **"HTTP Request"**
2. Set method to **GET**
3. Enter URL: `http://localhost:8000/api/`
4. Click **"Send"**

---

### 2. Create Reel (Step 1)

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/reels/`
- **Body Type:** `form-data`
- **Body Fields:**
  - `image` (File) - Select your image file
  - `script` (Text) - Your original script text
  - `tone` (Text) - `neutral`, `friendly`, `formal`, `energetic`, or `dramatic`
  - `use_rewrite` (Text) - `true` or `false`
  - `max_seconds` (Text, optional) - Target length in seconds (e.g., `30`)

**Example:**
```
image: [Select File] face.jpg
script: Hello everyone! Welcome to my channel. Today I'm going to share something amazing with you.
tone: friendly
use_rewrite: true
max_seconds: 30
```

**Expected Response:**
```json
{
  "id": "f6c79711-9e03-444d-a7b6-07916891fa69",
  "status": "script_pending_approval",
  "original_script": "Hello everyone! Welcome to my channel...",
  "final_script": "Hey there! Welcome to my channel. Today, I'm excited to share something amazing with you!",
  "script_approved": false,
  "tone": "friendly",
  "image_url": "http://localhost:8000/media/reels/images/face.jpg",
  "audio_url": null,
  "video_url": null,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:05Z",
  "error_message": null
}
```

**Postman Steps:**
1. Create new request: **POST** `{{base_url}}/api/reels/`
2. Go to **"Body"** tab
3. Select **"form-data"**
4. Add fields:
   - Key: `image`, Type: **File**, Value: [Click "Select Files" and choose your image]
   - Key: `script`, Type: **Text**, Value: `Hello everyone! Welcome to my channel.`
   - Key: `tone`, Type: **Text**, Value: `friendly`
   - Key: `use_rewrite`, Type: **Text**, Value: `true`
   - Key: `max_seconds`, Type: **Text**, Value: `30`
5. Click **"Send"**
6. **Copy the `id` from response** - you'll need it for next requests!

**Save Reel ID:**
- Copy the `id` from the response
- Update collection variable `reel_id` with this value
- Or manually copy it for the next requests

---

### 3. Get Reel Details

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/reels/{{reel_id}}/`
- **Headers:** None required

**Example URL:**
```
http://localhost:8000/api/reels/f6c79711-9e03-444d-a7b6-07916891fa69/
```

**Expected Response:**
```json
{
  "id": "f6c79711-9e03-444d-a7b6-07916891fa69",
  "status": "script_pending_approval",
  "original_script": "...",
  "final_script": "...",
  "script_approved": false,
  ...
}
```

**Postman Steps:**
1. Create new request: **GET** `{{base_url}}/api/reels/{{reel_id}}/`
2. Replace `{{reel_id}}` with actual ID from Step 2
3. Click **"Send"**

---

### 4. Regenerate Script (Optional - Step 2)

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/reels/{{reel_id}}/regenerate-script/`
- **Body Type:** `raw` → `JSON`
- **Body:**
```json
{
  "tone": "energetic",
  "max_seconds": 45
}
```

**Note:** Both fields are optional. Omit fields you don't want to change.

**Expected Response:**
```json
{
  "id": "...",
  "status": "script_pending_approval",
  "final_script": "New rewritten version with energetic tone...",
  "script_approved": false,
  "message": "Script regenerated. Review and approve when ready."
}
```

**Postman Steps:**
1. Create new request: **POST** `{{base_url}}/api/reels/{{reel_id}}/regenerate-script/`
2. Go to **"Body"** tab
3. Select **"raw"** → **"JSON"**
4. Paste JSON body (optional fields)
5. Click **"Send"**

**You can call this multiple times** until you're satisfied with the script!

---

### 5. Approve Script & Generate Video (Step 3)

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/reels/{{reel_id}}/approve-script/`
- **Body Type:** `raw` → `JSON` (optional)
- **Body (optional):**
```json
{
  "async": false
}
```

**Expected Response (Synchronous):**
```json
{
  "id": "...",
  "status": "processing",
  "script_approved": true,
  ...
}
```

**Expected Response (Async):**
```json
{
  "id": "...",
  "status": "script_approved",
  "script_approved": true,
  "message": "Script approved. Video generation started. Poll /api/reels/<id>/ for status."
}
```

**Postman Steps:**
1. Create new request: **POST** `{{base_url}}/api/reels/{{reel_id}}/approve-script/`
2. (Optional) Add JSON body with `{"async": false}`
3. Click **"Send"**

**Note:** If `USE_RUNPOD=false` or Runpod not configured, video generation will fail. That's expected for local testing without Runpod.

---

### 6. Check Video Status

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/reels/{{reel_id}}/`

**Expected Response (When Done):**
```json
{
  "id": "...",
  "status": "done",
  "script_approved": true,
  "final_script": "...",
  "video_url": "http://localhost:8000/media/reels/f6c79711-9e03-444d-a7b6-07916891fa69/video.mp4",
  "audio_url": "http://localhost:8000/media/reels/f6c79711-9e03-444d-a7b6-07916891fa69/audio.mp3",
  ...
}
```

**Postman Steps:**
1. Use the same request from Step 3 (Get Reel Details)
2. Click **"Send"** repeatedly to poll status
3. When `status` is `"done"`, video is ready!

---

### 7. List All Reels

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/reels/`
- **Query Parameters (optional):**
  - `status` - Filter by status (e.g., `?status=done`)
  - `page` - Page number (e.g., `?page=1`)
  - `page_size` - Items per page (e.g., `?page_size=10`)

**Example:**
```
http://localhost:8000/api/reels/?status=done&page=1
```

**Expected Response:**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/reels/?page=2",
  "previous": null,
  "results": [
    {
      "id": "...",
      "status": "done",
      ...
    },
    ...
  ]
}
```

**Postman Steps:**
1. Create new request: **GET** `{{base_url}}/api/reels/`
2. (Optional) Add query params in **"Params"** tab
3. Click **"Send"**

---

### 8. Delete Reel

**Request:**
- **Method:** `DELETE`
- **URL:** `{{base_url}}/api/reels/{{reel_id}}/`

**Expected Response:**
```json
{
  "message": "Reel deleted successfully"
}
```

**Postman Steps:**
1. Create new request: **DELETE** `{{base_url}}/api/reels/{{reel_id}}/`
2. Click **"Send"**

---

## 🔄 Complete Workflow Example

### Step-by-Step in Postman:

1. **Get API Info**
   - `GET {{base_url}}/api/`
   - Verify API is working

2. **Create Reel**
   - `POST {{base_url}}/api/reels/`
   - Upload image, add script
   - **Copy the `id` from response**

3. **Review Script**
   - `GET {{base_url}}/api/reels/{{reel_id}}/`
   - Check `final_script` field

4. **Regenerate (if not satisfied)**
   - `POST {{base_url}}/api/reels/{{reel_id}}/regenerate-script/`
   - Change tone or other parameters
   - Repeat until satisfied

5. **Approve & Generate Video**
   - `POST {{base_url}}/api/reels/{{reel_id}}/approve-script/`
   - Video generation starts

6. **Poll for Completion**
   - `GET {{base_url}}/api/reels/{{reel_id}}/`
   - Check `status` field
   - When `status == "done"`, get `video_url`

---

## 📸 Postman Screenshots Guide

### Creating a Request with Form Data:

1. **Method & URL:**
   ```
   POST http://localhost:8000/api/reels/
   ```

2. **Body Tab:**
   - Select **"form-data"**
   - Add fields:
     ```
     image: [File] [Select Files]
     script: [Text] Your script here
     tone: [Text] friendly
     use_rewrite: [Text] true
     ```

3. **Send Button:**
   - Click **"Send"**
   - View response in bottom panel

### Creating a JSON Request:

1. **Method & URL:**
   ```
   POST http://localhost:8000/api/reels/{{reel_id}}/regenerate-script/
   ```

2. **Body Tab:**
   - Select **"raw"**
   - Select **"JSON"** from dropdown
   - Paste JSON:
     ```json
     {
       "tone": "energetic"
     }
     ```

3. **Headers:**
   - Postman automatically adds `Content-Type: application/json`

---

## 🎯 Postman Collection JSON

You can import this collection directly into Postman:

**Save as:** `AI_Reel_Generator.postman_collection.json`

```json
{
  "info": {
    "name": "AI Reel Generator API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000",
      "type": "string"
    },
    {
      "key": "reel_id",
      "value": "",
      "type": "string"
    }
  ],
  "item": [
    {
      "name": "1. Get API Info",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/api/",
          "host": ["{{base_url}}"],
          "path": ["api", ""]
        }
      }
    },
    {
      "name": "2. Create Reel",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "image",
              "type": "file",
              "src": []
            },
            {
              "key": "script",
              "type": "text",
              "value": "Hello everyone! Welcome to my channel."
            },
            {
              "key": "tone",
              "type": "text",
              "value": "friendly"
            },
            {
              "key": "use_rewrite",
              "type": "text",
              "value": "true"
            }
          ]
        },
        "url": {
          "raw": "{{base_url}}/api/reels/",
          "host": ["{{base_url}}"],
          "path": ["api", "reels", ""]
        }
      }
    },
    {
      "name": "3. Get Reel Details",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/api/reels/{{reel_id}}/",
          "host": ["{{base_url}}"],
          "path": ["api", "reels", "{{reel_id}}", ""]
        }
      }
    },
    {
      "name": "4. Regenerate Script",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"tone\": \"energetic\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/reels/{{reel_id}}/regenerate-script/",
          "host": ["{{base_url}}"],
          "path": ["api", "reels", "{{reel_id}}", "regenerate-script", ""]
        }
      }
    },
    {
      "name": "5. Approve Script",
      "request": {
        "method": "POST",
        "header": [],
        "url": {
          "raw": "{{base_url}}/api/reels/{{reel_id}}/approve-script/",
          "host": ["{{base_url}}"],
          "path": ["api", "reels", "{{reel_id}}", "approve-script", ""]
        }
      }
    },
    {
      "name": "6. List All Reels",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/api/reels/",
          "host": ["{{base_url}}"],
          "path": ["api", "reels", ""]
        }
      }
    },
    {
      "name": "7. Delete Reel",
      "request": {
        "method": "DELETE",
        "header": [],
        "url": {
          "raw": "{{base_url}}/api/reels/{{reel_id}}/",
          "host": ["{{base_url}}"],
          "path": ["api", "reels", "{{reel_id}}", ""]
        }
      }
    }
  ]
}
```

**To Import:**
1. Open Postman
2. Click **"Import"**
3. Paste the JSON above or upload the file
4. Collection will be imported with all requests!

---

## ⚠️ Common Issues & Solutions

### Issue: "400 Bad Request" on Create Reel
**Solution:** Make sure:
- `image` field is set to **File** type (not Text)
- All required fields are filled
- Image file exists and is readable

### Issue: "404 Not Found" on Get Reel
**Solution:** 
- Check that `reel_id` is correct
- Make sure you copied the full UUID from create response

### Issue: "500 Internal Server Error"
**Solution:**
- Check Django server logs
- Verify `.env` file has `OPENAI_API_KEY` set
- Check that server is running

### Issue: Video Generation Fails
**Solution:**
- This is expected if `USE_RUNPOD=false` or Runpod not configured
- Script rewriting should still work
- Set up Runpod Serverless for video generation (see `SERVERLESS_DEPLOYMENT.md`)

---

## 💡 Pro Tips

1. **Save Responses:** Click **"Save Response"** to save examples
2. **Tests Tab:** Add tests to automatically check response status
3. **Pre-request Scripts:** Use to set variables automatically
4. **Environments:** Create different environments (dev, prod)
5. **Collection Runner:** Run all requests in sequence

---

## 🎉 You're Ready!

Start testing your API with Postman. The script rewriting workflow should work perfectly even without Runpod configured!

Happy Testing! 🚀

