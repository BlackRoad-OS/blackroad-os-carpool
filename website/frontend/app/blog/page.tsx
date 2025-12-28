import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Blog — CarPool',
  description: 'Latest news and updates from CarPool',
}

export default function BlogPage() {
  return (
    <iframe
      src="/templates/blackroad-template-06-blog.html"
      className="w-full h-screen border-0"
      title="Blog"
    />
  )
}
