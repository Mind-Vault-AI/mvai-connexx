# Gunicorn configuration for Hostinger VPS deployment
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"

# BELANGRIJK: gebruik 1 worker zodat in-memory state consistent blijft.
# Bij meerdere workers: zet RATELIMIT_STORAGE_URL=redis://... in .env
workers = int(os.environ.get('GUNICORN_WORKERS', '1'))
threads = int(os.environ.get('GUNICORN_THREADS', '4'))
worker_class = "sync"
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
keepalive = 5

# Logging naar stdout/stderr (via systemd: journalctl -u mvai-connexx)
errorlog = "-"
accesslog = "-"
loglevel = "info"

# Graceful restart - lopende requests afhandelen voor herstart
graceful_timeout = 30
max_requests = 1000
max_requests_jitter = 50
