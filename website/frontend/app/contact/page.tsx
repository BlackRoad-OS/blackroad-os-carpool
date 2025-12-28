import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Contact — CarPool',
  description: 'Get in touch with the CarPool team',
}

export default function ContactPage() {
  return (
    <iframe
      src="/templates/blackroad-template-07-contact.html"
      className="w-full h-screen border-0"
      title="Contact"
    />
  )
}
