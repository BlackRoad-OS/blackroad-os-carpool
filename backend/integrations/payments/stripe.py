"""
Stripe Integration

Handles all Stripe operations:
- Subscriptions
- Payments
- Webhooks
- Connect (for creator payouts)
"""

import stripe
from typing import Dict, Optional, List
from datetime import datetime
import os


class StripeIntegration:
    """
    Stripe integration for BlackRoad OS payments.

    Account: acct_1SUDM8ChUUSEbzyh
    Products configured per 14-CORPORATE.md
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("STRIPE_SECRET_KEY")
        stripe.api_key = self.api_key

    # Subscriptions

    async def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        metadata: Optional[Dict] = None
    ) -> stripe.Subscription:
        """Create a new subscription"""
        return stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
            metadata=metadata or {},
            expand=["latest_invoice.payment_intent"]
        )

    async def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True
    ) -> stripe.Subscription:
        """Cancel a subscription"""
        return stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=at_period_end
        )

    async def get_subscription(self, subscription_id: str) -> stripe.Subscription:
        """Get subscription details"""
        return stripe.Subscription.retrieve(subscription_id)

    # Customers

    async def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> stripe.Customer:
        """Create a new customer"""
        return stripe.Customer.create(
            email=email,
            name=name,
            metadata=metadata or {}
        )

    async def get_customer(self, customer_id: str) -> stripe.Customer:
        """Get customer details"""
        return stripe.Customer.retrieve(customer_id)

    # Checkout Sessions

    async def create_checkout_session(
        self,
        price_id: str,
        success_url: str,
        cancel_url: str,
        customer_id: Optional[str] = None,
        client_reference_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> stripe.checkout.Session:
        """Create a Stripe Checkout session"""
        params = {
            "mode": "subscription",
            "line_items": [{"price": price_id, "quantity": 1}],
            "success_url": success_url,
            "cancel_url": cancel_url,
            "metadata": metadata or {},
        }

        if customer_id:
            params["customer"] = customer_id
        if client_reference_id:
            params["client_reference_id"] = client_reference_id

        return stripe.checkout.Session.create(**params)

    # Invoices

    async def get_invoice(self, invoice_id: str) -> stripe.Invoice:
        """Get invoice details"""
        return stripe.Invoice.retrieve(invoice_id)

    async def list_invoices(
        self,
        customer_id: str,
        limit: int = 10
    ) -> List[stripe.Invoice]:
        """List customer invoices"""
        return stripe.Invoice.list(
            customer=customer_id,
            limit=limit
        ).data

    # Webhooks

    def construct_webhook_event(
        self,
        payload: bytes,
        sig_header: str,
        webhook_secret: str
    ) -> stripe.Event:
        """
        Verify and construct webhook event.

        Raises:
            ValueError: Invalid payload
            stripe.error.SignatureVerificationError: Invalid signature
        """
        return stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )

    # Products & Prices

    async def list_products(self, active: bool = True) -> List[stripe.Product]:
        """List Stripe products"""
        return stripe.Product.list(active=active).data

    async def list_prices(
        self,
        product_id: Optional[str] = None,
        active: bool = True
    ) -> List[stripe.Price]:
        """List prices for a product"""
        params = {"active": active}
        if product_id:
            params["product"] = product_id

        return stripe.Price.list(**params).data

    # Connect (for creator payouts)

    async def create_transfer(
        self,
        amount: int,
        currency: str,
        destination: str,
        metadata: Optional[Dict] = None
    ) -> stripe.Transfer:
        """Create a transfer to a Connect account"""
        return stripe.Transfer.create(
            amount=amount,
            currency=currency,
            destination=destination,
            metadata=metadata or {}
        )

    async def create_payout(
        self,
        amount: int,
        currency: str,
        metadata: Optional[Dict] = None
    ) -> stripe.Payout:
        """Create a payout"""
        return stripe.Payout.create(
            amount=amount,
            currency=currency,
            metadata=metadata or {}
        )

    # Utility

    def cents_to_roadcoin(self, cents: int) -> float:
        """
        Convert Stripe cents to RoadCoin.

        Per 13-ROADCOIN.md: $1 = 100 RC
        So: 100 cents = 100 RC
        """
        return float(cents)

    def roadcoin_to_cents(self, roadcoin: float) -> int:
        """
        Convert RoadCoin to Stripe cents.

        Per 13-ROADCOIN.md: 100 RC = $0.90 (after 10% fee)
        """
        return int(roadcoin * 0.9)  # 10% platform fee
