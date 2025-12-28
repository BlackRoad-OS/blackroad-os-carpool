/**
 * BlackRoad OS API Client
 * Connects the OS interface to backend APIs
 *
 * Base URL: https://api.blackroad.io/v1
 * Authentication: Bearer token (Clerk JWT)
 */

class BlackRoadAPI {
    constructor(config = {}) {
        this.baseURL = config.baseURL || 'https://api.blackroad.io/v1';
        this.token = config.token || null;
        this.debug = config.debug || false;
    }

    // Set authentication token
    setToken(token) {
        this.token = token;
    }

    // Generic request handler
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const config = {
            ...options,
            headers
        };

        if (this.debug) {
            console.log(`[BlackRoadAPI] ${options.method || 'GET'} ${url}`, config);
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error?.message || 'API request failed');
            }

            return data;
        } catch (error) {
            if (this.debug) {
                console.error('[BlackRoadAPI] Error:', error);
            }
            throw error;
        }
    }

    // Auth endpoints
    async getCurrentUser() {
        return this.request('/auth/me');
    }

    // Workspace endpoints
    async getWorkspaces() {
        return this.request('/workspaces');
    }

    async createWorkspace(name) {
        return this.request('/workspaces', {
            method: 'POST',
            body: JSON.stringify({ name })
        });
    }

    async getWorkspace(workspaceId) {
        return this.request(`/workspaces/${workspaceId}`);
    }

    async updateWorkspace(workspaceId, updates) {
        return this.request(`/workspaces/${workspaceId}`, {
            method: 'PATCH',
            body: JSON.stringify(updates)
        });
    }

    async deleteWorkspace(workspaceId) {
        return this.request(`/workspaces/${workspaceId}`, {
            method: 'DELETE'
        });
    }

    // API Keys endpoints
    async getAPIKeys(workspaceId) {
        return this.request(`/workspaces/${workspaceId}/keys`);
    }

    async addAPIKey(workspaceId, provider, apiKey, endpointUrl = null) {
        return this.request(`/workspaces/${workspaceId}/keys`, {
            method: 'POST',
            body: JSON.stringify({ provider, apiKey, endpointUrl })
        });
    }

    async removeAPIKey(workspaceId, provider) {
        return this.request(`/workspaces/${workspaceId}/keys/${provider}`, {
            method: 'DELETE'
        });
    }

    async testAPIKey(workspaceId, provider) {
        return this.request(`/workspaces/${workspaceId}/keys/${provider}/test`, {
            method: 'POST'
        });
    }

    // Conversations endpoints
    async getConversations(workspaceId, params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/workspaces/${workspaceId}/conversations?${query}`);
    }

    async createConversation(workspaceId, title) {
        return this.request(`/workspaces/${workspaceId}/conversations`, {
            method: 'POST',
            body: JSON.stringify({ title })
        });
    }

    async getConversation(workspaceId, conversationId) {
        return this.request(`/workspaces/${workspaceId}/conversations/${conversationId}`);
    }

    async updateConversation(workspaceId, conversationId, updates) {
        return this.request(`/workspaces/${workspaceId}/conversations/${conversationId}`, {
            method: 'PATCH',
            body: JSON.stringify(updates)
        });
    }

    async deleteConversation(workspaceId, conversationId) {
        return this.request(`/workspaces/${workspaceId}/conversations/${conversationId}`, {
            method: 'DELETE'
        });
    }

    // Messages endpoints
    async getMessages(workspaceId, conversationId, params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/workspaces/${workspaceId}/conversations/${conversationId}/messages?${query}`);
    }

    async sendMessage(workspaceId, conversationId, content, modelId = null) {
        return this.request(`/workspaces/${workspaceId}/conversations/${conversationId}/messages`, {
            method: 'POST',
            body: JSON.stringify({ content, modelId })
        });
    }

    // Agents endpoints
    async getAgents(workspaceId) {
        return this.request(`/workspaces/${workspaceId}/agents`);
    }

    async createAgent(workspaceId, agentData) {
        return this.request(`/workspaces/${workspaceId}/agents`, {
            method: 'POST',
            body: JSON.stringify(agentData)
        });
    }

    async getAgent(workspaceId, agentId) {
        return this.request(`/workspaces/${workspaceId}/agents/${agentId}`);
    }

    async updateAgent(workspaceId, agentId, updates) {
        return this.request(`/workspaces/${workspaceId}/agents/${agentId}`, {
            method: 'PATCH',
            body: JSON.stringify(updates)
        });
    }

    async deleteAgent(workspaceId, agentId) {
        return this.request(`/workspaces/${workspaceId}/agents/${agentId}`, {
            method: 'DELETE'
        });
    }

    // Models endpoints
    async getAvailableModels(workspaceId) {
        return this.request(`/workspaces/${workspaceId}/models`);
    }

    // RoadChain endpoints (custom)
    async getRoadChainStatus() {
        return this.request('/roadchain/status');
    }

    async getRoadChainBlocks(limit = 10) {
        return this.request(`/roadchain/blocks?limit=${limit}`);
    }

    async getRoadChainBlock(blockNumber) {
        return this.request(`/roadchain/blocks/${blockNumber}`);
    }

    // RoadCoin endpoints (custom)
    async getRoadCoinBalance(address) {
        return this.request(`/roadcoin/balance/${address}`);
    }

    async getRoadCoinMiningStats() {
        return this.request('/roadcoin/mining/stats');
    }

    async startMining(workspaceId) {
        return this.request(`/workspaces/${workspaceId}/mining/start`, {
            method: 'POST'
        });
    }

    async stopMining(workspaceId) {
        return this.request(`/workspaces/${workspaceId}/mining/stop`, {
            method: 'POST'
        });
    }

    // Email endpoints (RoadMail)
    async getEmails(workspaceId, folder = 'inbox', params = {}) {
        const query = new URLSearchParams({ folder, ...params }).toString();
        return this.request(`/workspaces/${workspaceId}/mail?${query}`);
    }

    async getEmail(workspaceId, emailId) {
        return this.request(`/workspaces/${workspaceId}/mail/${emailId}`);
    }

    async sendEmail(workspaceId, to, subject, body) {
        return this.request(`/workspaces/${workspaceId}/mail`, {
            method: 'POST',
            body: JSON.stringify({ to, subject, body })
        });
    }

    // Social endpoints (BlackRoad Social)
    async getSocialFeed(workspaceId, params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/workspaces/${workspaceId}/social/feed?${query}`);
    }

    async createPost(workspaceId, content, community = null) {
        return this.request(`/workspaces/${workspaceId}/social/posts`, {
            method: 'POST',
            body: JSON.stringify({ content, community })
        });
    }

    async likePost(workspaceId, postId) {
        return this.request(`/workspaces/${workspaceId}/social/posts/${postId}/like`, {
            method: 'POST'
        });
    }

    // Video endpoints (BlackStream)
    async getVideos(workspaceId, params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/workspaces/${workspaceId}/videos?${query}`);
    }

    async uploadVideo(workspaceId, videoData) {
        return this.request(`/workspaces/${workspaceId}/videos`, {
            method: 'POST',
            body: JSON.stringify(videoData)
        });
    }
}

