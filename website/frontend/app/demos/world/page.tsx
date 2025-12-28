import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Living World — Demos',
  description: '730 entities with weather and AI agents',
}

export default function WorldDemoPage() {
  return (
    <iframe
      src="/templates/blackroad-living-world.html"
      className="w-full h-screen border-0"
      title="Living World"
    />
  )
}
