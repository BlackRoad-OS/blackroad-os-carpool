# 05 — User Flows

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## Overview

This document describes the step-by-step user journeys through BlackRoad. Use these flows for:
- UX design decisions
- Testing scenarios
- Onboarding optimization
- Feature prioritization

---

## Flow 1: New User Onboarding

### Goal
Get user from landing page to first meaningful AI conversation.

### Steps

```
1. LANDING PAGE (blackroad.io)
   User sees: Hero, value prop, "Get Started" CTA
   User clicks: "Get Started" button
   
2. CLERK AUTH (app.blackroad.io/sign-up)
   User sees: Sign up form (email/password or OAuth)
   User action: Creates account via email or Google/GitHub
   System: Creates user record, Clerk webhook fires
   
3. WORKSPACE CREATION (app.blackroad.io/onboarding/workspace)
   User sees: "Name your workspace" input
   User action: Enters workspace name
   System: Creates workspace, sets user as owner
   
4. API KEY SETUP (app.blackroad.io/onboarding/keys)
   User sees: Provider cards (OpenAI, Anthropic, etc.)
   User sees: "Skip for now" option
   User action: Adds at least one API key OR skips
   System: Encrypts and stores key, tests validity
   
5. MEET LUCIDIA (app.blackroad.io/onboarding/welcome)
   User sees: Lucidia introduction message
   User sees: Suggested first prompts
   User action: Sends first message or clicks suggestion
   
6. FIRST CONVERSATION (app.blackroad.io/chat)
   User sees: Chat interface with streaming response
   User action: Continues conversation
   System: Routes to best available model
   
7. DASHBOARD (after first conversation ends)
   User sees: Dashboard with recent conversations
   User sees: Prompt to add more API keys
```

### Success Criteria
- Time from landing to first message: < 3 minutes
- First message sends successfully
- User sees streaming response

### Fallback Paths
- If no API key added: Show demo mode with limited responses
- If API key invalid: Show error, allow retry
- If all providers down: Show status page

---

## Flow 2: Adding API Keys

### Goal
User connects a new AI provider to their workspace.

### Steps

```
1. SETTINGS ENTRY
   From: Dashboard sidebar → "Settings" → "API Keys"
   OR: Chat interface "Add provider" button
   
2. PROVIDER SELECTION (app.blackroad.io/settings/keys)
   User sees: Grid of provider cards
   - OpenAI (GPT-4, GPT-4o, o1)
   - Anthropic (Claude 3.5, Claude 4)
   - Google (Gemini 1.5, Gemini 2.0)
   - xAI (Grok)
   - Custom (OpenAI-compatible endpoint)
   User action: Clicks provider card
   
3. KEY INPUT MODAL
   User sees: 
   - Provider logo and name
   - Text input for API key
   - Link to provider's key management page
   - "Test" button
   - "Save" button
   User action: Pastes API key, clicks "Test"
   
4. KEY VALIDATION
   System: Calls provider API to verify key
   If valid:
   - Shows green checkmark
   - Lists available models
   - "Save" button enabled
   If invalid:
   - Shows red X with error message
   - "Save" button disabled
   
5. CONFIRMATION
   User action: Clicks "Save"
   System: Encrypts key, stores in database
   User sees: Toast "OpenAI connected successfully"
   User sees: Provider card now shows "Connected"
```

### For Custom Providers (Ollama, vLLM, etc.)

```
3b. CUSTOM PROVIDER MODAL
   User sees:
   - "Provider Name" input
   - "Endpoint URL" input (e.g., http://localhost:11434/v1)
   - "API Key" input (optional for local)
   - "Test Connection" button
```

---

## Flow 3: Chat Conversation

### Goal
User has a productive conversation with AI, model is intelligently selected.

### Steps

```
1. START CONVERSATION
   From: Dashboard "New Chat" button
   OR: Sidebar "+" button
   OR: Keyboard shortcut (Cmd+N)
   
2. CHAT INTERFACE (app.blackroad.io/chat/[id])
   User sees:
   - Empty chat area with welcome message
   - Input field at bottom
   - Model indicator (e.g., "via GPT-4o" or "Auto")
   - Sidebar with conversation history
   
3. SEND MESSAGE
   User action: Types message, presses Enter
   System:
   - Stores user message
   - Analyzes intent (code, creative, research, etc.)
   - Selects best available model
   - Calls provider API
   
4. STREAMING RESPONSE
   User sees:
   - Model indicator updates ("Responding via Claude 3.5...")
   - Text streams in character by character
   - Typing indicator while waiting
   
5. RESPONSE COMPLETE
   User sees:
   - Full response
   - Token count (hover for details)
   - Copy button
   - Regenerate button
   
6. CONTINUE OR END
   User action: Sends follow-up OR closes tab
   System: Auto-generates title from first exchange
```

### Model Selection Logic (Lucidia Orchestrator)

```
Intent Detection:
- "Write code" → Prefer Claude or GPT-4
- "Creative writing" → Prefer Claude
- "Quick question" → Prefer GPT-4o-mini or Gemini Flash
- "Complex reasoning" → Prefer o1 or Claude
- "Image analysis" → Prefer GPT-4V or Gemini

Availability Check:
- Which providers does user have connected?
- Are those providers currently operational?
- Is user within rate limits?

Final Selection:
- Pick best available model for task
- Show model badge in UI
```

