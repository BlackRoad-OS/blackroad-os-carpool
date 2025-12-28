import { SignUp } from '@clerk/nextjs'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Sign Up — CarPool',
  description: 'Create your CarPool account',
}

export default function SignupPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <SignUp
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
        path="/auth/signup"
        signInUrl="/auth/login"
        redirectUrl="/app"
      />
    </div>
  )
}
