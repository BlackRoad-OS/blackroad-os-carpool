# BlackRoad Deployment Guide

## Deployment Status

### CarPool (carpool.blackroad.io)
- **Platform**: Vercel
- **Status**: DEPLOYED ✅
- **Production URL**: https://frontend-luho5b6w0-alexa-amundsons-projects.vercel.app
- **Target Domain**: carpool.blackroad.io

### BlackRoad OS (os.blackroad.io)
- **Platform**: Cloudflare Pages
- **Status**: DEPLOYED ✅
- **Production URL**: https://41d5c52d.blackroad-os-web.pages.dev
- **Target Domain**: os.blackroad.io
- **Project**: blackroad-os-web

## DNS Configuration Required

### 1. CarPool Domain (carpool.blackroad.io)
Add the following DNS record in Cloudflare for blackroad.io:

```
Type: CNAME
Name: carpool
Target: cname.vercel-dns.com
Proxy: DNS only (gray cloud)
TTL: Auto
```

Then verify in Vercel:
```bash
vercel domains add carpool.blackroad.io
```

### 2. BlackRoad OS Domain (os.blackroad.io)
Configure in Cloudflare Dashboard:

1. Go to Cloudflare Dashboard → Pages → blackroad-os-web
2. Click "Custom domains" → "Set up a custom domain"
3. Enter: os.blackroad.io
4. Cloudflare will automatically create the DNS records

Or manually add DNS:
```
Type: CNAME
Name: os
Target: blackroad-os-web.pages.dev
Proxy: Proxied (orange cloud)
TTL: Auto
```

## Environment Variables

### Vercel (CarPool)
All environment variables are configured:
- ✅ NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
- ✅ CLERK_SECRET_KEY
- ✅ NEXT_PUBLIC_API_URL
- ✅ NEXT_PUBLIC_APP_URL
- ✅ NEXT_PUBLIC_OS_URL

## Clerk Configuration

### Production URLs to Add
Update in Clerk Dashboard (https://dashboard.clerk.com):

1. **Authorized Domains**:
   - carpool.blackroad.io
   - os.blackroad.io

2. **Allowed redirect URLs**:
   - https://carpool.blackroad.io/auth/login
   - https://carpool.blackroad.io/auth/signup
   - https://carpool.blackroad.io/app

3. **Sign-in URL**:
   - https://carpool.blackroad.io/auth/login

4. **Sign-up URL**:
   - https://carpool.blackroad.io/auth/signup

5. **After sign-in URL**:
   - https://carpool.blackroad.io/app

6. **After sign-up URL**:
   - https://carpool.blackroad.io/app

## Deployment Commands

### CarPool (Vercel)
```bash
cd /Users/alexa/blackroad-os-carpool/website/frontend
vercel --prod
```

### BlackRoad OS (Cloudflare Pages)
```bash
# Prepare deployment
mkdir -p /tmp/blackroad-os-deploy
cp website/templates/blackroad-os-landing-connected.html /tmp/blackroad-os-deploy/index.html
cp website/templates/blackroad-os-api.js /tmp/blackroad-os-deploy/blackroad-os-api.js

# Deploy
cd /tmp/blackroad-os-deploy
wrangler pages deploy . --project-name=blackroad-os-web --branch=main
```

## Testing

### CarPool
1. Visit https://carpool.blackroad.io (after DNS configured)
2. Click "Get Started" or "Login"
3. Sign in with Google (via Clerk)
4. Should redirect to dashboard showing user info

### BlackRoad OS
1. Visit https://os.blackroad.io (after DNS configured)
2. Desktop interface should load with:
   - RoadMail window
   - RoadChain Network window
   - RoadCoin Miner window
   - Social Feed window
3. Windows should be draggable/resizable
4. API integration ready (currently using mock data)

## Troubleshooting

### Vercel Build Errors
If build fails:
1. Check environment variables are set
2. Verify Clerk keys are correct
3. Clear build cache: `rm -rf .next`
4. Redeploy: `vercel --prod --force`

### Cloudflare Pages Deployment
If deployment fails:
1. Verify you're authenticated: `wrangler whoami`
2. Check project exists: `wrangler pages project list`
3. Deploy to existing project or create new one

### DNS Not Resolving
1. DNS propagation can take up to 48 hours
2. Check status: `dig carpool.blackroad.io` or `dig os.blackroad.io`
3. Verify CNAME records are correct in Cloudflare dashboard

### Clerk Authentication Errors
1. Verify publishable key starts with `pk_test_` or `pk_live_`
2. Check redirect URLs match exactly (include https://)
3. Ensure domain is in allowed domains list

## Next Steps

1. Configure DNS records in Cloudflare
2. Update Clerk production URLs
3. Test authentication flow on both domains
4. Monitor deployments for errors
5. Connect real backend APIs (currently using mock data)

## Repository Structure

```
blackroad-os-carpool/
├── website/
│   ├── frontend/          # Next.js CarPool app (Vercel)
│   │   ├── app/
│   │   ├── middleware.ts
│   │   ├── vercel.json
│   │   └── .env.local
│   └── templates/         # BlackRoad OS static files (Cloudflare)
│       ├── blackroad-os-landing-connected.html
│       └── blackroad-os-api.js
└── docs/
    └── 04-API-CONTRACTS.md
```

## Support

- Vercel Docs: https://vercel.com/docs
- Cloudflare Pages: https://developers.cloudflare.com/pages
- Clerk Docs: https://clerk.com/docs
- BlackRoad API: https://api.blackroad.io/v1/docs
