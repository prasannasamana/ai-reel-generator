# GitHub Setup Guide - Step by Step

## 📋 Overview

This guide will help you create a GitHub repository and push your existing `AI_ReelMaker` code to it.

---

## Part 1: Create GitHub Repository

### Step 1.1: Go to GitHub Website

1. **Open your browser**
2. **Go to:** https://github.com
3. **Login** to your GitHub account (or sign up if you don't have one)

### Step 1.2: Create New Repository

1. **Click the "+" icon** (top right corner, next to your profile picture)
2. **Click "New repository"** from the dropdown menu

### Step 1.3: Fill Repository Details

**Repository name:**
- Type: `ai-reel-generator`
- (Or any name you prefer, but keep it simple - no spaces, use hyphens)

**Description (optional):**
- Type: `AI Reel Generator - Django API for generating talking-head videos using SadTalker and OpenAI`
- (This helps others understand what your project does)

**Visibility:**
- ✅ **Choose "Public"** (recommended - free, others can see your code)
- OR **Choose "Private"** (only you can see it - if you want to keep it secret)

**Why Public?**
- Free
- Easy to share
- Can be used in portfolio
- Easier for collaboration

**Why Private?**
- Keep code secret
- Hide from public
- More control

**👉 RECOMMENDATION: Choose "Public"** (unless you have sensitive code)

### Step 1.4: Initialize Repository Options

**IMPORTANT:** Do NOT check any of these boxes:
- ❌ **DO NOT** check "Add a README file" (you already have one)
- ❌ **DO NOT** check "Add .gitignore" (you already have one)
- ❌ **DO NOT** check "Choose a license" (we'll add it manually)

**Why?** Because you already have these files in your local project!

### Step 1.5: Choose License

**Scroll down to "License" dropdown:**

**Recommended: MIT License** (most common, permissive)
- Click dropdown
- Select **"MIT License"**
- This allows others to use your code freely

**Other options:**
- **Apache License 2.0** - Similar to MIT, more legal protection
- **GPL-3.0** - Requires others to open-source their changes
- **No License** - Others can't legally use your code

**👉 RECOMMENDATION: Choose "MIT License"**

### Step 1.6: Create Repository

1. **Review your settings:**
   - Name: `ai-reel-generator`
   - Public/Private: (your choice)
   - License: MIT License
   - No README/gitignore checked

2. **Click green "Create repository" button**

3. **You'll see a page** with setup instructions - **DON'T follow those yet!** (They're for empty repos)

---

## Part 2: Push Your Existing Code

### Step 2.1: Open Command Prompt/PowerShell

**On your local computer:**

1. **Press `Windows Key + R`**
2. **Type:** `cmd` or `powershell`
3. **Press Enter**

**OR**

1. **Right-click** on your `AI_ReelMaker` folder
2. **Select "Open in Terminal"** or **"Open PowerShell window here"**

### Step 2.2: Navigate to Your Project

**In Command Prompt/PowerShell:**

```bash
cd "C:\Users\prasa\Desktop\Yellas Tech Work\Madhu_sir_works\AI_ReelMaker"
```

**Verify you're in the right place:**
```bash
dir
```

You should see: `Dockerfile`, `manage.py`, `requirements.txt`, etc.

### Step 2.3: Initialize Git (if not already done)

**Check if Git is initialized:**
```bash
dir .git
```

**If you see "Directory not found":**

```bash
git init
```

**If you see a `.git` folder, skip this step** (Git is already initialized)

### Step 2.4: Check Git Status

```bash
git status
```

**You should see** a list of files that are "untracked" or "modified"

### Step 2.5: Add All Files

```bash
git add .
```

**This adds all files** to Git's staging area

**Verify files are added:**
```bash
git status
```

**You should see** files listed as "Changes to be committed" (in green)

### Step 2.6: Create .gitignore (if not exists)

**Check if .gitignore exists:**
```bash
dir .gitignore
```

**If it doesn't exist**, create it:
```bash
notepad .gitignore
```

**Paste this content:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

**Save and close** Notepad

**Add .gitignore:**
```bash
git add .gitignore
```

### Step 2.7: Make Initial Commit

```bash
git commit -m "Initial commit: AI Reel Generator API"
```

**What this does:** Saves all your files to Git's history

**If you see an error** about name/email:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Then try commit again:
```bash
git commit -m "Initial commit: AI Reel Generator API"
```

### Step 2.8: Connect to GitHub Repository

**Replace `YOUR_USERNAME` with your actual GitHub username:**

```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-reel-generator.git
```

**Example:**
```bash
git remote add origin https://github.com/johnsmith/ai-reel-generator.git
```

**Verify connection:**
```bash
git remote -v
```

**You should see:**
```
origin  https://github.com/YOUR_USERNAME/ai-reel-generator.git (fetch)
origin  https://github.com/YOUR_USERNAME/ai-reel-generator.git (push)
```

### Step 2.9: Rename Branch to Main (if needed)

```bash
git branch -M main
```

**This ensures** your branch is named "main" (GitHub's default)

### Step 2.10: Push to GitHub

```bash
git push -u origin main
```

**What happens:**
- Git will ask for your GitHub credentials
- **Username:** Your GitHub username
- **Password:** You need a **Personal Access Token** (NOT your GitHub password!)

### Step 2.11: Create Personal Access Token (if needed)

**If Git asks for password and it doesn't work:**

1. **Go to GitHub.com**
2. **Click your profile picture** (top right)
3. **Click "Settings"**
4. **Scroll down** → Click **"Developer settings"** (left sidebar)
5. **Click "Personal access tokens"** → **"Tokens (classic)"**
6. **Click "Generate new token"** → **"Generate new token (classic)"**
7. **Note:** Give it a name like "Local Git Access"
8. **Expiration:** Choose "90 days" or "No expiration"
9. **Select scopes:** Check **"repo"** (this gives full repository access)
10. **Scroll down** → Click **"Generate token"**
11. **COPY THE TOKEN** (you won't see it again!)
12. **Use this token** as your password when Git asks

**Then try push again:**
```bash
git push -u origin main
```

**Enter:**
- Username: Your GitHub username
- Password: The Personal Access Token you just created

### Step 2.12: Verify Upload

**After successful push:**

1. **Go to GitHub.com**
2. **Navigate to your repository:** `https://github.com/YOUR_USERNAME/ai-reel-generator`
3. **You should see** all your files there!

**Files you should see:**
- ✅ `Dockerfile`
- ✅ `requirements.txt`
- ✅ `manage.py`
- ✅ `README.md`
- ✅ `reel_platform/` folder
- ✅ `reels/` folder
- ✅ etc.

---

## Part 3: Verify Everything is Correct

### Step 3.1: Check Repository Settings

**On GitHub:**

1. **Go to your repository**
2. **Click "Settings"** tab (top of repository page)
3. **Scroll down** → Check **"General"** settings:
   - ✅ Repository name is correct
   - ✅ Visibility is Public/Private (as you chose)
   - ✅ License shows "MIT License"

### Step 3.2: Check Files

**On GitHub:**

1. **Go to main page** of your repository
2. **Verify all files** are there
3. **Click on `README.md`** - should show your project documentation
4. **Click on `LICENSE`** - should show MIT License text

---

## Part 4: Future Updates

### How to Push Changes Later

**When you make changes to your code:**

1. **Navigate to project:**
   ```bash
   cd "C:\Users\prasa\Desktop\Yellas Tech Work\Madhu_sir_works\AI_ReelMaker"
   ```

2. **Check what changed:**
   ```bash
   git status
   ```

3. **Add changes:**
   ```bash
   git add .
   ```

4. **Commit:**
   ```bash
   git commit -m "Description of your changes"
   ```

5. **Push:**
   ```bash
   git push
   ```

---

## Troubleshooting

### Problem: "Repository not found"
**Solution:**
- Check repository name is correct
- Check your GitHub username is correct
- Make sure repository exists on GitHub

### Problem: "Authentication failed"
**Solution:**
- Use Personal Access Token (not password)
- Make sure token has "repo" scope
- Token might have expired - create new one

### Problem: "Permission denied"
**Solution:**
- Check you're using correct GitHub username
- Make sure repository exists
- Check if repository is private and you're logged in

### Problem: "Files not showing on GitHub"
**Solution:**
- Make sure you ran `git add .`
- Make sure you ran `git commit`
- Make sure you ran `git push`
- Refresh GitHub page

---

## Summary Checklist

- [ ] GitHub repository created
- [ ] Repository name: `ai-reel-generator`
- [ ] Visibility: Public or Private (chosen)
- [ ] License: MIT License (chosen)
- [ ] Git initialized locally
- [ ] Files added to Git
- [ ] Initial commit made
- [ ] Connected to GitHub remote
- [ ] Code pushed to GitHub
- [ ] Verified files on GitHub

---

## ✅ You're Done!

Your code is now on GitHub! You can:
- Share the repository URL
- Clone it on Runpod
- Collaborate with others
- Track changes

**Next Step:** Follow the `SERVERLESS_DEPLOYMENT.md` guide to deploy on Runpod!

---

## Quick Reference

**Repository URL:**
```
https://github.com/YOUR_USERNAME/ai-reel-generator
```

**Clone Command:**
```bash
git clone https://github.com/YOUR_USERNAME/ai-reel-generator.git
```

**Push Changes:**
```bash
git add .
git commit -m "Your message"
git push
```

