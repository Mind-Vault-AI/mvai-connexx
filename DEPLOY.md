# MVAI Connexx — Deployment Guide

> **Canonical deploy reference.** Altijd up-to-date. Alle legacy docs staan in [`docs/archive/deploy/`](docs/archive/deploy/).

---

## Inhoudsopgave

1. [Productie — Hostinger VPS (primair)](#1-productie--hostinger-vps-primair)
2. [Productie/Backup — Render (actief)](#2-productiebackup--render-actief)
3. [Lokaal ontwikkelen](#3-lokaal-ontwikkelen)
4. [Database persistence](#4-database-persistence)
5. [Legacy / Gearchiveerd](#5-legacy--gearchiveerd)

---

## 1. Productie — Hostinger VPS (primair)

**Live URL:** [connexx.mindvault-ai.com](https://connexx.mindvault-ai.com)  
**Workflow:** [`.github/workflows/deploy-hostinger.yml`](.github/workflows/deploy-hostinger.yml)  
**Trigger:** push naar `main` of handmatige dispatch via GitHub Actions

### Hoe werkt de pipeline

```
git push origin main
      ↓
GitHub Actions: deploy-hostinger.yml
      ↓
SSH naar Hostinger VPS
      ↓
git pull → pip install → systemctl restart mvai-connexx
      ↓
Live op connexx.mindvault-ai.com ✅
```

### Vereiste GitHub Secrets

Stel deze in via **GitHub repo → Settings → Secrets and variables → Actions**:

| Secret       | Beschrijving                                 |
|--------------|----------------------------------------------|
| `VPS_HOST`   | IP-adres of hostname van de Hostinger VPS    |
| `VPS_USER`   | SSH-gebruikersnaam (bijv. `root` of `ubuntu`)|
| `VPS_SSH_KEY`| Privé SSH-sleutel (RSA of Ed25519)           |

### Server-vereisten (eenmalig)

1. Ubuntu 22.04 LTS op Hostinger VPS (minimaal KVM 1)
2. Python 3.11 + venv geïnstalleerd
3. Repo gecloned naar `/var/www/mvai-connexx`
4. Systemd-service `mvai-connexx` aangemaakt
5. Nginx reverse proxy geconfigureerd voor poort 5000 → 443
6. SSL via Let's Encrypt (Certbot)

### Environment variables op VPS

Het deploy-script maakt automatisch een `.env` aan als die ontbreekt. Minimale set:

```bash
SECRET_KEY=<genereer met: python3 -c 'import secrets; print(secrets.token_hex(32))'>
FLASK_ENV=production
DATABASE_PATH=/var/www/mvai-connexx/data/mvai_connexx.db
```

Optioneel (zet handmatig in `/var/www/mvai-connexx/.env`):

```bash
PAYMENT_PROVIDER=gumroad
OPENAI_API_KEY=sk-proj-...
SMTP_USERNAME=...
SMTP_PASSWORD=...
```

---

## 2. Productie/Backup — Render (actief)

**Config:** [`render.yaml`](render.yaml)  
**Auto-deploy:** push naar `main` → Render deployt automatisch  
**Disk:** persistent 1 GB gemount op `/app/data`

### Render setup (eenmalig)

1. Ga naar [render.com](https://render.com) → Login met GitHub
2. **New → Web Service** → selecteer `Mind-Vault-AI/mvai-connexx`
3. Branch: `main` | Runtime: `Python`
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app --config gunicorn.conf.py`
6. Klik **Create Web Service** — Render leest `render.yaml` automatisch

### Vereiste environment variables (Render dashboard)

| Variabele            | Waarde / Instructie                          |
|----------------------|----------------------------------------------|
| `SECRET_KEY`         | Auto-gegenereerd via `render.yaml`           |
| `FLASK_ENV`          | `production`                                 |
| `DATABASE_PATH`      | `/app/data/mvai_connexx.db`                  |
| `PAYMENT_PROVIDER`   | `gumroad`                                    |
| `OPENAI_API_KEY`     | Stel in als secret in Render dashboard       |
| `GUMROAD_SECRET`     | Stel in als secret in Render dashboard       |
| `SMTP_USERNAME`      | Stel in als secret in Render dashboard       |
| `SMTP_PASSWORD`      | Stel in als secret in Render dashboard       |

### Custom domain (optioneel)

1. Render → Settings → Custom Domains → voeg domein toe
2. Hostinger DNS → CNAME aanmaken naar het Render-adres

---

## 3. Lokaal ontwikkelen

```bash
# Clone en installeer
git clone https://github.com/Mind-Vault-AI/mvai-connexx.git
cd mvai-connexx
pip install -r requirements.txt

# Demo data seeden
python seed_demo.py

# Start development server
python app.py
# Open: http://localhost:5000
```

**Admin login:** gebruik de access code die `seed_demo.py` print.

---

## 4. Database persistence

MVAI Connexx gebruikt **SQLite**. Let op:

| Platform      | Database locatie                                    |
|---------------|-----------------------------------------------------|
| Hostinger VPS | `/var/www/mvai-connexx/data/mvai_connexx.db`        |
| Render        | `/app/data/mvai_connexx.db` (persistent disk 1 GB)  |
| Lokaal        | `./mvai_connexx.db` (project root)                  |

- Hostinger: de `data/` map wordt aangemaakt door het deploy-script.
- Render: de disk is geconfigureerd in `render.yaml` (`mountPath: /app/data`).
- **Maak regelmatig een backup** via `backup.py` voordat je migreert.

---

## 5. Legacy / Gearchiveerd

Alle verouderde deployment docs en scripts zijn gearchiveerd in:

📁 [`docs/archive/deploy/`](docs/archive/deploy/)

| Gearchiveerd bestand                  | Beschrijving                          |
|---------------------------------------|---------------------------------------|
| `DEPLOYMENT.md`                       | Oude uitgebreide handleiding (Render/Fly) |
| `DEPLOYMENT_READY.md`                 | Fly.io deployment checklist           |
| `QUICK_START.txt`                     | Fly.io quick start script             |
| `FLY_DEPLOY.md`                       | Fly.io specifieke handleiding         |
| `FINAL_DEPLOYMENT_GUIDE.md`           | Verouderde volledige gids             |
| `fly.toml`                            | Fly.io configuratie                   |
| `cloudbuild.yaml`                     | Google Cloud Build configuratie       |
| `render.yaml` (archive)               | Oude Render config (Docker-based)     |
| `DEPLOY_NOW.sh`, `DEPLOY_SIMPLE.sh`   | Verouderde deploy scripts             |
| `PRE_DEPLOY_CHECK.md`                 | Verouderde pre-deploy checklist       |
| `AUTODEPLOY_SETUP.md`                 | Verouderde auto-deploy setup          |

> Deze bestanden zijn bewaard voor referentie, maar zijn **niet actief**.
