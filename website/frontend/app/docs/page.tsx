import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Documentation — CarPool',
  description: 'CarPool documentation and guides',
}

export default function DocsPage() {
  return (
    <iframe
      src="/templates/blackroad-template-05-docs.html"
      className="w-full h-screen border-0"
      title="Documentation"
    />
  )
}
