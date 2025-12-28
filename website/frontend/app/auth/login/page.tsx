import { SignIn } from '@clerk/nextjs'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Login — CarPool',
  description: 'Sign in to your CarPool account',
}

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <SignIn
        appearance={{
          elements: {
            rootBox: 'mx-auto',
            card: 'bg-gray-900 border border-gray-800',
            headerTitle: 'text-white',
            headerSubtitle: 'text-gray-400',
            socialButtonsBlockButton: 'border-gray-700 hover:bg-gray-800',
            formButtonPrimary: 'bg-gradient-to-r from-amber-500 via-pink-500 to-blue-500',
            footerActionLink: 'text-pink-500 hover:text-pink-400',
          },
        }}
        routing="path"
        path="/auth/login"
        signUpUrl="/auth/signup"
        redirectUrl="/app"
      />
    </div>
  )
}
