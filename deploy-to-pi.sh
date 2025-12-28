#!/bin/bash
# BlackRoad Universal Pi Deployment Script
# Deploys any repo to the appropriate Pi based on pi-infrastructure.yaml

set -e

REPO_NAME=$(basename $(git rev-parse --show-toplevel) 2>/dev/null || echo "unknown")
INFRASTRUCTURE_FILE="$(dirname "$0")/pi-infrastructure.yaml"

echo "═══════════════════════════════════════════════════════════"
echo "  BlackRoad Pi Deployment System"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Repository: $REPO_NAME"
echo ""

# Parse YAML to find which Pi and port this repo should deploy to
# This is a simple grep-based parser - replace with yq/jq for production
find_deployment_target() {
    local repo=$1
    # This would normally use yq, but we'll create a Python helper
    echo "Finding deployment target for $repo..."
}

# For now, let's create a comprehensive deployment script
# that can be customized per repo

cat << 'SCRIPT_END'

# Deployment Steps:
# 1. Build the application (if needed)
# 2. Create Docker container
# 3. Copy to appropriate Pi
# 4. Start container on correct port
# 5. Update Caddy configuration
# 6. Restart Caddy

echo "Building application..."
if [ -f "package.json" ]; then
    npm install --legacy-peer-deps
    npm run build
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Creating deployment package..."
DEPLOY_DIR="/tmp/deploy-${REPO_NAME}-$(date +%s)"
mkdir -p "$DEPLOY_DIR"

# Copy built files
if [ -d ".next" ]; then
    cp -r .next "$DEPLOY_DIR/"
    cp -r public "$DEPLOY_DIR/" 2>/dev/null || true
    cp package.json "$DEPLOY_DIR/"
elif [ -d "dist" ]; then
    cp -r dist "$DEPLOY_DIR/"
elif [ -d "build" ]; then
    cp -r build "$DEPLOY_DIR/"
else
    # Copy all source files
    cp -r . "$DEPLOY_DIR/"
fi

echo "Deployment package ready at: $DEPLOY_DIR"
echo ""
echo "Next: Upload to Pi and start container"

SCRIPT_END

chmod +x "$0"
