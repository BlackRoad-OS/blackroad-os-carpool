'use client'

import { useUser, UserButton } from '@clerk/nextjs'

export default function DashboardPage() {
  const { user, isLoaded } = useUser()

  if (!isLoaded) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="text-2xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-amber-500 via-pink-500 to-blue-500 bg-clip-text text-transparent">
              🚀 CarPool Dashboard
            </h1>
            <p className="text-gray-400 text-sm">Welcome back, {user?.firstName || user?.username}!</p>
          </div>
          <UserButton afterSignOutUrl="/" />
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Welcome Card */}
        <div className="bg-gradient-to-r from-amber-500/10 via-pink-500/10 to-blue-500/10 border border-amber-500/20 rounded-lg p-8 mb-8">
          <h2 className="text-3xl font-bold mb-2">
            Welcome, {user?.firstName || user?.username}! 🎉
          </h2>
          <p className="text-gray-300">
            You're successfully authenticated with Clerk! Your BlackRoad OS ecosystem is ready.
          </p>
        </div>

        {/* User Info Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <div className="text-sm text-gray-400 mb-2">EMAIL</div>
            <div className="font-mono text-amber-500">
              {user?.emailAddresses[0]?.emailAddress}
            </div>
          </div>

          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <div className="text-sm text-gray-400 mb-2">USERNAME</div>
            <div className="font-mono text-pink-500">
              {user?.username || 'Not set'}
            </div>
          </div>

          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <div className="text-sm text-gray-400 mb-2">USER ID</div>
            <div className="font-mono text-blue-500 text-xs">
              {user?.id}
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <div className="text-4xl mb-2">💬</div>
            <div className="text-2xl font-bold text-amber-500">0</div>
            <div className="text-sm text-gray-400">Conversations</div>
          </div>

          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <div className="text-4xl mb-2">🤖</div>
            <div className="text-2xl font-bold text-pink-500">0</div>
            <div className="text-sm text-gray-400">AI Agents</div>
          </div>

          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <div className="text-4xl mb-2">🔑</div>
            <div className="text-2xl font-bold text-blue-500">0</div>
            <div className="text-sm text-gray-400">API Keys</div>
          </div>

          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <div className="text-4xl mb-2">⛓️</div>
            <div className="text-2xl font-bold text-violet-500">42,069</div>
            <div className="text-sm text-gray-400">RoadChain Block</div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button className="bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-lg p-4 hover:opacity-90 transition">
              <div className="text-2xl mb-2">💬</div>
              <div className="font-semibold">New Chat</div>
            </button>

            <button className="bg-gradient-to-r from-pink-500 to-red-500 text-white rounded-lg p-4 hover:opacity-90 transition">
              <div className="text-2xl mb-2">🤖</div>
              <div className="font-semibold">Create Agent</div>
            </button>

            <button className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-lg p-4 hover:opacity-90 transition">
              <div className="text-2xl mb-2">🔑</div>
              <div className="font-semibold">Add API Key</div>
            </button>

            <button className="bg-gradient-to-r from-violet-500 to-purple-500 text-white rounded-lg p-4 hover:opacity-90 transition">
              <div className="text-2xl mb-2">⚙️</div>
              <div className="font-semibold">Settings</div>
            </button>
          </div>
        </div>

        {/* Debug Info */}
        <details className="mt-8 bg-gray-900 border border-gray-800 rounded-lg p-4">
          <summary className="cursor-pointer text-gray-400 hover:text-white">
            🔍 Debug: User Data (Click to expand)
          </summary>
          <pre className="mt-4 text-xs text-green-400 overflow-auto">
            {JSON.stringify(user, null, 2)}
          </pre>
        </details>
      </main>
    </div>
  )
}
