# BlackRoad OS API Integration Guide

**Created:** December 28, 2024
**Status:** ✅ Ready for implementation

---

## 🎯 Overview

This guide shows how to connect the BlackRoad OS desktop interface (`os.blackroad.io`) to the backend APIs (`api.blackroad.io`).

**Files:**
- **API Client:** `website/templates/blackroad-os-api.js`
- **OS Interface:** `website/templates/blackroad-os-landing.html`
- **Connected Version:** `website/templates/blackroad-os-landing-connected.html`

---

## 🔧 API Client Setup

### Installation

Add to your HTML:

```html
<!-- Include API client -->
<script src="blackroad-os-api.js"></script>

<script>
// Initialize API client (use mock for demo, real for production)
const api = new BlackRoadAPIMock({ debug: true });

// Or for production:
// const api = new BlackRoadAPI({
//     baseURL: 'https://api.blackroad.io/v1',
//     token: clerkToken,
//     debug: false
// });
</script>
```

### Authentication with Clerk

```html
<!-- Include Clerk -->
<script src="https://cdn.clerk.dev/clerk.browser.js"></script>

<script>
// Initialize Clerk
const clerk = new Clerk('YOUR_CLERK_PUBLISHABLE_KEY');
await clerk.load();

// Get JWT token
const session = await clerk.session;
const token = await session.getToken();

// Set token in API client
api.setToken(token);

// Now all API calls are authenticated
const user = await api.getCurrentUser();
console.log('Logged in as:', user.data.email);
</script>
```

---

## 📧 RoadMail Integration

### Loading Emails

```javascript
async function loadEmails() {
    try {
        // Get current workspace
        const workspaces = await api.getWorkspaces();
        const workspace = workspaces.data.workspaces[0];

        // Fetch emails
        const response = await api.getEmails(workspace.id, 'inbox');
        const emails = response.data.emails;

        // Render emails in UI
        const emailList = document.querySelector('.email-list');
        emailList.innerHTML = '';

        emails.forEach(email => {
            const item = document.createElement('div');
            item.className = `email-item ${email.unread ? 'unread' : ''}`;
            item.innerHTML = `
                <div style="font-weight: ${email.unread ? 'bold' : 'normal'};">
                    ${email.from}
                </div>
                <div style="color: rgba(255,255,255,0.5); font-size: 11px;">
                    ${email.subject}
                </div>
                <div style="color: rgba(255,255,255,0.3); font-size: 10px;">
                    ${formatTime(email.timestamp)}
                </div>
            `;
            item.onclick = () => openEmail(email.id);
            emailList.appendChild(item);
        });
    } catch (error) {
        console.error('Failed to load emails:', error);
    }
}

// Call on window open
document.getElementById('roadmail').addEventListener('open', loadEmails);
```

### Sending Emails

```javascript
async function sendEmail(to, subject, body) {
    const workspaces = await api.getWorkspaces();
    const workspace = workspaces.data.workspaces[0];

    await api.sendEmail(workspace.id, to, subject, body);

    // Reload inbox
    await loadEmails();
}
```

---

## ⛓️ RoadChain Integration

### Network Status

```javascript
async function updateRoadChainStatus() {
    const status = await api.getRoadChainStatus();
    const data = status.data;

    // Update stats in UI
    document.querySelector('[data-stat="blockHeight"]').textContent =
        data.blockHeight.toLocaleString();
    document.querySelector('[data-stat="totalTxns"]').textContent =
        (data.totalTransactions / 1000000).toFixed(1) + 'M';
    document.querySelector('[data-stat="activeNodes"]').textContent =
        data.activeNodes.toLocaleString();
    document.querySelector('[data-stat="hashrate"]').textContent =
        data.hashrate;
}

// Refresh every 30 seconds
setInterval(updateRoadChainStatus, 30000);
```

### Latest Blocks

```javascript
async function loadLatestBlocks() {
    const response = await api.getRoadChainBlocks(10);
    const blocks = response.data.blocks;

    const container = document.querySelector('.blockchain-container');
    container.innerHTML = '<h3>Latest Blocks</h3>';

    blocks.forEach(block => {
        const blockEl = document.createElement('div');
        blockEl.className = 'block';
        blockEl.innerHTML = `
            <div class="block-header">Block #${block.number}</div>
            <div>Timestamp: ${new Date(block.timestamp).toLocaleString()}</div>
            <div>Transactions: ${block.transactions}</div>
            <div>Hash: <span class="hash">${block.hash}</span></div>
        `;
        container.appendChild(blockEl);
    });
}
```

---

## ⛏️ RoadCoin Miner Integration

### Mining Stats

