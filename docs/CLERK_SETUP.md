# Clerk Authentication Setup Guide

**Created:** December 28, 2024
**Purpose:** Configure Clerk authentication for BlackRoad OS & CarPool

---

## 🎯 Overview

BlackRoad uses **Clerk** for authentication across all platforms:
- `os.blackroad.io` - Desktop OS interface
- `carpool.blackroad.io` - Product platform
- `api.blackroad.io` - Backend APIs

---

## 🚀 Quick Start

### 1. Create Clerk Account

1. Go to https://clerk.com
2. Sign up with your email: **amundsonalexa@gmail.com**
3. Create a new application: "BlackRoad OS"

### 2. Get API Keys

In Clerk Dashboard:
1. Go to **API Keys**
2. Copy your keys:
   - **Publishable Key:** `pk_test_...` (safe for frontend)
   - **Secret Key:** `sk_test_...` (backend only, keep private!)

### 3. Configure Environment Variables

Create `/website/frontend/.env.local`:

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_actual_key_here
CLERK_SECRET_KEY=sk_test_your_actual_secret_here
```

**⚠️ IMPORTANT:** Add `.env.local` to `.gitignore` (already done)

---

## 🔧 Clerk Configuration

### Enable Gmail OAuth

In Clerk Dashboard → **User & Authentication** → **Social Connections**:

1. Enable **Google** OAuth
2. Configure OAuth settings:
   - **Client ID:** (from Google Cloud Console)
   - **Client Secret:** (from Google Cloud Console)
3. Add authorized redirect:
   - `https://carpool.blackroad.io/auth/callback`
   - `https://os.blackroad.io/auth/callback`
   - `http://localhost:3000/auth/callback` (for dev)

### User Profile Fields

Configure which fields to collect:
- ✅ **Email** (required)
- ✅ **Name** (optional)
- ✅ **Avatar** (optional)
- ✅ **Username** (optional)

### Session Settings

- **Session lifetime:** 7 days
- **Refresh tokens:** Enabled
- **Multi-session:** Enabled (allow multiple devices)

---

## 💻 Frontend Integration (Next.js)

### Install Clerk

```bash
cd website/frontend
npm install @clerk/nextjs
```

### Configure Middleware

Create `middleware.ts`:

```typescript
import { authMiddleware } from "@clerk/nextjs";

export default authMiddleware({
  // Public routes that don't require authentication
  publicRoutes: [
    "/",
    "/about",
    "/pricing",
    "/products",
    "/contact",
    "/blog",
    "/docs",
    "/demos(.*)",
  ],

  // Routes that require authentication
  protectedRoutes: [
    "/app(.*)",
  ],
});

export const config = {
  matcher: ["/((?!.*\\..*|_next).*)", "/", "/(api|trpc)(.*)"],
};
```

### Root Layout

Update `app/layout.tsx`:

```typescript
import { ClerkProvider } from '@clerk/nextjs'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  )
}
```

### Login Page

`app/auth/login/page.tsx`:

```typescript
import { SignIn } from "@clerk/nextjs";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <SignIn
        appearance={{
          elements: {
            rootBox: "mx-auto",
            card: "bg-gray-900 border border-gray-800",
          },
        }}
        routing="path"
        path="/auth/login"
        signUpUrl="/auth/signup"
      />
    </div>
  );
}
```

### User Button

Add to dashboard:

```typescript
import { UserButton } from "@clerk/nextjs";

export default function Dashboard() {
  return (
    <div>
      <header>
        <UserButton afterSignOutUrl="/" />
      </header>
    </div>
  );
}
```

---

## 🌐 OS Landing Page Integration

For `os.blackroad.io`, add authentication:

