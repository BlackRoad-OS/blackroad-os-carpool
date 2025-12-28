#!/bin/bash
# BlackRoad Single Hub Deployment
# Uses octavia (100GB) as the deployment master

set -e

echo "══════════════════════════════════════════════════════════════════"
echo "    🎯 BlackRoad Single Hub Deployment"
echo "    Hub: octavia (192.168.4.74) - 100GB available"
echo "══════════════════════════════════════════════════════════════════"
echo ""

HUB="octavia"
HUB_IP="192.168.4.74"

echo "Step 1: Setting up deployment hub on $HUB..."
echo ""

# Create deployment structure on hub
ssh $HUB "mkdir -p ~/blackroad-hub/{repos,scripts,caddyfiles,logs}"

# Copy all automation to hub
echo "  Copying deployment automation..."
scp blackroad-pi-deploy.py $HUB:~/blackroad-hub/scripts/
scp pi-infrastructure.yaml $HUB:~/blackroad-hub/
scp deploy-everything.sh $HUB:~/blackroad-hub/scripts/

# Generate master Caddyfile on hub
echo "  Generating master Caddyfile..."
python3 blackroad-pi-deploy.py caddyfile > /tmp/Caddyfile.master
scp /tmp/Caddyfile.master $HUB:~/blackroad-hub/caddyfiles/

echo "  ✅ Hub configured"
echo ""

echo "Step 2: Deploying Caddyfile to lucidia (web server)..."
echo ""

# Deploy Caddyfile to lucidia (the actual web server)
scp /tmp/Caddyfile.master lucidia:~/blackroad-console/Caddyfile
ssh lucidia "docker restart blackroad-caddy"

echo "  ✅ Caddyfile deployed to lucidia"
echo ""

echo "Step 3: Creating deployment script on hub..."
echo ""

# Create a deployment orchestrator on hub
ssh $HUB 'cat > ~/blackroad-hub/scripts/deploy-to-pi.sh' << 'DEPLOYSCRIPT'
#!/bin/bash
# Deploy from hub to any Pi
# Usage: ./deploy-to-pi.sh <repo> <pi> <port>

REPO=$1
PI=$2
PORT=$3

echo "🚀 Deploying $REPO to $PI on port $PORT..."

# Clone/pull repo on hub
cd ~/blackroad-hub/repos
if [ -d "$REPO" ]; then
    cd $REPO
    git pull
else
    git clone https://github.com/BlackRoad-OS/$REPO.git
    cd $REPO
fi

# Build if needed
if [ -f "package.json" ]; then
    npm install --legacy-peer-deps
    npm run build || true
fi

# Create tarball
tar -czf /tmp/$REPO.tar.gz .

# Deploy to target Pi
echo "  Uploading to $PI..."
scp /tmp/$REPO.tar.gz $PI:/tmp/

# Execute deployment on target Pi
ssh $PI << REMOTESCRIPT
    mkdir -p ~/apps/$REPO
    cd ~/apps/$REPO
    tar -xzf /tmp/$REPO.tar.gz
    rm /tmp/$REPO.tar.gz

    # Stop existing container
    docker stop $REPO 2>/dev/null || true
    docker rm $REPO 2>/dev/null || true

    # Start container
    if [ -f "docker-compose.yml" ]; then
        docker compose up -d
    else
        # Create Dockerfile if doesn't exist
        if [ ! -f "Dockerfile" ]; then
            cat > Dockerfile << 'DOCKEREOF'
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install --legacy-peer-deps || true
EXPOSE 3000
CMD ["npm", "start"]
DOCKEREOF
        fi

        docker build -t $REPO:latest .
        docker run -d --name $REPO \
            -p $PORT:3000 \
            --restart unless-stopped \
            $REPO:latest
    fi

    echo "✅ $REPO deployed on $PI:$PORT"
REMOTESCRIPT

echo "✅ Deployment complete!"
DEPLOYSCRIPT

ssh $HUB "chmod +x ~/blackroad-hub/scripts/*.sh ~/blackroad-hub/scripts/*.py"

echo "  ✅ Deployment orchestrator created"
echo ""

echo "══════════════════════════════════════════════════════════════════"
echo "                    ✅ SINGLE HUB SETUP COMPLETE!"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "🎯 Deployment Hub: $HUB ($HUB_IP)"
echo "   • 100GB storage for all repos"
echo "   • Orchestrates deployments to all Pis"
echo "   • Generates Caddyfiles"
echo ""
echo "🌐 Web Server: lucidia (192.168.4.38)"
echo "   • Caddy with 33 domains configured"
echo "   • Minimal storage footprint"
echo "   • Reverse proxies to all Pis"
echo ""
echo "📋 To deploy an app:"
echo "   ssh $HUB '~/blackroad-hub/scripts/deploy-to-pi.sh <repo> <pi> <port>'"
echo ""
echo "Examples:"
echo "   ssh $HUB '~/blackroad-hub/scripts/deploy-to-pi.sh blackroad-os-web lucidia 3000'"
echo "   ssh $HUB '~/blackroad-hub/scripts/deploy-to-pi.sh blackroad-os-carpool lucidia 3002'"
echo "   ssh $HUB '~/blackroad-hub/scripts/deploy-to-pi.sh blackroad-os-dashboard aria 3102'"
echo ""
echo "🔄 To update Caddyfile:"
echo "   python3 blackroad-pi-deploy.py caddyfile > /tmp/Caddyfile.new"
echo "   scp /tmp/Caddyfile.new lucidia:~/blackroad-console/Caddyfile"
echo "   ssh lucidia 'docker restart blackroad-caddy'"
echo ""
