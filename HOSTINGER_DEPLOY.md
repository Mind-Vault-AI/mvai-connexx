# MVAI Connexx - Hostinger VPS Deployment Guide

## Vereisten
- Hostinger VPS (minimaal KVM 1)
- Ubuntu 22.04 LTS
- Domain gekoppeld aan VPS IP

## Stap 1: Server Setup
```bash
# Update systeem
sudo apt update && sudo apt upgrade -y

# Installeer Python en dependencies
sudo apt install python3 python3-pip python3-venv nginx -y
```

## Stap 2: Clone Repository
```bash
cd /var/www
sudo git clone https://github.com/Mind-Vault-AI/mvai-connexx.git
cd mvai-connexx
```

## Stap 3: Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

## Stap 4: Environment Variables
```bash
sudo cp .env.example .env
sudo nano .env
# Vul in: SECRET_KEY, DATABASE_PATH, etc.
```

## Stap 5: Database Initialiseren
```bash
python3 -c "from database import init_db; init_db()"
```

## Stap 6: Gunicorn Service
Kopieer het service bestand naar systemd:
```bash
sudo cp mvai-connexx.service /etc/systemd/system/
sudo systemctl daemon-reload
```

Start service:
```bash
sudo systemctl start mvai-connexx
sudo systemctl enable mvai-connexx
sudo systemctl status mvai-connexx
```

## Stap 7: Nginx Configuratie
Maak `/etc/nginx/sites-available/mvai-connexx`:
```nginx
server {
    listen 80;
    server_name jouw-domein.nl www.jouw-domein.nl;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/mvai-connexx/mvai-connexx.sock;
    }

    location /static {
        alias /var/www/mvai-connexx/static;
    }
}
```

Activeer:
```bash
sudo ln -s /etc/nginx/sites-available/mvai-connexx /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## Stap 8: SSL met Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d jouw-domein.nl -d www.jouw-domein.nl
```

## Stap 9: Firewall
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Verificatie
Bezoek https://jouw-domein.nl - app moet draaien.

## Troubleshooting
```bash
# Check Gunicorn status
sudo systemctl status mvai-connexx

# Check logs
sudo journalctl -u mvai-connexx

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```
