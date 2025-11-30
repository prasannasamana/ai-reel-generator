# GitHub Setup - Common Errors & Solutions

## 🔍 Quick Error Finder

**Find your error below and follow the solution:**

---

## Error 1: "fatal: not a git repository"

**What you see:**
```
fatal: not a git repository (or any of the parent directories): .git
```

**Solution:**
```bash
git init
```

**Then continue with:**
```bash
git add .
git commit -m "Initial commit"
```

---

## Error 2: "Please tell me who you are"

**What you see:**
```
*** Please tell me who you are.
Run
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
```

**Solution:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Then try commit again:**
```bash
git commit -m "Initial commit: AI Reel Generator API"
```

---

## Error 3: "remote origin already exists"

**What you see:**
```
fatal: remote origin already exists.
```

**Solution:**

**Option A: Remove and re-add:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/ai-reel-generator.git
```

**Option B: Update existing remote:**
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/ai-reel-generator.git
```

---

## Error 4: "Authentication failed" or "Permission denied"

**What you see:**
```
remote: Support for password authentication was removed on August 13, 2021.
remote: Please use a personal access token instead.
```

**OR:**
```
fatal: Authentication failed
```

**Solution:**

1. **Create Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: "Local Git Access"
   - Expiration: 90 days (or No expiration)
   - Check **"repo"** scope
   - Click "Generate token"
   - **COPY THE TOKEN** (you won't see it again!)

2. **Use token as password:**
   ```bash
   git push -u origin main
   ```
   - Username: Your GitHub username
   - Password: **Paste the token** (not your GitHub password!)

---

## Error 5: "Repository not found"

**What you see:**
```
remote: Repository not found.
fatal: repository 'https://github.com/USERNAME/repo.git/' not found
```

**Solution:**

1. **Check repository name is correct:**
   - Go to GitHub.com
   - Check your repository name exactly
   - Make sure it matches: `ai-reel-generator` (or whatever you named it)

2. **Check repository exists:**
   - Make sure you created it on GitHub first
   - Check if it's Private (you need to be logged in)

3. **Update remote URL:**
   ```bash
   git remote set-url origin https://github.com/YOUR_USERNAME/ai-reel-generator.git
   ```

---

## Error 6: "failed to push some refs"

**What you see:**
```
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/...'
```

**Solution:**

**Option A: Pull first (if repository has files):**
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

**Option B: Force push (if you're sure - be careful!):**
```bash
git push -u origin main --force
```

**⚠️ Warning:** Only use `--force` if you're sure you want to overwrite remote files!

---

## Error 7: "branch 'main' does not exist"

**What you see:**
```
error: src refspec main does not exist.
```

**Solution:**

**Check current branch:**
```bash
git branch
```

**If you see `master` instead of `main`:**

**Option A: Rename branch:**
```bash
git branch -M main
git push -u origin main
```

**Option B: Use master:**
```bash
git push -u origin master
```

---

## Error 8: "nothing to commit"

**What you see:**
```
On branch main
nothing to commit, working tree clean
```

**This is NOT an error!** It means all files are already committed.

**Solution:**
- If you want to push: `git push -u origin main`
- If you made changes: `git add .` then `git commit -m "message"`

---

## Error 9: "Large files" or "file too large"

**What you see:**
```
remote: error: File media/reels/.../video.mp4 is 1024.00 MB; this exceeds GitHub's file size limit of 100.00 MB
```

**Solution:**

**Your `.gitignore` should already exclude `/media` folder!**

**If files are already tracked:**
```bash
git rm --cached -r media/
git commit -m "Remove media files"
git push -u origin main
```

**Verify `.gitignore` has:**
```
/media
```

---

## Error 10: "SSL certificate problem" (Windows)

**What you see:**
```
SSL certificate problem: unable to get local issuer certificate
```

**Solution:**

```bash
git config --global http.sslVerify false
```

**Then try push again:**
```bash
git push -u origin main
```

---

## Error 11: "Connection timeout"

**What you see:**
```
fatal: unable to access 'https://github.com/...': Failed to connect to github.com port 443: Timed out
```

**Solution:**

1. **Check internet connection**
2. **Try using SSH instead:**
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/ai-reel-generator.git
   ```
3. **Or try again later** (GitHub might be down)

---

## Error 12: "Command not found: git"

**What you see:**
```
'git' is not recognized as an internal or external command
```

**Solution:**

**Install Git:**
1. Download from: https://git-scm.com/download/win
2. Install with default settings
3. Restart Command Prompt/PowerShell
4. Try again

---

## ✅ Step-by-Step Checklist

**If you're stuck, follow this order:**

1. **Check you're in the right folder:**
   ```bash
   cd "C:\Users\prasa\Desktop\Yellas Tech Work\Madhu_sir_works\AI_ReelMaker"
   dir
   ```
   Should see: `Dockerfile`, `manage.py`, etc.

2. **Initialize Git:**
   ```bash
   git init
   ```

3. **Configure Git (if not done):**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

4. **Add files:**
   ```bash
   git add .
   ```

5. **Commit:**
   ```bash
   git commit -m "Initial commit: AI Reel Generator API"
   ```

6. **Add remote:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ai-reel-generator.git
   ```

7. **Rename branch:**
   ```bash
   git branch -M main
   ```

8. **Push:**
   ```bash
   git push -u origin main
   ```
   - Use Personal Access Token as password (not GitHub password!)

---

## 🆘 Still Stuck?

**Share these details:**

1. **What command did you run?**
2. **What's the exact error message?** (copy/paste)
3. **What step are you on?** (from GITHUB_SETUP.md)

**Common things to check:**
- ✅ Repository exists on GitHub
- ✅ Repository name matches exactly
- ✅ Using Personal Access Token (not password)
- ✅ Internet connection is working
- ✅ Git is installed (`git --version`)

---

## Quick Test Commands

**Test Git is installed:**
```bash
git --version
```

**Test you're in right folder:**
```bash
pwd
dir
```

**Test remote is set:**
```bash
git remote -v
```

**Test files are staged:**
```bash
git status
```

**Test you have commits:**
```bash
git log
```