// Mock data for development/demo
class BlackRoadAPIMock extends BlackRoadAPI {
    async getCurrentUser() {
        return {
            success: true,
            data: {
                id: 'user_123',
                clerkId: 'user_abc',
                email: 'cecilia@blackroad.io',
                name: 'Cecilia',
                avatarUrl: '🤖',
                createdAt: new Date().toISOString()
            }
        };
    }

    async getWorkspaces() {
        return {
            success: true,
            data: {
                workspaces: [
                    {
                        id: 'ws_1',
                        name: 'BlackRoad Main',
                        slug: 'blackroad-main',
                        plan: 'pro',
                        role: 'owner',
                        createdAt: '2024-01-01T00:00:00Z'
                    }
                ]
            }
        };
    }

    async getRoadChainStatus() {
        return {
            success: true,
            data: {
                blockHeight: 42069,
                totalTransactions: 1200000,
                activeNodes: 3891,
                hashrate: '847 TH/s',
                difficulty: 1847293,
                networkStatus: 'healthy'
            }
        };
    }

    async getRoadChainBlocks(limit = 10) {
        const blocks = [];
        for (let i = 0; i < limit; i++) {
            blocks.push({
                number: 42069 - i,
                hash: `0x${Math.random().toString(16).substr(2, 8)}...`,
                timestamp: new Date(Date.now() - i * 180000).toISOString(),
                transactions: Math.floor(Math.random() * 200) + 50,
                miner: 'cecilia@blackroad.io'
            });
        }
        return {
            success: true,
            data: { blocks }
        };
    }

    async getRoadCoinMiningStats() {
        return {
            success: true,
            data: {
                hashrate: '42.7 MH/s',
                totalMined: 1247,
                currentValue: 18705,
                earnings24h: 23.4,
                status: 'mining',
                pool: 'pool.roadchain.network',
                nextPayout: '2h 34m'
            }
        };
    }

    async getEmails(workspaceId, folder = 'inbox') {
        return {
            success: true,
            data: {
                emails: [
                    {
                        id: 'email_1',
                        from: 'notifications@github.com',
                        subject: 'New PR in blackboxprogramming',
                        preview: 'New pull request has been opened...',
                        timestamp: new Date(Date.now() - 7200000).toISOString(),
                        unread: true
                    },
                    {
                        id: 'email_2',
                        from: 'alerts@digitalocean.com',
                        subject: 'Droplet NYC3 - High CPU Usage',
                        preview: 'Your droplet is experiencing...',
                        timestamp: new Date(Date.now() - 10800000).toISOString(),
                        unread: true
                    }
                ]
            }
        };
    }

    async getSocialFeed() {
        return {
            success: true,
            data: {
                posts: [
                    {
                        id: 'post_1',
                        user: '@cecilia',
                        avatar: '🤖',
                        content: 'Just deployed 100 new AI agents to the BlackRoad ecosystem!',
                        timestamp: new Date(Date.now() - 7200000).toISOString(),
                        likes: 342,
                        comments: 47
                    },
                    {
                        id: 'post_2',
                        user: '@roadchain_official',
                        avatar: '⛓️',
                        content: '🎉 MILESTONE ALERT! Block #42,069 has been mined!',
                        timestamp: new Date(Date.now() - 18000000).toISOString(),
                        likes: 567,
                        comments: 89
                    }
                ]
            }
        };
    }
}

// Export both real and mock clients
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { BlackRoadAPI, BlackRoadAPIMock };
}
