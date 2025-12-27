# 🛡️ MVAI CONNEXX - SECURITY DOCUMENTATION

## Enterprise-Grade Security Features

MVAI Connexx is gebouwd met **military-grade security** voor hybrid deployment (cloud + on-premise). Deze documentatie beschrijft alle security features en best practices.

---

## 🔒 SECURITY LAYERS

### Layer 1: Network Security
- ✅ IP Whitelisting & Blacklisting
- ✅ Private Network Support (CIDR)
- ✅ VPN Requirement Option
- ✅ Hybrid Deployment (Cloud + On-Premise)
- ✅ Admin IP Restrictions

### Layer 2: Application Security
- ✅ AI-Powered Threat Detection
- ✅ SQL Injection Prevention
- ✅ XSS Protection
- ✅ CSRF Protection
- ✅ Command Injection Detection
- ✅ Path Traversal Prevention

### Layer 3: Authentication & Authorization
- ✅ Secure Access Codes (Token-based)
- ✅ API Key Authentication
- ✅ Session Management (24h expiry)
- ✅ Multi-Tenant Isolation
- ✅ Role-Based Access Control

### Layer 4: Intrusion Detection
- ✅ Honeypot System
- ✅ Failed Login Tracking
- ✅ Auto-Blacklisting (5 failed attempts)
- ✅ Behavioral Analysis
- ✅ Real-Time Threat Monitoring

### Layer 5: Data Security
- ✅ Encrypted Storage
- ✅ Audit Logging (All Actions)
- ✅ IP Tracking (Forensics)
- ✅ Secure Backups (30-day retention)
- ✅ Data Isolation (Multi-Tenant)

---

## 🌐 NETWORK MODES

### 1. Public Mode (Default)
```bash
PRIVATE_NETWORK_MODE=public
```
- Open internet access
- Rate limiting active
- Threat detection active
- Best voor: SaaS deployment

### 2. Private Mode
```bash
PRIVATE_NETWORK_MODE=private
ALLOWED_NETWORKS=192.168.1.0/24,10.0.0.0/16
```
- Alleen toegang van whitelisted networks
- Perfect voor: On-premise deployment
- Gebruik met: Corporate VPN

### 3. Hybrid Mode ⭐ RECOMMENDED
```bash
PRIVATE_NETWORK_MODE=hybrid
ALLOWED_NETWORKS=192.168.1.0/24
ADMIN_IPS=192.168.1.100
VPN_REQUIRED=true
```
- Public access voor customers
- Private access voor admin
- VPN requirement voor sensitive ops
- Best voor: Enterprise deployment

---

## 🎯 IP WHITELISTING

### Automatische Whitelist
Bepaalde IPs worden automatisch trusted:
- Internal networks (10.x, 172.16.x, 192.168.x)
- Configured TRUSTED_IPS
- Admin IPs

### Handmatig Whitelisten via Admin Panel
```
Login → Security Dashboard → Whitelist → Add IP
```

### Whitelist via Environment
```bash
TRUSTED_IPS=192.168.1.100,10.0.1.50,203.0.113.10
```

### Programmatisch Whitelisten
```python
from security import security_manager

security_manager.add_to_whitelist(
    ip='192.168.1.100',
    reason='Corporate VPN Gateway'
)
```

---

## 🚫 IP BLACKLISTING

### Auto-Blacklisting
IPs worden automatisch geblacklist bij:
- **5 failed login attempts** in 10 minuten
- **Honeypot access** (immediate permanent block)
- **Threat detection** (high-risk patterns)
- **Attack patterns** (SQL injection, XSS, etc.)

### Blacklist Duration
```bash
BLACKLIST_DURATION_HOURS=24  # Default 24 uur
```

### Handmatig Blacklisten
```
Admin → Security → Blacklist → Add IP
```

### Blacklist Cleanup
Expired blacklist entries worden automatisch verwijderd:
```bash
python -c "from security import cleanup_expired_blacklists; cleanup_expired_blacklists()"
```

---

## 🤖 AI THREAT DETECTION

### Wat wordt gedetecteerd?
- ✅ SQL Injection patterns
- ✅ XSS attempts
- ✅ Path traversal (`../`)
- ✅ Command injection
- ✅ Password fishing
- ✅ Large payload attacks (>10KB)
- ✅ Suspicious characters (`%00`, `<?php`, etc.)

