# MVAI Connexx - Deployment Handleiding

## 📋 Inhoudsopgave

1. [Lokale Deployment](#lokale-deployment)
2. [Fly.io Deployment](#flyio-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Database Setup](#database-setup)
5. [Productie Configuratie](#productie-configuratie)
6. [Troubleshooting](#troubleshooting)

---

## 🏠 Lokale Deployment

### Vereisten

- Python 3.9 of hoger
- pip (Python package manager)
- Git

### Stap 1: Clone Repository

```bash
git clone https://github.com/Mind-Vault-AI/mvai-connexx.git
cd mvai-connexx
```

### Stap 2: Installeer Dependencies

```bash
pip install -r requirements.txt
```

### Stap 3: Seed Demo Data

```bash
python seed_demo.py
```

**Let op:** Dit maakt demo klanten en een admin account aan. Login credentials worden geprint!

### Stap 4: Start Applicatie

**Development mode:**
```bash
python app.py
```

**Production mode (aanbevolen):**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### Stap 5: Open in Browser

Ga naar: `http://localhost:5000`

---

## ☁️ Fly.io Deployment

### Vereisten

- Fly.io account (gratis tier beschikbaar)
- Fly CLI geïnstalleerd

### Stap 1: Installeer Fly CLI

**macOS/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### Stap 2: Login bij Fly.io

```bash
fly auth login
```

### Stap 3: Maak Fly App aan

```bash
fly launch
```

Beantwoord de vragen:
- **App name:** mvai-connexx (of eigen naam)
- **Region:** Amsterdam (ams) - aanbevolen voor NL
- **Database:** Nee (we gebruiken SQLite)
- **Deploy now:** Nee (eerst configuratie)

### Stap 4: Configureer fly.toml

De `fly.toml` zou moeten bestaan. Verifieer deze instellingen:

```toml
app = "mvai-connexx"
primary_region = "ams"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "5000"

[http_service]
  internal_port = 5000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

### Stap 5: Deploy

```bash
fly deploy
```

### Stap 6: Seed Demo Data (Remote)

```bash
# SSH naar je Fly machine
fly ssh console

# Binnen de container:
cd /app
python seed_demo.py

# Exit
exit
```

### Stap 7: Open Applicatie

```bash
fly open
```

Of bezoek: `https://mvai-connexx.fly.dev` (vervang met jouw app naam)

### Stap 8: Check Logs

```bash
fly logs
```

### Productie Secret Key Instellen

**BELANGRIJK voor productie:**

```bash
# Genereer random secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Stel in als Fly secret
fly secrets set SECRET_KEY="<generated-key>"

# Deploy opnieuw
fly deploy
```

---

## 🐳 Docker Deployment

### Lokaal Docker Deployment

**Build image:**
```bash
docker build -t mvai-connexx:latest .
```

**Run container:**
```bash
docker run -d \
  --name mvai-connexx \
  -p 5000:5000 \
  -e SECRET_KEY="your-secret-key" \
  mvai-connexx:latest
```

**Seed demo data:**
```bash
docker exec -it mvai-connexx python seed_demo.py
```

**Stop container:**
```bash
docker stop mvai-connexx
docker rm mvai-connexx
```

### Docker met Volume (Persistente Database)

**Maak volume:**
```bash
docker volume create mvai-data
```

**Run met volume:**
```bash
docker run -d \
  --name mvai-connexx \
  -p 5000:5000 \
  -v mvai-data:/app/data \
  -e SECRET_KEY="your-secret-key" \
  mvai-connexx:latest
```

**Note:** Pas `app.py` aan om database naar `/app/data/mvai_connexx.db` te schrijven.

---

## 🗄️ Database Setup

### Nieuwe Database (Demo Data)

```bash
python seed_demo.py
```

Dit maakt:
- SQLite database (`mvai_connexx.db`)
- 1 admin account
- 5 demo klanten
- 50+ demo logs

### Migratie van JSON Data

Als je bestaande `mvai_data.json` hebt:

```bash
python migrate.py
```

Dit:
1. Maakt SQLite database aan
2. Migreert alle JSON logs
3. Maakt "Legacy Data" klant aan
4. Backup van JSON naar `mvai_data.json.backup.TIMESTAMP`

### Handmatig Admin Aanmaken

```bash
python -c "
import database as db
db.init_db()
admin = db.create_admin('admin', 'jouw-wachtwoord')
print(f'Admin access code: {admin[\"access_code\"]}')
"
```

### Handmatig Klant Aanmaken

```bash
python -c "
import database as db
db.init_db()
customer = db.create_customer('Bedrijfsnaam', 'email@example.com')
print(f'Access code: {customer[\"access_code\"]}')
"
```

---

## ⚙️ Productie Configuratie

### Environment Variables

| Variable | Beschrijving | Default | Productie |
|----------|--------------|---------|-----------|
| `SECRET_KEY` | Flask secret key voor sessions | `dev-secret-key-change-in-production` | **VERPLICHT AANPASSEN** |
| `PORT` | Poort waarop app draait | `5000` | `5000` (of Fly.io assigned) |

### Secret Key Genereren

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Gunicorn Productie Settings

**Aanbevolen productie commando:**

```bash
gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 4 \
  --worker-class sync \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  app:app
```

**Workers berekenen:**
- Formula: `(2 x CPU cores) + 1`
- Voorbeeld: 2 cores = 5 workers

### HTTPS / SSL

**Fly.io:**
- Automatisch HTTPS via Let's Encrypt
- Force HTTPS in `fly.toml` met `force_https = true`

**Eigen server:**
- Gebruik reverse proxy (Nginx, Caddy)
- Laat proxy SSL afhandelen
- Proxy naar Gunicorn op localhost:5000

### Database Backup

**Automatische backup script:**

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"
DB_FILE="mvai_connexx.db"

mkdir -p $BACKUP_DIR
cp $DB_FILE "$BACKUP_DIR/mvai_connexx_$DATE.db"

# Houd laatste 7 dagen
find $BACKUP_DIR -name "mvai_connexx_*.db" -mtime +7 -delete

echo "Backup aangemaakt: $BACKUP_DIR/mvai_connexx_$DATE.db"
```

**Cron job (dagelijks om 3:00):**
```bash
0 3 * * * /path/to/backup.sh
```

---

## 🐛 Troubleshooting

### Database Locked

**Probleem:** `database is locked` error

**Oplossing:**
```bash
# Stop alle processen
pkill -f "python app.py"
pkill -f "gunicorn"

# Restart
gunicorn --bind 0.0.0.0:5000 app:app
```

### Port Al In Gebruik

**Probleem:** `Address already in use`

**Oplossing:**
```bash
# Vind proces
lsof -i :5000

# Of op Linux:
netstat -tulpn | grep 5000

# Kill proces
kill -9 <PID>
```

### Import Errors

**Probleem:** `ModuleNotFoundError: No module named 'flask'`

**Oplossing:**
```bash
pip install --upgrade -r requirements.txt
```

### Database Corruptie

**Oplossing:**
```bash
# Maak backup
cp mvai_connexx.db mvai_connexx.db.corrupted

# Verwijder database
rm mvai_connexx.db

# Seed opnieuw
python seed_demo.py
```

### Fly.io Out of Memory

**Probleem:** App crashed, "out of memory"

**Oplossing:**
```bash
# Verhoog memory in fly.toml
[[vm]]
  memory_mb = 512  # Was 256

# Deploy opnieuw
fly deploy
```

### Sessions Verlopen Snel

**Probleem:** Gebruikers worden vaak uitgelogd

**Check:**
- `SECRET_KEY` moet persistent zijn (niet wijzigen bij deploy)
- Session timeout: 24 uur (configureerbaar in `app.py`)

**Wijzig timeout in `app.py`:**
```python
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=48)  # 48 uur
```

---

## 📊 Monitoring & Logs

### Fly.io Logs

```bash
# Real-time logs
fly logs

# Laatste 100 regels
fly logs --lines 100

# Filter op niveau
fly logs --level error
```

### Lokale Logs

Gunicorn print automatisch naar stdout/stderr.

**Log naar bestand:**
```bash
gunicorn \
  --bind 0.0.0.0:5000 \
  --access-logfile access.log \
  --error-logfile error.log \
  app:app
```

---

## 🔐 Security Checklist

- [ ] `SECRET_KEY` aangepast (niet default)
- [ ] HTTPS enabled (Fly.io: automatisch)
- [ ] Admin access codes veilig opgeslagen
- [ ] Klant access codes veilig gedeeld
- [ ] Database backups ingesteld
- [ ] Error pages tonen geen debug info
- [ ] Gunicorn in productie mode
- [ ] Firewall regels ingesteld (alleen 443/80)

---

## 📈 Schaalbaarheid

### Fly.io Scaling

**Verticaal (meer resources per machine):**
```bash
# In fly.toml
[[vm]]
  memory_mb = 512
  cpus = 2
```

**Horizontaal (meer machines):**
```bash
fly scale count 3  # 3 machines
```

**Auto-scaling:**
```toml
# In fly.toml
[http_service]
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1
```

### Database Scaling

**Huidige setup:** SQLite (tot ~100k requests/dag)

**Voor grotere load:**
- Migreer naar PostgreSQL
- Gebruik Fly.io Postgres addon
- Update `database.py` voor PostgreSQL support

---

## ✅ Post-Deployment Checklist

1. [ ] App is bereikbaar via URL
2. [ ] Login werkt (admin + customer)
3. [ ] Data kan worden opgeslagen
4. [ ] Export functionaliteit werkt
5. [ ] Admin kan klanten aanmaken
6. [ ] HTTPS werkt (groene slot)
7. [ ] Mobiel responsive (test op telefoon)
8. [ ] Logs zijn leesbaar
9. [ ] Database backups draaien
10. [ ] Access codes veilig gedeeld met klanten

---

## 📞 Support

**Vragen over deployment?**
- GitHub Issues: https://github.com/Mind-Vault-AI/mvai-connexx/issues
- Email: support@mindvault.ai

---

**Veel succes met de deployment! 🚀**

*MVAI Connexx | Enterprise Multi-Tenant Platform*
