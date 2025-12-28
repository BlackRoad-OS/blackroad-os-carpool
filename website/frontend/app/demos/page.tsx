import { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Demos — CarPool',
  description: 'Interactive demos and showcases',
}

export default function DemosPage() {
  const demos = [
    { href: '/demos/earth', title: 'Earth Map', desc: '3D globe with real terrain topology', emoji: '🌍' },
    { href: '/demos/motion', title: 'Motion System', desc: 'Animation showcase and design patterns', emoji: '🎨' },
    { href: '/demos/world', title: 'Living World', desc: '730 entities with weather and AI agents', emoji: '🏡' },
    { href: '/demos/game', title: 'City Builder', desc: 'RPG hybrid with quests and progression', emoji: '🎮' },
  ]

  return (
    <div className="min-h-screen bg-black text-white p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-amber-500 via-pink-500 to-blue-500 bg-clip-text text-transparent">
          Interactive Demos
        </h1>
        <p className="text-gray-400 mb-12">Explore BlackRoad&apos;s visualization and animation capabilities</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {demos.map((demo) => (
            <Link
              key={demo.href}
              href={demo.href}
              className="group relative p-8 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 transition-all hover:scale-105"
            >
              <div className="text-6xl mb-4">{demo.emoji}</div>
              <h2 className="text-2xl font-bold mb-2">{demo.title}</h2>
              <p className="text-gray-400">{demo.desc}</p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
