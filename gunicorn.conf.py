# Gunicorn configuration for Hostinger VPS
bind = "unix:mvai-connexx.sock"
workers = 3
threads = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"
