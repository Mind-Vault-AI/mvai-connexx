# Lessons Learned — MVAI Connexx

| Datum | Les | Toepassing |
|-------|-----|-----------|
| 2026-03-12 | Hostinger API werkt niet via MCP door Cloudflare filtering | Altijd hPanel gebruiken voor DNS/VPS beheer |
| 2026-03-12 | SQLite op VPS: gebruik persistent volume op `/app/data/` | Zorg dat `DATABASE_PATH` env var altijd correct is |
| 2026-03-12 | Multi-worker gunicorn + SQLite = race conditions | Gebruik 1 worker OF schakel over naar Redis/PostgreSQL |
| 2026-03-12 | Session loss bij restart = geen sticky sessions | Gebruik `SECRET_KEY` env var (nooit hardcoded) |
| 2026-03-13 | BOX Drive sync = na elke sprint handmatig kopiëren | Automatiseer met BOX CLI of post-deploy hook |
| 2026-03-14 | 23 commits op feature branch, nooit naar main gemerged | Feature branches direct na goedkeuring mergen |
