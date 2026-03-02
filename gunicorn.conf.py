# Gunicorn configuration for Render deployment
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = int(os.environ.get('GUNICORN_WORKERS', '2'))
threads = int(os.environ.get('GUNICORN_THREADS', '2'))
worker_class = "sync"
worker_connections = 1000
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
keepalive = 2

# Render logs to stdout/stderr
errorlog = "-"
accesslog = "-"
loglevel = "info"
