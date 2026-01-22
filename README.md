# MVAI Connexx - Multi-Tenant Enterprise Platform

## 📋 Overzicht

MVAI Connexx is een **production-ready multi-tenant platform** voor logistieke data borging en procesoptimalisatie. Het systeem biedt veilige, geïsoleerde omgevingen voor meerdere klanten met professioneel dashboard, analytics en export functionaliteit.

## ✨ Features

### 🔐 Authentication & Security
- **Access code authenticatie** voor klanten en admins
- **Session management** met 24-uur expiratie
- **Multi-tenant isolatie** - elke klant ziet alleen eigen data
- **IP tracking** via X-Forwarded-For headers (proxy-aware)

### 👥 Customer Dashboard
- Real-time data input via terminal interface
- Live statistieken (totaal logs, vandaag, deze week)
- Data visualisatie en overzichten
- **CSV export** van alle data
- Zoekfunctionaliteit in eigen logs
- Mobile-optimized UI (Samsung S23 Plus getest)

### 👨‍💼 Admin Panel
- Overzicht alle klanten en data
- Klantenbeheer (toevoegen, activeren/deactiveren)
- **Automatische access code generatie**
- Globale statistieken en analytics
- Top 5 actiefste klanten
- Zoeken in klanten en logs
- **CSV export** van alle data

### 🎨 Professional UI/UX
- Modern **dark theme** (MVAI branding)
- Mobile-first responsive design
- Terminal-style data input interface
- Clean en intuitive navigation
- Samsung S23 Plus geoptimaliseerd

### 💳 Subscription & Payments (NIEUW!)
- **6 Pricing Tiers** (Demo, Particulier, MKB, Starter, Professional, Enterprise)
- **Gumroad integratie** - PayPal backend (info@mindvault-ai.com)
- **Automatic tier activation** via webhooks
- **Usage tracking** met real-time limits
- **Self-service upgrades/downgrades**
- **Email notifications** (welcome, upgrades, alerts)
- **Stripe ready** (voor later, na KVK)

### 💾 Database
- **SQLite** database met multi-tenant schema
- Automatische migratie van JSON naar SQLite
- Efficient indexing voor performance
- Foreign key constraints voor data integriteit

## 🚀 Quick Start

### 1. Installatie

```bash
# Clone repository
git clone https://github.com/Mind-Vault-AI/mvai-connexx.git
cd mvai-connexx

# Installeer dependencies
pip install -r requirements.txt
```

### 2. Demo Data Seeding

Voor een snelle demo met fictieve bedrijven:

```bash
python seed_demo.py
```

Dit maakt aan:
- 1 admin account
- 5 demo klanten (TransLog Nederland, VanderMeer Logistics, etc.)
- 50+ fictieve log entries

**Login credentials worden geprint na seeding!**

### 3. Start Applicatie

```bash
# Development
python app.py

# Production (met Gunicorn)
gunicorn --bind 0.0.0.0:5000 app:app
```

Open browser: `http://localhost:5000`

### 4. Migratie van Bestaande Data (optioneel)

Als je bestaande `mvai_data.json` hebt:

```bash
python migrate.py
```

Dit migreert alle JSON logs naar SQLite en maakt een backup.

## 📁 Project Structuur

```
mvai-connexx/
├── app.py                 # Flask applicatie (multi-tenant)
├── database.py            # Database module (SQLite)
├── migrate.py             # JSON → SQLite migratie script
├── seed_demo.py           # Demo data seeding
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container
├── templates/
│   ├── login.html         # Login pagina
│   ├── customer_dashboard.html
│   ├── customer_logs.html
│   ├── customer_search.html
│   ├── admin_dashboard.html
│   ├── admin_customers.html
│   ├── admin_customer_detail.html
│   ├── admin_create_customer.html
│   ├── admin_logs.html
│   ├── admin_search.html
│   └── error.html
└── mvai_connexx.db        # SQLite database (aangemaakt bij eerste run)
```

## 🗄️ Database Schema

### Customers
- `id` - Primary key
- `name` - Bedrijfsnaam (unique)
- `access_code` - Unieke login code
- `status` - active/inactive
- `contact_email` - Contact email
- `company_info` - Extra info/notities
- `created_at` - Timestamp

### Logs
- `id` - Primary key
- `customer_id` - Foreign key naar customers
- `ip_address` - Client IP (X-Forwarded-For aware)
- `timestamp` - Log tijdstip
- `data` - JSON data
- `metadata` - Extra metadata (optioneel)

### Admins
- `id` - Primary key
- `username` - Admin gebruikersnaam
- `access_code` - Admin login code
- `created_at` - Timestamp

## 🔧 API Endpoints

### Public Routes
- `GET /` - Redirect naar login/dashboard
- `GET /login` - Login pagina
- `POST /login` - Login verwerking
- `GET /logout` - Uitloggen

