#!/bin/bash
# Script om 6 aparte PRs te maken (voor als je dat wilt)

echo "Creating 6 separate PRs from mega branch..."

# Checkout main
git checkout main

# PR 1: Multi-tenant Foundation
git checkout -b pr/1-multi-tenant
git cherry-pick 3979010
git push -u origin pr/1-multi-tenant
echo "PR 1 ready: Multi-tenant Foundation"

# PR 2: TO THE MOON
git checkout main
git checkout -b pr/2-to-the-moon
git cherry-pick 343232f
git push -u origin pr/2-to-the-moon
echo "PR 2 ready: TO THE MOON"

# PR 3: Security Fortress
git checkout main
git checkout -b pr/3-security
git cherry-pick 3cc6b8b
git push -u origin pr/3-security
echo "PR 3 ready: Security Fortress"

# PR 4: AI Secretaresse
git checkout main
git checkout -b pr/4-ai-assistant
git cherry-pick adc70be
git push -u origin pr/4-ai-assistant
echo "PR 4 ready: AI Secretaresse"

# PR 5: Enterprise GODMODE
git checkout main
git checkout -b pr/5-enterprise
git cherry-pick 1b19c9f
git push -u origin pr/5-enterprise
echo "PR 5 ready: Enterprise GODMODE"

# PR 6: Legal Framework
git checkout main
git checkout -b pr/6-legal
git cherry-pick 5e21901
git push -u origin pr/6-legal
echo "PR 6 ready: Legal Framework"

echo ""
echo "✅ All 6 PRs created!"
echo "Now create PR on GitHub for each branch:"
echo "  - pr/1-multi-tenant"
echo "  - pr/2-to-the-moon"
echo "  - pr/3-security"
echo "  - pr/4-ai-assistant"
echo "  - pr/5-enterprise"
echo "  - pr/6-legal"
