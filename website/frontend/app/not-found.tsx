import { Metadata } from 'next'

export const metadata: Metadata = {
  title: '404 — Page Not Found',
  description: 'This page could not be found',
}

export default function NotFound() {
  return (
    <iframe
      src="/templates/blackroad-template-10-error.html"
      className="w-full h-screen border-0"
      title="404 Error"
    />
  )
}
