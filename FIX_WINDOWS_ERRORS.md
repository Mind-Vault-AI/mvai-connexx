# 🔧 Fix Windows File Corruption Errors

## Problem

After `git pull`, you encountered two errors:
1. **api.py syntax error:** `h"""` instead of `"""`
2. **.env parsing error:** Line 9 parsing issue

These errors are caused by Git file corruption during pull on Windows (line ending or encoding issues).

## Solution

### Step 1: Pull the Fix Script

```powershell
cd C:\Users\erik_\Documents\mvai-connexx
git pull origin claude/mvai-connexx-multi-tenant-upgrade-8eDvw
```

This downloads `fix_windows_files.ps1`.

### Step 2: Add Your OpenAI API Key to Fix Script

**IMPORTANT:** Before running the script, you need to add your OpenAI API key.

Open `fix_windows_files.ps1` in Notepad and find line 33:

```powershell
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
```

Replace `YOUR_OPENAI_API_KEY_HERE` with your actual key (starts with `sk-proj-...`)

Save and close Notepad.

### Step 3: Run the Fix Script

```powershell
cd C:\Users\erik_\Documents\mvai-connexx
.\fix_windows_files.ps1
```

**Expected output:**
```
=== FIXING CORRUPTED FILES ===

1. Checking Git status...
   (shows any modified files)

2. Resetting corrupted files from repository...
   - Resetting api.py...
   - Recreating .env (not in git)...
   - Resetting database.py...

3. Verifying files...
   ✓ api.py: FIXED
   ✓ .env: FIXED

4. Testing Python imports...
   ✓ Python imports: WORKING

=== FIX COMPLETE ===

Next step: python app.py
```

### Step 4: Test Flask App

```powershell
python app.py
```

**Expected output:**
```
2026-02-03 22:45:12,345 - mvai-connexx - INFO - Starting MVAI Connexx v2.0
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

✅ **If you see this:** App is running! Open http://localhost:5000 in browser.

❌ **If you see errors:** Copy the full error message and share it.

## Alternative: Manual Fix

If the script doesn't work, manually fix the files:

### Fix api.py

```powershell
# Reset api.py from git
git checkout HEAD -- api.py
```

### Fix database.py

```powershell
# Reset database.py from git
git checkout HEAD -- database.py
```

### Fix .env

Delete the corrupted .env and create new one:

```powershell
# Delete old .env
Remove-Item .env

# Create new .env with Notepad
notepad .env
```

Paste this into Notepad:

```
# MVAI Connexx - Local Environment Configuration
# ⚠️ THIS FILE IS GIT-IGNORED - NEVER COMMIT TO VERSION CONTROL!

# ═══════════════════════════════════════════════════════
# OPENAI API KEY (ACTIEF)
# ═══════════════════════════════════════════════════════
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
OPENAI_MODEL=gpt-4-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7

# ═══════════════════════════════════════════════════════
# FLASK
# ═══════════════════════════════════════════════════════
SECRET_KEY=dev-secret-key-for-local-testing-change-in-production
FLASK_ENV=development
SESSION_LIFETIME_HOURS=24

# ═══════════════════════════════════════════════════════
# FEATURES
# ═══════════════════════════════════════════════════════
ENABLE_AI_ASSISTANT=true
ENABLE_DEMO_MODE=true

# ═══════════════════════════════════════════════════════
# PAYMENTS
# ═══════════════════════════════════════════════════════
PAYMENT_PROVIDER=gumroad

# ═══════════════════════════════════════════════════════
# SECURITY (Development Mode - Relaxed)
# ═══════════════════════════════════════════════════════
ENABLE_IP_WHITELIST=false
RATELIMIT_ENABLED=false
ENABLE_THREAT_DETECTION=true
```

Save as `UTF-8` encoding (Notepad default) and close.

### Test

```powershell
python app.py
```

## Why This Happened

Git on Windows sometimes corrupts files during pull when:
1. **Line endings** differ (Windows CRLF vs Linux LF)
2. **Encoding** changes (UTF-8 with BOM vs without)
3. **Merge conflicts** aren't properly resolved

The fix script resets files to match the repository exactly.

## Prevention

To prevent this in the future, configure Git properly on Windows:

```powershell
# Set line ending handling
git config --global core.autocrlf false

# Set default merge strategy
git config --global pull.rebase false
```

## Next Steps After Fix

1. ✅ **Test Flask app locally:** `python app.py`
2. ✅ **Test OpenAI integration:** Open http://localhost:5000/customer/ai
3. ✅ **Deploy to Hostinger:** SSH and `git pull` on VPS
4. ✅ **Build Android app:** Create keystore and build APK

---

**🎯 DOEL:** Werkende Flask app lokaal, dan Hostinger deployment, dan Google Play upload!
