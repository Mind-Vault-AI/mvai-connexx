# MVAI Connexx - Fix Corrupted Files on Windows
# This script resets files to match the repository

Write-Host "=== FIXING CORRUPTED FILES ===" -ForegroundColor Yellow
Write-Host ""

# Check if in git repository
if (-not (Test-Path ".git")) {
    Write-Host "ERROR: Not in mvai-connexx directory!" -ForegroundColor Red
    Write-Host "Run this from: C:\Users\erik_\Documents\mvai-connexx" -ForegroundColor Yellow
    exit 1
}

Write-Host "1. Checking Git status..." -ForegroundColor Cyan
git status --short

Write-Host ""
Write-Host "2. Resetting corrupted files from repository..." -ForegroundColor Cyan

# Reset specific files that are causing issues
Write-Host "   - Resetting api.py..." -ForegroundColor Gray
git checkout HEAD -- api.py

Write-Host "   - Recreating .env (not in git)..." -ForegroundColor Gray
# .env is git-ignored, so recreate it from scratch
@"
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
"@ | Out-File -FilePath ".env" -Encoding utf8 -NoNewline

Write-Host "   - Resetting database.py..." -ForegroundColor Gray
git checkout HEAD -- database.py

Write-Host ""
Write-Host "3. Verifying files..." -ForegroundColor Cyan

# Check api.py first line
$apiFirstLine = Get-Content api.py -First 1
if ($apiFirstLine -eq '"""') {
    Write-Host "   ✓ api.py: FIXED" -ForegroundColor Green
} else {
    Write-Host "   ✗ api.py: STILL BROKEN (first line: $apiFirstLine)" -ForegroundColor Red
}

# Check .env exists and has OPENAI_API_KEY
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "OPENAI_API_KEY") {
        Write-Host "   ✓ .env: FIXED" -ForegroundColor Green
    } else {
        Write-Host "   ✗ .env: Missing OPENAI_API_KEY" -ForegroundColor Red
    }
} else {
    Write-Host "   ✗ .env: FILE MISSING" -ForegroundColor Red
}

Write-Host ""
Write-Host "4. Testing Python imports..." -ForegroundColor Cyan

$testResult = python -c "import api; print('OK')" 2>&1

if ($testResult -match "OK") {
    Write-Host "   ✓ Python imports: WORKING" -ForegroundColor Green
} else {
    Write-Host "   ✗ Python imports: FAILED" -ForegroundColor Red
    Write-Host "   Error: $testResult" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== FIX COMPLETE ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next step: python app.py" -ForegroundColor Cyan
Write-Host ""
