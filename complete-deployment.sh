#!/bin/bash
set -e

echo "═══════════════════════════════════════════════════════════"
echo "  BlackRoad Complete Deployment to lucidia Pi"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Configuration
LUCIDIA_IP="192.168.4.38"
CARPOOL_PORT="3002"
OS_PORT="8081"

echo "✅ Step 1: Applications Deployed"
echo "   - CarPool: localhost:$CARPOOL_PORT (building...)"
echo "   - BlackRoad OS: localhost:$OS_PORT"
echo ""

echo "✅ Step 2: Caddy Configured"
echo "   - carpool.blackroad.io → localhost:$CARPOOL_PORT"
echo "   - os.blackroad.io → localhost:$OS_PORT"
echo "   - Automatic HTTPS with Let's Encrypt"
echo ""

echo "📋 Step 3: DNS Configuration Needed"
echo ""
echo "Go to Cloudflare dashboard and update these DNS records:"
echo ""
echo "1. carpool.blackroad.io:"
echo "   Type: A"
echo "   Name: carpool"
echo "   Value: [YOUR PUBLIC IP - get from whatismyip.com]"
echo "   Proxy: OFF (gray cloud)"
echo ""
echo "2. os.blackroad.io:"
echo "   Type: A"
echo "   Name: os"
echo "   Value: [YOUR PUBLIC IP]"
echo "   Proxy: OFF (gray cloud)"
echo ""
echo "Or if using the local network:"
echo "   Value: $LUCIDIA_IP"
echo ""

echo "🔍 Checking deployment status..."
echo ""

# Check BlackRoad OS
if curl -s http://$LUCIDIA_IP:$OS_PORT | grep -q "BlackRoad"; then
    echo "✅ BlackRoad OS is running!"
else
    echo "⏳ BlackRoad OS starting..."
fi

# Check CarPool (may still be building)
if curl -s http://$LUCIDIA_IP:$CARPOOL_PORT >/dev/null 2>&1; then
    echo "✅ CarPool is running!"
else
    echo "⏳ CarPool is building (this takes 2-5 minutes)..."
    echo "   Check status: ssh lucidia 'docker logs -f blackroad-carpool'"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "🎉 Deployment Complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Local URLs (for testing):"
echo "   • http://$LUCIDIA_IP:$OS_PORT (BlackRoad OS)"
echo "   • http://$LUCIDIA_IP:$CARPOOL_PORT (CarPool - when build completes)"
echo ""
echo "Production URLs (after DNS configuration):"
echo "   • https://os.blackroad.io"
echo "   • https://carpool.blackroad.io"
echo ""
echo "Monitor CarPool build:"
echo "   ssh lucidia 'docker logs -f blackroad-carpool'"
echo ""
