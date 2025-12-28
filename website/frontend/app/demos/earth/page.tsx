import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Earth Map — Demos',
  description: '3D globe with real terrain topology',
}

export default function EarthDemoPage() {
  return (
    <iframe
      src="/templates/blackroad-earth-street.html"
      className="w-full h-screen border-0"
      title="Earth Map"
    />
  )
}
