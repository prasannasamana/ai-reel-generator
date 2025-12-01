# Fix GitHub Credentials Issue

## Problem
Git is using cached credentials for `prasannasamana` instead of `prasanna7189`.

## Solution: Clear Cached Credentials

### Method 1: Windows Credential Manager (Easiest)

1. **Press `Windows Key + R`**
2. **Type:** `control` and press Enter
3. **Click "Credential Manager"** (or search for it)
4. **Click "Windows Credentials"**
5. **Find entries** starting with `git:https://github.com`
6. **Click on each one** → Click "Remove"
7. **Remove all GitHub-related credentials**

### Method 2: Using Command Line

**Run these commands in your terminal:**

```bash
# Clear Git credential cache
git credential-manager-core erase
```

**When prompted, type:**
```
protocol=https
host=github.com
```

**Press Enter twice**

### Method 3: Update Remote URL with Username

**Update the remote URL to include your username:**

```bash
git remote set-url origin https://prasanna7189@github.com/prasanna7189/ai-reel-generator.git
```

**Then push:**
```bash
git push -u origin main
```

**When asked for password:** Use your Personal Access Token (not GitHub password)

---

## Create Personal Access Token

**If you don't have a token yet:**

1. **Go to:** https://github.com/settings/tokens
2. **Click:** "Generate new token" → "Generate new token (classic)"
3. **Name:** "Local Git Access"
4. **Expiration:** 90 days (or No expiration)
5. **Select scopes:** Check **"repo"** (full repository access)
6. **Click:** "Generate token"
7. **COPY THE TOKEN** (you won't see it again!)
8. **Use this token** as your password when Git asks

---

## After Clearing Credentials

**Try pushing again:**

```bash
git push -u origin main
```

**Enter:**
- Username: `prasanna7189`
- Password: Your Personal Access Token

---

## Alternative: Use SSH Instead

**If HTTPS keeps having issues, use SSH:**

1. **Generate SSH key** (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "prasannawork89@gmail.com"
   ```
   (Press Enter for all prompts)

2. **Copy your public key:**
   ```bash
   type %USERPROFILE%\.ssh\id_ed25519.pub
   ```
   Copy the output

3. **Add to GitHub:**
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste your key
   - Save

4. **Change remote to SSH:**
   ```bash
   git remote set-url origin git@github.com:prasanna7189/ai-reel-generator.git
   ```

5. **Push:**
   ```bash
   git push -u origin main
   ```

