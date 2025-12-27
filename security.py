"""
MVAI Connexx - Security Module
Advanced security met IP whitelisting, threat detection en intrusion prevention
"""
import re
import json
from datetime import datetime, timedelta
from collections import defaultdict
import database as db
from functools import wraps
from flask import request, jsonify
import hashlib

# ═══════════════════════════════════════════════════════
# IP WHITELISTING & BLACKLISTING
# ═══════════════════════════════════════════════════════

class IPSecurityManager:
    """Beheer IP whitelists en blacklists"""

    def __init__(self):
        self.whitelist = set()
        self.blacklist = set()
        self.suspicious_ips = defaultdict(int)
        self.failed_attempts = defaultdict(list)
        self.load_lists()

    def load_lists(self):
        """Laad IP lists van database"""
        with db.get_db() as conn:
            cursor = conn.cursor()

            # Whitelist
            cursor.execute('SELECT ip_address FROM ip_whitelist WHERE is_active = 1')
            self.whitelist = {row['ip_address'] for row in cursor.fetchall()}

            # Blacklist
            cursor.execute('SELECT ip_address FROM ip_blacklist WHERE is_active = 1')
            self.blacklist = {row['ip_address'] for row in cursor.fetchall()}

    def is_whitelisted(self, ip):
        """Check of IP whitelisted is"""
        return ip in self.whitelist

    def is_blacklisted(self, ip):
        """Check of IP blacklisted is"""
        return ip in self.blacklist

    def add_to_whitelist(self, ip, reason=None):
        """Voeg IP toe aan whitelist"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO ip_whitelist (ip_address, reason, added_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (ip, reason))
        self.whitelist.add(ip)

    def add_to_blacklist(self, ip, reason=None, duration_hours=24):
        """Voeg IP toe aan blacklist"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO ip_blacklist (ip_address, reason, added_at, expires_at)
                VALUES (?, ?, CURRENT_TIMESTAMP, datetime('now', ?))
            ''', (ip, reason, f'+{duration_hours} hours'))
        self.blacklist.add(ip)

    def record_failed_attempt(self, ip, reason):
        """Registreer gefaalde login poging"""
        self.failed_attempts[ip].append({
            'timestamp': datetime.now(),
            'reason': reason
        })

        # Auto-blacklist na 5 pogingen in 10 minuten
        recent_attempts = [
            a for a in self.failed_attempts[ip]
            if datetime.now() - a['timestamp'] < timedelta(minutes=10)
        ]

        if len(recent_attempts) >= 5:
            self.add_to_blacklist(ip, f'Auto-blocked: {len(recent_attempts)} failed attempts', duration_hours=24)
            return True

        return False

    def check_ip_reputation(self, ip):
        """Check IP reputatie (basis implementatie)"""
        # Blacklisted = immediate block
        if self.is_blacklisted(ip):
            return {
                'status': 'blocked',
                'reason': 'IP is blacklisted',
                'threat_level': 'high'
            }

        # Whitelisted = trusted
        if self.is_whitelisted(ip):
            return {
                'status': 'trusted',
                'threat_level': 'none'
            }

        # Check recent failed attempts
        recent_failures = len([
            a for a in self.failed_attempts.get(ip, [])
            if datetime.now() - a['timestamp'] < timedelta(minutes=30)
        ])

        if recent_failures > 2:
            return {
                'status': 'suspicious',
                'reason': f'{recent_failures} recent failed attempts',
                'threat_level': 'medium'
            }

        return {
            'status': 'unknown',
            'threat_level': 'low'
        }

# Global security manager
security_manager = IPSecurityManager()

# ═══════════════════════════════════════════════════════
# AI-POWERED THREAT DETECTION
# ═══════════════════════════════════════════════════════

class AIThreatDetector:
    """AI-based threat detection systeem"""

    def __init__(self):
        self.attack_patterns = [
            r'(?i)(union|select|insert|update|delete|drop|create|alter)\s+',  # SQL injection
            r'<script[^>]*>.*?</script>',  # XSS
            r'\.\./|\.\.\\',  # Path traversal
            r'(?i)(exec|eval|system|cmd)',  # Command injection
            r'(?i)(password|passwd|pwd).*[=:]',  # Password fishing
        ]

    def analyze_request(self, request_data):
        """Analyseer request op threats"""
        threats = []
        threat_score = 0

        # Check voor attack patterns
        for pattern in self.attack_patterns:
            if re.search(pattern, str(request_data)):
                threats.append({
                    'type': 'pattern_match',
                    'pattern': pattern,
                    'severity': 'high'
                })
                threat_score += 50

        # Check voor abnormale request size
        if len(str(request_data)) > 10000:
            threats.append({
                'type': 'large_payload',
                'size': len(str(request_data)),
                'severity': 'medium'
            })
            threat_score += 20

        # Check voor abnormale characters
        suspicious_chars = ['%00', '\x00', '<?php', '<%', '{$']
        for char in suspicious_chars:
            if char in str(request_data):
                threats.append({
                    'type': 'suspicious_characters',
                    'char': char,
                    'severity': 'high'
                })
                threat_score += 30

        return {
            'is_threat': threat_score > 30,
            'threat_score': threat_score,
            'threats': threats,
            'risk_level': 'high' if threat_score > 50 else 'medium' if threat_score > 20 else 'low'
        }

    def analyze_behavior(self, ip, actions):
        """Analyseer gebruikersgedrag voor anomalieën"""
        behavior_score = 0

        # Check request frequency
        if len(actions) > 100:  # Meer dan 100 acties
            behavior_score += 40

        # Check voor rapid-fire requests
        if len(actions) > 1:
            time_diffs = [
                (actions[i]['timestamp'] - actions[i-1]['timestamp']).total_seconds()
                for i in range(1, len(actions))
            ]
            avg_diff = sum(time_diffs) / len(time_diffs) if time_diffs else 0

            if avg_diff < 0.5:  # Sneller dan 0.5 seconden per request
                behavior_score += 50

        # Check voor verschillende user agents (bot behavior)
        user_agents = {a.get('user_agent') for a in actions if a.get('user_agent')}
        if len(user_agents) > 5:
            behavior_score += 30

        return {
            'is_suspicious': behavior_score > 50,
            'behavior_score': behavior_score,
            'indicators': {
                'high_frequency': len(actions) > 100,
                'rapid_requests': avg_diff < 0.5 if len(actions) > 1 else False,
                'multiple_agents': len(user_agents) > 5
            }
        }

threat_detector = AIThreatDetector()

# ═══════════════════════════════════════════════════════
# ENCRYPTION HELPERS
# ═══════════════════════════════════════════════════════

def encrypt_sensitive_data(data):
    """Encrypt gevoelige data (basic hashing voor demo)"""
    # In productie: gebruik proper encryption library (cryptography, fernet)
    return hashlib.sha256(data.encode()).hexdigest()

def generate_secure_token():
    """Genereer veilige random token"""
    import secrets
    return secrets.token_urlsafe(32)

# ═══════════════════════════════════════════════════════
# HONEYPOT SYSTEEM
# ═══════════════════════════════════════════════════════

class HoneypotManager:
    """Honeypot systeem om hackers te detecteren"""

    def __init__(self):
        self.honeypot_endpoints = [
            '/admin/phpMyAdmin',
            '/wp-admin',
            '/.env',
            '/config.php',
            '/backup.sql',
            '/admin/config.json'
        ]
        self.trapped_ips = set()

    def is_honeypot(self, path):
        """Check of endpoint een honeypot is"""
        return any(path.startswith(hp) for hp in self.honeypot_endpoints)

    def trap_ip(self, ip, endpoint):
        """Trap IP die honeypot probeert te accessen"""
        self.trapped_ips.add(ip)

        # Auto-blacklist
        security_manager.add_to_blacklist(
            ip,
            f'Honeypot accessed: {endpoint}',
            duration_hours=168  # 7 dagen
        )

        # Log incident
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO security_incidents (ip_address, incident_type, details, severity, timestamp)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (ip, 'honeypot_access', f'Accessed {endpoint}', 'critical'))

honeypot = HoneypotManager()

# ═══════════════════════════════════════════════════════
# SECURITY DECORATORS
# ═══════════════════════════════════════════════════════

def require_secure_ip(f):
    """Decorator die IP security checkt"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

        # Check blacklist
        if security_manager.is_blacklisted(ip):
            return jsonify({
                'error': 'Access denied',
                'reason': 'IP address is blacklisted'
            }), 403

        # Check honeypot
        if honeypot.is_honeypot(request.path):
            honeypot.trap_ip(ip, request.path)
            return jsonify({'error': 'Not found'}), 404

        # Check reputation
        reputation = security_manager.check_ip_reputation(ip)
        if reputation['status'] == 'blocked':
            return jsonify({
                'error': 'Access denied',
                'reason': reputation['reason']
            }), 403

        return f(*args, **kwargs)

    return decorated_function

def require_threat_scan(f):
    """Decorator die request scant op threats"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

        # Scan request data
        request_data = {
            'args': dict(request.args),
            'form': dict(request.form),
            'json': request.get_json(silent=True),
            'headers': dict(request.headers)
        }

        analysis = threat_detector.analyze_request(request_data)

        if analysis['is_threat']:
            # Log threat
            with db.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO security_incidents (ip_address, incident_type, details, severity, timestamp)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (ip, 'threat_detected', json.dumps(analysis['threats']), analysis['risk_level']))

            # Block high-risk threats
            if analysis['risk_level'] == 'high':
                security_manager.add_to_blacklist(ip, 'Threat detected', duration_hours=48)
                return jsonify({
                    'error': 'Security violation detected',
                    'incident_id': cursor.lastrowid
                }), 403

        return f(*args, **kwargs)

    return decorated_function

# ═══════════════════════════════════════════════════════
# SECURITY MONITORING
# ═══════════════════════════════════════════════════════

def get_security_status():
    """Haal security status op"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        # Recent incidents (laatste 24 uur)
        cursor.execute('''
            SELECT COUNT(*) as count, severity
            FROM security_incidents
            WHERE timestamp >= datetime('now', '-24 hours')
            GROUP BY severity
        ''')
        incidents = {row['severity']: row['count'] for row in cursor.fetchall()}

        # Blacklisted IPs
        cursor.execute('SELECT COUNT(*) as count FROM ip_blacklist WHERE is_active = 1')
        blacklisted_count = cursor.fetchone()['count']

        # Whitelisted IPs
        cursor.execute('SELECT COUNT(*) as count FROM ip_whitelist WHERE is_active = 1')
        whitelisted_count = cursor.fetchone()['count']

        # Recent threats
        cursor.execute('''
            SELECT * FROM security_incidents
            WHERE timestamp >= datetime('now', '-1 hour')
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        recent_threats = [dict(row) for row in cursor.fetchall()]

    return {
        'status': 'secure' if incidents.get('critical', 0) == 0 else 'alert',
        'incidents_24h': incidents,
        'blacklisted_ips': blacklisted_count,
        'whitelisted_ips': whitelisted_count,
        'recent_threats': recent_threats,
        'threat_level': 'high' if incidents.get('critical', 0) > 0 else 'low'
    }

def cleanup_expired_blacklists():
    """Verwijder verlopen blacklist entries"""
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE ip_blacklist
            SET is_active = 0
            WHERE expires_at < datetime('now')
        ''')
        removed = cursor.rowcount

    # Reload lists
    security_manager.load_lists()

    return removed

if __name__ == '__main__':
    print("Security module loaded successfully")
    print(f"Whitelisted IPs: {len(security_manager.whitelist)}")
    print(f"Blacklisted IPs: {len(security_manager.blacklist)}")
