#!/bin/bash
# Setup ALL Pis with deployment scripts and Caddyfile

set -e

echo "══════════════════════════════════════════════════════════════════"
echo "    🏗️  BlackRoad Complete Pi Infrastructure Setup"
echo "══════════════════════════════════════════════════════════════════"
echo ""

# Generate master Caddyfile
echo "Step 1: Generating master Caddyfile for all 33 domains..."
python3 blackroad-pi-deploy.py caddyfile > /tmp/Caddyfile.master
echo "✅ Generated Caddyfile ($(wc -l < /tmp/Caddyfile.master) lines)"
echo ""

# Pi targets
declare -a PIS=("lucidia" "aria" "alice" "octavia")

echo "Step 2: Deploying to all Pis..."
echo ""

for pi in "${PIS[@]}"; do
    echo "━━━ Deploying to $pi ━━━"

    # Check if Pi is online
    if ! ssh -o ConnectTimeout=3 $pi "echo ok" > /dev/null 2>&1; then
        echo "  ⏸️  $pi offline, skipping..."
        echo ""
        continue
    fi

    # Create directories
    ssh $pi "mkdir -p ~/blackroad/{scripts,config,deployments}"

    # Copy deployment automation
    scp /Users/alexa/blackroad-os-carpool/blackroad-pi-deploy.py $pi:~/blackroad/scripts/
    scp /Users/alexa/blackroad-os-carpool/pi-infrastructure.yaml $pi:~/blackroad/config/

    # Deploy Caddyfile to lucidia (primary)
    if [ "$pi" == "lucidia" ]; then
        echo "  📝 Deploying master Caddyfile..."

        # Check if Caddy is running
        if ssh $pi "docker ps | grep -q blackroad-caddy"; then
            scp /tmp/Caddyfile.master $pi:~/blackroad-console/Caddyfile
            ssh $pi "docker restart blackroad-caddy"
            echo "  ✅ Caddyfile deployed and Caddy restarted"
        else
            echo "  ⚠️  Caddy not running, creating Caddyfile for later..."
            ssh $pi "mkdir -p ~/blackroad-console"
            scp /tmp/Caddyfile.master $pi:~/blackroad-console/Caddyfile
        fi
    fi

    # Create a simple deployment receiver script
    cat > /tmp/deploy-receiver.sh << 'RECEIVER_EOF'
#!/bin/bash
# Simple deployment receiver for this Pi
# Called by webhook or manual trigger

REPO=$1
BRANCH=${2:-master}
PORT=$3

echo "Deploying $REPO (branch: $BRANCH) on port $PORT"

cd ~/blackroad/deployments
mkdir -p $REPO
cd $REPO

# Clone or pull
if [ -d ".git" ]; then
    git pull origin $BRANCH
else
    git clone https://github.com/BlackRoad-OS/$REPO.git .
    git checkout $BRANCH
fi

# Build if needed
if [ -f "package.json" ]; then
    npm install --legacy-peer-deps
    npm run build || echo "No build script"
fi

# Deploy with Docker
if [ -f "Dockerfile" ]; then
    docker build -t $REPO:latest .
    docker stop $REPO 2>/dev/null || true
    docker rm $REPO 2>/dev/null || true
    docker run -d --name $REPO \
        -p $PORT:3000 \
        --restart unless-stopped \
        $REPO:latest
    echo "✅ Deployed $REPO on port $PORT"
elif [ -f "docker-compose.yml" ]; then
    docker compose up -d
    echo "✅ Deployed $REPO via docker-compose"
else
    echo "⚠️  No Dockerfile or docker-compose.yml found"
fi
RECEIVER_EOF

    scp /tmp/deploy-receiver.sh $pi:~/blackroad/scripts/
    ssh $pi "chmod +x ~/blackroad/scripts/*.sh ~/blackroad/scripts/*.py"

    echo "  ✅ $pi setup complete"
    echo ""
done

echo "Step 3: Testing deployments..."
echo ""

# Test lucidia (primary)
if ssh lucidia "docker ps | grep -q blackroad-caddy"; then
    echo "✅ Caddy running on lucidia"

    # Test if ports are responding
    for port in 8081 3002; do
        if curl -s -o /dev/null -w "%{http_code}" http://192.168.4.38:$port | grep -q "200\|404"; then
            echo "✅ Port $port responding on lucidia"
        else
            echo "⏸️  Port $port not responding (may not be deployed yet)"
        fi
    done
fi

echo ""
echo "══════════════════════════════════════════════════════════════════"
echo "                 ✅ ALL PIS CONFIGURED!"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "What was deployed:"
echo "  • Master Caddyfile on lucidia (33 domains)"
echo "  • Deployment automation on all Pis"
echo "  • Pi infrastructure config synchronized"
echo ""
echo "Each Pi now has:"
echo "  ~/blackroad/scripts/      - Deployment automation"
echo "  ~/blackroad/config/       - Infrastructure config"
echo "  ~/blackroad/deployments/  - App deployments"
echo ""
echo "To deploy an app to any Pi:"
echo "  ssh <pi> '~/blackroad/scripts/deploy-receiver.sh <repo> master <port>'"
echo ""
echo "Examples:"
echo "  ssh lucidia '~/blackroad/scripts/deploy-receiver.sh blackroad-os-web master 3000'"
echo "  ssh aria '~/blackroad/scripts/deploy-receiver.sh blackroad-os-dashboard master 3102'"
echo ""
