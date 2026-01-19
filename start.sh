#!/bin/sh
# MVAI Connexx - Production Startup Script

echo "🚀 MVAI Connexx starting..."

# Create data directory if needed
mkdir -p /app/data

# Database location
if [ -d "/app/data" ]; then
    export DATABASE_PATH="/app/data/mvai_connexx.db"
    echo "✅ Using persistent storage: /app/data/mvai_connexx.db"
else
    export DATABASE_PATH="mvai_connexx.db"
    echo "⚠️  Using local storage: mvai_connexx.db"
fi

# Auto-generate SECRET_KEY if not set
if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    echo "⚠️  Generated random SECRET_KEY (set SECRET_KEY env var for persistence)"
fi

# Start gunicorn
echo "🎯 Starting Gunicorn..."
exec gunicorn \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    app:app
