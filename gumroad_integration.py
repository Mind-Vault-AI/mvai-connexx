"""
MVAI Connexx - Gumroad Payment Integration
Simpel, direct, sales-ready via Gumroad → PayPal

Gumroad Setup:
1. Eerst $100 verkopen via Gumroad
2. Daarna PayPal actief (info@mindvault-ai.com)
3. Later: Stripe (na KVK aanvraag)
"""
import os
from typing import Dict
from unit_economics import PricingConfig

class GumroadService:
    """Handle Gumroad payments - simpel en effectief"""

    def __init__(self):
        self.pricing_tiers = PricingConfig.PRICING_TIERS
        self.gumroad_username = os.getenv('GUMROAD_USERNAME', 'mindvault-ai')

        # Gumroad product URLs (moet je aanmaken in Gumroad dashboard)
        # Format: https://gumroad.com/l/{product-permalink}
        self.product_urls = {
            'particulier': os.getenv('GUMROAD_PARTICULIER_URL', 'https://mindvault-ai.gumroad.com/l/mvai-particulier'),
            'mkb': os.getenv('GUMROAD_MKB_URL', 'https://mindvault-ai.gumroad.com/l/mvai-mkb'),
            'starter': os.getenv('GUMROAD_STARTER_URL', 'https://mindvault-ai.gumroad.com/l/mvai-starter'),
            'professional': os.getenv('GUMROAD_PROFESSIONAL_URL', 'https://mindvault-ai.gumroad.com/l/mvai-professional'),
            'enterprise': os.getenv('GUMROAD_ENTERPRISE_URL', 'https://mindvault-ai.gumroad.com/l/mvai-enterprise')
        }

    def get_checkout_url(self, tier: str, customer_id: int = None, customer_email: str = None) -> str:
        """
        Get Gumroad checkout URL voor tier

        Args:
            tier: Pricing tier (particulier, mkb, etc.)
            customer_id: Optional - voor tracking
            customer_email: Optional - pre-fill email

        Returns:
            Direct Gumroad checkout URL
        """
        if tier == 'demo':
            raise ValueError("Demo tier is gratis - geen checkout nodig")

        if tier not in self.product_urls:
            raise ValueError(f"Ongeldige tier: {tier}")

        base_url = self.product_urls[tier]

        # Add query parameters voor tracking en pre-fill
        params = []

        if customer_email:
            # Pre-fill email in Gumroad checkout
            params.append(f"email={customer_email}")

        if customer_id:
            # Add customer ID voor tracking (komt terug in webhook)
            params.append(f"customer_id={customer_id}")

        if params:
            url = f"{base_url}?{'&'.join(params)}"
        else:
            url = base_url

        return url

    def verify_webhook(self, payload: dict) -> Dict:
        """
        Verify Gumroad webhook (komt na succesvolle verkoop)

        Gumroad stuurt webhook naar: /webhooks/gumroad
        Bevat: sale_id, product_permalink, email, price, etc.

        Returns:
            dict met sale details
        """
        # Gumroad webhook fields
        sale_id = payload.get('sale_id')
        product_permalink = payload.get('product_permalink')
        email = payload.get('email')
        price = payload.get('price')
        customer_id = payload.get('customer_id')  # Our custom field

        # Map product permalink to tier
        tier_mapping = {
            'mvai-particulier': 'particulier',
            'mvai-mkb': 'mkb',
            'mvai-starter': 'starter',
            'mvai-professional': 'professional',
            'mvai-enterprise': 'enterprise'
        }

        tier = tier_mapping.get(product_permalink)

        return {
            'sale_id': sale_id,
            'tier': tier,
            'email': email,
            'price': price,
            'customer_id': customer_id,
            'valid': bool(sale_id and tier)
        }

    def get_tier_info(self, tier: str) -> Dict:
        """Get pricing tier info voor Gumroad product"""
        if tier not in self.pricing_tiers:
            raise ValueError(f"Ongeldige tier: {tier}")

        tier_data = self.pricing_tiers[tier]

        return {
            'tier': tier,
            'name': tier.upper(),
            'price': tier_data['price_per_month'],
            'description': tier_data['description'],
            'included_logs': tier_data['included_logs'],
            'features': tier_data.get('features', []),
            'checkout_url': self.get_checkout_url(tier)
        }


# Convenience functions
gumroad_service = GumroadService()

def get_checkout_url(tier: str, customer_id: int = None, customer_email: str = None) -> str:
    """Get Gumroad checkout URL - direct te gebruiken"""
    return gumroad_service.get_checkout_url(tier, customer_id, customer_email)

def verify_gumroad_webhook(payload: dict) -> Dict:
    """Verify Gumroad webhook - direct te gebruiken"""
    return gumroad_service.verify_webhook(payload)

def get_tier_info(tier: str) -> Dict:
    """Get tier info - direct te gebruiken"""
    return gumroad_service.get_tier_info(tier)
