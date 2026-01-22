# 🚀 Fly.io Deployment Guide - ASAP

## ⚡ Quick Deploy Checklist

Je hebt **fly.toml** al klaarstaan! Volg deze stappen om binnen 10 minuten live te zijn op Fly.io.

---

## 📋 Vereisten

- [ ] Fly.io account (maak gratis aan op https://fly.io/app/sign-up)
- [ ] Terminal toegang (lokaal op je machine)
- [ ] Git repository gecloned

---

## 🔧 Stap 1: Installeer Fly CLI (2 minuten)

### macOS / Linux:
```bash
curl -L https://fly.io/install.sh | sh
```

### Windows (PowerShell als Administrator):
```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Verify installatie:
```bash
fly version
# Should show: flyctl v0.x.x
```

---

## 🔐 Stap 2: Login bij Fly.io (1 minuut)

```bash
fly auth login
```

Dit opent je browser voor authenticatie. Log in met je Fly.io account.

**Verify login:**
```bash
fly auth whoami
# Should show your email
```

---

## 🔍 Stap 3: Check Bestaande App (30 seconden)

```bash
fly apps list
```

**Twee mogelijkheden:**

### A. App bestaat al (mvai-connexx in lijst):
```bash
# Resume suspended app
fly apps resume mvai-connexx

# Of verwijder oude app en maak nieuwe
fly apps destroy mvai-connexx --yes
```

### B. App bestaat niet:
Ga door naar Stap 4.

---

## 🚀 Stap 4: Create/Launch App (2 minuten)

Vanaf de root van je repository:

```bash
cd /pad/naar/mvai-connexx

# Launch met fly.toml configuratie
fly launch --config fly.toml --name mvai-connexx --region ams --no-deploy
```

**Beantwoord prompts:**
- Create .dockerignore? → **No** (hebben we al)
- Create Postgres database? → **No** (we gebruiken SQLite)
- Create Redis database? → **No**
- Deploy now? → **No** (eerst secrets configureren)

---

## 💾 Stap 5: Create Persistent Volume (1 minuut)

Voor database persistentie:

```bash
fly volumes create mvai_data --region ams --size 1
```

**Output:**
```
        ID: vol_xxxxx
      Name: mvai_data
       App: mvai-connexx
    Region: ams
      Zone: xxxx
   Size GB: 1
```

---

## 🔑 Stap 6: Configure Secrets (2 minuten)

### REQUIRED SECRET:

```bash
# Generate strong SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"
# Copy output

# Set SECRET_KEY
fly secrets set SECRET_KEY="PASTE_GENERATED_KEY_HERE"
```

### OPTIONAL SECRETS (voor production):

```bash
# Email notificaties
fly secrets set SMTP_USERNAME="info@mindvault-ai.com"
fly secrets set SMTP_PASSWORD="your-app-password"

# Stripe payments
fly secrets set STRIPE_SECRET_KEY="sk_live_..."
fly secrets set STRIPE_PUBLIC_KEY="pk_live_..."

# Monitoring
fly secrets set SENTRY_DSN="https://...@sentry.io/..."
```

---

## 🚢 Stap 7: Deploy! (3-5 minuten)

```bash
fly deploy
```

**Dit doet:**
1. ✅ Build Docker image (2-3 min)
2. ✅ Push naar Fly.io registry
3. ✅ Create VM in Amsterdam
4. ✅ Mount persistent volume
5. ✅ Start application
6. ✅ Health check
7. ✅ Assign URL: mvai-connexx.fly.dev

**Watch deployment:**
```bash
# In separate terminal
fly logs
```

---

## 🌱 Stap 8: Seed Demo Data (2 minuten)

```bash
# SSH into Fly.io machine
fly ssh console

# Inside container - run:
python seed_demo.py
```

**IMPORTANT:** Save de admin credentials die worden geprint!

```
Admin created!
Username: admin
Access Code: [SAVE THIS CODE!]
```

Type `exit` om SSH sessie te sluiten.

---

## ✅ Stap 9: Test Deployment (1 minuut)

```bash
# Open in browser
fly open
```

Of bezoek direct: **https://mvai-connexx.fly.dev/**

**Test checklist:**
- [ ] Landing page laadt
- [ ] Login pagina werkt
- [ ] Admin login met access code werkt
- [ ] Dashboard toont data

---

## 📊 Stap 10: Monitor & Verify (1 minuut)

```bash
# Check status
fly status

# Expected output:
# Instances
# ID       PROCESS VERSION REGION  STATE   CHECKS          
# xxxxx    app     1       ams     running 1 total, 1 passing

# View logs
fly logs

# Check metrics
fly dashboard
```

---

## 🌐 Custom Domain Setup (Optional)

### Voeg domain toe:
```bash
fly certs add mindvault-ai.com
```

### Configure DNS bij je registrar:
```
Type: A
Name: @
Value: [IP from: fly ips list]
TTL: 3600

Type: AAAA (IPv6)
Name: @
Value: [IPv6 from: fly ips list]
```

### Verify SSL:
```bash
fly certs show mindvault-ai.com
# Wait 5-10 min for Let's Encrypt SSL
```

---

## 🔄 Updates Deployen

Elke keer als je code update:

```bash
git add .
git commit -m "Update feature X"
git push

# Deploy naar Fly.io
fly deploy
```

**Zero-downtime deployment!** Fly.io maakt nieuwe VM, test, dan switch.

---

## 🛠️ Troubleshooting

### App crashed / won't start:
```bash
fly logs --app mvai-connexx
# Check error messages

# Restart app
fly apps restart mvai-connexx
```

### Database errors:
```bash
# Check if volume is mounted
fly volumes list

# SSH and check database
fly ssh console
ls -la /app/data/
```

### Out of memory:
```bash
# Increase RAM in fly.toml:
[[vm]]
  memory_mb = 1024  # Was 512

# Redeploy
fly deploy
```

### Connection timeout:
```bash
# Check health checks
fly checks list

# Verify app is running
fly status
```

---

## 💰 Kosten (Free Tier)

**Fly.io Free Tier:**
- 3 shared-cpu VMs (we gebruiken 1)
- 256MB RAM per VM (we gebruiken 512MB - **$1.94/mo**)
- 3GB persistent volumes (we gebruiken 1GB - gratis)
- 160GB bandwidth/mo

**Totale kosten:** ~**$2/mo** voor production deployment!

**Upgrade opties:**
- 512MB → 1GB RAM: $3.88/mo
- Add 2nd VM (HA): +$1.94/mo
- More regions: Contact Fly.io

---

## 🆚 Fly.io vs Render

| Feature | Fly.io | Render |
|---------|--------|--------|
| **Kosten** | ~$2/mo | Free (met sleep) |
| **Cold Start** | <1s | ~30s |
| **Regions** | 30+ global | Frankfurt only |
| **CLI** | ✅ Excellent | Basic |
| **Auto-Deploy** | ❌ Manual | ✅ GitHub |
| **Database** | Volumes | Disk addon |
| **Performance** | ⚡ Faster | Good |

**Aanbeveling:**
- **Fly.io:** Primary production (performance, global)
- **Render:** Backup/staging (auto-deploy, gratis)

---

## 📞 Support

**Fly.io Issues:**
- Community: https://community.fly.io/
- Docs: https://fly.io/docs/
- Status: https://status.flyio.net/

**MVAI Connexx:**
- Email: info@mindvault-ai.com
- GitHub: https://github.com/Mind-Vault-AI/mvai-connexx

---

## ✅ Post-Deployment Checklist

- [ ] App deployed en draait
- [ ] SSL certificate actief
- [ ] Demo data geseeded
- [ ] Admin login getest
- [ ] Landing page werkt
- [ ] Database persistent
- [ ] Logs monitoren
- [ ] Backup strategie (Render als backup)
- [ ] Custom domain (optioneel)
- [ ] Monitoring setup (Sentry)

---

## 🎉 Success!

**Je MVAI Connexx platform draait nu op:**

🌐 **Fly.io:** https://mvai-connexx.fly.dev/
🌐 **Render:** https://mvai-connexx.onrender.com/ (backup)

**Contact:** info@mindvault-ai.com
**SLA:** 99.9% uptime guarantee
**Deployment:** Amsterdam (Fly.io) + Frankfurt (Render)

**DUAL DEPLOYMENT = HIGH AVAILABILITY!** 🚀

---

*Deployment tijd: ~15 minuten | Kosten: ~$2/mo | Uptime: 99.9%+*
