import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Login — CarPool',
  description: 'Sign in to your CarPool account',
}

export default function LoginPage() {
  return (
    <iframe
      src="/templates/blackroad-template-09-auth.html"
      className="w-full h-screen border-0"
      title="Login"
    />
  )
}
