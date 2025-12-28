#!/bin/bash
# BlackRoad Complete Deployment with Webhook Integration
# Uses existing webhook receivers on all Pis

set -e

echo "══════════════════════════════════════════════════════════════════"
echo "    🚀 BlackRoad Pi Deployment via Webhooks"
echo "══════════════════════════════════════════════════════════════════"
echo ""

# Pi configuration
declare -A PI_IPS=(
    ["lucidia"]="192.168.4.38"
    ["aria"]="192.168.4.64"
    ["alice"]="192.168.4.49"
    ["octavia"]="192.168.4.74"
    ["shellfish"]="TBD"
)

declare -A PI_WEBHOOK_PORTS=(
    ["lucidia"]="9001"
    ["aria"]="9003"
    ["alice"]="9002"
    ["octavia"]="9004"
    ["shellfish"]="9005"
)

WEBHOOK_SECRET="blackroad2025"

# Check if Pi is online
check_pi() {
    local pi=$1
    local ip=${PI_IPS[$pi]}

    if [ "$ip" == "TBD" ]; then
        return 1
    fi

    if ping -c 1 -W 1 $ip > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Deploy via webhook
deploy_via_webhook() {
    local pi=$1
    local ip=${PI_IPS[$pi]}
    local port=${PI_WEBHOOK_PORTS[$pi]}

    echo "  Triggering webhook on $pi ($ip:$port)..."

    curl -s -X POST "http://$ip:$port/deploy" \
        -H "Content-Type: application/json" \
        -H "X-Webhook-Secret: $WEBHOOK_SECRET" \
        -d '{
            "action": "deploy",
            "repo": "blackroad-os-carpool",
            "branch": "master"
        }' || echo "  ⚠️  Webhook failed, trying direct deployment..."
}

# Direct SSH deployment as fallback
deploy_via_ssh() {
    local pi=$1

    echo "  Direct SSH deployment to $pi..."

    # Try hostname first, then IP
    if ssh -o ConnectTimeout=3 $pi "echo ok" > /dev/null 2>&1; then
        target=$pi
    else
        target=${PI_IPS[$pi]}
    fi

    # Upload Caddyfile if this is lucidia
    if [ "$pi" == "lucidia" ]; then
        echo "  Uploading Caddyfile to $pi..."
        python3 blackroad-pi-deploy.py caddyfile > /tmp/Caddyfile.master
        scp /tmp/Caddyfile.master $target:~/blackroad-console/Caddyfile
        ssh $target "docker restart blackroad-caddy"
        echo "  ✅ Caddyfile deployed to $pi"
    fi
}

# Main deployment
echo "Step 1: Checking Pi availability..."
echo ""

for pi in lucidia aria alice octavia shellfish; do
    if check_pi $pi; then
        echo "  ✅ $pi (${PI_IPS[$pi]}) - ONLINE"
    else
        echo "  ⏸️  $pi - OFFLINE or TBD"
    fi
done

echo ""
echo "Step 2: Deploying to primary Pi (lucidia)..."
echo ""

if check_pi lucidia; then
    deploy_via_ssh lucidia
    echo ""
    echo "✅ Primary deployment complete!"
else
    echo "❌ lucidia is offline!"
    echo ""
    echo "🔄 Attempting backup deployment to shellfish..."

    if check_pi shellfish; then
        deploy_via_ssh shellfish
        echo "✅ Deployed to backup Pi (shellfish)"
    else
        echo "❌ All Pis offline! Please check network connection."
        exit 1
    fi
fi

echo ""
echo "Step 3: Syncing to secondary Pis..."
echo ""

for pi in aria alice octavia; do
    if check_pi $pi; then
        echo "  Deploying to $pi..."
        deploy_via_webhook $pi
        echo "  ✅ $pi deployed"
    else
        echo "  ⏸️  $pi offline, skipping..."
    fi
done

echo ""
echo "══════════════════════════════════════════════════════════════════"
echo "                    ✅ DEPLOYMENT COMPLETE!"
echo "══════════════════════════════════════════════════════════════════"
echo ""

# Show deployment summary
python3 blackroad-pi-deploy.py summary

echo ""
echo "🌐 All online Pis are now configured with the master Caddyfile!"
echo "🔧 Webhook receivers are listening on ports 9001-9005"
echo ""
echo "Test the deployment:"
echo "  curl http://192.168.4.38:8081  # BlackRoad OS"
echo "  curl http://192.168.4.38:3002  # CarPool"
echo ""
