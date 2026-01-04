# 🎯 Gumroad Setup Guide - MVAI Connexx

**Simpel, professioneel, direct geld verdienen!**

Gumroad → PayPal (info@mindvault-ai.com) → Later Stripe (na KVK)

---

## Waarom Gumroad?

✅ **Geen KVK nodig** - direct starten
✅ **PayPal integratie** - na $100 verkopen
✅ **Geen maandelijkse kosten** - alleen % per verkoop
✅ **iDEAL + creditcard** - NL markt ready
✅ **Automatische facturen** - BTW handling

**Kosten:** 10% + €0,30 per transactie (daalt naar 3,5% + €0,30 na Gumroad Membership)

---

## 📋 Setup Stappen (15 minuten)

### 1. Gumroad Account Aanmaken
1. Ga naar https://gumroad.com/
2. Sign up met **info@mindvault-ai.com**
3. Bevestig email
4. Kies username: **mindvault-ai**

### 2. PayPal Koppelen
1. Gumroad Dashboard → Settings → Payments
2. Connect PayPal account (info@mindvault-ai.com)
3. **Let op:** PayPal wordt pas actief na $100 verkopen via Gumroad

### 3. Producten Aanmaken

Maak 5 producten aan in Gumroad:

#### Product 1: MVAI Connexx - Particulier
- **Name:** MVAI Connexx - Particulier
- **Price:** €19/maand (recurring)
- **Permalink:** mvai-particulier
- **Description:**
  ```
  MVAI Connexx - Particulier Tier

  Perfect voor particulieren en zelfstandigen

  ✅ 500 logs per maand
  ✅ Basic analytics
  ✅ CSV export
  ✅ Mobile app toegang

  Maandelijks opzegbaar
  ```
- **Type:** Membership (recurring)
- **Billing:** Monthly

#### Product 2: MVAI Connexx - MKB (POPULAIR)
- **Name:** MVAI Connexx - MKB
- **Price:** €49/maand
- **Permalink:** mvai-mkb
- **Description:**
  ```
  MVAI Connexx - MKB Tier

  Ideaal voor MKB bedrijven (1-50 medewerkers)

  ✅ 5.000 logs per maand
  ✅ Advanced analytics
  ✅ API access
  ✅ Priority support

  Maandelijks opzegbaar
  ```
- **Type:** Membership (recurring)
- **Billing:** Monthly

#### Product 3: MVAI Connexx - Starter
- **Name:** MVAI Connexx - Starter
- **Price:** €29/maand
- **Permalink:** mvai-starter
- **Description:**
  ```
  MVAI Connexx - Starter Tier

  Starter pakket voor kleine bedrijven

  ✅ 1.000 logs per maand
  ✅ Basic analytics
  ✅ CSV export

  Maandelijks opzegbaar
  ```
- **Type:** Membership (recurring)
- **Billing:** Monthly

#### Product 4: MVAI Connexx - Professional
- **Name:** MVAI Connexx - Professional
- **Price:** €99/maand
- **Permalink:** mvai-professional
- **Description:**
  ```
  MVAI Connexx - Professional Tier

  Professional pakket voor groeiende bedrijven

  ✅ 10.000 logs per maand
  ✅ Advanced analytics
  ✅ API access
  ✅ AI Assistant

  Maandelijks opzegbaar
  ```
- **Type:** Membership (recurring)
- **Billing:** Monthly

#### Product 5: MVAI Connexx - Enterprise
- **Name:** MVAI Connexx - Enterprise
- **Price:** €299/maand
- **Permalink:** mvai-enterprise
- **Description:**
  ```
  MVAI Connexx - Enterprise Tier

  Enterprise pakket met 99.9% SLA garantie

  ✅ 100.000 logs per maand
  ✅ All features
  ✅ Dedicated support
  ✅ Custom integration
  ✅ SLA guarantee

  Maandelijks opzegbaar
  ```
- **Type:** Membership (recurring)
- **Billing:** Monthly

### 4. Webhook Configureren

**Let op:** Dit is cruciaal voor automatische tier activatie!

1. Gumroad Dashboard → Settings → Advanced
2. Ping URL: `https://jouw-domein.com/webhooks/gumroad`
   - Vervang `jouw-domein.com` met je Fly.io URL
   - Bijv: `https://mvai-connexx.fly.dev/webhooks/gumroad`