---

## Flow 4: Training a Custom Model

### Goal
User fine-tunes an open-source model on their conversation history.

### Steps

```
1. TRAINING ENTRY
   From: Settings → "Models" → "Train New Model"
   OR: Dashboard card "Train your own AI"
   
2. BASE MODEL SELECTION (app.blackroad.io/settings/models/train)
   User sees: Grid of base models
   - LLaMA 3 8B (Recommended for most users)
   - LLaMA 3 70B (More capable, longer training)
   - Qwen 2.5 7B (Multilingual)
   - SmolLM 1.7B (Fast, edge-deployable)
   - Phi-3 (Efficient reasoning)
   User action: Selects base model
   
3. DATA SELECTION
   User sees:
   - "All conversations" checkbox
   - List of conversations with checkboxes
   - Estimated training data size
   - Minimum data warning if insufficient
   User action: Selects data sources
   
4. CONFIGURATION
   User sees:
   - Training method (LoRA recommended, Full fine-tune)
   - Epochs slider (1-5, default 3)
   - Learning rate (auto-suggested)
   - Estimated cost
   - Estimated time
   User action: Adjusts settings, clicks "Start Training"
   
5. CONFIRMATION MODAL
   User sees:
   - Summary of selections
   - Cost confirmation
   - "This will take approximately X hours"
   User action: Confirms
   
6. TRAINING IN PROGRESS
   User sees:
   - Progress bar
   - Current epoch / total epochs
   - Loss graph (live updating)
   - "Cancel" button
   System: Runs training job, updates status via WebSocket
   
7. TRAINING COMPLETE
   User sees:
   - Success message
   - Model performance metrics
   - "Deploy" button
   - "Test in Playground" button
```

---

## Flow 5: Deploying a Forked Model

### Goal
User deploys their trained model for use in conversations.

### Steps

```
1. MODEL LISTING (app.blackroad.io/settings/models)
   User sees: List of trained models
   - Model name
   - Base model
   - Training date
   - Status (Ready / Deployed / Training)
   
2. DEPLOY ACTION
   User action: Clicks "Deploy" on a ready model
   
3. DEPLOYMENT OPTIONS
   User sees:
   - "BlackRoad Cloud" (managed, pay-per-use)
   - "Export for Local" (download adapter weights)
   - "Custom Endpoint" (provide own inference URL)
   User action: Selects deployment target
   
4. CLOUD DEPLOYMENT
   If BlackRoad Cloud selected:
   - System provisions inference endpoint
   - User sees: Progress spinner
   - User sees: Endpoint URL when ready
   - User sees: Estimated cost per 1K tokens
   
5. USE IN CONVERSATION
   User sees: New model appears in model selector
   User action: Starts new chat, selects custom model
   System: Routes messages to deployed endpoint
```

---

## Flow 6: Team Workspace (Pro/Team Plans)

### Goal
User invites team members to shared workspace.

### Steps

```
1. WORKSPACE SETTINGS (app.blackroad.io/workspace/settings)
   User sees: Workspace name, members list
   User action: Clicks "Invite Member"
   
2. INVITE MODAL
   User sees:
   - Email input
   - Role selector (Admin, Member)
   - "Send Invite" button
   User action: Enters email, selects role, sends
   
3. INVITE EMAIL
   Invitee receives: Email with workspace invite link
   
4. INVITEE JOINS
   Invitee action: Clicks link, signs up/in
   System: Adds invitee to workspace_members
   
5. SHARED ACCESS
   All members see:
   - Shared conversation history
   - Shared API keys (keys themselves hidden)
   - Shared trained models
   Admins can:
   - Manage members
   - Manage billing
   - Delete workspace
```

---

## Flow 7: Billing & Upgrade

### Goal
User upgrades from Free to Pro plan.

### Steps

```
1. UPGRADE PROMPT
   Triggers:
   - Hit conversation limit
   - Try to add 2nd workspace
   - Try to invite team member
   User sees: "Upgrade to Pro" modal with feature comparison
   
2. PLAN SELECTION (app.blackroad.io/settings/billing)
   User sees:
   - Free tier (current)
   - Pro ($20/mo)
   - Team ($50/user/mo)
   - Enterprise (Contact us)
   User action: Clicks "Upgrade to Pro"
   
3. STRIPE CHECKOUT
   User sees: Stripe-hosted checkout page
   User action: Enters payment details, completes purchase
   
4. CONFIRMATION
   Stripe webhook fires
   System: Updates workspace plan
   User sees: "Welcome to Pro!" modal
   User sees: New features unlocked
```

---

## Error States

### API Key Invalid
```
User sees: Red banner "Your OpenAI key is invalid"
User sees: "Update key" button
Action: Navigate to settings, re-enter key
```

### Provider Rate Limited
```
User sees: Warning "OpenAI rate limited. Switching to Anthropic..."
System: Auto-routes to backup provider
User sees: Response continues from alternate provider
```

### All Providers Down
```
User sees: Full-screen error "All AI providers unavailable"
User sees: Status page link
User sees: "Retry" button
```

### Insufficient Permissions
```
User sees: "You don't have permission to [action]"
User sees: "Contact workspace admin" or upgrade prompt
```
