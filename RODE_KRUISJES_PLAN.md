# 🎯 RODE KRUISJES ELIMINEREN - Action Plan

## Status: 4 Features te implementeren

### ❌ 1. Pricing Tiers
**Status:** EIGENLIJK AL KLAAR! ✅
- `unit_economics.py` heeft al 6 pricing tiers
- Demo: €0, Particulier: €19, MKB: €49, Starter: €29, Professional: €99, Enterprise: €299
- **Actie:** Alleen UI toevoegen in customer dashboard

### ❌ 2. Payment Processing
**Status:** Stripe/Mollie integratie nodig
- Stripe API keys al in config.py
- **Actie:** Payment endpoints + checkout flow

### ❌ 3. Subscriptie Logica
**Status:** Database fields al aanwezig
- `pricing_tier` column in customers table
- **Actie:** Upgrade/downgrade functies + billing cycle

### ❌ 4. Email Notificaties
**Status:** SMTP config al klaar
- config.py heeft SMTP settings
- **Actie:** Email templates + send functions

---

## Quick Win Implementation (2 uur werk)

### Phase 1: Pricing Tiers UI (30 min)
```python
# In app.py - customer dashboard
@app.route('/customer/subscription')
def customer_subscription():
    # Show current tier + upgrade options
    current_tier = get_customer_tier(session['customer_id'])
    return render_template('customer_subscription.html',
                         current_tier=current_tier,
                         pricing_tiers=PRICING_TIERS)
```

### Phase 2: Stripe Integration (45 min)
```python
# stripe_integration.py
import stripe
stripe.api_key = config.STRIPE_SECRET_KEY

def create_checkout_session(customer_id, tier):
    session = stripe.checkout.Session.create(
        customer_email=customer.email,
        payment_method_types=['card', 'ideal'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': f'MVAI Connexx - {tier}'},
                'unit_amount': int(PRICING_TIERS[tier]['price_per_month'] * 100),
                'recurring': {'interval': 'month'}
            },
            'quantity': 1
        }],
        mode='subscription',
        success_url='https://mindvault-ai.com/success',
        cancel_url='https://mindvault-ai.com/cancel'
    )
    return session.url
```

### Phase 3: Email Notifications (30 min)
```python
# email_notifications.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_welcome_email(customer_email, access_code):
    msg = MIMEMultipart()
    msg['From'] = config.SMTP_FROM_EMAIL
    msg['To'] = customer_email
    msg['Subject'] = 'Welkom bij MVAI Connexx!'

    body = f"""
    Welkom bij MVAI Connexx!

    Je account is aangemaakt.
    Access Code: {access_code}

    Login: https://mindvault-ai.com/login
    """

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        server.send_message(msg)
```

### Phase 4: Subscription Logic (15 min)
```python
# subscription_manager.py
def upgrade_customer_tier(customer_id, new_tier):
    db.execute("""
        UPDATE customers
        SET pricing_tier = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (new_tier, customer_id))

    # Send email notification
    send_tier_upgrade_email(customer_id, new_tier)

    return True

def check_usage_limits(customer_id):
    customer = get_customer(customer_id)
    tier_limits = PRICING_TIERS[customer['pricing_tier']]

    current_usage = get_monthly_log_count(customer_id)

    if current_usage > tier_limits['included_logs']:
        return {
            'exceeded': True,
            'current': current_usage,
            'limit': tier_limits['included_logs'],
            'overage': current_usage - tier_limits['included_logs']
        }

    return {'exceeded': False}
```

---

## Implementatie Volgorde

**MOET NU (voor launch):**
1. ✅ Email notificaties (SMTP werkt direct)
2. ✅ Pricing tiers UI (data is er al)

**KAN LATER (week 1):**
3. ⏳ Stripe payment (test mode eerst)
4. ⏳ Subscriptie logica (usage tracking)

---

## Development Time

- **Email:** 30 min (send_email.py + templates)
- **Pricing UI:** 30 min (customer_subscription.html)
- **Stripe:** 1 uur (stripe_integration.py + checkout)
- **Subscription:** 30 min (upgrade/downgrade logic)

**TOTAL:** 2.5 uur werk

---

## Wat NU doen?

### Option A: Deploy EERST naar Fly.io (15 min)
Dan kunnen we live testen met echte users

### Option B: Features EERST (2.5 uur)
Alle rode kruisjes weg, dan deployen

### Option C: Quick Win (1 uur)
Email + Pricing UI → Deploy → Stripe later toevoegen

---

**JIJ KIEST!** A, B of C?
