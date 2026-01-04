#!/bin/bash
# MVAI Connexx - Automatic Merge Conflict Fixer
# Fixes .env.example payment section conflict

echo "🔧 Fixing .env.example merge conflict..."
echo ""

# Check if conflict exists
if grep -q "<<<<<<< " .env.example; then
    echo "⚠️  Conflict markers found - fixing now..."

    # Remove conflict markers and keep Gumroad version
    sed -i '/<<<<<<< main/,/=======/{//!d}' .env.example
    sed -i '/=======/d' .env.example
    sed -i '/<<<<<<< main/d' .env.example
    sed -i '/>>>>>>> claude/d' .env.example

    echo "✅ Conflict markers removed"
else
    echo "✅ No conflict markers found"
fi

# Verify correct content
if grep -q "GUMROAD" .env.example; then
    echo "✅ Gumroad configuration present"

    # Count Gumroad URLs
    count=$(grep -c "GUMROAD_.*_URL=" .env.example)
    echo "✅ Found $count Gumroad product URLs"

    if [ "$count" -ge 5 ]; then
        echo "✅ All pricing tiers configured"
    else
        echo "⚠️  Missing some Gumroad URLs (found $count, expected 5)"
    fi
else
    echo "❌ Gumroad configuration missing!"
    echo "   Run: git checkout claude/mvai-connexx-multi-tenant-upgrade-8eDvw -- .env.example"
    exit 1
fi

# Stage if fixed
if git status --porcelain | grep -q ".env.example"; then
    echo ""
    echo "📝 Changes ready to commit:"
    git add .env.example
    echo "   git add .env.example"
    echo ""
    echo "To commit: git commit -m 'fix: Resolve .env.example merge conflict - Gumroad active'"
else
    echo ""
    echo "✅ .env.example is clean - no changes needed"
fi

echo ""
echo "=========================================="
echo "✅ DONE - Ready to deploy!"
echo "=========================================="
