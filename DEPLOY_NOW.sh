#!/bin/bash
# MVAI Connexx - Direct Fly.io Deployment
# NO BULLSHIT - Just deploy!

echo "🚀 MVAI Connexx - Fly.io Deployment START"
echo "=========================================="
echo ""

# Check if in correct directory
if [ ! -f "fly.toml" ]; then
    echo "❌ ERROR: fly.toml niet gevonden!"
    echo "Run dit script vanuit /mvai-connexx directory"
    exit 1
fi

echo "📂 Directory: OK"
echo "📁 fly.toml: OK"
echo ""

# Generate SECRET_KEY
echo "🔑 Generating SECRET_KEY..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
echo "SECRET_KEY generated: ${SECRET_KEY:0:20}..."
echo ""

echo "=========================================="
echo "🎯 READY TO DEPLOY!"
echo "=========================================="
echo ""
echo "Copy-paste deze commando's in JE EIGEN TERMINAL:"
echo ""
echo "# 1. Login bij Fly.io (opent browser)"
echo "fly auth login"
echo ""
echo "# 2. Launch app (kies 'No' voor databases)"
echo "fly launch --config fly.toml --name mvai-connexx --region ams --no-deploy"
echo ""
echo "# 3. Create persistent volume"
echo "fly volumes create mvai_data --region ams --size 1"
echo ""
echo "# 4. Set SECRET_KEY"
echo "fly secrets set SECRET_KEY=\"$SECRET_KEY\""
echo ""
echo "# 5. DEPLOY!"
echo "fly deploy"
echo ""
echo "# 6. SSH en seed data"
echo "fly ssh console"
echo "python seed_demo.py"
echo "# SAVE THE ADMIN CODE!"
echo "exit"
echo ""
echo "# 7. Open app"
echo "fly open"
echo ""
echo "=========================================="
echo "💾 SECRET_KEY bewaard in: fly_secrets.txt"
echo "$SECRET_KEY" > fly_secrets.txt
echo "=========================================="
