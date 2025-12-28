import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'City Builder — Demos',
  description: 'RPG hybrid with quests and progression',
}

export default function GameDemoPage() {
  return (
    <iframe
      src="/templates/blackroad-game.html"
      className="w-full h-screen border-0"
      title="City Builder"
    />
  )
}
