# MVAI Connexx - Deployment Handleiding

## 🚀 ENTERPRISE-GRADE MULTI-TENANT PLATFORM

**MVAI Connexx** is een volledig production-ready enterprise platform met:
- ✅ **Professional Luxury Landing Page** (Stripe/Vercel quality)
- ✅ **Multi-Tenant Architecture** met complete data isolatie
- ✅ **Hybrid Security Fortress** (AI threat detection, incident response)
- ✅ **AI Secretaresse** - Persoonlijke AI assistant per klant
- ✅ **Enterprise GODMODE** - Complete Business Intelligence Suite
- ✅ **ICT Monitoring & Error Reporting** met MTTR tracking
- ✅ **Lean Six Sigma DMAIC** - Quality management framework
- ✅ **Unit Economics** - LTV/CAC, MRR/ARR, Customer profitability
- ✅ **Marketing Intelligence** - Funnel analytics, Channel ROI
- ✅ **Legal Framework** - AVG/GDPR compliant (juridisch dicht getimmerd)
- ✅ **6 Pricing Tiers** - Demo → Particulier → MKB → Professional → Enterprise

**Contact:** info@mindvault-ai.com
**Domain:** mindvault-ai.com (global positioning)
**SLA:** 99.9% uptime guarantee

---

## 📋 Inhoudsopgave