3. Test de webhook met een test sale

**Webhook Events:**
- `sale` - Nieuwe verkoop (activeer tier)
- `subscription_ended` - Subscription geannuleerd (downgrade naar demo)
- `subscription_updated` - Tier change

### 5. URLs Toevoegen aan .env

Na het aanmaken van producten, kopieer de URLs:

```bash
# In je .env file:
PAYMENT_PROVIDER=gumroad

GUMROAD_USERNAME=mindvault-ai
GUMROAD_PARTICULIER_URL=https://mindvault-ai.gumroad.com/l/mvai-particulier
GUMROAD_MKB_URL=https://mindvault-ai.gumroad.com/l/mvai-mkb
GUMROAD_STARTER_URL=https://mindvault-ai.gumroad.com/l/mvai-starter
GUMROAD_PROFESSIONAL_URL=https://mindvault-ai.gumroad.com/l/mvai-professional
GUMROAD_ENTERPRISE_URL=https://mindvault-ai.gumroad.com/l/mvai-enterprise
```

---

## 🧪 Testen

### Test Purchase Flow
1. Login op je MVAI Connexx platform
2. Ga naar `/customer/subscription`
3. Klik op "🚀 Upgrade" bij een tier
4. Word doorgestuurd naar Gumroad checkout
5. Gebruik Gumroad test mode voor gratis test
6. Check of webhook terugkomt en tier wordt geactiveerd

### Test Webhook Handmatig
```bash
# Stuur test webhook naar je server:
curl -X POST https://jouw-domein.com/webhooks/gumroad \
  -d "sale_id=test123" \
  -d "product_permalink=mvai-mkb" \
  -d "email=test@example.com" \
  -d "price=49" \
  -d "customer_id=1"
```

---

## 💰 Gumroad vs Stripe

| Feature | Gumroad | Stripe |
|---------|---------|--------|
| **KVK vereist** | ❌ Nee | ✅ Ja |
| **Setup tijd** | 15 min | 2-3 dagen (KVK) |
| **Kosten** | 10% + €0,30 | 1,4% + €0,25 |
| **PayPal** | ✅ Na $100 | ❌ Niet direct |
| **iDEAL** | ✅ Ja | ✅ Ja |
| **Facturen** | ✅ Automatisch | Handmatig |

**Advies:** Start met Gumroad, switch naar Stripe zodra je KVK hebt.

---

## 🚀 Go Live Checklist

- [ ] Gumroad account aangemaakt (info@mindvault-ai.com)
- [ ] PayPal gekoppeld (actief na $100)
- [ ] 5 producten aangemaakt (particulier, mkb, starter, professional, enterprise)
- [ ] Permalinks correct (mvai-particulier, etc.)
- [ ] Webhook geconfigureerd naar `/webhooks/gumroad`
- [ ] URLs getest in browser
- [ ] .env file updated met Gumroad URLs
- [ ] Test purchase gedaan
- [ ] Webhook ontvangen en tier geactiveerd

---

## 📊 Na Eerste $100

Zodra je $100 hebt verkocht via Gumroad:
1. PayPal wordt automatisch actief
2. Uitbetalingen gaan naar info@mindvault-ai.com (PayPal)
3. Facturen worden automatisch verstuurd
4. BTW wordt correct afgehandeld (Gumroad doet dit)

---

## 🔄 Later Upgraden naar Stripe

Zodra je KVK nummer hebt:
1. Stripe account aanmaken met KVK
2. Update .env: `PAYMENT_PROVIDER=stripe`
3. Configureer Stripe producten
4. Migreer bestaande klanten (optioneel)
5. Stripe webhook activeren

**Let op:** Gumroad en Stripe kunnen parallel draaien!

---

## 📧 Support

**Gumroad Support:** https://help.gumroad.com/
**MVAI Connexx Webhook:** `/webhooks/gumroad` in app.py
**Test Gumroad:** https://app.gumroad.com/test-mode

---

**Status:** READY TO SELL VIA GUMROAD! 🚀

**Next:** Maak producten aan in Gumroad dashboard en update .env met echte URLs.