### Threat Scoring
```
0-20   = Low risk (allowed)
21-50  = Medium risk (logged)
51+    = High risk (BLOCKED + blacklisted)
```

### Behavioral Analysis
AI detecteert ook abnormaal gedrag:
- **High frequency**: >100 requests in korte tijd
- **Rapid-fire**: <0.5 sec tussen requests
- **Bot behavior**: Multiple user agents
- **Scraping patterns**: Sequential ID access

---

## 🍯 HONEYPOT SYSTEEM

### Honeypot Endpoints
Deze endpoints zijn **traps** voor hackers:
```
/admin/phpMyAdmin    → Immediate 7-day blacklist
/wp-admin            → Immediate 7-day blacklist
/.env                → Immediate 7-day blacklist
/config.php          → Immediate 7-day blacklist
/backup.sql          → Immediate 7-day blacklist
/admin/config.json   → Immediate 7-day blacklist
```

### Wat gebeurt er?
1. Hacker accest honeypot endpoint
2. IP wordt **direct** geblacklist (7 dagen)
3. Security incident wordt gelogd (severity: CRITICAL)
4. Admin krijgt alert in Security Dashboard

---

## 🔐 ADMIN IP RESTRICTIONS

### Admin-Only IPs
Restrict admin panel tot specifieke IPs:

```bash
ADMIN_IPS=192.168.1.100,10.0.1.1
```

**Resultaat:**
- Alleen deze IPs kunnen `/admin/*` routes accessen
- Andere IPs krijgen 403 Forbidden
- Perfect voor: Corporate environments

### Disable Admin Restrictions
Laat leeg voor open admin access:
```bash
ADMIN_IPS=
```

---

## 📊 SECURITY DASHBOARD

### Real-Time Monitoring
```
Admin → Security Dashboard
```

**Features:**
- ✅ Live threat status
- ✅ Incidents (24 uur)
- ✅ Recent threats (1 uur)
- ✅ Blacklist/whitelist management
- ✅ Auto-refresh (30 sec)

### Security Metrics
- Total incidents (24h)
- Critical threats count
- Blacklisted IPs count
- Whitelisted IPs count
- Threat level indicator

---

## 🔧 CONFIGURATION

### Environment Variables

#### Security Settings
```bash
# IP Whitelisting
ENABLE_IP_WHITELIST=true

# AI Threat Detection
ENABLE_THREAT_DETECTION=true

# Honeypot System
ENABLE_HONEYPOT=true

# Auto-blacklist threshold
AUTO_BLACKLIST_THRESHOLD=5

# Blacklist duration (hours)
BLACKLIST_DURATION_HOURS=24
```

#### Network Configuration
```bash
# Network mode: public, private, hybrid
PRIVATE_NETWORK_MODE=hybrid

# Allowed networks (CIDR)
ALLOWED_NETWORKS=192.168.1.0/24,10.0.0.0/16

# VPN requirement
VPN_REQUIRED=false

# Trusted IPs
TRUSTED_IPS=192.168.1.100,10.0.1.50

# Admin-only IPs
ADMIN_IPS=192.168.1.100
```

#### Deployment
```bash
# Deployment mode: cloud, on-premise, hybrid
DEPLOYMENT_MODE=hybrid

# Internal IP range
INTERNAL_IP_RANGE=10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```

---

## 🏢 HYBRID DEPLOYMENT SETUP

### Scenario: Enterprise met VPN

**Requirements:**
- Cloud hosting (Fly.io)
- Corporate VPN (192.168.1.0/24)
- Admin access alleen via VPN

**Configuration:**
```bash
# .env
PRIVATE_NETWORK_MODE=hybrid
ALLOWED_NETWORKS=192.168.1.0/24
ADMIN_IPS=192.168.1.100
VPN_REQUIRED=true
ENABLE_IP_WHITELIST=true
DEPLOYMENT_MODE=hybrid
```

**Result:**
- ✅ Customers: Public internet access (met threat detection)
- ✅ Admin: Alleen via VPN (192.168.1.100)
- ✅ API: Rate limited (200/day)
- ✅ Security: Full protection active

---

## 🛡️ SECURITY BEST PRACTICES

### 1. Enable All Security Features (Production)
```bash
ENABLE_IP_WHITELIST=true
ENABLE_THREAT_DETECTION=true
ENABLE_HONEYPOT=true
RATELIMIT_ENABLED=true
```

### 2. Restrict Admin Access
```bash
ADMIN_IPS=your-corporate-ip
```