```javascript
async function updateMiningStats() {
    const stats = await api.getRoadCoinMiningStats();
    const data = stats.data;

    // Update stat cards
    document.querySelector('[data-mining-stat="hashrate"] .stat-value').textContent =
        data.hashrate;
    document.querySelector('[data-mining-stat="totalMined"] .stat-value').textContent =
        data.totalMined.toLocaleString() + ' RC';
    document.querySelector('[data-mining-stat="currentValue"] .stat-value').textContent =
        '$' + data.currentValue.toLocaleString();
    document.querySelector('[data-mining-stat="earnings24h"] .stat-value').textContent =
        data.earnings24h + ' RC';

    // Update status indicator
    const statusEl = document.querySelector('.mining-status');
    statusEl.textContent = data.status === 'mining' ? '● MINING ACTIVE' : '○ MINING STOPPED';
    statusEl.style.color = data.status === 'mining' ? '#4ade80' : 'rgba(255,255,255,0.5)';
}

// Refresh every 5 seconds
setInterval(updateMiningStats, 5000);
```

### Start/Stop Mining

```javascript
async function toggleMining() {
    const workspaces = await api.getWorkspaces();
    const workspace = workspaces.data.workspaces[0];

    const currentStatus = await api.getRoadCoinMiningStats();

    if (currentStatus.data.status === 'mining') {
        await api.stopMining(workspace.id);
        alert('Mining stopped');
    } else {
        await api.startMining(workspace.id);
        alert('Mining started!');
    }

    await updateMiningStats();
}
```

---

## 👥 BlackRoad Social Integration

### Loading Feed

```javascript
async function loadSocialFeed() {
    const workspaces = await api.getWorkspaces();
    const workspace = workspaces.data.workspaces[0];

    const response = await api.getSocialFeed(workspace.id);
    const posts = response.data.posts;

    const feed = document.querySelector('.social-feed');
    feed.innerHTML = '';

    posts.forEach(post => {
        const postEl = document.createElement('div');
        postEl.className = 'post';
        postEl.innerHTML = `
            <div class="post-header">
                <div class="post-avatar">${post.avatar}</div>
                <div>
                    <div class="post-user">${post.user}</div>
                    <div class="post-time">${formatTime(post.timestamp)}</div>
                </div>
            </div>
            <div class="post-content">${post.content}</div>
            <div class="post-actions">
                <div class="post-action" onclick="likePost('${post.id}')">
                    👍 ${post.likes} Likes
                </div>
                <div class="post-action">💬 ${post.comments} Comments</div>
                <div class="post-action">🔄 Share</div>
            </div>
        `;
        feed.appendChild(postEl);
    });
}
```

### Creating Posts

```javascript
async function createPost(content, community = null) {
    const workspaces = await api.getWorkspaces();
    const workspace = workspaces.data.workspaces[0];

    await api.createPost(workspace.id, content, community);

    // Reload feed
    await loadSocialFeed();
}
```

---

## 💬 AI Chat Integration

### Conversations List

```javascript
async function loadConversations() {
    const workspaces = await api.getWorkspaces();
    const workspace = workspaces.data.workspaces[0];

    const response = await api.getConversations(workspace.id);
    const conversations = response.data.conversations;

    // Render in sidebar
    const sidebar = document.querySelector('.chat-sidebar');
    conversations.forEach(conv => {
        const item = document.createElement('div');
        item.className = 'conversation-item';
        item.textContent = conv.title;
        item.onclick = () => openConversation(conv.id);
        sidebar.appendChild(item);
    });
}
```

### Sending Messages

```javascript
async function sendMessage(conversationId, content) {
    const workspaces = await api.getWorkspaces();
    const workspace = workspaces.data.workspaces[0];

    // Send message
    const response = await api.sendMessage(
        workspace.id,
        conversationId,
        content
    );

    // Display message
    displayMessage(response.data.message);

    // Wait for AI response
    // (In real app, use WebSocket or polling for streaming)
}
```

---

## 🎮 Game Integration

### Road City - Save/Load

```javascript
async function saveGame(gameState) {
    const workspaces = await api.getWorkspaces();
    const workspace = workspaces.data.workspaces[0];

    await api.request(`/workspaces/${workspace.id}/games/road-city/save`, {
        method: 'POST',
        body: JSON.stringify(gameState)
    });
}

async function loadGame() {
    const workspaces = await api.getWorkspaces();
    const workspace = workspaces.data.workspaces[0];

    const response = await api.request(`/workspaces/${workspace.id}/games/road-city/load`);
    return response.data.gameState;
}
```

---

## 🔄 Real-time Updates

### WebSocket Connection

```javascript
// Connect to WebSocket for real-time updates
const ws = new WebSocket('wss://api.blackroad.io/ws');

ws.onopen = () => {
    console.log('Connected to BlackRoad realtime');

    // Authenticate
    ws.send(JSON.stringify({
        type: 'auth',
        token: clerkToken
    }));

    // Subscribe to channels
    ws.send(JSON.stringify({
        type: 'subscribe',
        channels: ['roadchain', 'mining', 'social']
    }));
};

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);

    switch (message.type) {
        case 'block_mined':
            updateRoadChainStatus();
            loadLatestBlocks();
            break;

        case 'mining_update':
            updateMiningStats();
            break;

        case 'new_post':
            loadSocialFeed();
            break;

        case 'new_email':
            loadEmails();
            showNotification('📧 New email received');
            break;
    }
};
```

