import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Pricing — CarPool',
  description: 'CarPool pricing plans and tiers',
}

export default function PricingPage() {
  return (
    <iframe
      src="/templates/blackroad-template-03-pricing.html"
      className="w-full h-screen border-0"
      title="Pricing"
    />
  )
}
