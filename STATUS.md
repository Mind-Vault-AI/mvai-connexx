# PROJECT STATUS - MVAI Connexx

## Huidige Status
🟢 PRODUCTION

## Deployment
| Platform      | Status    | URL / Trigger                                        |
|---------------|-----------|------------------------------------------------------|
| Hostinger VPS | ✅ Primair | connexx.mindvault-ai.com — push naar `main`         |
| Render        | ✅ Actief  | render.yaml — push naar `main`                       |

- **GitHub Actions workflow:** `.github/workflows/deploy-hostinger.yml`
- **Default branch:** `main`
- **Volledige deploy handleiding:** [DEPLOY.md](DEPLOY.md)

## Wat werkt
- [x] Multi-tenant customer management
- [x] API key authentication
- [x] Rate limiting
- [x] Health endpoints
- [x] Hostinger VPS deployment (GitHub Actions via SSH)
- [x] Render deployment (render.yaml)
- [x] Persistent SQLite storage
- [x] Security module (IP whitelist/blacklist)
- [x] Structured logging
- [x] Config class integration
- [x] Input validation on API parameters
- [x] Gumroad payment integration
- [x] 6 Pricing tiers
- [x] Email notifications
- [x] AI Assistant (BYOK)

## Wat niet werkt / TODO
- [ ] Stripe (wacht op KVK registratie)
- [ ] PDF export met grafieken
- [ ] Real-time notificaties

## Contact
- **Owner:** Mind-Vault-AI
- **Email:** info@mindvault-ai.com