---

## 📊 Complete Integration Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BlackRoad OS - Connected</title>

    <!-- Include dependencies -->
    <script src="https://cdn.clerk.dev/clerk.browser.js"></script>
    <script src="blackroad-os-api.js"></script>
</head>
<body>
    <div id="desktop">
        <!-- OS interface here -->
    </div>

    <script>
        // Global state
        let api;
        let currentWorkspace;
        let ws;

        // Initialize everything
        async function init() {
            try {
                // 1. Initialize Clerk
                const clerk = new Clerk('YOUR_CLERK_KEY');
                await clerk.load();

                // 2. Get auth token
                const session = await clerk.session;
                if (!session) {
                    // Redirect to login
                    window.location.href = 'https://carpool.blackroad.io/auth/login';
                    return;
                }

                const token = await session.getToken();

                // 3. Initialize API client
                api = new BlackRoadAPI({
                    baseURL: 'https://api.blackroad.io/v1',
                    token: token,
                    debug: true
                });

                // 4. Load user data
                const user = await api.getCurrentUser();
                console.log('Logged in as:', user.data.email);

                // 5. Get workspace
                const workspaces = await api.getWorkspaces();
                currentWorkspace = workspaces.data.workspaces[0];

                // 6. Connect WebSocket
                connectWebSocket(token);

                // 7. Load initial data for all windows
                await Promise.all([
                    loadEmails(),
                    updateRoadChainStatus(),
                    updateMiningStats(),
                    loadSocialFeed()
                ]);

                console.log('✅ BlackRoad OS initialized');

            } catch (error) {
                console.error('Failed to initialize:', error);
                alert('Failed to connect to BlackRoad. Please try again.');
            }
        }

        // Connect WebSocket
        function connectWebSocket(token) {
            ws = new WebSocket('wss://api.blackroad.io/ws');

            ws.onopen = () => {
                ws.send(JSON.stringify({ type: 'auth', token }));
                ws.send(JSON.stringify({
                    type: 'subscribe',
                    channels: ['roadchain', 'mining', 'social', 'mail']
                }));
            };

            ws.onmessage = (event) => {
                const msg = JSON.parse(event.data);
                handleRealtimeUpdate(msg);
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            ws.onclose = () => {
                console.log('WebSocket closed, reconnecting...');
                setTimeout(() => connectWebSocket(token), 5000);
            };
        }

        // Handle realtime updates
        function handleRealtimeUpdate(message) {
            switch (message.type) {
                case 'block_mined':
                    updateRoadChainStatus();
                    loadLatestBlocks();
                    showNotification('⛓️ New block mined!');
                    break;
                case 'mining_update':
                    updateMiningStats();
                    break;
                case 'new_post':
                    loadSocialFeed();
                    break;
                case 'new_email':
                    loadEmails();
                    showNotification('📧 New email');
                    break;
            }
        }

        // Notification system
        function showNotification(message) {
            // Create toast notification
            const toast = document.createElement('div');
            toast.className = 'toast-notification';
            toast.textContent = message;
            document.body.appendChild(toast);

            setTimeout(() => toast.remove(), 3000);
        }

        // Start initialization
        init();
    </script>
</body>
</html>
```

---

## 🚀 Deployment

### Environment Variables

```env
# Clerk
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# API
NEXT_PUBLIC_API_URL=https://api.blackroad.io/v1
NEXT_PUBLIC_WS_URL=wss://api.blackroad.io/ws

# Features
NEXT_PUBLIC_ENABLE_ROADCHAIN=true
NEXT_PUBLIC_ENABLE_MINING=true
NEXT_PUBLIC_ENABLE_SOCIAL=true
```

### Production Checklist

- [ ] API client uses production URL
- [ ] Clerk authentication configured
- [ ] WebSocket connection tested
- [ ] Error handling for all API calls
- [ ] Loading states for all windows
- [ ] Offline mode fallback
- [ ] Rate limiting handled
- [ ] Token refresh logic

---

## 📝 API Endpoints Summary

| Window | Endpoints Used |
|--------|---------------|
| **RoadMail** | `/workspaces/:id/mail` |
| **RoadChain** | `/roadchain/status`, `/roadchain/blocks` |
| **RoadCoin Miner** | `/roadcoin/mining/stats`, `/workspaces/:id/mining/*` |
| **BlackRoad Social** | `/workspaces/:id/social/*` |
| **AI Chat** | `/workspaces/:id/conversations`, `/workspaces/:id/messages` |
| **File Explorer** | `/workspaces/:id/files` (future) |
| **BlackStream** | `/workspaces/:id/videos` |

---

**Status:** ✅ API client ready
**Next:** Integrate into OS landing page
**Docs:** See `04-API-CONTRACTS.md` for complete API reference

🌌 **The BlackRoad OS is ready to go live with real backend data!**