1. [Lokale Deployment](#lokale-deployment)
2. [Fly.io Deployment](#flyio-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Database Setup](#database-setup)
5. [Productie Configuratie](#productie-configuratie)
6. [Enterprise Features Setup](#enterprise-features-setup)
7. [Troubleshooting](#troubleshooting)

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

## 🏢 Enterprise Features Setup

### Landing Page
De professional luxury landing page is automatisch actief op `/`.

**Features:**
- Hero section met trust signals (99.9% uptime, 1000+ customers)
- 6 Feature cards (AI Assistant, Security, Analytics, API, Multi-tenant, BI)
- 3 Product showcase (MVAI Connexx + 2 future products met waitlist)
- 6 Pricing tiers met feature comparison
- Demo/video section (placeholder voor promo video)
- Contact section (info@mindvault-ai.com)
- Professional footer met legal links

**Customization:**
- Update `/templates/landing.html` voor eigen branding
- Voeg promo video toe in demo section
- Pas pricing tiers aan in `unit_economics.py`

### Enterprise Admin Dashboard

Toegang via `/admin/enterprise` (admin login required)

**Dashboards:**
- `/admin/enterprise` - Complete enterprise overview
- `/admin/ict-monitoring` - Error logs, alerts, incidents, MTTR
- `/admin/unit-economics` - MRR, customer profitability, cohort analysis
- `/admin/lean-six-sigma` - Quality metrics, DMAIC projects, Pareto analysis
- `/admin/marketing` - Funnel, channels, segments, growth strategies

**Setup:**
```bash
# Seed demo data voor enterprise metrics
python seed_demo.py

# Of handmatig data toevoegen via API endpoints
curl -X POST http://localhost:5000/api/v1/log \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"data": "your data"}'
```

### ICT Monitoring

**Error Logging:**
```python
from monitoring import ErrorLogger, ErrorSeverity

logger = ErrorLogger()
logger.log_error(
    error_type="DatabaseError",
    message="Connection timeout",
    severity=ErrorSeverity.HIGH,
    component="database",
    stack_trace=traceback.format_exc(),
    customer_id=None  # or specific customer
)
```

**System Health Check:**
```python
from monitoring import SystemHealthMonitor

monitor = SystemHealthMonitor()
health = monitor.get_overall_health()
# Returns: {'overall_status': 'healthy', 'uptime_percentage': 99.9, ...}
```

**Alerts:**
- Auto-generated voor CRITICAL/HIGH severity errors
- Email/webhook notificaties (configure SMTP in config.py)
- MTTR tracking voor incident resolution

### Incident Response

**Emergency Exit Strategy:**
```python
from incident_response import execute_emergency_exit_strategy

result = execute_emergency_exit_strategy(
    reason="Suspected security breach detected"
)
# Automatically: backup DB, enable maintenance, snapshot, alert admins
```

**Automated Response Actions:**
- `BLOCK_IP` - Blacklist malicious IP
- `ENABLE_MAINTENANCE_MODE` - Lock down system
- `BACKUP_DATABASE` - Emergency backup
- `SHUTDOWN_SYSTEM` - Complete shutdown
- `ISOLATE_CUSTOMER` - Suspend customer account
- `RATE_LIMIT_STRICT` - Tighten rate limits
- `ALERT_ADMIN` - Email/SMS admin
- `SNAPSHOT_LOGS` - Forensic evidence

### Unit Economics

**Pricing Tiers (6 levels):**
```python
# In unit_economics.py
PRICING_TIERS = {
    'demo': {'price_per_month': 0.00, 'included_logs': 100},       # 14-day trial
    'particulier': {'price_per_month': 19.00, 'included_logs': 500},   # Freelancers
    'mkb': {'price_per_month': 49.00, 'included_logs': 5000},      # SMB (1-50 employees)
    'starter': {'price_per_month': 29.00, 'included_logs': 1000},
    'professional': {'price_per_month': 99.00, 'included_logs': 10000},
    'enterprise': {'price_per_month': 299.00, 'included_logs': 100000}
}
```

**Customer Profitability:**
```python
from unit_economics import UnitEconomicsCalculator

calc = UnitEconomicsCalculator()
result = calc.calculate_customer_profitability(customer_id=1)
# Returns: LTV, CAC, LTV:CAC ratio, margin, grade (A+ → F)
```

### Lean Six Sigma

**DMAIC Projects:**
```python
from lean_six_sigma import DMAICProject

project = DMAICProject()
project_id = project.create_project(
    title="Reduce API Response Time",
    problem_statement="API responses >500ms for 20% of requests",
    goal="Achieve <200ms for 95% of requests"
)
```

**Quality Metrics:**
- Sigma levels (1σ → 6σ)
- DPM (Defects Per Million)
- Pareto analysis (80/20 rule)
- Continuous improvement recommendations

### Marketing Intelligence

**Funnel Stages:**
```python
from marketing_intelligence import MarketingFunnel

funnel = MarketingFunnel()
metrics = funnel.calculate_funnel_metrics(days=30)
# Returns conversion rates per stage: AWARENESS → INTEREST → CONSIDERATION → TRIAL → PURCHASE
```

**Channel Performance (8 channels):**
- Organic Search, Paid Search, Social Media, Email Marketing
- Content Marketing, Referral, Direct, Partner
- Metrics: CPL, CPA, ROI%, Grade (A+ → D)

**Growth Strategies:**
5 data-driven recommendations based on actual performance

### AI Assistant

**Per-Customer AI:**
```python
from ai_assistant import AIAssistant

assistant = AIAssistant(customer_id=1)
response = assistant.process_query(
    query="What were my top 5 busiest days last month?",
    context={"timezone": "Europe/Amsterdam"}
)
```

**Features:**
- Natural language queries
- Proactive suggestions
- Pattern detection
- Anomaly alerts
- Custom reports

### Security Features

**IP Whitelisting:**
```python
from security import add_ip_to_whitelist

add_ip_to_whitelist(
    ip_address="203.0.113.0/24",  # CIDR supported
    description="Company HQ",
    customer_id=1  # or None for global
)
```

**AI Threat Detection:**
- SQL injection detection
- XSS detection
- Path traversal detection
- Automated blocking (5+ threats → blacklist)

**Honeypot System:**
- Trap endpoints (`/admin.php`, `/wp-login.php`, etc.)
- Auto-blacklist attackers

### Legal Pages

**AVG/GDPR Compliant:**
- `/legal#terms` - Algemene Voorwaarden
- `/legal#privacy` - Privacy Policy (GDPR)
- `/legal#disclaimer` - Disclaimer

**Legal Protection:**
- Max liability: €10,000
- Data retention: 30 days after cancellation
- Customer indemnification
- Nederlands recht applicable

### Environment Variables

**Required for Production:**
```bash
# Flask
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export FLASK_ENV="production"

# Company
export DOMAIN="mindvault-ai.com"
export COMPANY_EMAIL="info@mindvault-ai.com"

# Email (SMTP)
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export SMTP_FROM_EMAIL="info@mindvault-ai.com"

# Payments (Stripe or Mollie)
export PAYMENT_PROVIDER="stripe"
export STRIPE_PUBLIC_KEY="pk_live_..."
export STRIPE_SECRET_KEY="sk_live_..."

# Monitoring (optional)
export SENTRY_DSN="https://...@sentry.io/..."

# Security
export ENABLE_IP_WHITELIST="true"
export ENABLE_THREAT_DETECTION="true"
export ENABLE_HONEYPOT="true"

# Features
export ENABLE_AI_ASSISTANT="true"
export ENABLE_DEMO_MODE="true"
export DEMO_ACCOUNT_EXPIRY_DAYS="14"
```

**Save to `.env` file:**
```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env
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
