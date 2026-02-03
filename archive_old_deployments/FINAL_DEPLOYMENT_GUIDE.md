# 🚀 MVAI Connexx - FINAL DEPLOYMENT GUIDE

**Eerlijke status: Alle deployment opties vereisen creditcard.**

---

## 🎯 DEPLOYMENT OPTIES

### Option 1: **RENDER.COM** (Makkelijkst)
**Vereist:** Creditcard (gratis tier beschikbaar)
**Kosten:** €0-7/maand
**Setup tijd:** 5 minuten

#### Stappen:
1. Ga naar https://dashboard.render.com/
2. Sign in met GitHub
3. **New → Web Service**
4. Select repo: `Mind-Vault-AI/mvai-connexx`
5. Branch: `claude/mvai-connexx-multi-tenant-upgrade-8eDvw`
6. Settings (auto-detect):
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn --bind 0.0.0.0:$PORT app:app`
7. Environment variables:
   - `PAYMENT_PROVIDER` = `gumroad`
   - `SECRET_KEY` = (auto-generate of custom)
8. Click **Create Web Service**

**Live in 3-5 minuten!**

---

### Option 2: **GOOGLE CLOUD RUN** (Je hebt al account)
**Vereist:** Creditcard (€300 gratis credit)
**Kosten:** ~€0-5/maand
**Setup tijd:** 10 minuten

#### Via Cloud Console:
1. Ga naar https://console.cloud.google.com/run
2. **CREATE SERVICE**
3. **Deploy from source**
   - Repository: Connect GitHub → `Mind-Vault-AI/mvai-connexx`
   - Branch: `claude/mvai-connexx-multi-tenant-upgrade-8eDvw`
4. Settings:
   - Region: `europe-west1` (Netherlands)
   - Authentication: **Allow unauthenticated**
   - Memory: `1 GiB`
   - CPU: `1`
5. Environment variables:
   - `PAYMENT_PROVIDER` = `gumroad`
   - `FLASK_ENV` = `production`
6. **CREATE**

**Live in 5-7 minuten!**

#### Via gcloud CLI (alternatief):
```bash
cd mvai-connexx

gcloud run deploy mvai-connexx \
  --source . \
  --region=europe-west1 \
  --platform=managed \
  --allow-unauthenticated \
  --memory=1Gi \
  --set-env-vars="PAYMENT_PROVIDER=gumroad,FLASK_ENV=production"
```

---

### Option 3: **FLY.IO**
**Vereist:** Creditcard ($5 gratis credit)
**Kosten:** ~€2/maand
**Setup tijd:** 15 minuten

#### Stappen:
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
fly launch --config fly.toml --name mvai-connexx --region ams --no-deploy
fly volumes create mvai_data --region ams --size 1
fly secrets set SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
fly secrets set PAYMENT_PROVIDER="gumroad"
fly deploy

# Open app
fly open
```

---

### Option 4: **DOCKER LOKAAL** (Voor demo/testing)
**Vereist:** Docker Desktop
**Kosten:** €0
**Setup tijd:** 5 minuten

#### Stappen:
```bash
cd mvai-connexx

# Build image
docker build -t mvai-connexx .

# Run container
docker run -d \
  -p 5000:5000 \
  -e PAYMENT_PROVIDER=gumroad \
  -e SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))') \
  --name mvai-connexx \
  mvai-connexx

# Check logs
docker logs -f mvai-connexx

# Open browser
# http://localhost:5000
```

**Stop container:**
```bash
docker stop mvai-connexx
docker rm mvai-connexx
```

---

## 🔧 POST-DEPLOYMENT SETUP

### 1. Database Seeding
Na eerste deployment, seed demo data:

**Render/Cloud Run:**
Via dashboard → Shell/Console:
```bash
python seed_demo.py
```

**Fly.io:**
```bash
fly ssh console
python seed_demo.py
exit
```

**Save de admin access code!**

### 2. Gumroad Setup (Voor betalingen)
1. Ga naar https://gumroad.com/
2. Sign up: `info@mindvault-ai.com`
3. Create 5 products:
   - `mvai-particulier` (€19/maand)
   - `mvai-mkb` (€49/maand)
   - `mvai-starter` (€29/maand)
   - `mvai-professional` (€99/maand)
   - `mvai-enterprise` (€299/maand)
4. Webhook URL: `https://your-app.com/webhooks/gumroad`
5. PayPal koppelen (actief na $100 verkopen)

### 3. Environment Variables
Minimaal vereist:
- `SECRET_KEY` - Flask session security
- `PAYMENT_PROVIDER` - `gumroad`

Optioneel (email):
- `SMTP_SERVER` - SMTP server
- `SMTP_PORT` - SMTP poort
- `SMTP_USERNAME` - Email username
- `SMTP_PASSWORD` - Email password
- `SMTP_FROM_EMAIL` - Van email adres

---

## 🐛 TROUBLESHOOTING

### "ModuleNotFoundError: No module named 'flask'"
**Lokaal:** `pip install -r requirements.txt`
**Deployment:** Build command moet `pip install -r requirements.txt` bevatten

### "database is locked"
- Gebruik SQLite op persistent volume
- Check concurrent connections
- Restart app

### "SECRET_KEY environment variable required"
- Add `SECRET_KEY` environment variable
- Of: app auto-genereert random key (zie logs)

### App start niet
Check logs:
- **Render:** Dashboard → Logs tab
- **Cloud Run:** Console → Logs Explorer
- **Fly.io:** `fly logs`
- **Docker:** `docker logs mvai-connexx`

---

## ✅ VERIFICATION CHECKLIST

Na deployment, test:

- [ ] App opent in browser
- [ ] Login werkt (use seed_demo.py access code)
- [ ] Customer dashboard werkt
- [ ] `/customer/subscription` pagina laadt
- [ ] Pricing tiers zichtbaar
- [ ] Admin panel werkt

---

## 💰 KOSTEN OVERZICHT

| Platform | Gratis Tier | Paid Tier | Credit Nodig |
|----------|------------|-----------|--------------|
| **Render** | 750 uur/maand | €7/maand | ✅ Ja |
| **Cloud Run** | €300 credit | ~€5/maand | ✅ Ja |
| **Fly.io** | $5 credit | ~€2/maand | ✅ Ja |
| **Docker Lokaal** | Gratis | €0 | ❌ Nee |

**Alle cloud platforms vereisen creditcard, ook voor gratis tier.**

---

## 🎯 AANBEVELING

### Voor verkoop/demo:
**Docker lokaal** - Geen creditcard, direct werkend

### Voor productie:
1. **Google Cloud Run** - Je hebt al account, €300 credit
2. **Render** - Makkelijkst, auto-deploy
3. **Fly.io** - Goedkoopst (€2/maand)

---

## 📞 SUPPORT

**GitHub:** https://github.com/Mind-Vault-AI/mvai-connexx/issues
**Docs:** Zie andere `.md` files in repo
**Email:** info@mindvault-ai.com

---

**Status:** Code is deployment-ready. Kies platform en deploy!
