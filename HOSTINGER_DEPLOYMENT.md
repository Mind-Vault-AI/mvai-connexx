# 🚀 MVAI Connexx - HOSTINGER DEPLOYMENT

**Simpel, Nederlands, één platform.**

---

## 📋 VEREISTEN

1. **Hostinger account** (VPS of Business hosting)
2. **Domain** (mindvault-ai.com of vaultflow.com)
3. **SSH toegang** tot server

---

## 🎯 HOSTINGER VPS DEPLOYMENT

### Stap 1: VPS Setup (5 min)

1. **Login Hostinger:** https://hostinger.com/cpanel-login
2. **VPS Dashboard** → Select je VPS
3. **Operating System:** Ubuntu 22.04 (aanbevolen)
4. **SSH Details** ophalen:
   - IP address: `xxx.xxx.xxx.xxx`
   - Username: `root` of `ubuntu`
   - Password: (zie Hostinger dashboard)

### Stap 2: Connect via SSH (1 min)

**Windows (PowerShell):**
```bash
ssh root@xxx.xxx.xxx.xxx
# Voer password in
```

**Mac/Linux:**
```bash
ssh root@xxx.xxx.xxx.xxx
# Voer password in
```

### Stap 3: Server Setup (10 min)

Eenmaal ingelogd via SSH:

```bash
# Update systeem
apt update && apt upgrade -y

# Install Python en dependencies
apt install -y python3 python3-pip python3-venv git nginx

# Install Docker (optioneel, voor container deployment)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Create app user
useradd -m -s /bin/bash mvai
su - mvai
```

### Stap 4: Deploy App (5 min)

Als `mvai` user:

```bash
# Clone repository
cd ~
git clone https://github.com/Mind-Vault-AI/mvai-connexx.git
cd mvai-connexx

# Checkout juiste branch
git checkout claude/mvai-connexx-multi-tenant-upgrade-8eDvw

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
PAYMENT_PROVIDER=gumroad
FLASK_ENV=production
DATABASE_PATH=/home/mvai/mvai-connexx/mvai_connexx.db
EOF

# Seed database
python seed_demo.py
# SAVE THE ADMIN ACCESS CODE!

# Test app
python app.py
# CTRL+C om te stoppen
```

### Stap 5: Gunicorn Service (5 min)

Exit uit mvai user (type `exit`), terug naar root:

```bash
# Create systemd service
cat > /etc/systemd/system/mvai-connexx.service << 'EOF'
[Unit]
Description=MVAI Connexx Flask App
After=network.target

[Service]
Type=notify
User=mvai
Group=mvai
WorkingDirectory=/home/mvai/mvai-connexx
Environment="PATH=/home/mvai/mvai-connexx/venv/bin"
ExecStart=/home/mvai/mvai-connexx/venv/bin/gunicorn \
    --bind 127.0.0.1:5000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile /var/log/mvai-connexx-access.log \
    --error-logfile /var/log/mvai-connexx-error.log \
    app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Start service
systemctl daemon-reload
systemctl start mvai-connexx
systemctl enable mvai-connexx
systemctl status mvai-connexx
```

### Stap 6: Nginx Reverse Proxy (5 min)

```bash
# Create Nginx config
cat > /etc/nginx/sites-available/mvai-connexx << 'EOF'
server {
    listen 80;
    server_name mindvault-ai.com www.mindvault-ai.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/mvai-connexx /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Stap 7: SSL Certificaat (5 min)

```bash
# Install Certbot
apt install -y certbot python3-certbot-nginx

# Get SSL certificate
certbot --nginx -d mindvault-ai.com -d www.mindvault-ai.com

# Auto-renew test
certbot renew --dry-run
```

---

## 🔧 MANAGEMENT COMMANDS

### App beheren:
```bash
# Status checken
systemctl status mvai-connexx

# Logs bekijken
journalctl -u mvai-connexx -f

# App herstarten
systemctl restart mvai-connexx

# App stoppen
systemctl stop mvai-connexx
```

### Updates deployen:
```bash
# Als mvai user
su - mvai
cd mvai-connexx
git pull origin claude/mvai-connexx-multi-tenant-upgrade-8eDvw
source venv/bin/activate
pip install -r requirements.txt
exit

# Als root
systemctl restart mvai-connexx
```

### Database backup:
```bash
# Als mvai user
su - mvai
cd mvai-connexx
cp mvai_connexx.db mvai_connexx_backup_$(date +%Y%m%d).db
```

---

## 🌐 DOMAIN KOPPELEN

### In Hostinger Dashboard:

1. **Domains** → Select `mindvault-ai.com`
2. **DNS Zone**
3. Add **A Record:**
   - Type: `A`
   - Name: `@`
   - Points to: `[VPS IP ADDRESS]`
   - TTL: `3600`
4. Add **A Record** (www):
   - Type: `A`
   - Name: `www`
   - Points to: `[VPS IP ADDRESS]`
   - TTL: `3600`

**Propagation:** 15 minuten - 24 uur

---

## 💰 KOSTEN (Hostinger VPS)

| Plan | CPU | RAM | Storage | Prijs |
|------|-----|-----|---------|-------|
| **VPS 1** | 1 core | 1GB | 20GB | €3.99/maand |
| **VPS 2** | 2 cores | 2GB | 40GB | €5.99/maand |
| **VPS 3** | 3 cores | 3GB | 60GB | €8.99/maand |

**Aanbeveling:** VPS 2 (€5.99/maand) - Genoeg voor 100+ gebruikers

---

## 🐛 TROUBLESHOOTING

### App start niet:
```bash
# Check logs
journalctl -u mvai-connexx -n 50

# Test handmatig
su - mvai
cd mvai-connexx
source venv/bin/activate
python app.py
```

### Database errors:
```bash
# Check permissions
ls -la /home/mvai/mvai-connexx/mvai_connexx.db

# Reset database
su - mvai
cd mvai-connexx
rm mvai_connexx.db
python seed_demo.py
exit
systemctl restart mvai-connexx
```

### Nginx niet bereikbaar:
```bash
# Check nginx status
systemctl status nginx

# Check config
nginx -t

# Check firewall
ufw status
ufw allow 80
ufw allow 443
```

---

## ✅ VERIFICATION CHECKLIST

Na deployment:

- [ ] VPS bereikbaar via SSH
- [ ] App draait: `systemctl status mvai-connexx`
- [ ] Nginx draait: `systemctl status nginx`
- [ ] Domain wijst naar VPS IP
- [ ] HTTP werkt: `http://mindvault-ai.com`
- [ ] HTTPS werkt: `https://mindvault-ai.com`
- [ ] Login werkt met admin code
- [ ] Database persistent (na reboot)

---

## 🔒 SECURITY HARDENING

```bash
# Create firewall rules
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow http
ufw allow https
ufw enable

# Disable root SSH login
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd

# Auto security updates
apt install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
```

---

## 📊 MONITORING

```bash
# Disk usage
df -h

# Memory usage
free -h

# CPU usage
top

# App logs real-time
journalctl -u mvai-connexx -f
```

---

## 🎯 SUMMARY

**Total setup tijd:** ~35 minuten
**Kosten:** €5.99/maand (VPS 2)
**Domain:** mindvault-ai.com (al in bezit)
**SSL:** Gratis (Let's Encrypt)

**Status:** Production-ready, schaalbaar, Nederlands platform

**Support:** Hostinger 24/7 live chat (Nederlands)

---

**KLAAR OM TE DEPLOYEN!**
