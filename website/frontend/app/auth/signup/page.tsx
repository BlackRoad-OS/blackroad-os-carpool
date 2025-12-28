import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Sign Up — CarPool',
  description: 'Create your CarPool account',
}

export default function SignupPage() {
  return (
    <iframe
      src="/templates/blackroad-template-09-auth.html"
      className="w-full h-screen border-0"
      title="Sign Up"
    />
  )
}
