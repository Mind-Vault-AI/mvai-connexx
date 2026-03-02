# MVAI Connexx - Deployment (Render)

## Stack
- **Server:** Render (render.com)
- **Code:** GitHub (Mind-Vault-AI/mvai-connexx)
- **Domein:** mindvault-ai.com (via Hostinger DNS)
- **Auto-deploy:** Push naar `main` → Render deployt automatisch

---

## Render Setup (eenmalig)

### Stap 1 - Render account
1. Ga naar https://render.com
2. Login met GitHub account

### Stap 2 - Nieuwe Web Service
1. Klik **New → Web Service**
2. Selecteer GitHub repo: `Mind-Vault-AI/mvai-connexx`
3. Branch: `main`
4. Runtime: `Python`
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app --config gunicorn.conf.py`
7. Plan: **Free** (of Starter $7/maand voor betere performance)

### Stap 3 - Environment Variables
Voeg toe in Render dashboard → Environment:

```
SECRET_KEY         = (genereer zelf, bijv. 32 random tekens)
OPENAI_API_KEY     = sk-proj-...jouw-key...
FLASK_ENV          = production
PAYMENT_PROVIDER   = gumroad
ENABLE_AI_ASSISTANT = true
ENABLE_DEMO_MODE   = true
```

### Stap 4 - Deploy Hook instellen
1. Render dashboard → Settings → Deploy Hook
2. Kopieer de URL
3. GitHub repo → Settings → Secrets → `RENDER_DEPLOY_HOOK`
4. Plak de URL

### Stap 5 - Custom Domain (mindvault-ai.com)
1. Render → Settings → Custom Domains
2. Voeg toe: `mvai-connexx.mindvault-ai.com` (of `app.mindvault-ai.com`)
3. Ga naar Hostinger DNS → voeg CNAME toe die Render aangeeft

---

## Lokaal testen (Windows)

```powershell
cd C:\Users\erik_\Documents\mvai-connexx
python app.py
# Open: http://localhost:5000
```

**Admin login:** http://localhost:5000/login
- Gebruik admin access code (aangemaakt via `python seed_demo.py`)

---

## Auto-deploy flow

```
jij pusht naar main
    ↓
GitHub Actions triggert Render webhook
    ↓
Render bouwt nieuwe versie
    ↓
Live op render URL / mindvault-ai.com
    ↓
Jij doet niets - gaat automatisch!
```

---

## Admin aanmaken (eerste keer)

```powershell
python seed_demo.py
```

Output toont:
```
Admin username: admin
Admin access code: XXXX-XXXX
```

Gebruik deze code om in te loggen op /login
