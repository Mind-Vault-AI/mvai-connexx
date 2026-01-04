#!/bin/sh
# MVAI Connexx - Startup Script voor Fly.io
# Zorgt voor correct database setup voor deployment

echo "🚀 MVAI Connexx - Starting..."

# Maak /app/data directory als het niet bestaat (voor volume mount)
if [ ! -d "/app/data" ]; then
    echo "📁 Creating /app/data directory..."
    mkdir -p /app/data
fi

# Check permissions (Fly.io volume is writable voor user)
if [ ! -w "/app/data" ]; then
    echo "⚠️  Warning: /app/data not writable!"
fi

# Database locatie info
if [ -d "/app/data" ]; then
    echo "✅ Using persistent storage: /app/data/mvai_connexx.db"
else
    echo "⚠️  Using local storage: mvai_connexx.db (not persistent!)"
fi

# Start gunicorn
echo "🎯 Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    app:app
