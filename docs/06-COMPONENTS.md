# 06 — Component Inventory

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## Overview

This document lists every UI component needed for BlackRoad. Components are built with:
- **React** (Next.js App Router)
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** (base components)
- **Lucide React** (icons)

---

## Design System

### Colors

```css
/* Brand Gradient */
--brand-orange: #FF9D08;
--brand-pink: #FF0066;
--brand-purple: #7780FF;
--brand-blue: #0866FF;

/* Neutrals (Dark Mode Default) */
--bg-primary: #0A0A0A;
--bg-secondary: #141414;
--bg-tertiary: #1F1F1F;
--bg-hover: #2A2A2A;

--text-primary: #FFFFFF;
--text-secondary: #A1A1A1;
--text-muted: #666666;

--border: #2A2A2A;
--border-hover: #3A3A3A;

/* Semantic */
--success: #22C55E;
--warning: #F59E0B;
--error: #EF4444;
--info: #3B82F6;
```

### Typography

```css
/* Font Family */
font-family: 'Inter', system-ui, sans-serif;

/* Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```

### Spacing

```css
/* Base unit: 4px */
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
```

---

## Base Components (shadcn/ui)

These come from shadcn/ui and are customized for BlackRoad:

| Component | Use Case |
|-----------|----------|
| `Button` | All buttons |
| `Input` | Text inputs |
| `Textarea` | Multi-line inputs |
| `Select` | Dropdowns |
| `Dialog` | Modals |
| `Sheet` | Slide-out panels |
| `Dropdown` | Context menus |
| `Tooltip` | Hover hints |
| `Avatar` | User/agent avatars |
| `Badge` | Status indicators |
| `Card` | Content containers |
| `Separator` | Visual dividers |
| `Skeleton` | Loading states |
| `Toast` | Notifications |
| `Tabs` | Tab navigation |

---

## Custom Components

### Layout Components

#### `AppShell`
Main application layout wrapper.

```tsx
<AppShell>
  <Sidebar />
  <main>{children}</main>
</AppShell>
```

Props:
- `children`: React.ReactNode

#### `Sidebar`
Left navigation panel.

```tsx
<Sidebar
  conversations={conversations}
  currentId={currentConversationId}
  onNewChat={() => {}}
  onSelectChat={(id) => {}}
/>
```

Props:
- `conversations`: Conversation[]
- `currentId`: string | null
- `onNewChat`: () => void
- `onSelectChat`: (id: string) => void
- `collapsed`: boolean

#### `Header`
Top bar with user menu.

```tsx
<Header
  user={user}
  workspace={workspace}
/>
```

Props:
- `user`: User
- `workspace`: Workspace

---

### Chat Components

#### `ChatContainer`
Main chat area wrapper.

```tsx
<ChatContainer
  conversationId={id}
  messages={messages}
  isLoading={isLoading}
/>
```

#### `MessageList`
Scrollable list of messages.

```tsx
<MessageList
  messages={messages}
  isStreaming={isStreaming}
/>
```

#### `Message`
Single message bubble.

```tsx
<Message
  role="assistant"
  content="Hello! How can I help?"
  modelUsed="gpt-4o"
  providerUsed="openai"
  timestamp={new Date()}
/>
```

Props:
- `role`: 'user' | 'assistant' | 'system'
- `content`: string
- `modelUsed`: string (optional)
- `providerUsed`: string (optional)
- `timestamp`: Date
- `isStreaming`: boolean

#### `ChatInput`
Message input area.

```tsx
<ChatInput
  onSend={(message) => {}}
  disabled={isLoading}
  placeholder="Send a message..."
/>
```

Props:
- `onSend`: (message: string) => void
- `disabled`: boolean
- `placeholder`: string
- `attachmentsEnabled`: boolean

#### `ModelBadge`
Shows which model responded.

```tsx
<ModelBadge
  model="gpt-4o"
  provider="openai"
/>
```

#### `StreamingIndicator`
Shows AI is generating response.

```tsx
<StreamingIndicator model="claude-3-5-sonnet" />
```

---

### Settings Components

#### `ApiKeyCard`
Card for managing a provider's API key.

```tsx
<ApiKeyCard
  provider="openai"
  providerName="OpenAI"
  providerLogo="/logos/openai.svg"
  isConnected={true}
  keyHint="...abc"
  onAdd={() => {}}
  onRemove={() => {}}
  onTest={() => {}}
/>
```

#### `ApiKeyModal`
Modal for adding/editing API key.

```tsx
<ApiKeyModal
  provider="openai"
  open={isOpen}
  onOpenChange={setIsOpen}
  onSave={(key) => {}}
/>
```

#### `ProviderGrid`
Grid of all provider cards.

```tsx
<ProviderGrid
  providers={providers}
  connectedProviders={connectedProviders}
/>
```

---

### Agent Components

#### `AgentCard`
Card displaying an agent.