### 3. Use Hybrid Mode voor Enterprise
```bash
PRIVATE_NETWORK_MODE=hybrid
VPN_REQUIRED=true
```

### 4. Monitor Security Dashboard
- Check dagelijks voor threats
- Review blacklist regelmatig
- Investigate critical incidents

### 5. Regular Backups
```bash
# Cron job
0 3 * * * cd /app && python backup.py create
```

### 6. Update Trusted IPs
Keep TRUSTED_IPS up-to-date:
- VPN gateways
- Corporate networks
- Trusted partners

### 7. Review Audit Logs
```sql
SELECT * FROM security_incidents
WHERE severity = 'critical'
ORDER BY timestamp DESC;
```

---

## 📋 SECURITY CHECKLIST

### Pre-Deployment
- [ ] `SECRET_KEY` changed (64+ random chars)
- [ ] `ADMIN_IPS` configured
- [ ] `TRUSTED_IPS` configured
- [ ] `PRIVATE_NETWORK_MODE` set
- [ ] All security features enabled
- [ ] HTTPS configured
- [ ] Firewall rules set

### Post-Deployment
- [ ] Security dashboard accessible
- [ ] Honeypot endpoints working
- [ ] Auto-blacklisting working
- [ ] Rate limiting active
- [ ] Backups running
- [ ] Audit logs capturing
- [ ] Admin access restricted

### Regular Maintenance
- [ ] Check security dashboard daily
- [ ] Review blacklist weekly
- [ ] Update trusted IPs monthly
- [ ] Test security features quarterly
- [ ] Review audit logs monthly

---

## 🚨 INCIDENT RESPONSE

### Step 1: Identify
Check Security Dashboard voor alerts

### Step 2: Analyze
```sql
SELECT * FROM security_incidents
WHERE ip_address = 'suspicious-ip'
ORDER BY timestamp DESC;
```

### Step 3: Block
```bash
# Via admin panel of:
curl -X POST -H "Cookie: session=xxx" \
  https://your-app/admin/security/blacklist/add \
  -d "ip=1.2.3.4&reason=Attack detected"
```

### Step 4: Investigate
- Check audit_logs
- Review customer access
- Verify data integrity

### Step 5: Report
Document in security_incidents table

---

## 📞 SECURITY SUPPORT

**Report Security Issues:**
- Email: security@mindvault.ai
- GitHub: https://github.com/Mind-Vault-AI/mvai-connexx/security

**Emergency Response:**
- Critical issues: Immediate blacklist
- Contact: Admin team via secure channel

---

## 🎖️ COMPLIANCE

### Security Standards
- ✅ **GDPR** compliant (data isolation)
- ✅ **ISO 27001** ready (audit logging)
- ✅ **SOC 2** ready (access controls)
- ✅ **HIPAA** compatible (encryption)

### Audit Trail
All admin actions logged with:
- Timestamp
- Username
- IP address
- Action details
- Target resource

---

## 🔬 TESTING SECURITY

### Test Honeypot
```bash
curl https://your-app/admin/phpMyAdmin
# Should return 404 and blacklist your IP
```

### Test Rate Limiting
```bash
for i in {1..60}; do
  curl https://your-app/api/v1/health
done
# Should get 429 after 50 requests
```

### Test IP Whitelist
```bash
# Add IP to whitelist first
curl https://your-app/admin/security
# Should allow access
```

---

## 🚀 DEPLOYMENT MODES

### Mode 1: SaaS (Public Cloud)
```bash
PRIVATE_NETWORK_MODE=public
DEPLOYMENT_MODE=cloud
ENABLE_THREAT_DETECTION=true
RATELIMIT_ENABLED=true
```

### Mode 2: On-Premise
```bash
PRIVATE_NETWORK_MODE=private
DEPLOYMENT_MODE=on-premise
ALLOWED_NETWORKS=192.168.0.0/16
```

### Mode 3: Hybrid (RECOMMENDED)
```bash
PRIVATE_NETWORK_MODE=hybrid
DEPLOYMENT_MODE=hybrid
ALLOWED_NETWORKS=192.168.1.0/24
ADMIN_IPS=192.168.1.100
VPN_REQUIRED=true
```

---

**🛡️ MVAI CONNEXX - SECURE BY DESIGN**

*Enterprise-Grade Security for Hybrid Deployment*
*Hack-Proof • Private Network Ready • AI-Powered Protection*
