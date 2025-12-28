import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'CarPool by BlackRoad OS',
  description: 'Bring any AI. Train your own. Never leave.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