```tsx
<AgentCard
  agent={agent}
  onClick={() => {}}
  onEdit={() => {}}
/>
```

#### `AgentAvatar`
Agent avatar with status.

```tsx
<AgentAvatar
  name="Lucidia"
  imageUrl="/agents/lucidia.png"
  isSystem={true}
  size="lg"
/>
```

#### `AgentConfigForm`
Form for creating/editing agents.

```tsx
<AgentConfigForm
  agent={existingAgent}
  onSave={(config) => {}}
  onCancel={() => {}}
/>
```

---

### Training Components

#### `TrainingJobCard`
Card showing training job status.

```tsx
<TrainingJobCard
  job={job}
  onCancel={() => {}}
  onViewDetails={() => {}}
/>
```

#### `TrainingProgress`
Real-time training progress display.

```tsx
<TrainingProgress
  status="running"
  currentEpoch={2}
  totalEpochs={3}
  loss={0.45}
  estimatedTimeRemaining="15 min"
/>
```

#### `ModelSelector`
Grid for selecting base model.

```tsx
<ModelSelector
  models={availableModels}
  selected={selectedModel}
  onSelect={(model) => {}}
/>
```

#### `DataSourceSelector`
UI for selecting training data.

```tsx
<DataSourceSelector
  conversations={conversations}
  selected={selectedIds}
  onSelect={(ids) => {}}
/>
```

---

### Workspace Components

#### `WorkspaceSwitcher`
Dropdown for switching workspaces.

```tsx
<WorkspaceSwitcher
  workspaces={workspaces}
  current={currentWorkspace}
  onSwitch={(id) => {}}
  onCreate={() => {}}
/>
```

#### `MemberList`
List of workspace members.

```tsx
<MemberList
  members={members}
  currentUserId={userId}
  onRemove={(memberId) => {}}
  onRoleChange={(memberId, role) => {}}
/>
```

#### `InviteModal`
Modal for inviting team members.

```tsx
<InviteModal
  open={isOpen}
  onOpenChange={setIsOpen}
  onInvite={(email, role) => {}}
/>
```

---

### Marketing Components (blackroad.io)

#### `Hero`
Landing page hero section.

```tsx
<Hero
  headline="Bring any AI. Train your own. Never leave."
  subheadline="The operating system for AI agents."
  ctaText="Get Started"
  ctaHref="/sign-up"
/>
```

#### `FeatureGrid`
Grid of feature cards.

```tsx
<FeatureGrid features={features} />
```

#### `PricingTable`
Pricing comparison table.

```tsx
<PricingTable
  plans={plans}
  currentPlan={userPlan}
  onSelectPlan={(plan) => {}}
/>
```

#### `Testimonial`
Customer testimonial card.

```tsx
<Testimonial
  quote="BlackRoad changed how we work with AI."
  author="Jane Doe"
  role="CEO, TechCo"
  avatarUrl="/testimonials/jane.jpg"
/>
```

---

## Component File Structure

```
src/
├── components/
│   ├── ui/                    # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   └── ...
│   │
│   ├── layout/
│   │   ├── app-shell.tsx
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   └── footer.tsx
│   │
│   ├── chat/
│   │   ├── chat-container.tsx
│   │   ├── message-list.tsx
│   │   ├── message.tsx
│   │   ├── chat-input.tsx
│   │   ├── model-badge.tsx
│   │   └── streaming-indicator.tsx
│   │
│   ├── settings/
│   │   ├── api-key-card.tsx
│   │   ├── api-key-modal.tsx
│   │   └── provider-grid.tsx
│   │
│   ├── agents/
│   │   ├── agent-card.tsx
│   │   ├── agent-avatar.tsx
│   │   └── agent-config-form.tsx
│   │
│   ├── training/
│   │   ├── training-job-card.tsx
│   │   ├── training-progress.tsx
│   │   ├── model-selector.tsx
│   │   └── data-source-selector.tsx
│   │
│   ├── workspace/
│   │   ├── workspace-switcher.tsx
│   │   ├── member-list.tsx
│   │   └── invite-modal.tsx
│   │
│   └── marketing/
│       ├── hero.tsx
│       ├── feature-grid.tsx
│       ├── pricing-table.tsx
│       └── testimonial.tsx
```

---

## Icon Usage

Use Lucide React icons consistently:

```tsx
import {
  MessageSquare,    // Chat
  Settings,         // Settings
  Key,             // API Keys
  Bot,             // Agents
  Zap,             // Training
  Users,           // Team
  CreditCard,      // Billing
  Plus,            // Add/New
  Send,            // Send message
  Copy,            // Copy
  RefreshCw,       // Regenerate
  Check,           // Success
  X,               // Error/Close
  Loader2,         // Loading spinner
  ChevronDown,     // Dropdown
  ExternalLink,    // External link
} from 'lucide-react';
```
