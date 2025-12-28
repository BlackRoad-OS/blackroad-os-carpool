import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Dashboard — CarPool',
  description: 'CarPool application dashboard',
}

export default function DashboardPage() {
  return (
    <iframe
      src="/templates/blackroad-template-08-dashboard.html"
      className="w-full h-screen border-0"
      title="Dashboard"
    />
  )
}
