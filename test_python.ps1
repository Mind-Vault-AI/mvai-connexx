# MVAI Connexx - Windows Python Test Script
# Check Python + Dependencies

Write-Host "=== MVAI CONNEXX PYTHON CHECK ===" -ForegroundColor Green
Write-Host ""

# Check Python version
Write-Host "1. Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   Found: $pythonVersion" -ForegroundColor Green

    # Check if Python 3.9+
    if ($pythonVersion -match "Python 3\.(\d+)") {
        $minorVersion = [int]$matches[1]
        if ($minorVersion -lt 9) {
            Write-Host "   WARNING: Python 3.9+ required!" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "   ERROR: Python not found!" -ForegroundColor Red
    Write-Host "   Download: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit
}

Write-Host ""

# Check pip
Write-Host "2. Checking pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "   Found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "   ERROR: pip not found!" -ForegroundColor Red
    exit
}

Write-Host ""

# Check .env file
Write-Host "3. Checking .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   Found: .env" -ForegroundColor Green

    # Check for OpenAI key
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "OPENAI_API_KEY=sk-proj-") {
        Write-Host "   OpenAI API Key: CONFIGURED" -ForegroundColor Green
    } else {
        Write-Host "   WARNING: OpenAI API Key missing or invalid!" -ForegroundColor Red
    }
} else {
    Write-Host "   ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "   Creating .env file..." -ForegroundColor Yellow

    @"
# MVAI Connexx - Environment Configuration
# ⚠️ IMPORTANT: Replace with your actual OpenAI API key!
# Get your key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE_REPLACE_THIS
OPENAI_MODEL=gpt-4-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
ENABLE_AI_ASSISTANT=true
PAYMENT_PROVIDER=gumroad
"@ | Out-File -FilePath ".env" -Encoding utf8

    Write-Host "   Created .env file with OpenAI key" -ForegroundColor Green
}

Write-Host ""

# Install dependencies
Write-Host "4. Installing dependencies..." -ForegroundColor Yellow
Write-Host "   This may take 1-2 minutes..." -ForegroundColor Gray

try {
    pip install -r requirements.txt --quiet 2>&1 | Out-Null
    Write-Host "   Dependencies installed!" -ForegroundColor Green
} catch {
    Write-Host "   ERROR installing dependencies!" -ForegroundColor Red
    Write-Host "   Run manually: pip install -r requirements.txt" -ForegroundColor Yellow
}

Write-Host ""

# Test OpenAI import
Write-Host "5. Testing OpenAI library..." -ForegroundColor Yellow
$testResult = python -c "from openai import OpenAI; print('OK')" 2>&1

if ($testResult -match "OK") {
    Write-Host "   OpenAI library: WORKING" -ForegroundColor Green
} else {
    Write-Host "   ERROR: OpenAI library not working!" -ForegroundColor Red
    Write-Host "   Installing openai..." -ForegroundColor Yellow
    pip install openai
}

Write-Host ""
Write-Host "=== CHECK COMPLETE ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next step: python app.py" -ForegroundColor Cyan
