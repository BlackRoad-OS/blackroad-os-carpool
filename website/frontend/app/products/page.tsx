import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Products — CarPool',
  description: 'CarPool products and features',
}

export default function ProductsPage() {
  return (
    <iframe
      src="/templates/blackroad-template-04-products.html"
      className="w-full h-screen border-0"
      title="Products"
    />
  )
}
