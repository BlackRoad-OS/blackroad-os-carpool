#!/bin/bash
set -e

echo "═══════════════════════════════════════════════════════════"
echo "  BlackRoad Unified Deployment to blackroad-hello"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Configuration
PROJECT="blackroad-hello"
FRONTEND_DIR="/Users/alexa/blackroad-os-carpool/website/frontend"
TEMPLATES_DIR="/Users/alexa/blackroad-os-carpool/website/templates"
DEPLOY_DIR="/tmp/blackroad-unified-deploy"

# Clean and create deployment directory
echo "📦 Preparing deployment directory..."
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"

# Build CarPool frontend
echo "🚀 Building CarPool frontend..."
cd "$FRONTEND_DIR"
npm run build

# Copy CarPool build to deployment
echo "📋 Copying CarPool build..."
cp -r "$FRONTEND_DIR/.next/static" "$DEPLOY_DIR/_next/"
cp -r "$FRONTEND_DIR/.next/server" "$DEPLOY_DIR/_next/"
cp -r "$FRONTEND_DIR/public/"* "$DEPLOY_DIR/" 2>/dev/null || true

# Copy BlackRoad OS files
echo "🖥️  Copying BlackRoad OS files..."
cp "$TEMPLATES_DIR/blackroad-os-landing-connected.html" "$DEPLOY_DIR/os.html"
cp "$TEMPLATES_DIR/blackroad-os-api.js" "$DEPLOY_DIR/blackroad-os-api.js"

# Create index routing page
cat > "$DEPLOY_DIR/index.html" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>BlackRoad - Choose Your Path</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #000;
            color: #fff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            width: 100%;
        }
        h1 {
            font-size: 4rem;
            background: linear-gradient(135deg, #F5A623, #FF1D6C, #2979FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 3rem;
            text-align: center;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        .card {
            background: linear-gradient(135deg, rgba(245,166,35,0.1), rgba(255,29,108,0.1));
            border: 2px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 3rem;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            display: block;
        }
        .card:hover {
            transform: translateY(-8px);
            border-color: rgba(255,255,255,0.3);
            box-shadow: 0 20px 60px rgba(255,29,108,0.3);
        }
        .card h2 {
            font-size: 2rem;
            margin-bottom: 1rem;
            color: #fff;
        }
        .card p {
            color: rgba(255,255,255,0.7);
            line-height: 1.6;
        }
        .emoji {
            font-size: 4rem;
            margin-bottom: 1.5rem;
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>BlackRoad</h1>
        <div class="grid">
            <a href="/app" class="card">
                <span class="emoji">🚀</span>
                <h2>CarPool</h2>
                <p>AI-powered conversation platform with agent orchestration, authentication, and workspace management.</p>
            </a>
            <a href="/os.html" class="card">
                <span class="emoji">🖥️</span>
                <h2>BlackRoad OS</h2>
                <p>Desktop operating system interface with RoadMail, RoadChain Network, RoadCoin Miner, and Social Feed.</p>
            </a>
        </div>
    </div>
</body>
</html>
EOF

# Deploy to Cloudflare Pages
echo "☁️  Deploying to Cloudflare Pages ($PROJECT)..."
cd "$DEPLOY_DIR"
wrangler pages deploy . --project-name="$PROJECT" --branch=main

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ Deployment Complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🌐 Your apps are now live at:"
echo "   • Main: https://$PROJECT.pages.dev"
echo "   • CarPool: https://$PROJECT.pages.dev/app"
echo "   • BlackRoad OS: https://$PROJECT.pages.dev/os.html"
echo ""
echo "🔗 Custom domains:"
echo "   • carpool.blackroad.io → https://$PROJECT.pages.dev/app"
echo "   • os.blackroad.io → https://$PROJECT.pages.dev/os.html"
echo ""
echo "📝 To configure custom domain routing:"
echo "   wrangler pages project get $PROJECT"
echo ""
