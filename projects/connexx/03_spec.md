# Spec — MVAI Connexx

**Versie:** 2.0 (Multi-tenant upgrade)
**Datum:** 2026-03-14

## Overeengekomen scope

### Must have (v2.0)
- [x] Multi-tenant database architectuur
- [x] Customer dashboard (login, analytics, logs, export)
- [x] Admin panel (klantbeheer, security, unit economics)
- [x] AI providers hub (BYOK: OpenAI, Anthropic, Groq, etc.)
- [x] Integraties (webhooks, externe API koppelingen)
- [x] Rate limiting + security module
- [x] MVAI huisstijl: `#0f1520` navy, `#5aafaf` teal
- [x] Responsive mobile-first design
- [x] Gumroad payment integration
- [x] Email notificaties (SMTP)
- [x] Structured JSON logging (productie-compliant)
- [x] Darts501 demo pagina

### Deployment
- Platform: Hostinger VPS
- Domain: connexx.mindvault-ai.com
- Auto-deploy: push naar `main` → GitHub Actions → SSH

### BOX Drive sync
- Na elke sprint: kopieer `projects/connexx/` naar BOX Drive/MVAI/01_PROJECTEN/connexx/
