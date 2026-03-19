# MVAI Connexx - Production Readiness Backlog

**Datum:** 2026-03-19
**Doel:** App marktklaar maken voor verkoop (99.9% SLA)
**Status:** Ingepland

---

## KRITIEK - App start niet goed op

- [ ] `requirements.txt` compleet maken (flask-limiter ontbreekt, structlog exact pin verwijderen)
- [ ] `.env.example` fixen: `PAYMENT_PROVIDER=gumroad` (niet stripe)
- [ ] Duplicate `retry_on_locked` functie in `database.py` verwijderen

## HOOG - Security & Auth

- [ ] Admin authenticatie versterken: wachtwoord + lockout mechanisme
- [ ] Session security: `SESSION_COOKIE_SAMESITE` naar `Strict`, lifetime naar 4 uur
- [ ] API key query parameter support verwijderen (security risico)
- [ ] API keys hashen voor opslag (niet plaintext in DB)
- [ ] Gumroad webhook signature verificatie implementeren
- [ ] CSRF token protection toevoegen (Flask-WTF)
- [ ] `PRAGMA foreign_keys=ON` toevoegen in database.py
- [ ] Default admin wachtwoord `admin123` forceren om te wijzigen bij eerste login

## HOOG - Stabiliteit & Error Handling

- [ ] Error handling in `/api/save` - geen `str(e)` naar client lekken
- [ ] Error handling in Gumroad webhook - geen payload loggen
- [ ] Email notificaties: graceful fallback + dashboard alerts als SMTP niet geconfigureerd
- [ ] Health check (`/health`) uitbreiden met database connectivity check
- [ ] Sentry/error tracking standaard activeren in productie

## MEDIUM - Database & Schaalbaarheid

- [ ] SQLite evalueren vs PostgreSQL migratie voor concurrency
- [ ] Connection pooling implementeren
- [ ] Database backup strategie automatiseren
- [ ] Gunicorn workers > 1 + Redis voor rate limiting
- [ ] Database migratie systeem (Alembic) opzetten

## MEDIUM - Code Quality

- [ ] Alle `print()` statements vervangen door structured logging
- [ ] Hardcoded URLs (`mindvault-ai.com`) vervangen door `Config.DOMAIN`
- [ ] Ongebruikte dependencies verwijderen (`flask-socketio`)
- [ ] AI assistant error handling verbeteren (geen silent failures)
- [ ] Input validatie op alle endpoints

## LAAG - Nice to Have

- [ ] 2FA/TOTP support voor admin
- [ ] API key scopes (read-only, write, export)
- [ ] API key expiratie mechanisme
- [ ] Blue-green deployment in CI/CD
- [ ] Distributed tracing (OpenTelemetry)
- [ ] Webhook retry logic

## Deployment

- [ ] GitHub Actions workflow: health check na deploy toevoegen
- [ ] Graceful reload (niet hard restart) bij deployment
- [ ] Rollback mechanisme documenteren
- [ ] Environment variable validatie voor deploy

---

**Geschatte doorlooptijd:** 2-3 dagen intensief werk
**Prioriteit:** Kritiek + Hoog items eerst, dan Medium
