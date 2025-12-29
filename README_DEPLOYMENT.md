# Fly.io Deployment Handleiding - MVAI Connexx

Deze handleiding legt uit hoe je de MVAI Connexx applicatie gratis kunt deployen op Fly.io, met speciale instructies voor deployment vanaf een Samsung S23 Plus.

## 📋 Vereisten

### 1. Fly.io Account (Gratis)
- Ga naar [fly.io](https://fly.io) in je browser
- Klik op "Sign Up" om een gratis account aan te maken
- Je krijgt:
  - **Gratis compute credits** voor kleine apps
  - **3GB persistent volume** gratis
  - **SSL certificaten** automatisch
  - **Global CDN** included

### 2. Flyctl CLI Installatie (Optioneel)

#### Optie A: Via Termux op Samsung S23 Plus
Als je Termux op je Samsung S23 Plus hebt geïnstalleerd:

```bash
# Installeer curl (indien nog niet geïnstalleerd)
pkg install curl

# Download en installeer flyctl
curl -L https://fly.io/install.sh | sh

# Voeg flyctl toe aan je PATH
echo 'export PATH="$HOME/.fly/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verificatie
flyctl version
```

#### Optie B: Via Fly.io Dashboard (Web Browser)
Je kunt de volledige deployment ook via de Fly.io web interface doen zonder CLI te installeren (zie sectie "Alternatief - Deploy via Dashboard" hieronder).

---

## 🚀 Deployment Stappen (via CLI)

### Stap 1: Login bij Fly.io
```bash
flyctl auth login
```
Dit opent een browser waar je kunt inloggen met je Fly.io account.

### Stap 2: Navigeer naar je Project Directory
```bash
cd /pad/naar/mvai-connexx
```

### Stap 3: Launch de Applicatie
```bash
flyctl launch
```

De CLI zal:
- ✅ Je `fly.toml` configuratie detecteren
- ✅ Een unieke app naam voorstellen (of gebruik `mvai-connexx`)
- ✅ De regio voorstellen (ams = Amsterdam)
- ❓ Vragen of je een PostgreSQL database wilt → **Nee** (wij gebruiken JSON files)
- ❓ Vragen of je een Redis instance wilt → **Nee** (niet nodig)

**Belangrijk:** Zeg **NEE** als de CLI vraagt of je wilt deployen. We doen de eerste deploy pas nadat het volume is aangemaakt.

### Stap 4: Maak een Persistent Volume aan
```bash
flyctl volumes create mvai_data --region ams --size 1
```

Dit creëert een **1GB persistent volume** in Amsterdam voor je JSON data opslag.

**Verificatie:**
```bash
flyctl volumes list
```

### Stap 5: Deploy de Applicatie
```bash
flyctl deploy
```

Dit proces:
1. ✅ Bouwt je Docker image
2. ✅ Uploadt de image naar Fly.io registry
3. ✅ Creëert machines in de Amsterdam regio
4. ✅ Mountt het persistent volume op `/app/data`
5. ✅ Start de applicatie met health checks

**Deployment duurt ongeveer 2-5 minuten.**

### Stap 6: Check de Status
```bash
flyctl status
```

Je zou moeten zien:
```
Instances
ID       PROCESS VERSION REGION  STATE   HEALTH CHECKS  RESTARTS
abc123   web     1       ams     running 1 passing      0
```

### Stap 7: Bekijk je Live Applicatie
```bash
flyctl open
```

Of open handmatig: `https://<jouw-app-naam>.fly.dev`

---

## 🌐 Alternatief - Deploy via Fly.io Dashboard (Zonder CLI)

Voor deployment vanaf je Samsung S23 Plus browser **zonder Termux**:

### Stap 1: Push Code naar GitHub
Zorg dat je project op GitHub staat met alle bestanden:
- `fly.toml`
- `Dockerfile`
- `app.py`
- `requirements.txt`
- `.dockerignore`

### Stap 2: Koppel GitHub aan Fly.io
1. Log in op [fly.io/dashboard](https://fly.io/dashboard)
2. Klik op **"New App"**
3. Selecteer **"Import from GitHub"**
4. Autoriseer Fly.io om toegang te krijgen tot je repository
5. Selecteer de `mvai-connexx` repository

### Stap 3: Configureer de App
1. **App naam:** Kies een unieke naam (bijv. `mvai-connexx-prod`)
2. **Region:** Selecteer `ams` (Amsterdam)
3. **Fly.toml:** Fly.io detecteert automatisch je `fly.toml` bestand

### Stap 4: Maak Volume aan via Dashboard
1. Ga naar je app in het dashboard
2. Klik op **"Volumes"** in het linker menu
3. Klik op **"Create Volume"**
4. **Name:** `mvai_data`
5. **Size:** 1 GB
6. **Region:** ams
7. Klik **"Create"**

### Stap 5: Deploy
1. Klik op **"Deploy"** in je app dashboard
2. Wacht tot de build compleet is (2-5 minuten)
3. Fly.io bouwt automatisch de Docker image en start de app

### Stap 6: Automatische Deployments Instellen
1. Ga naar **Settings → GitHub** in je app dashboard
2. Schakel **"Auto Deploy"** in
3. Nu wordt je app automatisch gedeployd bij elke `git push` naar de main branch

---

## ✅ Verificatie

### 1. Test de Homepage
Open in je browser:
```
https://<jouw-app-naam>.fly.dev/
```

Je zou het **MVAI Dashboard** moeten zien met:
- 🚀 Starter / Demo sectie
- 💎 Enterprise Toolkit sectie
- Terminal interface onderaan

### 2. Test de Health Check
Open in je browser:
```
https://<jouw-app-naam>.fly.dev/health
```

Je zou moeten zien:
```json
{
  "status": "healthy",
  "service": "mvai-connexx"
}
```

### 3. Test Data Opslag
1. Ga naar je app dashboard
2. Scroll naar de terminal textarea onderaan
3. Typ wat tekst in het veld
4. Wacht 1-2 seconden
5. Status zou moeten veranderen naar **"Veilig Geborgd (Cloud Synced)"**

### 4. Verificeer Persistent Volume
```bash
# Via CLI
flyctl ssh console
ls -la /app/data/
cat /app/data/mvai_data.json
```

Of via dashboard:
- Ga naar **Monitoring → Metrics**
- Check of **Volume Usage** actief is

---

## 🔧 Troubleshooting

### Probleem 1: "Port Already in Use"
**Symptoom:** App crasht met port conflict error.

**Oplossing:**
- Fly.io stelt automatisch `PORT=5000` in via `fly.toml`
- Check je `app.py`: `port = int(os.environ.get("PORT", 5000))`
- Dit is al correct geconfigureerd in deze setup

### Probleem 2: Volume Mount Errors
**Symptoom:** App kan niet schrijven naar `/app/data/`.

**Diagnose:**
```bash
flyctl ssh console
ls -la /app/
```

**Oplossing:**
1. Check of het volume correct gemount is:
   ```bash
   flyctl volumes list
   ```
2. Zorg dat het volume de naam `mvai_data` heeft (exact zoals in `fly.toml`)
3. Check volume permissions via SSH:
   ```bash
   flyctl ssh console
   ls -la /app/
   touch /app/data/test.txt  # Test schrijfrechten
   ```
4. Als er permissie problemen zijn, is dit normaal bij eerste mount. Fly.io volumes krijgen automatisch de juiste permissions van de parent directory. De app heeft error handling ingebouwd.
5. Herstart de app:
   ```bash
   flyctl apps restart
   ```

**Note:** De app logt een waarschuwing bij permission errors maar blijft draaien. In de standaard Docker-image worden directory’s eigendom van `mvai_user` gezet, maar bij Fly.io volume mounts kunnen permissieproblemen toch optreden als de volume-ownership niet overeenkomt. Controleer in dat geval de permissions/ownership van het gemounte volume.

### Probleem 3: Health Check Fails
**Symptoom:** App blijft in "unhealthy" state.

**Diagnose:**
```bash
flyctl logs
```

**Oplossing:**
1. Check of `/health` endpoint bereikbaar is:
   ```bash
   curl https://<jouw-app-naam>.fly.dev/health
   ```
2. Controleer of de `grace_period` in `fly.toml` minimaal `20s` is:
   ```toml
   [[http_service.checks]]
     grace_period = "20s"
   ```
3. Deploy opnieuw: `flyctl deploy`

### Probleem 4: App Slaapt (Auto-Stop)
**Symptoom:** App reageert traag na inactiviteit.

**Dit is normaal gedrag voor gratis tier:**
- Apps worden automatisch gestopt na inactiviteit (om kosten te besparen)
- Bij eerste request wordt de app automatisch gestart (cold start ~3-5 seconden)

**Optioneel - Altijd aan (verbruikt meer credits):**
```bash
flyctl scale count 1 --region ams
```

Of wijzig in `fly.toml`:
```toml
[http_service]
  min_machines_running = 1  # Was 0
```

### Probleem 5: Logs Analyseren
**Zie realtime logs:**
```bash
flyctl logs
```

**Zie specifieke timeframe:**
```bash
flyctl logs --since 1h
```

**Filter op errors:**
```bash
flyctl logs | grep ERROR
```

---

## 📱 Samsung S23 Plus Specifieke Tips

### 1. Termux Tips
- **Installeer essentials:**
  ```bash
  pkg install git python openssh
  ```
- **Gebruik landscape mode** voor beter overzicht bij lange commando's
- **Copy/paste:** Lang drukken in Termux voor clipboard menu

### 2. Browser Deployment (Aanbevolen)
- Gebruik **Samsung Internet** of **Chrome** voor beste ervaring
- Bookmark je Fly.io dashboard voor snelle toegang
- Schakel **Desktop Site** modus in voor volledige interface

### 3. GitHub Mobile App
- Installeer **GitHub Mobile** app voor snelle code updates
- Push wijzigingen direct vanuit de app
- Auto-deploy triggert automatisch bij push

---

## 🔐 Security & Best Practices

### 1. Environment Variables (Secrets)
Voor gevoelige data gebruik je Fly.io secrets:
```bash
flyctl secrets set API_KEY=your-secret-key
```

Secrets zijn:
- ✅ Encrypted at rest
- ✅ Niet zichtbaar in logs
- ✅ Alleen beschikbaar in de app runtime

### 2. IP Protection
De app logt IP adressen via `X-Forwarded-For` header:
- Fly.io proxy voegt deze header automatisch toe
- Werkt achter load balancers en CDN
- Let op: IP-adressen worden automatisch gelogd; zorg zelf voor een passende GDPR-compliance (bijv. juiste grondslag, opt-in en privacyverklaring).

### 3. Volume Backups
**Belangrijk:** Maak regelmatig backups van je volume:

```bash
# Maak snapshot
flyctl volumes snapshots create mvai_data

# Lijst snapshots
flyctl volumes snapshots list
```

**Automatische backups (via cron/script):**
```bash
# Download data lokaal
flyctl ssh console -C "cat /app/data/mvai_data.json" > backup_$(date +%Y%m%d).json
```

---

## 💰 Kosten Optimalisatie (Gratis Tier)

Deze configuratie is geoptimaliseerd voor **gratis gebruik**:

✅ **Auto-stop machines:** App stopt automatisch na inactiviteit
✅ **Auto-start machines:** Start automatisch bij inkomend verzoek
✅ **Min machines running = 0:** Geen machines actief als er geen traffic is
✅ **1GB volume:** Valt binnen gratis tier limiet
✅ **Shared CPU:** Gratis compute instances

**Geschatte kosten:** **€0/maand** voor low-traffic apps (<100.000 requests/maand)

### Monitoring Credits
Check je verbruik:
```bash
flyctl dashboard
```

Of via web: [fly.io/dashboard/personal/billing](https://fly.io/dashboard/personal/billing)

---

## 📚 Nuttige Links

- **Fly.io Documentatie:** https://fly.io/docs
- **Fly.io Status:** https://status.fly.io
- **Community Forum:** https://community.fly.io
- **Pricing Calculator:** https://fly.io/docs/about/pricing

---

## 🎯 Volgende Stappen

Na succesvolle deployment:

1. **Custom Domain Koppelen** (optioneel):
   ```bash
   flyctl certs add jouw-domein.nl
   ```

2. **Monitoring Instellen:**
   - Fly.io dashboard → Metrics
   - Bekijk CPU, Memory, Request Rate

3. **CI/CD Instellen:**
   - GitHub Actions voor automated testing
   - Auto-deploy via GitHub integration

4. **Schalen (indien nodig):**
   ```bash
   flyctl scale vm shared-cpu-2x --memory 512
   ```

---

**Succes met je deployment! 🚀**

Voor vragen of problemen: open een issue op GitHub of check de Fly.io community forum.
