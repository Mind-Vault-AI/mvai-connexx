#!/bin/bash
# MVAI Connexx - Deployment Readiness Verification Script
# Checkt of alles 100% klaar is voor deployment

echo "🔍 MVAI Connexx - Deployment Readiness Check"
echo "=============================================="
echo ""

ERRORS=0

# Check 1: Required files
echo "📁 Checking required files..."
FILES=(
  "fly.toml"
  "render.yaml"
  "Dockerfile"
  "requirements.txt"
  ".gitignore"
  ".env.example"
  "app.py"
  "database.py"
  "seed_demo.py"
)

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "  ✅ $file"
  else
    echo "  ❌ $file MISSING!"
    ERRORS=$((ERRORS + 1))
  fi
done
echo ""

# Check 2: Python dependencies
echo "🐍 Checking Python installation..."
if command -v python3 &> /dev/null; then
  echo "  ✅ Python3 installed: $(python3 --version)"
else
  echo "  ❌ Python3 NOT installed!"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 3: Required Python packages
echo "📦 Checking Python packages..."
PACKAGES=("flask" "gunicorn")
for pkg in "${PACKAGES[@]}"; do
  if python3 -c "import $pkg" 2>/dev/null; then
    echo "  ✅ $pkg installed"
  else
    echo "  ⚠️  $pkg not installed (run: pip install -r requirements.txt)"
  fi
done
echo ""

# Check 4: fly.toml configuration
echo "⚙️  Checking fly.toml configuration..."
if grep -q "app = \"mvai-connexx\"" fly.toml 2>/dev/null; then
  echo "  ✅ App name correct"
else
  echo "  ❌ App name missing or incorrect in fly.toml"
  ERRORS=$((ERRORS + 1))
fi

if grep -q "primary_region = \"ams\"" fly.toml 2>/dev/null; then
  echo "  ✅ Region set to Amsterdam"
else
  echo "  ⚠️  Region not set to Amsterdam"
fi

if grep -q "mvai_data" fly.toml 2>/dev/null; then
  echo "  ✅ Persistent volume configured"
else
  echo "  ❌ Persistent volume NOT configured"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 5: Database
echo "💾 Checking database..."
if [ -f "mvai_connexx.db" ]; then
  SIZE=$(ls -lh mvai_connexx.db | awk '{print $5}')
  echo "  ✅ Database exists ($SIZE)"
  
  # Check if database has tables
  if command -v sqlite3 &> /dev/null; then
    TABLES=$(sqlite3 mvai_connexx.db ".tables" 2>/dev/null | wc -w)
    if [ "$TABLES" -gt 10 ]; then
      echo "  ✅ Database has $TABLES tables"
    else
      echo "  ⚠️  Database might be empty (only $TABLES tables)"
    fi
  fi
else
  echo "  ⚠️  Database not initialized yet (run: python seed_demo.py)"
fi
echo ""

# Check 6: Git status
echo "🔧 Checking Git status..."
if [ -d ".git" ]; then
  echo "  ✅ Git repository initialized"
  
  UNCOMMITTED=$(git status --porcelain | wc -l)
  if [ "$UNCOMMITTED" -eq 0 ]; then
    echo "  ✅ No uncommitted changes"
  else
    echo "  ⚠️  $UNCOMMITTED uncommitted changes"
  fi
  
  BRANCH=$(git branch --show-current)
  echo "  📍 Current branch: $BRANCH"
else
  echo "  ❌ Not a git repository"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# Summary
echo "=============================================="
if [ "$ERRORS" -eq 0 ]; then
  echo "✅ ALL CHECKS PASSED!"
  echo ""
  echo "🚀 Ready to deploy to Fly.io!"
  echo ""
  echo "Next steps:"
  echo "1. Run: python seed_demo.py (if not done yet)"
  echo "2. Test locally: python app.py"
  echo "3. Follow: FLY_DEPLOY.md"
  echo ""
  exit 0
else
  echo "❌ FOUND $ERRORS ERROR(S)"
  echo ""
  echo "⚠️  FIX ERRORS BEFORE DEPLOYING!"
  echo ""
  exit 1
fi
