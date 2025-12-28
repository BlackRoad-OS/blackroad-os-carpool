import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About — CarPool',
  description: 'Learn about CarPool and the BlackRoad OS mission',
}

export default function AboutPage() {
  return (
    <iframe
      src="/templates/blackroad-template-02-about.html"
      className="w-full h-screen border-0"
      title="About CarPool"
    />
  )
}
