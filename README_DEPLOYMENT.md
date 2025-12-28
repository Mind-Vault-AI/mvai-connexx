# MVAI Connexx - Fly.io Deployment Handleiding

## 📋 Inhoudsopgave

1. [Vereisten](#vereisten)
2. [Fly.io Account Setup](#flyio-account-setup)
3. [CLI Installatie](#cli-installatie)
4. [Deployment Stappen](#deployment-stappen)
5. [Alternatief: Deploy via Browser](#alternatief-deploy-via-browser)
6. [Verificatie](#verificatie)
7. [Troubleshooting](#troubleshooting)
8. [Belangrijke Opmerkingen](#belangrijke-opmerkingen)

---

## 🎯 Vereisten

### Minimale Vereisten
- **Fly.io account** (gratis tier beschikbaar)
- **Git repository** met mvai-connexx code
- **Internet verbinding**

### Optionele Tools
- **Flyctl CLI** (voor command-line deployment)
- **Termux** (voor Samsung S23 Plus deployment)

---

## 🚀 Fly.io Account Setup

### Stap 1: Account Aanmaken
1. Ga naar [fly.io/app/sign-up](https://fly.io/app/sign-up)
2. Registreer met email of GitHub account
3. Bevestig je email adres
4. Voeg creditcard toe (vereist, maar gratis tier kost €0/maand)

### Stap 2: Organisatie Aanmaken
1. Log in op [fly.io/dashboard](https://fly.io/dashboard)
2. Klik op "New Organization" (optioneel, of gebruik personal org)
3. Kies een naam (bijv. "mvai-connexx")

---

## 💻 CLI Installatie

### Optie 1: Linux/Mac (Desktop)
```bash
curl -L https://fly.io/install.sh | sh
```

Voeg toe aan PATH:
```bash
export FLYCTL_INSTALL="$HOME/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"
```

### Optie 2: Windows (Desktop)
Download installer: [fly.io/docs/hands-on/install-flyctl/](https://fly.io/docs/hands-on/install-flyctl/)

Of gebruik PowerShell:
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### Optie 3: Android (Termux op Samsung S23 Plus)

**Installeer Termux:**
1. Download Termux van F-Droid (niet Play Store!)
2. Open Termux

**Installeer benodigdheden:**
```bash
# Update packages
pkg update && pkg upgrade

# Installeer Git, curl, en build tools
pkg install git curl build-essential

# Installeer Flyctl
curl -L https://fly.io/install.sh | sh

# Voeg Flyctl toe aan PATH
echo 'export FLYCTL_INSTALL="$HOME/.fly"' >> ~/.bashrc
echo 'export PATH="$FLYCTL_INSTALL/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Test installatie:**
```bash
flyctl version
```

---

## 📦 Deployment Stappen

### Stap 1: Login bij Fly.io

```bash
flyctl auth login
```

Dit opent een browser voor authenticatie. Op Samsung S23:
- Browser opent automatisch
- Log in met je account
- Keer terug naar Termux

### Stap 2: Clone Repository (indien nodig)

```bash
git clone https://github.com/Mind-Vault-AI/mvai-connexx.git
cd mvai-connexx
```

### Stap 3: Maak Fly.io App Aan

```bash
flyctl launch --no-deploy
```

**Beantwoord de vragen:**
- **App name:** mvai-connexx (of een andere unieke naam)
- **Region:** ams (Amsterdam - dichtbij Nederland)
- **Deploy now?:** NO (we moeten eerst volume aanmaken)

Dit genereert een `fly.toml` bestand (maar wij hebben al een betere versie!).

### Stap 4: **BELANGRIJKSTE STAP** - Maak Persistent Volume Aan

⚠️ **VOOR JE DEPLOY - VOLUME EERST AANMAKEN!**

```bash
flyctl volumes create mvai_data --region ams --size 1
```

Dit maakt een 1GB persistent volume aan voor de database.

**Waarom is dit belangrijk?**
- Zonder volume wordt de database bij elke deploy gewist
- Dit volume slaat de SQLite database permanent op
- 1GB is genoeg voor >100.000 logs

### Stap 5: Deploy de Applicatie

```bash
flyctl deploy
```

Dit:
1. Build de Docker image
2. Upload naar Fly.io
3. Start de applicatie met volume gemount op `/app/data`
4. Voert health checks uit

**Let op:** Eerste deploy kan 2-5 minuten duren.

### Stap 6: Bekijk Status

```bash
flyctl status
```

Output moet "healthy" tonen voor alle instances.

---

## 🌐 Alternatief: Deploy via Browser (Zonder CLI)

### Methode 1: GitHub Integration (Aanbevolen voor Samsung Browser)

**Stap 1: Fork Repository**
1. Ga naar [github.com/Mind-Vault-AI/mvai-connexx](https://github.com/Mind-Vault-AI/mvai-connexx)
2. Klik op "Fork" (maak een eigen kopie)

**Stap 2: Koppel aan Fly.io**
1. Log in op [fly.io/dashboard](https://fly.io/dashboard)
2. Klik op "New App"
3. Selecteer "Deploy from GitHub"
4. Autoriseer GitHub toegang
5. Selecteer je geforkte mvai-connexx repository

**Stap 3: Configureer Deployment**
1. **App name:** kies unieke naam (bijv. mvai-connexx-yourname)
2. **Region:** Amsterdam (ams)
3. **Dockerfile:** Dockerfile (automatisch gedetecteerd)
4. **Build settings:** gebruik standaard settings

**Stap 4: Voeg Volume Toe**
⚠️ **KRITIEK - VOOR EERSTE DEPLOY!**

1. Ga naar App Dashboard → Storage
2. Klik "Create Volume"
3. **Name:** mvai_data
4. **Region:** ams
5. **Size:** 1GB
6. **Mount path:** /app/data
7. Klik "Create"

**Stap 5: Deploy**
1. Klik "Deploy"
2. Wacht tot deployment compleet is (2-5 minuten)
3. Bekijk logs voor errors

### Methode 2: Manual Upload via Fly.io Dashboard

1. Download repository als ZIP
2. Extract lokaal
3. Upload via Fly.io Dashboard (experimentele feature)

---

## ✅ Verificatie

### 1. Check App Status
```bash
flyctl status
```

Moet tonen:
- Status: **healthy**
- Health check: **passing**

### 2. Test Health Endpoint

**Via browser:**
```
https://mvai-connexx.fly.dev/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "mvai-connexx"
}
```

**Via curl (Termux):**
```bash
curl https://mvai-connexx.fly.dev/health
```

### 3. Test Dashboard

Open in browser:
```
https://mvai-connexx.fly.dev/
```

Je moet de MVAI Connexx landing/login pagina zien.

### 4. Check Database Volume

```bash
flyctl volumes list
```

Moet tonen:
- Volume: **mvai_data**
- Size: **1GB**
- Region: **ams**
- Status: **attached**

### 5. Bekijk Logs

```bash
flyctl logs
```

Moet tonen:
- "✓ Data directory aangemaakt: /app/data"
- "✓ Database tabellen aangemaakt"
- Gunicorn server start messages
- Geen errors

---

## 🔧 Troubleshooting

### Probleem 1: "Health check failing"

**Symptoom:**
```
Health check on port 5000 failed
```

**Oplossing:**
1. Check of `/health` endpoint werkt lokaal:
   ```bash
   python app.py
   curl http://localhost:5000/health
   ```
2. Verhoog grace_period in fly.toml:
   ```toml
   [[http_service.checks]]
     grace_period = "30s"  # was 20s
   ```
3. Deploy opnieuw:
   ```bash
   flyctl deploy
   ```

### Probleem 2: "Volume not found"

**Symptoom:**
```
Error: volume mvai_data not found
```

**Oplossing:**
1. Check bestaande volumes:
   ```bash
   flyctl volumes list
   ```
2. Maak volume aan (indien niet bestaat):
   ```bash
   flyctl volumes create mvai_data --region ams --size 1
   ```
3. Deploy opnieuw

### Probleem 3: "Database is locked"

**Symptoom:**
Logs tonen "database is locked" errors

**Oplossing:**
SQLite werkt alleen goed met 1 machine. Check scaling:
```bash
flyctl scale count 1
```

### Probleem 4: "App stops automatically"

**Symptoom:**
App stopt na periode van inactiviteit

**Oorzaak:**
Dit is normaal met `auto_stop_machines = true` in gratis tier.

**Oplossing:**
- App start automatisch bij volgende request
- Eerste request kan 2-5 seconden duren (cold start)
- Voor 24/7 uptime: upgrade naar betaald plan of wijzig fly.toml:
  ```toml
  auto_stop_machines = false
  min_machines_running = 1
  ```

### Probleem 5: "Out of memory"

**Symptoom:**
```
Error: Out of memory
```

**Oplossing:**
Verhoog memory in fly.toml:
```bash
flyctl scale memory 512  # default is 256MB
```

### Probleem 6: "Cannot connect to GitHub"

**Symptoom:**
GitHub integration werkt niet in browser

**Oplossing:**
1. Gebruik flyctl CLI methode (via Termux)
2. Of: Push naar GitHub eerst, dan koppel repository

---

## 📝 Belangrijke Opmerkingen

### Gratis Tier Limieten
- **Compute:** 3 shared-cpu-1x machines (we gebruiken 1)
- **Memory:** 256MB per machine (genoeg voor MVAI Connexx)
- **Storage:** 3GB total persistent volumes (we gebruiken 1GB)
- **Bandwidth:** 160GB uitgaand per maand
- **Kosten:** €0/maand voor deze configuratie

### Security Best Practices

**1. Secret Key Instellen:**
```bash
flyctl secrets set SECRET_KEY=$(openssl rand -hex 32)
```

**2. Admin Credentials Instellen:**
```bash
flyctl secrets set ADMIN_ACCESS_CODE=your-secure-code-here
```

**3. Database Backups:**
```bash
# Backup maken van database
flyctl ssh console
cd /app/data
sqlite3 mvai_connexx.db .dump > backup.sql
exit

# Download backup
flyctl ssh sftp get /app/data/backup.sql ./backup-$(date +%Y%m%d).sql
```

### Database Migratie naar Fly.io

Als je bestaande data hebt:

**Optie 1: Via SSH (Aanbevolen)**
```bash
# Upload lokale database naar Fly.io
flyctl ssh console
cd /app/data
exit

# Upload met sftp
flyctl ssh sftp shell
put mvai_connexx.db /app/data/mvai_connexx.db
quit

# Restart app
flyctl apps restart
```

**Optie 2: Via Seeding Script**
Deploy met lege database, dan seed via browser of API.

### Performance Tips

**1. Enable Persistent Connections:**
Fly.io ondersteunt HTTP Keep-Alive automatisch.

**2. Monitor Logs:**
```bash
flyctl logs -f  # Follow logs real-time
```

**3. Check Metrics:**
```bash
flyctl dashboard metrics
```

### IP Whitelisting

Fly.io geeft je app een dedicated IPv6 en optional IPv4:
```bash
flyctl ips list
```

Gebruik deze voor:
- DNS configuratie
- Firewall whitelists
- API integrations

### Custom Domain

Wil je eigen domein? (bijv. mvai-connexx.nl)

```bash
# Voeg SSL certificaat toe
flyctl certs add mvai-connexx.nl

# Voeg DNS records toe (bij je domain provider):
# A record: @ → [IPv4 van flyctl ips list]
# AAAA record: @ → [IPv6 van flyctl ips list]
```

---

## 🎉 Deployment Compleet!

Je MVAI Connexx app draait nu op Fly.io met:
- ✅ HTTPS enabled
- ✅ Auto-scaling (gratis tier)
- ✅ Persistent database storage
- ✅ Health monitoring
- ✅ Auto-stop/start voor kosten besparing

**Je app is live op:**
```
https://mvai-connexx.fly.dev/
```

---

## 📞 Support

**Fly.io Documentation:**
- [fly.io/docs](https://fly.io/docs)

**MVAI Connexx Issues:**
- GitHub Issues: [github.com/Mind-Vault-AI/mvai-connexx/issues](https://github.com/Mind-Vault-AI/mvai-connexx/issues)

**Community:**
- Fly.io Community: [community.fly.io](https://community.fly.io)

---

**Happy Deploying! 🚀**
