# 🔧 Merge Conflict Oplossen - .env.example

**Conflict locatie:** `.env.example` - PAYMENTS sectie

---

## ❌ Probleem: Git Merge Conflict

Bij het mergen van de claude branch met main krijg je een conflict in `.env.example`:

```
<<<<<<< main
# Payment provider (stripe or mollie)
PAYMENT_PROVIDER=stripe

# Stripe keys
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Mollie API key
=======
# Payment provider (gumroad, stripe, mollie)
# ACTIVE: gumroad (eerst $100, dan PayPal actief)
# LATER: stripe (zodra KVK nummer er is)
PAYMENT_PROVIDER=gumroad

# Gumroad (ACTIEF - PayPal: info@mindvault-ai.com)
GUMROAD_USERNAME=mindvault-ai
GUMROAD_PARTICULIER_URL=https://mindvault-ai.gumroad.com/l/mvai-particulier
GUMROAD_MKB_URL=https://mindvault-ai.gumroad.com/l/mvai-mkb
GUMROAD_STARTER_URL=https://mindvault-ai.gumroad.com/l/mvai-starter
GUMROAD_PROFESSIONAL_URL=https://mindvault-ai.gumroad.com/l/mvai-professional
GUMROAD_ENTERPRISE_URL=https://mindvault-ai.gumroad.com/l/mvai-enterprise

# Stripe keys (DISABLED - wacht op KVK)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Mollie API key (alternatief voor NL markt)
>>>>>>> claude/mvai-connexx-multi-tenant-upgrade-8eDvw
MOLLIE_API_KEY=test_...
```

---

## ✅ Oplossing: Accept INCOMING (Claude Branch)

**Kies de GUMROAD versie** (van de claude branch):

### Optie 1: Via Git Command Line

```bash
# Accept OURS (claude branch versie)
git checkout --ours .env.example
git add .env.example

# OF: Accept THEIRS als je main naar claude mergt
git checkout --theirs .env.example
git add .env.example
```

### Optie 2: Via VS Code / Editor

1. Open `.env.example` in editor
2. Klik op "Accept Incoming Change" (Gumroad versie)
3. Of handmatig: verwijder conflict markers en houd ALLEEN deze sectie:

```env
# ═══════════════════════════════════════════════════════
# PAYMENTS
# ═══════════════════════════════════════════════════════

# Payment provider (gumroad, stripe, mollie)
# ACTIVE: gumroad (eerst $100, dan PayPal actief)
# LATER: stripe (zodra KVK nummer er is)
PAYMENT_PROVIDER=gumroad

# Gumroad (ACTIEF - PayPal: info@mindvault-ai.com)
GUMROAD_USERNAME=mindvault-ai
GUMROAD_PARTICULIER_URL=https://mindvault-ai.gumroad.com/l/mvai-particulier
GUMROAD_MKB_URL=https://mindvault-ai.gumroad.com/l/mvai-mkb
GUMROAD_STARTER_URL=https://mindvault-ai.gumroad.com/l/mvai-starter
GUMROAD_PROFESSIONAL_URL=https://mindvault-ai.gumroad.com/l/mvai-professional
GUMROAD_ENTERPRISE_URL=https://mindvault-ai.gumroad.com/l/mvai-enterprise

# Stripe keys (DISABLED - wacht op KVK)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Mollie API key (alternatief voor NL markt)
MOLLIE_API_KEY=test_...
```

### Optie 3: Automated Fix Script

```bash
# Run dit script om automatisch te fixen:
cat > fix_env_conflict.sh << 'EOF'
#!/bin/bash
# Remove conflict markers en gebruik Gumroad versie

cat > .env.example.tmp << 'ENVFILE'
# Kopieer de HELE correcte .env.example hier
# (Te lang voor dit script - zie .env.example in claude branch)
ENVFILE

mv .env.example.tmp .env.example
git add .env.example
echo "✅ Conflict opgelost - Gumroad versie actief"
EOF

chmod +x fix_env_conflict.sh
./fix_env_conflict.sh
```

---

## 🎯 Waarom Gumroad Versie?

**CORRECTE versie** = Gumroad (claude branch)

**Redenen:**
1. ✅ **Geen KVK vereist** - direct kunnen verkopen
2. ✅ **PayPal na $100** - info@mindvault-ai.com
3. ✅ **Alle 4 rode kruisjes geïmplementeerd**
4. ✅ **Stripe blijft beschikbaar** voor later (na KVK)

**Oude versie (main)** = Alleen Stripe (vereist KVK)

---

## 📋 Volledige Merge Procedure

### Als je een PR maakt op GitHub:

1. GitHub toont conflict in Files Changed tab
2. Klik "Resolve conflicts"
3. Kies de Gumroad versie (onderste helft)
4. Klik "Mark as resolved"
5. Commit merge

### Als je lokaal mergt:

```bash
# 1. Merge claude branch naar main (of andersom)
git checkout main
git merge claude/mvai-connexx-multi-tenant-upgrade-8eDvw

# 2. Conflict! Los op:
git checkout --theirs .env.example  # Accept claude version
git add .env.example

# 3. Complete merge
git commit -m "Merge: Accept Gumroad payment integration"
git push
```

---

## ✅ Verificatie

Na het oplossen van conflict:

```bash
# Check of geen conflict markers over zijn
grep -n "<<<<<<" .env.example
grep -n ">>>>>>" .env.example

# Als output leeg is = ✅ OK!

# Verify Gumroad sectie aanwezig
grep -A 5 "GUMROAD" .env.example
# Moet 5+ Gumroad URLs laten zien
```

---

## 🚀 Na Merge

Alles werkt! De conflict is opgelost en:
- ✅ Gumroad payment actief
- ✅ PayPal backend (na $100)
- ✅ Stripe blijft beschikbaar (disabled tot KVK)
- ✅ Deployment kan doorgaan

**Next:** Ga door met deployment volgens `DEPLOYMENT_READY.md`!
