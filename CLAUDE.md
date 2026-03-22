# CLAUDE.md — MVAI Connexx

## Project Overview

MVAI Connexx is a **multi-tenant enterprise platform** for logistics data validation and process optimization, built by Mind Vault AI. It runs as a Python/Flask web application with SQLite storage, deployed on a Hostinger VPS at `connexx.mindvault-ai.com`.

**Language:** Dutch (UI, comments, variable names mix Dutch/English)
**Stack:** Python 3.11 + Flask 3.x + SQLite + Gunicorn + Nginx (on VPS)

## Quick Reference

```bash
# Run locally
python app.py

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=term-missing

# Seed demo data
python seed_demo.py

# Production start
gunicorn app:app --config gunicorn.conf.py
```

## Architecture

### Core Application Files (project root — no `src/` directory)

| File | Purpose |
|---|---|
| `app.py` | Main Flask app — all routes, auth decorators, session management (~1800 lines) |
| `database.py` | SQLite multi-tenant database layer with WAL mode, retry-on-locked, context manager |
| `config.py` | Configuration classes (Dev/Prod/Hybrid) loaded from `.env` via `python-dotenv` |
| `logging_config.py` | Structured logging with `structlog` — JSON in prod, console in dev |
| `api.py` | REST API endpoints (separate from web routes) |
| `security.py` | IP whitelisting, threat detection, honeypot traps |
| `analytics.py` | Customer analytics and statistics |
| `ai_assistant.py` | AI assistant feature (OpenAI/Anthropic/multi-provider) |
| `ai_providers.py` | Multi-AI provider abstraction (BYOK — Bring Your Own Key) |
| `integrations.py` | External service integrations and webhooks |
| `email_notifications.py` | SMTP email with HTML templates |
| `gumroad_integration.py` | Gumroad payment processing (active payment provider) |
| `stripe_integration.py` | Stripe integration (disabled — waiting for KVK registration) |
| `unit_economics.py` | Pricing tier economics and calculations |
| `lean_six_sigma.py` | Lean Six Sigma process optimization module |
| `marketing_intelligence.py` | Marketing analytics module |
| `monitoring.py` | Application monitoring and health checks |
| `incident_response.py` | Incident management system |
| `backup.py` | Database backup utilities |
| `migrate.py` | JSON-to-SQLite migration script |
| `seed_demo.py` | Demo data seeding (5 fake companies, 50+ log entries) |

### Templates (`templates/`)

Jinja2 HTML templates. Key patterns:
- `admin_*.html` — Admin panel views
- `customer_*.html` — Customer-facing views
- `login.html`, `landing.html`, `legal.html` — Public pages
- Dark theme with MVAI branding, mobile-first (Samsung S23 Plus optimized)

### Tests (`tests/`)

- **Framework:** pytest with markers (`unit`, `integration`, `security`)
- **Config:** `pytest.ini` — strict markers, verbose, short tracebacks
- **Fixtures:** `conftest.py` — temp database, sample customer, sample API key
- **Test files:** `test_config.py`, `test_database.py`, `test_logging_config.py`, `test_security.py`
- **Dev deps:** `requirements-dev.txt` (pytest, pytest-cov, pytest-flask, pytest-mock, coverage)

### Deployment

- **Target:** Hostinger VPS (Ubuntu, Nginx reverse proxy, systemd service)
- **CI/CD:** `.github/workflows/deploy-hostinger.yml` — SSH deploy on push to `main`
- **Docker:** `Dockerfile` available (Python 3.9-slim, non-root user)
- **Render:** `render.yaml` config (alternative deployment)
- **Startup:** `start.sh` for production, `gunicorn.conf.py` for worker config

### Other Directories

- `android/` — Android app blueprint and resources
- `mindvault-landing/` — Landing page assets
- `scripts/` — Utility scripts (`create_separate_prs.sh`)
- `archive_old_deployments/` — Historical deployment configs (Fly.io, GCP)
- `projects/` — Sub-project resources

## Key Conventions

### Database Access
Always use the context manager:
```python
from database import get_db

with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT ...', (param,))
```
- Uses parameterized queries (SQL injection protection)
- WAL mode enabled for concurrency
- `retry_on_locked` decorator for busy handling
- Single Gunicorn worker by default to avoid SQLite locking issues

### Configuration
All config via environment variables, loaded through `config.py`:
```python
from config import Config
value = Config.SOME_SETTING
```
- `.env` file for local development (never committed)
- `.env.example` as template with all available variables
- `ConfigValidator` validates required vars on production startup

### Logging
Use structured logging, not `print()`:
```python
from logging_config import get_logger, LogEvents
logger = get_logger(__name__)
logger.info(LogEvents.SOME_EVENT, key="value")
```
- JSON output in production (for log aggregators)
- Console output in development
- Event constants in `LogEvents` class for consistency

### Authentication
- Access code based (no passwords) — codes auto-generated
- Session-based with 24h expiry
- Multi-tenant isolation: customers only see own data
- Admin panel has separate access level
- Routes protected by decorators defined in `app.py`

### Payments
- **Active:** Gumroad (PayPal backend) — no KVK required
- **Future:** Stripe (after KVK registration)
- 6 pricing tiers: Demo, Particulier, MKB, Starter, Professional, Enterprise

## Environment Variables

Critical variables for production (see `.env.example` for full list):

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Flask session encryption (generate with `secrets.token_hex(32)`) |
| `FLASK_ENV` | Yes | `development` or `production` |
| `DATABASE_PATH` | Yes | Path to SQLite database file |
| `OPENAI_API_KEY` | No | For AI assistant functionality |
| `SMTP_USERNAME` | No | For email notifications |
| `SMTP_PASSWORD` | No | For email notifications |
| `PAYMENT_PROVIDER` | Prod | `gumroad`, `stripe`, or `mollie` |

## CI/CD Pipeline

Push to `main` triggers automatic deployment:
1. SSH into Hostinger VPS
2. `git pull origin main`
3. Activate venv, `pip install -r requirements.txt`
4. Ensure `.env` has SECRET_KEY, FLASK_ENV, DATABASE_PATH
5. `systemctl restart mvai-connexx`
6. Verify service is active

## Common Tasks

### Adding a new route
1. Add route function in `app.py` with appropriate decorator (`login_required`, `admin_required`)
2. Create template in `templates/`
3. Add navigation links in related templates

### Adding a new test
1. Create `tests/test_<module>.py`
2. Use fixtures from `conftest.py` (`temp_db`, `sample_customer`, etc.)
3. Mark with `@pytest.mark.unit`, `@pytest.mark.integration`, or `@pytest.mark.security`
4. Run: `pytest tests/test_<module>.py -v`

### Database schema changes
1. Modify `init_db()` in `database.py`
2. Add migration logic in `migrate.py` if needed
3. Test with fresh database: `rm mvai_connexx.db && python seed_demo.py`

## MCP Configuration

`.mcp.json` configures the Hostinger API MCP server for deployment operations. Requires `HOSTINGER_API_TOKEN` environment variable.

## Important Notes

- **Do not commit `.env` files** — they contain secrets
- **SQLite limitations:** Single-writer; use 1 Gunicorn worker or switch `RATELIMIT_STORAGE_URL` to Redis for multiple workers
- **The codebase is bilingual:** Dutch comments/UI, English code patterns. Maintain this style.
- **`app.py` is large (~1800 lines)** — routes, decorators, and business logic are all in one file. This is the current architecture; don't refactor without explicit request.
- **Production URL:** `connexx.mindvault-ai.com`
- **VPS path:** `/var/www/mvai-connexx`
