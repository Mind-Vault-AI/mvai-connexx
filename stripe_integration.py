"""
MVAI Connexx - Stripe Payment Integration
Production-ready subscription management via Stripe

DISABLED: Waiting for KVK - Use Gumroad for now
"""
import os
from typing import Dict, Optional
import config
from unit_economics import PricingConfig

# Optional Stripe import (disabled until KVK)
try:
    import stripe
    # Initialize Stripe only if configured
    if config.Config.STRIPE_SECRET_KEY:
        stripe.api_key = config.Config.STRIPE_SECRET_KEY
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None  # Prevent errors if stripe not installed

class StripePaymentService:
    """Handle Stripe payments and subscriptions"""

    def __init__(self):
        self.pricing_tiers = PricingConfig.PRICING_TIERS
        self.stripe_publishable_key = config.Config.STRIPE_PUBLIC_KEY

    def create_checkout_session(
        self,
        customer_id: int,
        customer_email: str,
        customer_name: str,
        tier: str,
        success_url: str = None,
        cancel_url: str = None
    ) -> Dict:
        """
        Create Stripe Checkout Session for subscription

        Returns:
            dict with 'session_id' and 'checkout_url'
        """
        if tier not in self.pricing_tiers:
            raise ValueError(f"Invalid tier: {tier}")

        tier_data = self.pricing_tiers[tier]

        # Don't allow checkout for free demo tier
        if tier_data['price_per_month'] == 0:
            raise ValueError("Cannot create checkout for free tier")

        # Default URLs
        if not success_url:
            success_url = f"https://{config.Config.DOMAIN}/customer/subscription?success=true"
        if not cancel_url:
            cancel_url = f"https://{config.Config.DOMAIN}/customer/subscription?canceled=true"

        try:
            # Create Stripe Checkout Session
            session = stripe.checkout.Session.create(
                customer_email=customer_email,
                payment_method_types=['card', 'ideal'],  # Card + iDEAL for NL market
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f'MVAI Connexx - {tier.upper()}',
                            'description': tier_data['description'],
                        },
                        'unit_amount': int(tier_data['price_per_month'] * 100),  # Convert to cents
                        'recurring': {
                            'interval': 'month'
                        }
                    },
                    'quantity': 1
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'tier': tier
                },
                allow_promotion_codes=True,  # Allow discount codes
                billing_address_collection='auto',  # Collect billing address
            )

            return {
                'session_id': session.id,
                'checkout_url': session.url,
                'status': 'created'
            }

        except stripe.error.StripeError as e:
            print(f"❌ Stripe error: {e}")
            raise Exception(f"Payment processing error: {str(e)}")

    def create_customer_portal_session(
        self,
        stripe_customer_id: str,
        return_url: str = None
    ) -> Dict:
        """
        Create Customer Portal session for managing subscriptions
        Allows customers to:
        - Update payment methods
        - View invoices
        - Cancel subscriptions
        """
        if not return_url:
            return_url = f"https://{config.Config.DOMAIN}/customer/subscription"

        try:
            session = stripe.billing_portal.Session.create(
                customer=stripe_customer_id,
                return_url=return_url,
            )

            return {
                'portal_url': session.url,
                'status': 'created'
            }

        except stripe.error.StripeError as e:
            print(f"❌ Stripe portal error: {e}")
            raise Exception(f"Portal creation error: {str(e)}")

    def verify_webhook_signature(self, payload: bytes, signature: str) -> Optional[dict]:
        """
        Verify Stripe webhook signature

        Returns:
            Event object if valid, None if invalid
        """
        webhook_secret = config.Config.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            return event
        except ValueError:
            # Invalid payload
            print("❌ Invalid webhook payload")
            return None
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            print("❌ Invalid webhook signature")
            return None

    def handle_webhook_event(self, event: dict) -> Dict:
        """
        Process Stripe webhook events

        Handles:
        - checkout.session.completed: Payment successful
        - customer.subscription.updated: Subscription changed
        - customer.subscription.deleted: Subscription canceled
        - invoice.payment_failed: Payment failed
        """
        event_type = event['type']
        data = event['data']['object']

        result = {
            'event_type': event_type,
            'handled': False,
            'action': None
        }

        if event_type == 'checkout.session.completed':
            # Payment successful - activate subscription
            customer_id = data['metadata'].get('customer_id')
            tier = data['metadata'].get('tier')
            stripe_customer_id = data['customer']

            result['action'] = 'activate_subscription'
            result['customer_id'] = customer_id
            result['tier'] = tier
            result['stripe_customer_id'] = stripe_customer_id
            result['handled'] = True

        elif event_type == 'customer.subscription.updated':
            # Subscription updated (tier change, payment method, etc.)
            customer_id = data['metadata'].get('customer_id')
            status = data['status']

            result['action'] = 'update_subscription'
            result['customer_id'] = customer_id
            result['status'] = status
            result['handled'] = True

        elif event_type == 'customer.subscription.deleted':
            # Subscription canceled
            customer_id = data['metadata'].get('customer_id')

            result['action'] = 'cancel_subscription'
            result['customer_id'] = customer_id
            result['handled'] = True

        elif event_type == 'invoice.payment_failed':
            # Payment failed - send warning email
            customer_id = data['metadata'].get('customer_id')

            result['action'] = 'payment_failed'
            result['customer_id'] = customer_id
            result['handled'] = True

        return result

    def get_subscription_status(self, stripe_customer_id: str) -> Dict:
        """
        Get current subscription status from Stripe

        Returns:
            dict with subscription details
        """
        try:
            subscriptions = stripe.Subscription.list(
                customer=stripe_customer_id,
                status='active',
                limit=1
            )

            if subscriptions.data:
                sub = subscriptions.data[0]
                return {
                    'active': True,
                    'status': sub.status,
                    'current_period_end': sub.current_period_end,
                    'cancel_at_period_end': sub.cancel_at_period_end,
                    'subscription_id': sub.id
                }
            else:
                return {
                    'active': False,
                    'status': 'none'
                }

        except stripe.error.StripeError as e:
            print(f"❌ Stripe subscription status error: {e}")
            return {
                'active': False,
                'status': 'error',
                'error': str(e)
            }

    def cancel_subscription(self, stripe_customer_id: str, immediately: bool = False) -> Dict:
        """
        Cancel subscription

        Args:
            stripe_customer_id: Stripe customer ID
            immediately: If True, cancel immediately. If False, cancel at period end.

        Returns:
            dict with cancellation status
        """
        try:
            subscriptions = stripe.Subscription.list(
                customer=stripe_customer_id,
                status='active',
                limit=1
            )

            if not subscriptions.data:
                return {
                    'success': False,
                    'error': 'No active subscription found'
                }

            sub = subscriptions.data[0]

            if immediately:
                # Cancel immediately
                canceled_sub = stripe.Subscription.delete(sub.id)
                return {
                    'success': True,
                    'canceled_immediately': True,
                    'subscription_id': sub.id
                }
            else:
                # Cancel at period end
                updated_sub = stripe.Subscription.modify(
                    sub.id,
                    cancel_at_period_end=True
                )
                return {
                    'success': True,
                    'canceled_at_period_end': True,
                    'period_end': updated_sub.current_period_end,
                    'subscription_id': sub.id
                }

        except stripe.error.StripeError as e:
            print(f"❌ Stripe cancellation error: {e}")
            return {
                'success': False,
                'error': str(e)
            }


# Convenience functions
payment_service = StripePaymentService()

def create_checkout_session(customer_id, customer_email, customer_name, tier):
    """Create Stripe checkout session - direct te gebruiken"""
    return payment_service.create_checkout_session(
        customer_id, customer_email, customer_name, tier
    )

def handle_webhook(payload, signature):
    """Handle Stripe webhook - direct te gebruiken"""
    event = payment_service.verify_webhook_signature(payload, signature)
    if event:
        return payment_service.handle_webhook_event(event)
    return None

def get_subscription_status(stripe_customer_id):
    """Get subscription status - direct te gebruiken"""
    return payment_service.get_subscription_status(stripe_customer_id)
