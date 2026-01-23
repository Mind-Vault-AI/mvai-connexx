# Gunicorn configuration for Hostinger VPS
import os

bind = "unix:mvai-connexx.sock"
workers = int(os.environ.get('GUNICORN_WORKERS', '3'))
threads = int(os.environ.get('GUNICORN_THREADS', '2'))
worker_class = "sync"
worker_connections = 1000
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '30'))
keepalive = 2

# Log files - using relative paths to avoid permission issues
# Logs will be in the working directory (/var/www/mvai-connexx)
# For system logs, create /var/log/gunicorn directory: sudo mkdir -p /var/log/gunicorn && sudo chown www-data:www-data /var/log/gunicorn
errorlog = "gunicorn-error.log"
accesslog = "gunicorn-access.log"
loglevel = "info"
