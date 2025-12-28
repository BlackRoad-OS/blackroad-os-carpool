import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Motion System — Demos',
  description: 'Animation showcase and design patterns',
}

export default function MotionDemoPage() {
  return (
    <iframe
      src="/templates/blackroad-animation.html"
      className="w-full h-screen border-0"
      title="Motion System"
    />
  )
}