```html
<!-- Add Clerk to OS landing page -->
<script src="https://cdn.clerk.dev/clerk.browser.js"></script>

<script>
async function initAuth() {
    // Initialize Clerk
    const clerk = window.Clerk;
    await clerk.load({
        publishableKey: 'pk_test_your_key_here'
    });

    // Check if user is signed in
    if (clerk.user) {
        // User is authenticated
        const user = clerk.user;
        console.log('Logged in as:', user.primaryEmailAddress.emailAddress);

        // Get JWT for API calls
        const token = await clerk.session.getToken();

        // Initialize OS with real data
        initializeOS(token, user);
    } else {
        // Show sign-in button
        showSignInButton();
    }
}

function showSignInButton() {
    // Add sign-in button to taskbar or start menu
    const signInBtn = document.createElement('button');
    signInBtn.textContent = '🔐 Sign In';
    signInBtn.onclick = () => {
        window.Clerk.openSignIn();
    };
    document.querySelector('.system-tray').prepend(signInBtn);
}

function initializeOS(token, user) {
    // Initialize API client with token
    const api = new BlackRoadAPI({
        baseURL: 'https://api.blackroad.io/v1',
        token: token
    });

    // Load user-specific data
    loadUserData(api, user);

    // Update UI with user info
    updateUserProfile(user);
}

// Start authentication
initAuth();
</script>
```

---

## 🔑 Using Your Gmail Account

### For Development

1. **Sign up through Clerk:**
   - Go to `http://localhost:3000/auth/signup`
   - Click "Continue with Google"
   - Sign in with: **amundsonalexa@gmail.com**
   - Clerk handles the OAuth flow

2. **First-time Setup:**
   - Clerk creates your user profile
   - You're redirected to the app
   - JWT token is automatically managed

### For Production

Same flow, but with production URLs:
- `https://carpool.blackroad.io/auth/signup`
- `https://os.blackroad.io/auth/login`

---

## 🔐 Security Best Practices

### ✅ DO:
- Use Clerk's OAuth for Google sign-in
- Let Clerk manage sessions and tokens
- Use environment variables for keys
- Add `.env.local` to `.gitignore`
- Use JWT tokens for API authentication

### ❌ DON'T:
- Never hardcode passwords in code
- Never commit `.env.local` to git
- Never expose secret keys on frontend
- Never store passwords in plain text

---

## 🧪 Testing Authentication

### Local Development

```bash
cd website/frontend
npm run dev
```

Visit `http://localhost:3000/auth/login`

### Test User Flow

1. Click "Sign in with Google"
2. Select your Gmail account
3. Grant permissions
4. Redirected to dashboard
5. User profile loaded from Clerk

### Getting User Data

```typescript
// In any component
import { useUser } from '@clerk/nextjs'

export default function MyComponent() {
  const { user } = useUser();

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h1>Welcome, {user.firstName}!</h1>
      <p>Email: {user.primaryEmailAddress.emailAddress}</p>
      <img src={user.imageUrl} alt="Avatar" />
    </div>
  );
}
```

---

## 🔄 Authentication Flow

```
User clicks "Sign In"
    ↓
Clerk OAuth popup opens
    ↓
User authenticates with Google (amundsonalexa@gmail.com)
    ↓
Google confirms identity
    ↓
Clerk creates/updates user profile
    ↓
Clerk issues JWT token
    ↓
User redirected to app
    ↓
Frontend gets token from Clerk
    ↓
Backend APIs validate JWT
    ↓
User data loaded
    ↓
OS/CarPool initialized with real data
```

---

## 📊 User Data Structure (from Clerk)

```json
{
  "id": "user_abc123",
  "firstName": "Alexa",
  "lastName": "Amundson",
  "emailAddresses": [
    {
      "emailAddress": "amundsonalexa@gmail.com",
      "verification": { "status": "verified" }
    }
  ],
  "imageUrl": "https://img.clerk.com/...",
  "createdAt": 1703721600000,
  "updatedAt": 1703721600000
}
```

---

## 🚀 Next Steps

1. **Create Clerk account** at https://clerk.com
2. **Get API keys** from dashboard
3. **Add keys to `.env.local`**
4. **Enable Google OAuth** in Clerk settings
5. **Test login flow** locally
6. **Deploy to production** with production keys

---

## 🆘 Troubleshooting

### "Invalid publishable key"
- Check you're using the correct key (pk_test_... for dev)
- Verify key is in `.env.local`
- Restart dev server after adding keys

### "Redirect URI mismatch"
- Add your URL to Clerk's allowed redirects
- Check URL exactly matches (http vs https, trailing slash)

### "User not found"
- First sign-up creates the user
- Use `/auth/signup` for first-time users
- Use `/auth/login` for returning users

---

**Status:** ✅ Ready to configure
**Next:** Create Clerk account and add API keys
**Security:** ✅ No passwords in code, OAuth only

🔐 **Your credentials are safe - we're using industry-standard OAuth!**
