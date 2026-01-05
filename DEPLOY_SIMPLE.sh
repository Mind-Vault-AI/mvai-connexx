#!/bin/bash
# SIMPELSTE DEPLOYMENT - GEEN GEDOE

echo "🚀 SIMPLE DEPLOYMENT - Google Cloud Run"
echo "========================================"
echo ""

# Gebruik simple Dockerfile
cp Dockerfile.simple Dockerfile

echo "✅ Using simple Dockerfile"
echo ""

# Deploy
gcloud run deploy mvai-connexx \
  --source . \
  --region=europe-west1 \
  --platform=managed \
  --allow-unauthenticated \
  --memory=1Gi \
  --timeout=300 \
  --set-env-vars="PAYMENT_PROVIDER=gumroad" \
  --project=mindvault-ai-com

echo ""
echo "✅ DEPLOYED!"
