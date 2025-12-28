import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'CarPool — Bring any AI. Train your own. Never leave.',
  description: 'Multi-AI orchestration platform with BYO-Everything, local model forking, and one-stop infrastructure.',
}

export default function HomePage() {
  return (
    <div className="min-h-screen bg-black text-white">
      {/* This will load the HTML template */}
      <iframe
        src="/templates/blackroad-template-01-homepage.html"
        className="w-full h-screen border-0"
        title="CarPool Homepage"
      />
    </div>
  )
}
