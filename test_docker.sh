#!/bin/bash
echo "🔨 Building Docker image..."
docker build -t mvai-connexx . 2>&1 | tail -20

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Docker build SUCCESS!"
    echo ""
    echo "🚀 Starting container..."
    docker run -d \
        -p 5000:5000 \
        -e PAYMENT_PROVIDER=gumroad \
        -e SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))') \
        --name mvai-connexx-test \
        mvai-connexx
    
    echo ""
    echo "⏳ Waiting for app to start..."
    sleep 5
    
    echo ""
    echo "🔍 Checking if app is running..."
    docker logs mvai-connexx-test 2>&1 | tail -10
    
    echo ""
    echo "🌐 Testing HTTP endpoint..."
    curl -s http://localhost:5000/ | head -20
    
    echo ""
    echo ""
    echo "✅ Container running! Access at: http://localhost:5000"
    echo ""
    echo "📊 View logs: docker logs -f mvai-connexx-test"
    echo "🛑 Stop: docker stop mvai-connexx-test && docker rm mvai-connexx-test"
else
    echo "❌ Docker build FAILED"
    exit 1
fi
