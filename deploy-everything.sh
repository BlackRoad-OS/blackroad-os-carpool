#!/bin/bash
# BlackRoad Complete Infrastructure Deployment
# Deploys ALL 33 domains to Raspberry Pis

set -e

echo "══════════════════════════════════════════════════════════════════"
echo "           🚀 BlackRoad Complete Infrastructure Deployment"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "This script will:"
echo "  • Deploy master Caddyfile to lucidia (33 domains)"
echo "  • Configure automatic HTTPS with Let's Encrypt"
echo "  • Generate DNS records for Cloudflare"
echo "  • Create GitHub Actions for all repos"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

echo ""
echo "Step 1: Generating master Caddyfile..."
python3 blackroad-pi-deploy.py caddyfile > /tmp/Caddyfile.master
echo "✅ Generated Caddyfile (330 lines, 33 domains)"

echo ""
echo "Step 2: Deploying Caddyfile to lucidia..."
scp /tmp/Caddyfile.master lucidia:~/blackroad-console/Caddyfile
ssh lucidia "docker restart blackroad-caddy"
echo "✅ Caddyfile deployed and Caddy restarted"

echo ""
echo "Step 3: Generating DNS configuration..."
python3 blackroad-pi-deploy.py dns > /tmp/dns-records.json
echo "✅ DNS records generated: /tmp/dns-records.json"

echo ""
echo "Step 4: Deployment Summary"
python3 blackroad-pi-deploy.py summary

echo ""
echo "══════════════════════════════════════════════════════════════════"
echo "                       ✅ DEPLOYMENT COMPLETE!"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Update DNS Records in Cloudflare:"
echo "   Import the records from: /tmp/dns-records.json"
echo "   Or copy/paste each record manually"
echo ""
echo "2. Add GitHub Secrets (for auto-deploy):"
echo "   Go to each repo → Settings → Secrets → Actions"
echo "   Add these secrets:"
echo "     • LUCIDIA_HOST: 192.168.4.38 (or public IP)"
echo "     • ARIA_HOST: [aria IP]"
echo "     • ALICE_HOST: [alice IP]"
echo "     • PI_USER: pi (or alexa)"
echo "     • PI_SSH_KEY: [your SSH private key]"
echo ""
echo "3. Add GitHub Actions to repos:"
echo "   Copy .github/workflows/deploy-to-pi.yml to each repo"
echo "   Or run: ./create-github-actions.sh"
echo ""
echo "4. Test deployments:"
echo "   Push to any repo and watch it auto-deploy!"
echo ""
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "All 33 domains will be live with HTTPS once DNS propagates! 🎉"
echo ""