### Customer Routes (login required)
- `GET /dashboard` - Customer dashboard
- `POST /api/save` - Data opslaan (backward compatible)
- `GET /customer/logs` - Alle logs bekijken
- `GET /customer/export/csv` - CSV export
- `GET /customer/search` - Zoeken in logs

### Admin Routes (admin required)
- `GET /admin` - Admin dashboard
- `GET /admin/customers` - Klantenoverzicht
- `GET /admin/customer/<id>` - Klant details
- `GET /admin/customer/create` - Nieuwe klant aanmaken
- `POST /admin/customer/<id>/toggle-status` - Status toggle
- `GET /admin/logs` - Alle logs
- `GET /admin/search` - Zoeken
- `GET /admin/export/all-csv` - Volledige CSV export

## 🚀 Production Deployment

### Hostinger VPS Deployment (Aanbevolen)

**Complete deployment guide:** Zie `HOSTINGER_DEPLOYMENT.md`

**Quick start:**
1. VPS huren bij Hostinger (€5.99/maand)
2. SSH naar server
3. Clone repo + install dependencies
4. Setup Gunicorn service
5. Configure Nginx reverse proxy
6. SSL certificaat (gratis Let's Encrypt)

**Total setup tijd:** ~35 minuten
**Kosten:** €5.99/maand
**Support:** Hostinger 24/7 Nederlands

### Lokaal Testen (Docker)

```bash
docker build -t mvai-connexx .
docker run -p 5000:5000 -e PAYMENT_PROVIDER=gumroad mvai-connexx
# Open: http://localhost:5000
```

## 🔐 Security Features

- ✅ **Geen hardcoded credentials** - access codes worden random gegenereerd
- ✅ **Session-based authentication** met secure cookies
- ✅ **Multi-tenant data isolatie** op database niveau
- ✅ **IP tracking** voor audit trail
- ✅ **Input sanitization** via Flask
- ✅ **SQL injection protection** via parameterized queries
- ✅ **XSS protection** via template escaping

## 📊 Admin Functies

### Nieuwe Klant Aanmaken

1. Login als admin
2. Ga naar "Klanten" → "Nieuwe Klant"
3. Vul bedrijfsnaam in (verplicht)
4. Optioneel: email en bedrijfsinfo
5. Klik "Klant Aanmaken"
6. **Access code wordt automatisch gegenereerd en getoond!**
7. Deel deze code veilig met de klant

### Klant Deactiveren

1. Ga naar klant detail pagina
2. Klik "Deactiveer Klant"
3. Klant kan niet meer inloggen (data blijft behouden)

### Data Exporteren

**Per klant (admin):**
- Ga naar klant detail → CSV export knop

**Alle data (admin):**
- Admin Dashboard → "Exporteer CSV"

**Per klant (customer):**
- Customer Dashboard → "Exporteer CSV"

## 🎯 Roadmap / Toekomstige Features

**✅ GEÏMPLEMENTEERD (production-ready):**
- ✅ **Pricing tiers** - 6 tiers (Demo, Particulier, MKB, Starter, Professional, Enterprise)
- ✅ **Payment processing** - Gumroad integratie (PayPal backend via info@mindvault-ai.com)
- ✅ **Subscriptie logica** - Upgrade/downgrade met automatic tier activation
- ✅ **Email notificaties** - SMTP met professional HTML templates (welcome, upgrade, alerts)

**Payment Strategie:**
- 🎯 **NU:** Gumroad → PayPal (actief na $100 verkopen) - geen KVK vereist
- 🔄 **LATER:** Stripe (zodra KVK nummer beschikbaar) - lagere fees

**Mogelijk in toekomst:**
- 📊 PDF export met grafieken
- 📱 Progressive Web App (PWA)
- 🔔 Real-time notificaties
- 📈 Geavanceerde analytics dashboards
- 🤖 AI-powered insights (basis AI Assistant al aanwezig)

## 🐛 Troubleshooting

### Database locked errors
```bash
# Stop alle processen
pkill -f "python app.py"

# Verwijder database en seed opnieuw
rm mvai_connexx.db
python seed_demo.py
```

### Port already in use
```bash
# Vind proces op poort 5000
lsof -i :5000

# Kill proces
kill -9 <PID>
```

### Import errors
```bash
# Herinstalleer dependencies
pip install --upgrade -r requirements.txt
```

## 📝 Licentie

© 2025 Mind Vault AI. All Rights Reserved.

## 🤝 Support

Voor vragen of issues:
- Email: support@mindvault.ai
- GitHub Issues: https://github.com/Mind-Vault-AI/mvai-connexx/issues

---

**Built with ❤️ by Mind Vault AI**

*Logistic Intelligence | Validatie, Borging & Procesoptimalisatie*
